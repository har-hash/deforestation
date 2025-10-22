"""
Simple authentication setup for development
This creates mock credentials so the server works without full GCP setup
"""

import os
import json
from pathlib import Path

def setup_mock_credentials():
    """Create mock credentials for development"""
    
    # Create credentials directory
    creds_dir = Path.home() / ".config" / "gcloud"
    creds_dir.mkdir(parents=True, exist_ok=True)
    
    # Mock application default credentials
    adc_path = creds_dir / "application_default_credentials.json"
    mock_creds = {
        "type": "authorized_user",
        "client_id": "mock-client-id",
        "client_secret": "mock-client-secret",
        "refresh_token": "mock-refresh-token",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
    
    with open(adc_path, 'w') as f:
        json.dump(mock_creds, f)
    
    print(f"Mock credentials created at: {adc_path}")
    return True

if __name__ == "__main__":
    setup_mock_credentials()
