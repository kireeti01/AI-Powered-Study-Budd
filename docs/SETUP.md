# Setup & Installation Guide

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 2GB (4GB+ recommended)
- **Internet Connection**: Required for API calls
- **Storage**: 500MB free space for dependencies and temporary files

## Installation Methods

### Method 1: Automated Setup (Recommended)

1. **Clone or Download Repository**
   ```bash
   git clone https://github.com/yourusername/study-buddy.git
   cd study-buddy
   ```

2. **Run Setup Script**
   ```bash
   # Windows
   python setup.py
   
   # macOS/Linux
   python3 setup.py
   ```

3. **Follow Interactive Prompts**
   - Confirm Python version
   - Create virtual environment
   - Install dependencies
   - Configure API key

### Method 2: Manual Setup

#### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/study-buddy.git
cd study-buddy
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# Use your preferred editor:
# - Windows: notepad .env
# - Linux/Mac: nano .env
```

Add to `.env`:
```
GEMINI_API_KEY=your_api_key_here
DEBUG=False
LOG_LEVEL=INFO
```

#### Step 5: Run Application
```bash
streamlit run app.py
```

## Obtaining Google Gemini API Key

1. **Visit Google AI Studio**
   - Go to https://makersuite.google.com/app/apikey

2. **Sign In**
   - Use your Google account
   - Create new account if needed

3. **Generate API Key**
   - Click "Create API Key"
   - Select "Create API key in new project"
   - Copy the generated key

4. **Add to .env File**
   ```
   GEMINI_API_KEY=paste_your_key_here
   ```

5. **Verify Connection**
   - The app will test the connection on startup
   - You'll see confirmation message if successful

## Troubleshooting Installation

### Python Not Found
```bash
# Check Python installation
python --version

# If not found, download from https://www.python.org/downloads/
```

### Permission Denied (macOS/Linux)
```bash
# Make script executable
chmod +x app.py

# Run with Python explicitly
python3 app.py
```

### Module Not Found Errors
```bash
# Verify virtual environment is activated
# Then reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### API Key Issues
- Verify key is in `.env` file
- Check for extra spaces in key
- Ensure API is enabled: https://cloud.google.com/console
- Regenerate key if needed

### Port Already in Use
```bash
# Streamlit default is 8501
# Change port in command:
streamlit run app.py --server.port 8502
```

## Verifying Installation

```bash
# Run diagnostic checks
python -c "
import sys
print(f'Python: {sys.version}')
import streamlit as st
print('✅ Streamlit installed')
import google.generativeai as genai
print('✅ Google AI installed')
from src.config.settings import Config
print('✅ Config loaded')
print('✅ Installation verified!')
"
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_modules.py::TestTextProcessor -v

# Generate coverage report
pytest tests/ --cov=src/
```

## Virtual Environment Management

### Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Delete Virtual Environment
```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

## Updating Dependencies

```bash
# Update all packages
pip install -r requirements.txt --upgrade

# Update specific package
pip install --upgrade streamlit

# Check for outdated packages
pip list --outdated
```

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
# Windows: rmdir /s venv
# macOS/Linux: rm -rf venv

# Delete project folder
# Windows: rmdir /s /q study-buddy
# macOS/Linux: rm -rf study-buddy
```

## Performance Optimization

### For Faster Startup
```bash
# Clear Streamlit cache
streamlit cache clear
```

### For Better Memory Usage
Edit `.streamlit/config.toml`:
```toml
[client]
maxMessageSize = 50

[server]
maxUploadSize = 50
```

### For Faster API Responses
Enable caching in `.env`:
```
CACHE_ENABLED=True
CACHE_TTL=3600
```

## Network Configuration

### Behind Proxy
```bash
pip install -r requirements.txt --proxy https://proxyserver:port
```

### SSL Certificate Issues
```bash
# Disable SSL verification (not recommended for production)
pip install --trusted-host pypi.org -r requirements.txt
```

## Getting Help

### Check Logs
```bash
# View application logs
tail -f logs/app.log

# Clear logs
rm logs/app.log
```

### Common Issues
- See TROUBLESHOOTING.md
- Check GitHub Issues
- Contact support

### Reporting Bugs
- Include Python version
- Provide error message
- List installed packages: `pip freeze`
- Describe reproduction steps

## Next Steps

1. ✅ Installation complete
2. Run: `streamlit run app.py`
3. Open browser to `http://localhost:8501`
4. Get Gemini API key (if not done)
5. Start learning!

---

**For detailed deployment instructions, see DEPLOYMENT.md**
