


import os
from dotenv import load_dotenv

import tempfile

from llama_index.core import VectorStoreIndex, Settings

from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler

from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.groq import Groq
from llama_index.core.chat_engine.types import ChatMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.embeddings.huggingface import SentenceTransformerEmbedding
from llama_index.core.postprocessor import SentenceEmbeddingOptimizer
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore, QueryBundle
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline

from fastapi import UploadFile
import shutil



#configuration

INDEX_NAME = 'personal-assitant'
api_key = os.getenv('GROQ_API_KEY')
llm = Groq(
    model='llama-3.1-8b-instant',
    api_key=api_key
)

Settings.llm = llm
Settings.embed_model = HuggingFaceEmbedding(
    model_name="mixedbread-ai/mxbai-embed-large-v1"
)
Settings.chunk_size = 512
Settings.chunk_overlap = 50


def get_index():
     #conecto to pinecone vector stroe and retunr index
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    
    pinecone_index = pc.Index(INDEX_NAME)
    
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    return index


def process_and_upload_file(file: UploadFile):
    """
    Recibe cualquier archivo desde la API, lo guarda temporalmente,
    lo procesa con LlamaIndex (soporta múltiples formatos) y limpia el disco.
    """
    uplaod_dir = '../../data'
    os.makedirs(uplaod_dir, exist_ok=True)
    
    file_path = os.path.join(uplaod_dir, file.filename)
    
    try:
        #guardar el archivo fisicamente de forma temporal
        
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        #cargar datos 
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        
        for doc in documents:
            doc.metadata['file_name'] = file.filename
            
        #run pipeline ingestion to pinecone
        
        index = get_index()
        pipeline = IngestionPipeline(
            transformations=get_transformation(),
            vector_store=index.vector_store,
        )
        
        processed_nodes = pipeline.run(documents=documents, show_progress=True, num_workers=1)
        return len(processed_nodes)
    
    except Exception as e:
        print(f'Error en el servicio al procesar archivo: {e}')
        raise e
    finally:
        #limpieza absoluto del servidor local
        if os.path.exists(file_path):
            os.remove(file_path)
        

def get_transformation():
    return [
        SentenceSplitter(
            chunk_size=Settings.chunk_size,
            chunk_overlap=Settings.chunk_overlap
        ),
        Settings.embed_model
    ]
    
def query(query:str):
    
   index = get_index()
   query_engine = index.as_query_engine()
   response = query_engine.query(query)
   
   return {
       'status':'success',
       'response': response.response
   }


