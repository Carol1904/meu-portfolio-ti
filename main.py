from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "Online",
        "mensagem": "API da Ana Caroline rodando com sucesso!",
        "desenvolvedora": "Ana Caroline",
        "tecnologias": ["Python", "FastAPI", "Git", "AWS"]
    }