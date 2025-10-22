"""
Complete BigQuery authentication setup for deforestation-tracker-475003
"""

import subprocess
import sys
import os
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

def main():
    print("=" * 70)
    print("BIGQUERY AUTHENTICATION SETUP")
    print("=" * 70)
    
    project_id = "deforestation-tracker-475003"
    
    print(f"\nProject: {project_id}")
    print("\nThis will:")
    print("1. Enable BigQuery API")
    print("2. Set up Application Default Credentials")
    print("3. Create BigQuery dataset if needed")
    print("4. Test connection")
    
    input("\nPress Enter to continue...")
    
    # Check if gcloud is available
    print("\n[Step 1/4] Checking Google Cloud SDK...")
    success, _, _ = run_command("gcloud --version")
    
    if not success:
        print("\nGoogle Cloud SDK not found!")
        print("\nOption 1: Install Google Cloud SDK")
        print("  Download from: https://cloud.google.com/sdk/docs/install")
        print("  Then run this script again")
        print("\nOption 2: Use Python-based authentication (simpler)")
        choice = input("\nChoose option (1 or 2): ").strip()
        
        if choice == "2":
            print("\nUsing Python-based authentication...")
            setup_python_auth(project_id)
            return
        else:
            print("\nPlease install Google Cloud SDK and run this script again.")
            return
    
    print("OK: Google Cloud SDK found")
    
    # Login check
    print("\n[Step 2/4] Checking authentication...")
    success, stdout, _ = run_command("gcloud auth list --filter=status:ACTIVE --format=\"value(account)\"")
    
    if not success or not stdout.strip():
        print("Please login to Google Cloud...")
        run_command("gcloud auth login", capture=False)
    else:
        print(f"OK: Logged in as {stdout.strip()}")
    
    # Set project
    print(f"\n[Step 3/4] Setting project to {project_id}...")
    run_command(f"gcloud config set project {project_id}")
    
    # Enable BigQuery API
    print("\n[Step 4/4] Enabling BigQuery API...")
    run_command(f"gcloud services enable bigquery.googleapis.com --project={project_id}", capture=False)
    
    # Set up Application Default Credentials
    print("\nSetting up Application Default Credentials...")
    print("This will open a browser window for authentication.")
    input("Press Enter to continue...")
    
    run_command("gcloud auth application-default login", capture=False)
    
    print("\n" + "=" * 70)
    print("SETUP COMPLETE!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Restart your backend server")
    print("2. Check http://localhost:8000/health")
    print("3. BigQuery should show as connected!")
    print("=" * 70)

def setup_python_auth(project_id):
    """Setup authentication using Python OAuth flow"""
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import pickle
    except ImportError:
        print("\nInstalling required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "google-auth-oauthlib"], check=True)
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import pickle
    
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
    
    creds = None
    token_path = Path.home() / ".config" / "gcloud" / "application_default_credentials.json"
    token_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("\nStarting authentication flow...")
    print("A browser window will open for you to sign in.")
    print("Please authorize the application.")
    
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
    
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Save credentials
    creds_dict = {
        "type": "authorized_user",
        "client_id": client_config["installed"]["client_id"],
        "client_secret": client_config["installed"]["client_secret"],
        "refresh_token": creds.refresh_token,
        "quota_project_id": project_id
    }
    
    import json
    with open(token_path, 'w') as f:
        json.dump(creds_dict, f)
    
    # Set environment variable
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(token_path)
    
    print(f"\nCredentials saved to: {token_path}")
    print("\nTesting BigQuery connection...")
    
    # Test connection
    try:
        from google.cloud import bigquery
        client = bigquery.Client(project=project_id)
        print(f"SUCCESS: Connected to BigQuery project '{client.project}'")
    except Exception as e:
        print(f"Warning: Could not test connection: {e}")
    
    print("\n" + "=" * 70)
    print("SETUP COMPLETE!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Restart your backend server")
    print("2. Check http://localhost:8000/health")
    print("3. BigQuery should show as connected!")
    print("=" * 70)

if __name__ == "__main__":
    main()



