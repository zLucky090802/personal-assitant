


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


def process_and_upload_file(file_path, vector_store):
    """Procesa el archivo subido por el usuario y lo indexa a Pinecone"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró ningún archivo en la ruta: {file_path}")
    try:
        
        documents = SimpleDirectoryReader(
            input_files=[file_path]
        ).load_data()
        
        file_name = os.path.basename(file_path)
        for doc in documents:
            doc.metadata["file_name"] = file_name
            
        pipeline = IngestionPipeline(
            transformations = get_transformation(),
            vector_store = vector_store,
        
        )
        
        processed_node = pipeline.run(documents=documents, show_progress=True, num_workers=1)
        
        print(f'\n Pipeline completed')
        print(f'    Nodes returned: {len(processed_node)}')
    except Exception as e:
        print(f"Error durante el procesamiento del archivo: {e}")
        raise e
        

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
   
   vector_store = index.vector_store
   
   ruta_local = "C:/Users/Daniel/Documents/Documentos personales/Daniel Espitia resume.pdf"
   
   process_and_upload_file(ruta_local, vector_store)
   
   query_engine = index.as_query_engine()
   
 
   
   response = query_engine.query(query)
   
   return {
       'status':'success',
       'response': response.response
   }


