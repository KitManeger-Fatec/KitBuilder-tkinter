import random
from datetime import date, datetime, timedelta

from app.database import SessionLocal, Base, engine
from app.models.funcionarios import Funcionario
from app.models.chefia_direta import ChefiaDireta

def random_date(start_date: date, end_date: date) -> date:
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))

def main():
    # Garante que as tabelas existem
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        nomes = [
            "Ana", "Bruno", "Carla", "Daniel", "Eduardo",
            "Fernanda", "Gabriel", "Helena", "Igor", "Juliana",
        ]
        cargos = ["Comprador", "Analista", "Chefe", "Gerente"]

        funcionarios = []
        for _ in range(10):
            nome = random.choice(nomes) + f" {random.randint(1,99)}"
            
            # Nível invertido: 1 = mais baixo, 5 = mais alto
            nivel_aleatorio = random.randint(1,5)

            f = Funcionario(
                nome_funcionario=nome,
                cargo_funcionario=random.choice(cargos),
                nivel_funcionario=nivel_aleatorio,
                usuario_funcionario=nome.lower().replace(" ", "")[:12],
                senha_funcionario="senha_hash",
                email_funcionario=f"{nome.lower().replace(' ','_')}@empresa.com",
                foi_criado_em=random_date(date(2023,1,1), date.today()),
                ultimo_acesso_em=datetime.now()
            )
            funcionarios.append(f)
            session.add(f)

        session.flush()  # garante que os IDs foram gerados

        # Cria vínculos de chefia aleatórios
        for func in funcionarios:
            chefe = random.choice(funcionarios)
            if chefe.idfuncionarios != func.idfuncionarios:
                session.add(
                    ChefiaDireta(
                        id_funcionario=func.idfuncionarios,
                        id_chefia=chefe.idfuncionarios
                    )
                )

        session.commit()

        # Para teste: fingir login de um funcionário e enviar apenas o ID
        funcionario_logado = random.choice(funcionarios)
        id_logado = funcionario_logado.idfuncionarios
        print(f"💡 Funcionário logado (apenas ID): {id_logado}")

if __name__ == "__main__":
    main()
