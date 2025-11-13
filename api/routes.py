from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from fastapi.staticfiles import StaticFiles
from app.models.funcionarios import Funcionario
from app.models.dados_pedido import DadosPedido
from app.models.pedido import Pedido    
from app.models.chefia_direta import ChefiaDireta
from pydantic import BaseModel
from api.schemas.loginRequest import LoginRequest
from passlib.context import CryptContext
from api.utils.security import verificar_senha
from fastapi.middleware.cors import CORSMiddleware



#------------------------------
# Fast API
#------------------------------

api = FastAPI(title="Minha API MVC")
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://127.0.0.1:5000"] se quiser limitar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# monta /assets -> app/assets (ex: /assets/images/arquivo.jpg)
api.mount("/assets", StaticFiles(directory="assets"), name="assets")


# Dependência para injetar a sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@api.get("/")
def home():
    return {"status": "ok", "mensagem": "API FastAPI conectada ao MVC!"}


@api.get("/pedidos")
def get_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(DadosPedido).all()
    return [pedido.to_dict() for pedido in pedidos]

@api.get("/pedido/{id_pedido}")
def get_linhas_pedido(id_pedido: int, db: Session = Depends(get_db)):
    # Busca todas as linhas do pedido com id_dados_pedido = id_pedido
    linhas = db.query(Pedido).filter(Pedido.id_dados_pedido == id_pedido, Pedido.aceito == 1).all()

    # Retorna cada linha em dicionário
    return [linha.to_dict() for linha in linhas]

@api.get("/dadosFuncionarios/{id_funcionario}")
def get_dados_funcionario(id_funcionario: int, db: Session = Depends(get_db)):
    funcionario = db.query(Funcionario).filter(Funcionario.idfuncionarios == id_funcionario).first()
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return {
        "idfuncionarios": funcionario.idfuncionarios,
        "nome_funcionario": funcionario.nome_funcionario,
        "cargo_funcionario": funcionario.cargo_funcionario,
        "nivel_funcionario": funcionario.nivel_funcionario,
    }

@api.get("/chefes/{id_funcionario}")
def get_chefes(id_funcionario: int, db: Session = Depends(get_db)):
    registros = db.query(ChefiaDireta).filter(ChefiaDireta.id_funcionario == id_funcionario).all()

    
    return [
        {
            "id_confere": reg.id_confere,
            "id_funcionario": reg.id_funcionario,
            "funcionario_nome": reg.funcionario.nome_funcionario if reg.funcionario else None,
            "id_chefia": reg.id_chefia,
            "chefe_nome": reg.chefe.nome_funcionario if reg.chefe else None,
        }
        for reg in registros
    ]

@api.post("/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Funcionario).filter(
        Funcionario.usuario_funcionario == request.username
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    # Aqui usamos bcrypt para verificar a senha
    if not verificar_senha(request.password, user.senha_funcionario):
        raise HTTPException(status_code=401, detail="Senha incorreta")

    return {
        "message": "Login bem-sucedido",
        "id": user.idfuncionarios,  # campo correto do seu modelo
        "usuario": user.usuario_funcionario,
        # "token": gerar_jwt(user.id_funcionario)  # opcional
    }

@api.get("/produto/{codigo}/imagem")
def get_produto_imagem(codigo: str, db: Session = Depends(get_db)):
    partes = codigo.split(".")
    if len(partes) != 4:
        raise HTTPException(400, "Código inválido")
    subcat_id = int(partes[2])

    sql_sub = text("SELECT db_subcategoria FROM subcategoria WHERE idsubcategoria = :id_sub")
    result = db.execute(sql_sub, {"id_sub": subcat_id}).fetchone()
    if not result:
        raise HTTPException(404, "Subcategoria não encontrada")

    nome_tabela = result[0]
    sql_item = text(f"SELECT imagem FROM {nome_tabela} WHERE codigo_produto = :codigo")
    item = db.execute(sql_item, {"codigo": codigo}).fetchone()
    if not item:
        raise HTTPException(404, "Item não encontrado")

    imagem_campo = item[0]  # ex: "images/botao_verde.jpg" ou "botao_verde.jpg"

    # 3️⃣ normaliza o caminho (sem app/)
    if imagem_campo.startswith("images/"):
        imagem_url = f"/assets/{imagem_campo}"
    else:
        imagem_url = f"/assets/images/{imagem_campo}"

    return {"codigo": codigo, "tabela": nome_tabela, "imagem": imagem_url}