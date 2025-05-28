# Lab NLP RAG Project

Dự án này sử dụng LangChain và Google Gemini để xây dựng hệ thống RAG (Retrieval-Augmented Generation) cho phòng lab NLP TDTU.

## Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd Lab-NLP-RAG
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Cài đặt các dependencies:
```bash
pip install -r requirements.txt
```

## Cấu hình

1. Tạo file `.env` trong thư mục gốc của dự án:
```bash
touch .env
```

2. Thêm API key của Google Gemini và đường dẫn Mongodb vào file `.env` :
```
GEMINI_API_KEY=your_api_key_here
MONGO_URI=your_url_here
```

Để lấy API key:
1. Truy cập [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Đăng nhập bằng tài khoản Google
3. Tạo API key mới
4. Copy API key và dán vào file `.env`

## Sử dụng

1. Đảm bảo đã kích hoạt môi trường ảo
2. Kiểm tra file `.env` đã được cấu hình đúng
3. Chạy ứng dụng:
```bash
uvicorn api:app
```
