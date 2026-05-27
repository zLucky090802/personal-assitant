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
    FRONTEND_URL,
    "http://localhost:5173",  # Asegura compatibilidad con tu entorno de desarrollo local
    "http://localhost:3000"   # Por si usas otro puerto común localmente
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # <-- Ya no es '*', ahora está restringido
    allow_credentials=True,      # Permite el flujo de cookies o headers de autenticación si los necesitas
    allow_methods=['*'],
    allow_headers=['*']
)

# Acoplamos tus rutas de LlamaIndex
app.include_router(api_router, prefix='/api')

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3003))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)