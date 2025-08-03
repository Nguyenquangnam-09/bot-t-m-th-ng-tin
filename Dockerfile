# Dùng Python 3.10 chính xác
FROM python:3.10-slim

# Tạo thư mục làm việc
WORKDIR /app

# Cài các thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn
COPY . .

# Chạy bot
CMD ["python", "student_bot.py"]
