"""
Automated GCP Setup Script
This will help you set up all required permissions and APIs
"""

import subprocess
import sys
import webbrowser
import time

def run_command(cmd):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("=" * 60)
    print("AUTOMATED GCP SETUP FOR DEFORESTATION TRACKER")
    print("=" * 60)
    print()
    
    project_id = "deforestation-tracker"
    
    # Step 1: Check if gcloud is installed
    print("[1/6] Checking Google Cloud SDK...")
    success, _, _ = run_command("gcloud --version")
    
    if not success:
        print("   ERROR: Google Cloud SDK not found!")
        print("   Please install from: https://cloud.google.com/sdk/docs/install")
        webbrowser.open("https://cloud.google.com/sdk/docs/install")
        print("   After installation, run this script again.")
        return
    
    print("   OK: Google Cloud SDK found")
    
    # Step 2: Login
    print("\n[2/6] Checking authentication...")
    success, stdout, _ = run_command("gcloud auth list --filter=status:ACTIVE --format=\"value(account)\"")
    
    if not success or not stdout.strip():
        print("   Please login to Google Cloud...")
        subprocess.run("gcloud auth login", shell=True)
    else:
        print(f"   OK: Logged in as {stdout.strip()}")
    
    # Step 3: Set project
    print(f"\n[3/6] Setting project to {project_id}...")
    success, _, stderr = run_command(f"gcloud config set project {project_id}")
    
    if not success:
        print(f"   WARNING: Project {project_id} may not exist")
        print(f"   Creating project {project_id}...")
        subprocess.run(f"gcloud projects create {project_id} --name=\"Deforestation Tracker\"", shell=True)
        time.sleep(2)
        subprocess.run(f"gcloud config set project {project_id}", shell=True)
    
    print(f"   OK: Project set to {project_id}")
    
    # Step 4: Enable APIs
    print("\n[4/6] Enabling required APIs...")
    apis = [
        "earthengine.googleapis.com",
        "bigquery.googleapis.com",
        "storage-api.googleapis.com",
        "serviceusage.googleapis.com"
    ]
    
    for api in apis:
        print(f"   Enabling {api}...")
        subprocess.run(f"gcloud services enable {api} --project={project_id}", shell=True, capture_output=True)
    
    print("   OK: All APIs enabled")
    
    # Step 5: Set up Application Default Credentials
    print("\n[5/6] Setting up Application Default Credentials...")
    print("   This will open a browser window...")
    subprocess.run("gcloud auth application-default login", shell=True)
    print("   OK: ADC configured")
    
    # Step 6: Register Earth Engine
    print("\n[6/6] Registering Earth Engine project...")
    print("   Opening Earth Engine signup page...")
    webbrowser.open("https://code.earthengine.google.com/register")
    print("   Please complete the signup process in your browser")
    print("   Select your project: deforestation-tracker")
    
    print("\n" + "=" * 60)
    print("SETUP INSTRUCTIONS")
    print("=" * 60)
    print("1. Complete the Earth Engine signup in your browser")
    print("2. Wait 2-3 minutes for permissions to propagate")
    print("3. Restart your backend server: cd backend && python -B main.py")
    print("4. Check http://localhost:8000/health - should show 'healthy'")
    print("=" * 60)

if __name__ == "__main__":
    main()



