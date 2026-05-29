
# 🧠 IndexMe - RAG Architecture AI Agent (Backend)

Este es el núcleo de procesamiento e inteligencia de **IndexMe**. Una API REST robusta construida con **FastAPI** y **LlamaIndex** que implementa una arquitectura **RAG (Retrieval-Augmented Generation)**. Cuenta con un pipeline de ingesta optimizado para evitar duplicidad de archivos mediante hashes únicos e indexación en bases de datos vectoriales.

Desplegado en producción a través de: **[Render](https://personal-assitant-5.onrender.com)**

## 🚀 Tecnologías y Arquitectura

* **Framework API:** FastAPI (Asíncrono, alto rendimiento)
* **Orquestador de IA:** LlamaIndex (Gestión de documentos, nodos y motores de chat)
* **LLM (Modelo de Lenguaje):** Groq (`llama-3.1-8b-instant`) para respuestas ultrarrápidas y precisas.
* **Vector Store (Base de Datos):** Pinecone (Almacenamiento y búsqueda semántica de vectores).
* **Embeddings Locales:** `FastEmbed` (`BAAI/bge-small-en-v1.5`) ejecutado de forma local/ONNX para optimizar el consumo de recursos en la nube.
* **Optimización de Memoria:** Recolección de basura nativa (`gc`) adaptada para entornos de RAM limitada (Capa gratuita de Render).

## 🛡️ Seguridad y CORS
El backend está blindado utilizando `CORSMiddleware` para permitir conexiones estrictamente desde el origen autorizado del frontend en Netlify y entornos locales de desarrollo.

## 🛠️ Configuración Local

### Prerrequisitos
Instalar [Python 3.10+](https://www.python.org/).

### Instalar dependencias
```bash
pip install -r requirements.txt
Variables de Entorno (.env)
Crea un archivo .env en la raíz del backend con las siguientes claves:

Fragmento de código
GROQ_API_KEY=tu_api_key_de_groq
PINECONE_API_KEY=tu_api_key_de_pinecone
FRONTEND_URL=http://localhost:4200
Ejecutar el servidor en Local
Bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
📈 Comando de Producción (Render)
Para evitar picos de memoria RAM en la nube, el servidor corre bajo un único worker optimizado:

Bash
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
