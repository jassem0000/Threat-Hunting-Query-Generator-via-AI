import subprocess
import sys
import os

def install_dependencies():
    """Install project dependencies with error handling"""
    print("Installing project dependencies...")
    
    # Upgrade pip first
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to upgrade pip: {e}")
    
    # Install requirements
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        print("Trying alternative installation approach...")
        
        # Try installing packages individually
        packages = [
            "Django==4.2.7",
            "djangorestframework==3.14.0",
            "python-multipart==0.0.7",
            "streamlit==1.28.1",
            "requests==2.32.3",
            "ollama==0.5.3",
            "elasticsearch==8.10.1",
            "splunk-sdk==1.7.4",
            "stix2==3.0.1",
            "taxii2-client==2.3.0",
            "pandas==2.1.3",
            "numpy==1.26.4",
            "python-dotenv==1.0.0",
            "pyyaml==6.0.1",
            "pytest==7.4.3",
            "httpx==0.27.0",
            "plotly==5.18.0"
        ]
        
        failed_packages = []
        for package in packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"Successfully installed {package}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {package}: {e}")
                failed_packages.append(package)
        
        if failed_packages:
            print(f"Failed to install the following packages: {failed_packages}")
            return False
        else:
            print("All packages installed successfully!")
            return True

if __name__ == "__main__":
    success = install_dependencies()
    if success:
        print("\nInstallation completed successfully!")
        print("You can now run the project:")
        print("1. cd backend && python manage.py migrate")
        print("2. cd backend && python manage.py runserver")
        print("3. In another terminal: streamlit run frontend/app.py")
    else:
        print("\nInstallation encountered issues. Please check the error messages above.")