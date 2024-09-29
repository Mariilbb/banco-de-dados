from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.engine.url import URL

# CONFIGURAR CONEXÃO
DATABASE_URL = URL.create(
    drivername="mysql+mysqlconnector",
    username="root",
    password="",
    host="localhost",
    database="aluguel_bancos"
)

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# CLASSES
class Pessoa(Base):
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    cpf = Column(String(14), unique=True)
    telefone = Column(String(20))
    email = Column(String(100))
    endereco = Column(String(255))

class Corretor(Base):
    __tablename__ = 'corretores'
    id = Column(Integer, ForeignKey('pessoas.id'), primary_key=True)
    creci = Column(String(20), unique=True)

class Proprietario(Base):
    __tablename__ = 'proprietarios'
    id = Column(Integer, ForeignKey('pessoas.id'), primary_key=True)
    corretor_id = Column(Integer, ForeignKey('corretores.id'))

class Inquilino(Base):
    __tablename__ = 'inquilinos'
    id = Column(Integer, ForeignKey('pessoas.id'), primary_key=True)
    corretor_id = Column(Integer, ForeignKey('corretores.id'))

class Imovel(Base):
    __tablename__ = 'imoveis'
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(255))
    endereco = Column(String(255))
    valor = Column(Float)
    tipo = Column(String(50))
    proprietario_id = Column(Integer, ForeignKey('proprietarios.id'))
    inquilino_id = Column(Integer, ForeignKey('inquilinos.id'), nullable=True)

# CRUD 

# CRIAR 
def criar(session, model, **kwargs):
    obj = session.query(model).filter_by(**{k: v for k, v in kwargs.items() if k != 'id'}).first()
    if obj: return obj
    obj = model(**kwargs)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

# LISTAR
def listar(session, model):
    return session.query(model).all()

#ATUALIZAR
def atualizar(session, model, obj_id, **kwargs):
    obj = session.query(model).get(obj_id)
    for k, v in kwargs.items():
        if v: setattr(obj, k, v)
    session.commit()

# DELETAR
def deletar(session, model, obj_id):
    obj = session.query(model).get(obj_id)
    session.delete(obj)
    session.commit()

# MENU INTERATIVO
def menu():
    session = SessionLocal()
    while True:
        opcao = int(input(
            "\n=== Menu Sistema de Aluguel de Imóveis ===\n"
            "1. Adicionar Pessoa\n2. Listar Pessoas\n3. Atualizar Pessoa\n4. Deletar Pessoa\n"
            "5. Adicionar Corretor\n6. Listar Corretores\n7. Atualizar Corretor\n8. Deletar Corretor\n"
            "9. Adicionar Proprietário\n10. Listar Proprietários\n11. Atualizar Proprietário\n12. Deletar Proprietário\n"
            "13. Adicionar Inquilino\n14. Listar Inquilinos\n15. Atualizar Inquilino\n16. Deletar Inquilino\n"
            "17. Adicionar Imóvel\n18. Listar Imóveis\n19. Atualizar Imóvel\n20. Deletar Imóvel\n"
            "21. Sair\nEscolha uma opção: "))

        if opcao == 1:
            criar(session, Pessoa, nome=input("Nome: "), cpf=input("CPF: "), telefone=input("Telefone: "), email=input("Email: "), endereco=input("Endereço: "))
        elif opcao == 2:
            for p in listar(session, Pessoa): print(f"{p.id} - {p.nome}, {p.cpf}")
        elif opcao == 3:
            atualizar(session, Pessoa, int(input("ID da Pessoa: ")), nome=input("Novo Nome: "), telefone=input("Novo Telefone: "), email=input("Novo Email: "), endereco=input("Novo Endereço: "))
        elif opcao == 4:
            deletar(session, Pessoa, int(input("ID da Pessoa: ")))

        elif opcao == 5:
            criar(session, Corretor, id=int(input("ID da Pessoa: ")), creci=input("CRECI: "))
        elif opcao == 6:
            for c in listar(session, Corretor): print(f"{c.id} - CRECI: {c.creci}")
        elif opcao == 7:
            atualizar(session, Corretor, int(input("ID do Corretor: ")), creci=input("Novo CRECI: "))
        elif opcao == 8:
            deletar(session, Corretor, int(input("ID do Corretor: ")))

        elif opcao == 9:
            criar(session, Proprietario, id=int(input("ID da Pessoa: ")), corretor_id=int(input("ID do Corretor: ")))
        elif opcao == 10:
            for p in listar(session, Proprietario): print(f"{p.id} - Corretor ID: {p.corretor_id}")
        elif opcao == 11:
            atualizar(session, Proprietario, int(input("ID do Proprietário: ")), corretor_id=int(input("Novo Corretor ID: ")))
        elif opcao == 12:
            deletar(session, Proprietario, int(input("ID do Proprietário: ")))

        elif opcao == 13:
            criar(session, Inquilino, id=int(input("ID da Pessoa: ")), corretor_id=int(input("ID do Corretor: ")))
        elif opcao == 14:
            for i in listar(session, Inquilino): print(f"{i.id} - Corretor ID: {i.corretor_id}")
        elif opcao == 15:
            atualizar(session, Inquilino, int(input("ID do Inquilino: ")), corretor_id=int(input("Novo Corretor ID: ")))
        elif opcao == 16:
            deletar(session, Inquilino, int(input("ID do Inquilino: ")))

        elif opcao == 17:
            criar(session, Imovel, descricao=input("Descrição: "), endereco=input("Endereço: "), valor=float(input("Valor: ")), tipo=input("Tipo: "), proprietario_id=int(input("ID do Proprietário: ")))
        elif opcao == 18:
            for im in listar(session, Imovel): print(f"{im.id} - {im.descricao}, {im.endereco}")
        elif opcao == 19:
            atualizar(session, Imovel, int(input("ID do Imóvel: ")), descricao=input("Nova Descrição: "), endereco=input("Novo Endereço: "), valor=float(input("Novo Valor: ")), tipo=input("Novo Tipo: "))
        elif opcao == 20:
            deletar(session, Imovel, int(input("ID do Imóvel: ")))

        elif opcao == 21:
            session.close()
            break

if __name__ == "__main__":
    menu()
