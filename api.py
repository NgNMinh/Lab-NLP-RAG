from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
from agent import agent_executor

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/chat")
def chat_response(msg: Message):
    input_message = msg.message
    config = {"configurable": {"thread_id": "def234"}}
    
    responses = ""
    for event in agent_executor.stream(
        {"messages": [{"role": "user", "content": input_message}]},
        stream_mode="updates",
        config=config,
    ):
        if event.get('agent') and event['agent']['messages'][0].content:
            responses = responses + event['agent']['messages'][0].content
    print(responses)
    return {"reply": responses}

@app.get("/")
def read_root():
    return {"Hello": "World"} 