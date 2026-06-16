"""
AI Study Buddy Setup Script
Automated setup and configuration
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50 + "\n")


def print_success(text):
    """Print success message"""
    print(f"✅ {text}")


def print_error(text):
    """Print error message"""
    print(f"❌ {text}")


def print_info(text):
    """Print info message"""
    print(f"ℹ️ {text}")


def check_python_version():
    """Check if Python version is supported"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error("Python 3.8 or higher required")
        return False
    
    print_success("Python version compatible")
    return True


def create_venv():
    """Create virtual environment"""
    print_header("Creating Virtual Environment")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        response = input("Virtual environment already exists. Recreate? (y/n): ")
        if response.lower() != 'y':
            print_info("Using existing virtual environment")
            return True
        else:
            import shutil
            shutil.rmtree(venv_path)
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_success("Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {str(e)}")
        return False


def get_pip_command():
    """Get pip command for current platform"""
    if platform.system() == "Windows":
        return Path("venv/Scripts/pip.exe")
    else:
        return Path("venv/bin/pip")


def install_requirements():
    """Install required packages"""
    print_header("Installing Dependencies")
    
    pip_cmd = get_pip_command()
    
    if not pip_cmd.exists():
        print_error("Virtual environment pip not found")
        return False
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.run([str(pip_cmd), "install", "-r", "requirements.txt"], check=True)
        print_success("Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {str(e)}")
        return False


def configure_env_file():
    """Configure .env file"""
    print_header("Configuring Environment Variables")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print_info(".env file already exists")
        response = input("Update API key? (y/n): ")
        if response.lower() != 'y':
            return True
    else:
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print_success(".env file created from template")
        else:
            print_warning("No .env.example found, creating new .env")
            with open(env_file, 'w') as f:
                f.write("GEMINI_API_KEY=\nDEBUG=False\nLOG_LEVEL=INFO\n")
    
    print("\nEnter your Gemini API key:")
    print("Get it from: https://makersuite.google.com/app/apikey")
    api_key = input("API Key (or press Enter to skip): ").strip()
    
    if api_key:
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Update or add API key
        if "GEMINI_API_KEY=" in content:
            content = content.replace(
                f"GEMINI_API_KEY=",
                f"GEMINI_API_KEY={api_key}"
            )
        else:
            content = f"GEMINI_API_KEY={api_key}\n{content}"
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print_success("API key configured")
    else:
        print_info("Skipping API key configuration")
        print("You can add it later to .env file")
    
    return True


def verify_installation():
    """Verify that installation was successful"""
    print_header("Verifying Installation")
    
    try:
        import streamlit
        print_success(f"Streamlit {streamlit.__version__} installed")
    except ImportError:
        print_error("Streamlit not found")
        return False
    
    try:
        import google.generativeai
        print_success("Google AI library installed")
    except ImportError:
        print_error("Google AI library not found")
        return False
    
    try:
        import PyPDF2
        print_success("PyPDF2 installed")
    except ImportError:
        print_error("PyPDF2 not found")
        return False
    
    try:
        from src.config.settings import Config
        print_success("Project configuration loaded")
    except ImportError as e:
        print_error(f"Configuration load failed: {str(e)}")
        return False
    
    print_success("Installation verified!")
    return True


def show_next_steps():
    """Show next steps after setup"""
    print_header("Setup Complete!")
    
    print("""
Next steps:

1. 📚 Start the application:
   streamlit run app.py

2. 🌐 Open your browser:
   http://localhost:8501

3. 🔑 If API key not configured:
   - Edit .env file
   - Add your Gemini API key
   - Restart Streamlit

4. 📖 For help:
   - Read: README.md
   - Setup guide: docs/SETUP.md
   - Troubleshooting: docs/TROUBLESHOOTING.md
   - Deployment: docs/DEPLOYMENT.md

5. 🧪 To run tests:
   pytest tests/ -v

6. 🐙 To use Git:
   git add .
   git commit -m "Initial commit"
   git push

Happy Learning! 📚✨
    """)


def main():
    """Main setup process"""
    print_header("AI Study Buddy - Setup Assistant")
    
    print("""
This script will help you set up AI Study Buddy.
It will:
✓ Check Python version
✓ Create virtual environment
✓ Install dependencies
✓ Configure environment variables
✓ Verify installation
    """)
    
    # Check Python
    if not check_python_version():
        print_error("Setup failed: Python version incompatible")
        return 1
    
    # Create venv
    if not create_venv():
        print_error("Setup failed: Could not create virtual environment")
        return 1
    
    # Install requirements
    if not install_requirements():
        print_error("Setup failed: Could not install dependencies")
        return 1
    
    # Configure .env
    if not configure_env_file():
        print_error("Setup failed: Could not configure environment")
        return 1
    
    # Verify
    if not verify_installation():
        print_error("Setup failed: Verification failed")
        return 1
    
    # Show next steps
    show_next_steps()
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)
