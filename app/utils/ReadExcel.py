import os
import re
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, MetaData, Table, Date, DateTime, DECIMAL
from sqlalchemy.orm import sessionmaker, declarative_base

# --- CONFIG DB ---
USER = "root"
PASSWORD = quote_plus("Supernatur@l1985")
HOST = "localhost"
DB = "db_listaCompras"

# --- ENGINE TEMP PARA DROP/CREATE DATABASE ---
engine_temp = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/")

# --- DROP + CREATE DB ---
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

# --- ORM BASE E TABELAS FIXAS ---
Base = declarative_base()

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_classe = Column(String(255), nullable=False)
    nome_categoria = Column(String(255), nullable=False)

class Subcategoria(Base):
    __tablename__ = "subcategoria"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_subcategoria = Column(String(255), nullable=False)
    db_subcategoria = Column(String(255), nullable=False)
    descricao_subcategoria = Column(String(255), nullable=False)
    categoria_id = Column(Integer, nullable=False)  # sem FK

class Renomear(Base):
    __tablename__ = "Renomear"
    idRenomear = Column(Integer, primary_key=True, autoincrement=True)
    renomear_coluna = Column(String(45), unique=True, nullable=False)
    renomear_colunaRenomeada = Column(String(45), nullable=False)

Base.metadata.create_all(engine)
print("📡 Banco e tabelas fixas prontos!")

# --- FUNÇÃO: mapear string de tipo do Excel para tipo SQLAlchemy ---
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

# --- ARQUIVO EXCEL ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
nome_arquivo = input("Digite o nome do arquivo Excel (ex: dados.xlsx): ").strip()
arquivo = os.path.join(BASE_DIR, nome_arquivo)

if not os.path.exists(arquivo):
    print(f"❌ Arquivo {arquivo} não encontrado na pasta {BASE_DIR}")
    session.close()
    raise SystemExit

planilhas = pd.read_excel(arquivo, sheet_name=None, header=None)
print("\n📑 Abas encontradas:", ", ".join(planilhas.keys()))

# --- PROCESSAMENTO DE CADA ABA ---
for aba, df in planilhas.items():
    try:
        # ====== LEITURA DA PRIMEIRA LINHA ======
        nome_classe = str(df.iloc[0, 0])
        nome_subcategoria = str(df.iloc[0, 1])
        db_subcategoria = str(df.iloc[0, 2])
        nome_categoria = str(df.iloc[0, 3])
        descricao_subcategoria = str(df.iloc[0, 4])

        print(f"\n➡️ Aba: {aba}")
        print("nome_classe:", nome_classe)
        print("nome_subcategoria:", nome_subcategoria)
        print("db_subcategoria:", db_subcategoria)
        print("nome_categoria:", nome_categoria)
        print("descricao_subcategoria:", descricao_subcategoria)

        # --- INSERIR CATEGORIA (se não existir) ---
        cat = session.query(Categoria).filter_by(nome_classe=nome_classe, nome_categoria=nome_categoria).first()
        if not cat:
            cat = Categoria(nome_classe=nome_classe, nome_categoria=nome_categoria)
            session.add(cat)
            session.flush()

        # --- INSERIR SUBCATEGORIA (se não existir) ---
        sub = session.query(Subcategoria).filter_by(db_subcategoria=db_subcategoria).first()
        if not sub:
            sub = Subcategoria(
                nome_subcategoria=nome_subcategoria,
                db_subcategoria=db_subcategoria,
                descricao_subcategoria=descricao_subcategoria,
                categoria_id=cat.id
            )
            session.add(sub)
            session.flush()

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

        # --- EXIBIÇÃO DOS CAMPOS (sem criar tabela dinâmica) ---
        print(f"\n🧩 Nova tabela simulada: {db_subcategoria}")
        print("Campo".ljust(30), "Tipo (Excel)".ljust(20), "Tipo (SQLAlchemy/MySQL)")
        print("-" * 80)
        print("id".ljust(30), "-".ljust(20), "Integer (PK, autoincrement)")
        for nome_campo, tipo_txt, sqla_type in campos:
            tipo_excel = "-" if (tipo_txt is None or str(tipo_txt).lower() == "nan") else str(tipo_txt)
            print(nome_campo.ljust(30), tipo_excel.ljust(20), str(sqla_type))

        # --- CRIAÇÃO E INSERÇÃO DE DADOS NA TABELA DINÂMICA ---
        metadata = MetaData()
        tabela = Table(
            db_subcategoria,
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
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
                conn.execute(tabela.insert().values(**row_dict))

        session.commit()
        print(f"✅ Tabela '{db_subcategoria}' criada e dados inseridos com sucesso.\n")

    except Exception as e:
        session.rollback()
        print(f"⚠️ Erro na aba {aba}: {e}")

session.close()
print("🎉 Processo finalizado!")
