import asyncio
from telegram import Bot

# Thay 'YOUR_TOKEN' bằng token của bot mà bạn đã nhận được từ BotFather
TOKEN = '7151465961:AAGQSBfRL4WIUE5OxGmIgPxZIMSC8bjptbA'
# Thay 'YOUR_CHAT_ID' bằng chat ID của người nhận
CHAT_ID = '6178408766'

bot = Bot(token=TOKEN)

async def send_message_periodically():
    while True:
        await bot.send_message(chat_id=CHAT_ID, text="em hung an cac")  # Sử dụng await ở đây
        await asyncio.sleep(2)  # Đợi 2 giây trước khi gửi lại

async def main():
    await send_message_periodically()

if __name_ == '_main_':
    asyncio.run(main())