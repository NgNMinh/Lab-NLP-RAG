from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver, InMemorySaver
from config import llm
from tools import retrieve, search_paper, get_all_personnel, get_all_intern, delete_user
from langgraph.checkpoint.mongodb import MongoDBSaver
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from prompts import user_prompt
load_dotenv()

DB_URI = os.getenv("MONGO_URI")
memory = InMemorySaver()

checkpointer = MongoDBSaver.from_conn_string(
    conn_string=DB_URI,
    db_name="NLK-PD",
    collection_name="chat_history",
)

agent_user = create_react_agent(
    llm, 
    [retrieve, search_paper], 
    checkpointer=checkpointer, 
    prompt=user_prompt
) 

agent_admin = create_react_agent(
    llm, 
    [get_all_intern, get_all_personnel, retrieve, search_paper, delete_user], 
    checkpointer=memory, 
    prompt="""
Bạn là trợ lí AI thân thiện chuyên hỗ trợ quản trị viên của NLP & KD Lab thuộc trường Đại học Tôn Đức Thắng (TDTU).
"""
)