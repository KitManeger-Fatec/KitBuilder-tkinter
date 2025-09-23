import os
import re
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, MetaData, Table, Date, DateTime, DECIMAL
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# --- Carregar variáveis do .env ---
load_dotenv()
USER = os.getenv("DB_USER")
PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
HOST = os.getenv("DB_HOST")
DB = os.getenv("DB_NAME")

# --- Importar models ORM ---
from app.database import Base, SessionLocal
from app.models.categoria import Categoria
from app.models.subcategoria import Subcategoria
from app.models.renomear import Renomear
from app.models.grupo import Grupo

# --- ENGINE TEMP PARA DROP/CREATE DATABASE ---
engine_temp = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}?charset=utf8mb4", echo=True)

resp = input(f"Deseja destruir e recriar o banco '{DB}'? (s/n): ").strip().lower()
if resp == 's':
    conn = engine_temp.raw_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {DB}")
        cursor.execute(f"CREATE DATABASE {DB}")
        conn.commit()
        cursor.close()
        print(f"📦 Banco '{DB}' destruído e recriado.")
    finally:
        conn.close()

# --- ENGINE FINAL ---
engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}")
Session = sessionmaker(bind=engine)
session = Session()

# --- Criar tabelas ORM caso não existam ---
Base.metadata.create_all(bind=engine)
print("📌 Tabelas ORM criadas com sucesso.")

# --- Função para mapear tipos do Excel para SQLAlchemy ---
def map_excel_type_to_sqla(t: str):
    if not t or str(t).strip().lower() == 'nan':
        return String(255)
    ts = str(t).strip().lower()
    m = re.match(r"varchar\s*\(\s*(\d+)\s*\)", ts)
    if m:
        return String(int(m.group(1)))
    m = re.match(r"char\s*\(\s*(\d+)\s*\)", ts)
    if m:
        return String(int(m.group(1)))
    m = re.match(r"decimal\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)", ts)
    if m:
        return DECIMAL(int(m.group(1)), int(m.group(2)))
    if ts.startswith("int"):
        return Integer()
    if ts in ("float", "double", "real"):
        return Float()
    if "text" in ts:
        return Text()
    if ts == "date":
        return Date()
    if ts in ("datetime", "timestamp"):
        return DateTime()
    if ts.startswith("tinyint(1)") or ts in ("bool", "boolean"):
        return Integer()
    return String(255)

# --- Arquivo Excel ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
nome_arquivo = input("Digite o nome do arquivo Excel (ex: dados.xlsx): ").strip()
arquivo = os.path.join(BASE_DIR, "app", "utils", nome_arquivo)

if not os.path.exists(arquivo):
    print(f"❌ Arquivo {arquivo} não encontrado")
    raise SystemExit

planilhas = pd.read_excel(arquivo, sheet_name=None, header=None)
print("\n📑 Abas encontradas:", ", ".join(planilhas.keys()))

