from fastapi import FastAPI, Depends, HTTPException
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

Base.metadata.create_all(bind=engine)

# Modelo Pydantic para validação
class ProjetoSchema(BaseModel):
    nome: str
    tecnologia: str

    class Config:
        from_attributes = True

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"mensagem": "API de Portfólio completa com CRUD e Banco de Dados SQL!"}

# 1. READ (Buscar todos)
@app.get("/projetos")
def listar_projetos(db: Session = Depends(get_db)):
    return db.query(ProjetoDB).all()

# 2. CREATE (Cadastrar)
@app.post("/projetos")
def cadastrar_projeto(projeto: ProjetoSchema, db: Session = Depends(get_db)):
    novo_projeto = ProjetoDB(nome=projeto.nome, tecnologia=projeto.tecnologia)
    db.add(novo_projeto)
    db.commit()
    db.refresh(novo_projeto)
    return {"mensagem": "Projeto salvo com sucesso!", "projeto": novo_projeto}

# 3. UPDATE (Atualizar por ID)
@app.put("/projetos/{projeto_id}")
def atualizar_projeto(projeto_id: int, dados_atualizados: ProjetoSchema, db: Session = Depends(get_db)):
    projeto_existente = db.query(ProjetoDB).filter(ProjetoDB.id == projeto_id).first()
    
    if not projeto_existente:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    projeto_existente.nome = dados_atualizados.nome
    projeto_existente.tecnologia = dados_atualizados.tecnologia
    
    db.commit()
    db.refresh(projeto_existente)
    return {"mensagem": "Projeto atualizado com sucesso!", "projeto": projeto_existente}

# 4. DELETE (Remover por ID)
@app.delete("/projetos/{projeto_id}")
def deletar_projeto(projeto_id: int, db: Session = Depends(get_db)):
    projeto_existente = db.query(ProjetoDB).filter(ProjetoDB.id == projeto_id).first()
    
    if not projeto_existente:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    db.delete(projeto_existente)
    db.commit()
    return {"mensagem": f"Projeto ID {projeto_id} removido com sucesso!"}