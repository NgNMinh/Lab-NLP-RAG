from typing import Optional, Literal
from langchain_core.tools import tool
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import vector_store
from dotenv import load_dotenv
import os
import requests
import re

load_dotenv()

def is_valid_email(email: str) -> bool:
    # Biểu thức chính quy kiểm tra định dạng email
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

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
    client = MongoClient(os.getenv("MONGO_URI"))
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

@tool
def get_all_personnel() -> dict:
    """
    Get all personnel users 
    """
    url = "http://localhost:3000/users/api/v1/personnel"
    
    # Nếu API không cần xác thực
    response = requests.get(url)
    
    # Nếu cần token Bearer (thêm Authorization header)
    # headers = {"Authorization": "Bearer YOUR_TOKEN"}
    # response = requests.get(url, headers=headers)
    
    print("Status code:", response.status_code)
    try:
        return response.json()
    except Exception as e:
        print("Không phải JSON:", response.text)
        return {"error": "Failed to retrieve users"}
    
@tool
def get_all_intern() -> dict:
    """
    Get all intern users 
    """
    url = "http://localhost:3000/users/api/v1/intern"
    
    # Nếu API không cần xác thực
    response = requests.get(url)
    
    # Nếu cần token Bearer (thêm Authorization header)
    # headers = {"Authorization": "Bearer YOUR_TOKEN"}
    # response = requests.get(url, headers=headers)
    
    print("Status code:", response.status_code)
    try:
        return response.json()
    except Exception as e:
        print("Không phải JSON:", response.text)
        return {"error": "Failed to retrieve users"}    
    
@tool
def delete_user(email: Optional[str], mobile: Optional[str], user_name: Optional[str]) -> str:
    """
    Xóa user dựa trên email, mobile hoặc user_name.
    Nếu đã cung cấp 1 thông tin thì không cần hỏi lại vì mỗi thông tin đều là duy nhất.
    """
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["NLK-PD"]
    collection = db["users"]  # sửa theo tên collection thật sự của bạn

    # Tạo bộ lọc theo điều kiện được cung cấp
    filter_query = {}
    if email:
        filter_query["email"] = email
    if mobile:
        filter_query["mobile"] = mobile
    if user_name:
        filter_query["username"] = user_name

    if email and not is_valid_email(email):
        return "Email không hợp lệ."

    if not filter_query:
        return {"status": "error", "message": "Cần ít nhất một thông tin để xóa (email, mobile hoặc user_name)."}

    result = collection.delete_one(filter_query)

    if result.deleted_count > 0:
        return "User đã được xóa."
    else:
        return"Không tìm thấy user phù hợp để xóa."