import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Securely load configuration
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_CHAT_ID = os.getenv("ALLOWED_CHAT_ID")

# Initialize interface
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# The Security Gatekeeper
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    # Fail-closed authorization check
    if str(message.from_user.id) != ALLOWED_CHAT_ID:
        print(f"Unauthorized access attempt from ID: {message.from_user.id}")
        return 
    
    await message.answer("Authentication successful. Hermes interface online. Awaiting commands.")

async def main() -> None:
    # Begin local polling (We will switch to Webhooks for AWS later)
    print("Hermes local polling started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())