# --- PROCESSAMENTO DE CADA ABA ---
for aba, df in planilhas.items():
    try:
        # ====== LEITURA DA PRIMEIRA LINHA ======
        nome_classe = str(df.iloc[0, 0]).strip()  # Grupo
        nome_categoria = str(df.iloc[0, 1]).strip()
        db_subcategoria = str(df.iloc[0, 2]).strip()
        nome_subcategoria = str(df.iloc[0, 3]).strip()
        descricao_subcategoria = str(df.iloc[0, 4]).strip()
        unidade_medida = str(df.iloc[0, 5]).strip() 

        print(f"\n➡️ Aba: {aba}")
        print("Grupo:", nome_classe)
        print("Categoria:", nome_categoria)
        print("Subcategoria DB:", db_subcategoria)
        print("Subcategoria Nome:", nome_subcategoria)
        print("Subcategoria unidade:", unidade_medida)
        print("Descrição Subcategoria:", descricao_subcategoria)

        # --- INSERIR GRUPO (se não existir) ---
        grupo = session.query(Grupo).filter_by(nome_classe=nome_classe).first()
        if not grupo:
            grupo = Grupo(nome_classe=nome_classe)
            session.add(grupo)
            session.flush()
            print(f"✅ Grupo '{nome_classe}' inserido com id {grupo.idClasses}")

        # --- INSERIR CATEGORIA (se não existir) ---
        cat = session.query(Categoria).filter_by(
            nome_categoria=nome_categoria,
            Classes_idClasses=grupo.idClasses
        ).first()
        if not cat:
            cat = Categoria(
                nome_categoria=nome_categoria,
                Classes_idClasses=grupo.idClasses
            )
            session.add(cat)
            session.flush()
            print(f"✅ Categoria '{nome_categoria}' vinculada ao grupo '{nome_classe}'")

        # --- INSERIR SUBCATEGORIA (se não existir) ---
        sub = session.query(Subcategoria).filter_by(db_subcategoria=db_subcategoria).first()
        if not sub:
            sub = Subcategoria(
                nome_subcategoria=nome_subcategoria,
                db_subcategoria=db_subcategoria,
                descricao_subcategoria=descricao_subcategoria,
                unidade_medida=unidade_medida,
                categorias_id_categoria=cat.id_categoria
            )
            session.add(sub)
            session.flush()
            print(f"✅ Subcategoria '{nome_subcategoria}' criada em '{nome_categoria}'")

        # --- CAMPOS DINÂMICOS A PARTIR DO EXCEL ---
        types_row = df.iloc[1, :].tolist() if len(df) > 1 else []
        names_row = df.iloc[2, :].tolist() if len(df) > 2 else []
        campos = []
        for i, name in enumerate(names_row):
            if pd.isna(name) or str(name).strip() == "":
                break
            tipo_txt = types_row[i] if i < len(types_row) else None
            sqla_type = map_excel_type_to_sqla(tipo_txt)
            campos.append((str(name).strip(), tipo_txt, sqla_type))

        # --- INSERIR NA TABELA RENOMEAR ---
        for i, nome_campo in enumerate(names_row):
            if pd.isna(nome_campo) or str(nome_campo).strip() == "":
                continue
            valor_linha3 = str(df.iloc[3, i]).strip() if len(df) > 3 else ""
            if pd.isna(valor_linha3) or valor_linha3 == "":
                continue
            existente = session.query(Renomear).filter_by(renomear_coluna=nome_campo).first()
            if not existente:
                r = Renomear(
                    renomear_coluna=nome_campo,
                    renomear_colunaRenomeada=valor_linha3
                )
                session.add(r)
        session.commit()

        # --- CRIAÇÃO E INSERÇÃO DE DADOS NA TABELA DINÂMICA COM CÓDIGO PRIMÁRIO ---
        metadata = MetaData()
        tabela = Table(
            db_subcategoria,
            metadata,
            Column("codigo_produto", String(19), primary_key=True),  # chave primária
            *(Column(nome_campo, sqla_type) for nome_campo, _, sqla_type in campos)
        )
        tabela.create(bind=engine, checkfirst=True)

        with engine.begin() as conn:
            for idx in range(4, len(df)):
                row = df.iloc[idx, :len(campos)].tolist()
                if all(pd.isna(cell) or str(cell).strip() == "" for cell in row):
                    break
                row_dict = {}
                for i, (nome_campo, _, _) in enumerate(campos):
                    valor = row[i] if i < len(row) else None
                    if pd.isna(valor):
                        valor = None
                    row_dict[nome_campo] = valor

                # --- GERAÇÃO DO CÓDIGO PRIMÁRIO DINÂMICO ---
                gid = grupo.idClasses
                cid = cat.id_categoria
                sid = sub.idsubcategoria

                prefixo = f"{gid:04d}.{cid:04d}.{sid:03d}."
                ultimo = conn.execute(
                    tabela.select()
                        .where(tabela.c.codigo_produto.like(prefixo + "%"))
                        .order_by(tabela.c.codigo_produto.desc())
                ).first()
                prox_seq = 1 if not ultimo else int(ultimo.codigo_produto.split(".")[-1]) + 1
                codigo_produto = f"{gid:04d}.{cid:04d}.{sid:03d}.{prox_seq:04d}"

                row_dict["codigo_produto"] = codigo_produto
                conn.execute(tabela.insert().values(**row_dict))

        session.commit()
        print(f"✅ Tabela '{db_subcategoria}' criada e produtos inseridos com sucesso.\n")

    except Exception as e:
        session.rollback()
        print(f"⚠️ Erro na aba {aba}: {e}")

session.close()
print("🎉 Processo finalizado!")
