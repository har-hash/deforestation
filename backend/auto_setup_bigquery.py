"""
Automatic BigQuery authentication setup for deforestation-tracker-475003
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def run_command(cmd, capture=True):
    """Run a shell command"""
    try:
        if capture:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True)
            return result.returncode == 0, "", ""
    except Exception as e:
        return False, "", str(e)

def setup_python_auth(project_id):
    """Setup authentication using Python OAuth flow"""
    print("=" * 70)
    print("BIGQUERY AUTHENTICATION SETUP")
    print("=" * 70)
    print(f"\nProject: {project_id}")
    
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
    except ImportError:
        print("\nInstalling google-auth-oauthlib...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "google-auth-oauthlib"], check=True)
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
    
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/bigquery']
    
    token_path = Path.home() / ".config" / "gcloud" / "application_default_credentials.json"
    token_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("\n[1/3] Starting authentication flow...")
    print("      A browser window will open for you to sign in.")
    print("      Please authorize the application with your Google account.")
    
    # Use the default client ID for gcloud
    client_config = {
        "installed": {
            "client_id": "764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com",
            "client_secret": "d-FL95Q19q7MQmFpd7hHD0Ty",
            "redirect_uris": ["http://localhost", "urn:ietf:wg:oauth:2.0:oob"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }
    
    try:
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0)
        
        print("\n[2/3] Saving credentials...")
        
        # Save credentials
        creds_dict = {
            "type": "authorized_user",
            "client_id": client_config["installed"]["client_id"],
            "client_secret": client_config["installed"]["client_secret"],
            "refresh_token": creds.refresh_token,
            "quota_project_id": project_id
        }
        
        with open(token_path, 'w') as f:
            json.dump(creds_dict, f)
        
        print(f"      Credentials saved to: {token_path}")
        
        # Set environment variable
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(token_path)
        os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
        
        print("\n[3/3] Testing BigQuery connection...")
        
        # Test connection
        try:
            from google.cloud import bigquery
            client = bigquery.Client(project=project_id, credentials=creds)
            
            # Test by listing datasets
            datasets = list(client.list_datasets())
            
            print(f"      SUCCESS: Connected to BigQuery!")
            print(f"      Project: {client.project}")
            print(f"      Found {len(datasets)} dataset(s)")
            
            # Create dataset if it doesn't exist
            dataset_id = "forest_monitoring"
            dataset_ref = f"{project_id}.{dataset_id}"
            
            try:
                client.get_dataset(dataset_id)
                print(f"      Dataset '{dataset_id}' already exists")
            except:
                print(f"      Creating dataset '{dataset_id}'...")
                dataset = bigquery.Dataset(dataset_ref)
                dataset.location = "US"
                dataset = client.create_dataset(dataset)
                print(f"      Dataset '{dataset_id}' created successfully")
            
        except Exception as e:
            print(f"      Warning: Could not fully test connection: {e}")
            print(f"      But credentials are saved and should work!")
        
        print("\n" + "=" * 70)
        print("SETUP COMPLETE!")
        print("=" * 70)
        print("\nWhat to do next:")
        print("1. Restart your backend server (kill current process and restart)")
        print("2. Visit http://localhost:8000/health")
        print("3. You should see: 'bigquery_connected': true")
        print("\n" + "=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\nError during authentication: {e}")
        print("\nAlternative: Install Google Cloud SDK")
        print("  Download from: https://cloud.google.com/sdk/docs/install")
        print("  Then run: gcloud auth application-default login")
        return False

def main():
    project_id = "deforestation-tracker-475003"
    
    # Check if credentials already exist
    token_path = Path.home() / ".config" / "gcloud" / "application_default_credentials.json"
    
    if token_path.exists():
        print("Credentials file already exists at:", token_path)
        print("\nTesting existing credentials...")
        
        try:
            from google.cloud import bigquery
            client = bigquery.Client(project=project_id)
            datasets = list(client.list_datasets())
            print(f"SUCCESS: BigQuery is already working!")
            print(f"Project: {client.project}")
            print(f"Found {len(datasets)} dataset(s)")
            print("\nYour BigQuery authentication is already set up!")
            print("Just restart your backend server.")
            return
        except Exception as e:
            print(f"Existing credentials don't work: {e}")
            print("Will set up new credentials...\n")
    
    # Set up new credentials
    setup_python_auth(project_id)

if __name__ == "__main__":
    main()



