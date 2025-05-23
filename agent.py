from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from config import llm
from tools import retrieve, search_paper

memory = MemorySaver()

agent_executor = create_react_agent(
    llm, 
    [retrieve, search_paper], 
    checkpointer=memory, 
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