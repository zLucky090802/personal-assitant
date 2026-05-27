import nest_asyncio
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Importación directa y limpia
from app.api.routes import router as api_router

load_dotenv()
nest_asyncio.apply()
app = FastAPI(title='personal-assistant')

# 1. Obtenemos la URL de producción desde las variables de entorno.
#    Si no existe (como en tu PC local), se usará por defecto el puerto de Angular/Vite/React.
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173") 

# 2. Configuramos los orígenes permitidos de forma explícita
origins = [
    "https://index-me.netlify.app",
    "http://localhost:4200", # Por si necesitas probar localmente
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite POST, GET, OPTIONS, etc.
    allow_headers=["*"], # Permite Content-Type, Authorization, etc.
)

# Acoplamos tus rutas de LlamaIndex
app.include_router(api_router, prefix='/api')

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3003))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)