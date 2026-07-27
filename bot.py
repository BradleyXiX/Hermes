import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from crew import execute_triage
from gmail_pipeline import fetch_and_categorize_emails

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

# Create the Agent Trigger Command
@dp.message(Command("triage"))
async def handle_triage(message: types.Message) -> None:
    # Security Check
    if str(message.from_user.id) != ALLOWED_CHAT_ID:
        await message.answer("Unauthorized access blocked.")
        return

    await message.answer("🤖 Hermes activated. Fetching unread emails from Gmail...")

    try:
        # Fetch emails from Gmail
        email_payload_json = await asyncio.to_thread(fetch_and_categorize_emails)
        
        # Check if there are no emails or if an error occurred
        if "No new unread emails" in email_payload_json or "Error" in email_payload_json:
            await message.answer(email_payload_json)
            return
            
        await message.answer("📥 Emails retrieved. Inbox Router engaged. Analyzing payload...")

        # Pass the fetched emails to CrewAI
        analysis_result = await asyncio.to_thread(execute_triage, email_payload_json)
        
        # Return the AI's final answer to the chat
        await message.answer(f"✅ **Analysis Complete**\n\n{analysis_result}", parse_mode="Markdown")
        
    except Exception as e:
        await message.answer(f"⚠️ Agent Error: {str(e)}")

async def main() -> None:
    # Begin local polling (We will switch to Webhooks for AWS later)
    print("Hermes local polling started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())