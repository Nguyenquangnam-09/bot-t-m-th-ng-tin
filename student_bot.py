import telegram
print("📦 Telegram Bot Library Version:", telegram.__version__)
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import pandas as pd
from datetime import datetime
import os

# Lấy token từ biến môi trường
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Đọc file Excel
try:
    df = pd.read_excel("data_hocsinh.xlsx")
except FileNotFoundError:
    df = None

FIELDS = [
    ('Mã lớp', 'Mã lớp'),
    ('Mã định danh Bộ GD&ĐT', 'Mã định danh Bộ GD&ĐT'),
    ('Ngày sinh', 'Ngày sinh'),
    ('Chỗ ở hiện nay', 'Chỗ ở hiện nay'),
    ('Số điện thoại liên hệ', 'Số điện thoại liên hệ'),
    ('Bệnh về mắt', 'Bệnh về mắt'),
    ('Số định danh cá nhân', 'Số định danh cá nhân'),
    ('Họ tên cha', 'Họ tên cha'),
    ('Họ tên mẹ', 'Họ tên mẹ')
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Gửi tên học sinh để tra cứu thông tin.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if df is None:
        await update.message.reply_text("Không thể tải dữ liệu học sinh.")
        return

    name = update.message.text.strip()
    results = df[df['Họ tên'].str.contains(name, case=False, na=False)]

    if results.empty:
        await update.message.reply_text(f"❌ Không tìm thấy học sinh nào với tên: {name}")
        return

    for _, row in results.iterrows():
        message = f"👤 *{row['Họ tên']}*\n"
        for key, label in FIELDS:
            value = row[key]
            if key == 'Ngày sinh' and pd.notna(value):
                try:
                    value = pd.to_datetime(value).strftime('%d/%m/%Y')
                except:
                    pass
            value = str(value) if pd.notna(value) else 'N/A'
            message += f"- *{label}*: `{value}`\n"
        await update.message.reply_text(message, parse_mode="Markdown")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

print("🤖 Bot đang chạy...")
app.run_polling()

