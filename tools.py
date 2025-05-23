from typing import Optional, Literal
from langchain_core.tools import tool
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import vector_store

@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to NLP & KD Lab TDTU like introduction, lab staff, contact address"""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

@tool
def search_paper(author: Optional[Literal["Lê Anh Cường", "Trần Thanh Phước", "Nguyễn Chí Thiện", "Trần Lương Quốc Đại", "Hồ Thị Linh"]], year: Optional[int] = None) -> list[dict]:
    '''
    Search paper of TDTU 
    '''
    client = MongoClient("mongodb+srv://mongodb:supersecret@cluster0.wvspy.mongodb.net/NLK-PD")
    db = client["NLK-PD"]

    query = {}
    if author == "Lê Anh Cường":
        query["owner_id"] = ObjectId("682bdb29f7c406761c467d93")
    elif author == "Trần Thanh Phước":
        query["owner_id"] = ObjectId("682bdb2af7c406761c467d98")
    elif author == "Nguyễn Chí Thiện":
        query["owner_id"] = ObjectId("682bdb2bf7c406761c467d9b")
    elif author == "Trần Lương Quốc Đại":
        query["owner_id"] = ObjectId("682bdb2cf7c406761c467d9e")
    elif author == "Hồ Thị Linh":
        query["owner_id"] = ObjectId("682bdb2df7c406761c467da1")

    if year:
        query["publicationDate"] = year

    results = list(db.publications.find(query).limit(5))
    
    return results 