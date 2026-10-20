from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modelo de dados que a API espera receber
class Projeto(BaseModel):
    id: int
    nome: str
    tecnologia: str

# Nosso "banco de dados" temporário na memória
banco_de_projetos = [
    {"id": 1, "nome": "Meu Portfolio TI", "tecnologia": "FastAPI & Python"},
    {"id": 2, "nome": "Automação AWS", "tecnologia": "Python & Cloud"}
]

@app.get("/")
def home():
    return {"mensagem": "API de Portfólio da Ana Caroline"}

# Rota para LISTAR todos os projetos (GET)
@app.get("/projetos")
def listar_projetos():
    return banco_de_projetos

# Rota para CADASTRAR um novo projeto (POST)
@app.post("/projetos")
def cadastrar_projeto(novo_projeto: Projeto):
    banco_de_projetos.append(novo_projeto.model_dump())
    return {"mensagem": "Projeto cadastrado com sucesso!", "projeto": novo_projeto}