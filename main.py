from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configuração do Banco de Dados SQLite
DATABASE_URL = "sqlite:///./portfolio.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo da Tabela no Banco de Dados
class ProjetoDB(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    tecnologia = Column(String)

# Cria as tabelas no banco de dados automaticamente
Base.metadata.create_all(bind=engine)

# Modelo Pydantic para validação de dados recebidos na API
class ProjetoSchema(BaseModel):
    nome: str
    tecnologia: str

    class Config:
        from_attributes = True

app = FastAPI()

# Função para obter a conexão com o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"mensagem": "API de Portfólio conectada ao Banco de Dados SQL!"}

# Rota GET: Busca todos os projetos salvos no Banco de Dados
@app.get("/projetos")
def listar_projetos(db: Session = Depends(get_db)):
    projetos = db.query(ProjetoDB).all()
    return projetos

# Rota POST: Salva um novo projeto permanentemente no Banco de Dados
@app.post("/projetos")
def cadastrar_projeto(projeto: ProjetoSchema, db: Session = Depends(get_db)):
    novo_projeto = ProjetoDB(nome=projeto.nome, tecnologia=projeto.tecnologia)
    db.add(novo_projeto)
    db.commit()
    db.refresh(novo_projeto)
    return {"mensagem": "Projeto salvo no banco de dados com sucesso!", "projeto": novo_projeto}