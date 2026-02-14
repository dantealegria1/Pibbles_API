from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Pibble API Free")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# CONFIGURACIÓN DE TU REPO
GITHUB_USER = "dantealegria1"
REPO_NAME = "Pibble_API"
BRANCH = "main"
FOLDER = "mis_pibbles" # La carpeta donde están las fotos en GitHub

BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{FOLDER}"

@app.get("/pibbles")
def get_pibbles():
    # Como ya sabes que descargaste 100 imágenes con nombres predecibles:
    coleccion = []
    for i in range(1, 101):
        coleccion.append({
            "id": i,
            "name": f"Pibble {i}",
            "url": f"{BASE_URL}/pibble_{i}.jpg"
        })
    
    return {"total": len(coleccion), "data": coleccion}

@app.get("/")
def home():
    return {"mensaje": "API de Pibbles funcionando. Ve a /pibbles para ver la colección."}