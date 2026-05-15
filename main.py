import os
from dotenv import load_dotenv

import tempfile

from llama_index.core import VectorStoreIndex, Settings

from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler
import streamlit as st
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.groq import Groq
from llama_index.core.chat_engine.types import ChatMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.postprocessor import SentenceEmbeddingOptimizer
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore, QueryBundle
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline


load_dotenv()

#configuration

INDEX_NAME = 'personal-assitant'
api_key = os.getenv('GROQ_API_KEY')
llm = Groq(
    model='llama-3.1-8b-instant',
    api_key=api_key
)

Settings.llm = llm
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.chunk.size = 512
Settings.chunk_overlap = 50


def get_index():
     #conecto to pinecone vector stroe and retunr index
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    
    pinecone_index = pc.Index(INDEX_NAME)
    
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    return index


def process_and_upload_file(uploaded_file, vector_store):
    """Procesa el archivo subido por el usuario y lo indexa a Pinecone"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
        
    try:
        documents = SimpleDirectoryReader(
            input_files=[tmp_path]
        ).load_data()
        
        pipeline = IngestionPipeline(
            transformations = get_transformation(),
            vector_store = vector_store,
        
        )
        
        processed_node = pipeline.run(documents=documents, show_progress=True, num_workers=4)
        
        print(f'\n Pipeline completed')
        print(f'    Nodes returned: {len(processed_node)}')
    finally:
        os.remove(tmp_path)
        

def get_transformation():
    return [
        SentenceSplitter(
            chunk_size=Settings.chunk_size,
            chunk_overlap=Settings.chunk_overlap
        ),
        Settings.embed_model
    ]
    


def main():
   
   
   sentence_optimizer = SentenceEmbeddingOptimizer(
       embed_model=Settings.embed_model,
       percentile_cutoff=0.5,
       threshold_cutoff=0.7,
       context_before=1,
       context_after=1,
   )

if __name__ == '__main__':
    main()