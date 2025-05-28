from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Model configuration
model_id = "gemini-2.0-flash" 

llm = ChatGoogleGenerativeAI(
    model=model_id,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# Embeddings configuration
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

client = MongoClient(os.getenv("MONGO_URI"))
collection = client["NLK-PD"]["lab_data"]  

# Xóa dữ liệu cũ trong collection
# collection.delete_many({})

vector_store = MongoDBAtlasVectorSearch(
    embedding=embeddings,
    collection=collection,
    index_name="vector_index",  
    relevance_score_fn="cosine",
)

# # Document loading and processing
# loader = PyPDFLoader('data/lab RAG.pdf')
# docs = loader.load()
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# all_splits = text_splitter.split_documents(docs)

# # Index chunks
# _ = vector_store.add_documents(documents=all_splits) 
