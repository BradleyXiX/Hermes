import os
import json
import requests
from dotenv import load_dotenv

# Import the pieces we already built
from gmail_pipeline import fetch_and_categorize_emails
from crew import execute_triage

# Load environment variables
load_dotenv()

def send_telegram_briefing(text):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # We will look for TELEGRAM_CHAT_ID first, but fallback to ALLOWED_CHAT_ID 
    # since that is what you were using previously in bot.py
    chat_id = os.getenv("TELEGRAM_CHAT_ID", os.getenv("ALLOWED_CHAT_ID"))
    
    if not bot_token or not chat_id:
        print("❌ Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing from your .env file.")
        return
        
    # The Telegram Bot API URL
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Telegram message length limit is 4096 characters
    max_length = 4000
    chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    
    for i, chunk in enumerate(chunks):
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "Markdown" 
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.ok:
                print(f"✅ Hermes successfully delivered briefing part {i+1}/{len(chunks)} to Telegram.")
            else:
                print(f"❌ Failed to send Telegram message part {i+1}. HTTP {response.status_code}")
                print(f"Response details: {response.text}")
                
                # Fallback: try sending without Markdown parse_mode if it was a formatting error
                if "parse entities" in response.text.lower():
                    print("⚠️ Markdown parsing failed. Attempting to send as plain text...")
                    payload.pop("parse_mode", None)
                    fallback_response = requests.post(url, json=payload)
                    if fallback_response.ok:
                        print(f"✅ Hermes successfully delivered part {i+1} as plain text.")
                    else:
                        print(f"❌ Fallback also failed: {fallback_response.text}")
                        
        except Exception as e:
            print(f"❌ Request failed on part {i+1}: {e}")

def main():
    print("Fetching emails...")
    
    # 1. Fetch unread emails using our existing pipeline
    email_payload_json = fetch_and_categorize_emails()
    
    if "No new unread emails" in email_payload_json or "Error" in email_payload_json:
        print("No new emails (or error occurred). Hermes goes back to sleep.")
        if "Error" in email_payload_json:
            print(f"Details: {email_payload_json}")
        return
        
    # Parse the JSON payload back into lists to format for the LLM
    try:
        emails = json.loads(email_payload_json)
        usiu_emails = emails.get("university_emails", [])
        personal_emails = emails.get("personal_emails", [])
    except json.JSONDecodeError:
        print("❌ Failed to parse email payload.")
        return

    # Check if both are empty
    if not usiu_emails and not personal_emails:
        print("No new emails. Hermes goes back to sleep.")
        return

    # Combine into a single text block for the LLM
    combined_email_data = f"--- USIU EMAILS ---\n{usiu_emails}\n\n--- PERSONAL EMAILS ---\n{personal_emails}"

    # 3. Hand the data to CrewAI and Gemini to sort into Urgent vs FYI
    print("Handing data to CrewAI for triage...")
    
    # We use our existing execute_triage bridge function instead of kicking it off here
    final_briefing = execute_triage(combined_email_data)

    # 4. Deliver the final payload to your phone
    send_telegram_briefing(final_briefing)

    # 5. (Optional) Mark emails as read via the Gmail API so they aren't processed twice next time
    # mark_emails_as_read(service, message_ids) 

if __name__ == "__main__":
    main()
