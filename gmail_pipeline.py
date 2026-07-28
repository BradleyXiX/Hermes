import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- Configuration ---
TOKEN_FILE = 'config/google_token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_emails(service, query):
    """Helper function to fetch and parse emails based on a Gmail search query."""
    results = service.users().messages().list(userId="me", q=query).execute()
    messages = results.get("messages", [])
    
    email_data_list = []
    for msg_ref in messages:
        msg = service.users().messages().get(userId="me", id=msg_ref["id"]).execute()
        headers = msg["payload"].get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")
        snippet = msg.get("snippet", "")
        
        email_data_list.append({
            "sender": sender,
            "subject": subject,
            "snippet": snippet
        })
    return email_data_list

def fetch_and_categorize_emails():
    print("Initializing single-pipeline Gmail fetcher...")
    
    if not os.path.exists(TOKEN_FILE):
        return "Error: google_token.json not found. Run auth_setup.py first."
        
    try:
        # 1. Authenticate using the staged token
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        service = build("gmail", "v1", credentials=creds)

        # Added "newer_than:2m" to restrict the timeframe
        print("Fetching emails from the last 2 months...")
        
        # 2. Fetching emails from the university domain or specific academic portals
        usiu_query = "from:(*@usiu.ac.ke OR *blackboard.com OR *instructure.com) is:unread newer_than:2m"
        usiu_messages = get_emails(service, query=usiu_query)

        # 3. Fetching personal emails while excluding the university domains to prevent duplication
        personal_query = "is:unread -from:(*@usiu.ac.ke OR *blackboard.com OR *instructure.com) newer_than:2m"
        personal_messages = get_emails(service, query=personal_query)

        triage_payload = {
            "university_emails": usiu_messages,
            "personal_emails": personal_messages
        }

        if not usiu_messages and not personal_messages:
            return json.dumps({"status": "No new unread emails."})

        return json.dumps(triage_payload, indent=2)

    except HttpError as error:
        return f"An error occurred with the Gmail API: {error}"

if __name__ == "__main__":
    # Test the extraction pipeline locally
    print(fetch_and_categorize_emails())
