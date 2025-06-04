from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
from agent import agent_user, agent_admin
import uuid
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver, InMemorySaver
from config import llm
from tools import retrieve, search_paper, get_all_personnel, get_all_intern, delete_user
from langgraph.checkpoint.mongodb import MongoDBSaver
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from prompts import user_prompt, admin_prompt
from fastapi.responses import StreamingResponse

load_dotenv()
DB_URI = os.getenv("MONGO_URI")

def is_json_list(text: str):
    try:
        parsed = json.loads(text)
        return isinstance(parsed, list)
    except json.JSONDecodeError:
        return False
    
app = FastAPI()

class Message(BaseModel):
    message: str
user_thread_id = str(uuid.uuid4())

@app.post("/chat")
def chat_response(msg: Message):
    input_message = msg.message
    config = {"configurable": {"thread_id": user_thread_id}}
    
    responses = ""
    with MongoDBSaver.from_conn_string(
        conn_string=os.getenv("MONGO_URI"),
        db_name="NLK-PD",
    ) as checkpointer:
        agent_user = create_react_agent(
            llm, 
            [retrieve, search_paper], 
            checkpointer=checkpointer, 
            prompt=user_prompt
        ) 
        for event in agent_user.stream(
            {"messages": [{"role": "user", "content": input_message}]},
            config=config,
        ):
            if event.get('agent') and event['agent']['messages'][0].content:
                responses = responses + event['agent']['messages'][0].content
    return {"reply": responses}

@app.get("/")
def read_root():
    return {"Hello": "World"} 

admin_thread_id = str(uuid.uuid4())

@app.post("/admin/chat")
def chat_response(msg: Message):
    input_message = msg.message
    config = {"configurable": {"thread_id": admin_thread_id}}
    
    responses = ""
    with MongoDBSaver.from_conn_string(
        conn_string=os.getenv("MONGO_URI"),
        db_name="NLK-PD",
    ) as checkpointer:
        agent_admin = create_react_agent(
            llm, 
            [get_all_intern, get_all_personnel, retrieve, search_paper, delete_user], 
            checkpointer=checkpointer, 
            prompt=admin_prompt)
        
        for event in agent_admin.stream(
            {"messages": [{"role": "user", "content": input_message}]},
            stream_mode="updates",
            config=config,
        ):
            if event.get('agent') and event['agent']['messages'][0].content:
                responses = responses + event['agent']['messages'][0].content
    return {"reply": responses}