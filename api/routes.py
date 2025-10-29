from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.funcionarios import Funcionario
from app.models.dados_pedido import DadosPedido
from app.models.pedido import Pedido    
from app.models.chefia_direta import ChefiaDireta
from pydantic import BaseModel
from api.schemas.loginRequest import LoginRequest
from passlib.context import CryptContext
from api.utils.security import verificar_senha

#------------------------------
# Fast API
#------------------------------

api = FastAPI(title="Minha API MVC")


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
