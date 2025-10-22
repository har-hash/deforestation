"""
Google Cloud Authentication Setup Script
This script will help you authenticate with Google Cloud services
"""

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Define the scopes needed for our application
SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/bigquery'
]

def authenticate():
    """Authenticate with Google Cloud using OAuth2"""
    print("Starting Google Cloud authentication...")
    print("This will open a browser window for you to sign in.")
    
    # Create credentials directory if it doesn't exist
    creds_dir = os.path.expanduser("~/.config/gcloud")
    os.makedirs(creds_dir, exist_ok=True)
    
    # Use the default client ID for Google Cloud SDK
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": "764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com",
                "client_secret": "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4y",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"]
            }
        },
        SCOPES
    )
    
    # Run the OAuth flow
    creds = flow.run_local_server(port=0)
    
    # Save credentials
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    
    # Save to default location
    import json
    creds_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes
    }
    
    # Save to application default credentials location
    adc_path = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
    with open(adc_path, 'w') as f:
        json.dump(creds_data, f)
    
    print(f"✅ Authentication successful!")
    print(f"Credentials saved to: {adc_path}")
    print("You can now use Google Cloud services like BigQuery.")
    
    return True

if __name__ == "__main__":
    try:
        authenticate()
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("\nAlternative: Install Google Cloud SDK and run:")
        print("gcloud auth application-default login")
