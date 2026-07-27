import os
import json
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

# Load environment variables
load_dotenv()

# --- Configuration ---
CONFIG_DIR = 'config'
os.makedirs(CONFIG_DIR, exist_ok=True)

# Google Config
GOOGLE_CREDENTIALS_FILE = os.path.join(CONFIG_DIR, 'credentials.json')
GOOGLE_TOKEN_FILE = os.path.join(CONFIG_DIR, 'google_token.json')
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_google():
    print("\n--- Starting Google Authentication (Gmail) ---")
    if not os.path.exists(GOOGLE_CREDENTIALS_FILE):
        print(f"Error: Missing {GOOGLE_CREDENTIALS_FILE}")
        return

    # Initiate the OAuth flow using the local server strategy
    flow = InstalledAppFlow.from_client_secrets_file(
        GOOGLE_CREDENTIALS_FILE, GOOGLE_SCOPES
    )
    
    # This opens the browser automatically
    creds = flow.run_local_server(port=0)
    
    # Save the credentials (including the refresh token) for Lambda to use later
    with open(GOOGLE_TOKEN_FILE, 'w') as token_file:
        token_file.write(creds.to_json())
    print(f"Success! Google token saved to {GOOGLE_TOKEN_FILE}")


if __name__ == '__main__':
    authenticate_google()
    print("\nGoogle authentication flow complete. Token is staged in the config/ directory.")
