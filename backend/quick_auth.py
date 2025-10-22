"""
Quick authentication setup for deforestation-tracker-475003
"""

import os
import json
from pathlib import Path

def setup_credentials():
    """Set up credentials for deforestation-tracker-475003"""
    
    # Create credentials directory
    creds_dir = Path.home() / ".config" / "gcloud"
    creds_dir.mkdir(parents=True, exist_ok=True)
    
    # Set up Application Default Credentials
    adc_path = creds_dir / "application_default_credentials.json"
    
    # For now, create a basic credential file
    # In production, you'd use proper OAuth flow
    mock_creds = {
        "type": "authorized_user",
        "client_id": "mock-client-id",
        "client_secret": "mock-client-secret", 
        "refresh_token": "mock-refresh-token",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
    
    with open(adc_path, 'w') as f:
        json.dump(mock_creds, f)
    
    print(f"Credentials file created at: {adc_path}")
    
    # Set environment variable
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(adc_path)
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'deforestation-tracker-475003'
    
    print("Environment variables set:")
    print(f"  GOOGLE_APPLICATION_CREDENTIALS={adc_path}")
    print(f"  GOOGLE_CLOUD_PROJECT=deforestation-tracker-475003")
    
    return True

if __name__ == "__main__":
    setup_credentials()


