from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from config import llm
from tools import retrieve, search_paper, get_all_personnel, get_all_intern, delete_user
from langgraph.checkpoint.mongodb import MongoDBSaver
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

# DB_URI = os.getenv("MONGO_URI")
# checkpointer = MongoDBSaver.from_conn_string(DB_URI)
checkpointer = MemorySaver()

agent_user = create_react_agent(
    llm, 
    [retrieve, search_paper], 
    checkpointer=checkpointer, 
    prompt="""
Bạn là trợ lí AI thân thiện chuyên hỗ trợ hỏi đáp cho NLP & KD Lab thuộc trường Đại học Tôn Đức Thắng (TDTU). 
Khi bạn sử dụng bất kỳ tool nào (như 'retrieve' hoặc 'search_paper'), 
nếu tool trả về thông tin hoặc dữ liệu có giá trị, hãy dùng kết quả đó thành một câu trả lời hoàn chỉnh 
và thân thiện để gửi đến người dùng. KHÔNG kết thúc với câu "tôi đã tìm được..." mà KHÔNG hiển thị thông tin chi tiết.

Ví dụ:
- Nếu tool tìm thấy bài báo, hãy liệt kê tên bài báo và tác giả.
- Nếu tool trả về danh sách, hãy viết lại danh sách đó theo cách dễ hiểu.

Luôn đảm bảo người dùng nhìn thấy kết quả có ích từ tool.
"""
) 

agent_admin = create_react_agent(
    llm, 
    [get_all_intern, get_all_personnel, retrieve, search_paper, delete_user], 
    checkpointer=checkpointer, 
    prompt="""
Bạn là trợ lí AI thân thiện chuyên hỗ trợ quản trị viên của NLP & KD Lab thuộc trường Đại học Tôn Đức Thắng (TDTU).
"""
)