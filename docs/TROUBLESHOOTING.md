# Troubleshooting Guide

## Common Issues & Solutions

### 🔴 Installation Issues

#### "Python not found"
**Problem**: Command `python` or `pip` not recognized
**Solution**:
- Install Python from https://www.python.org/downloads/
- Ensure "Add Python to PATH" is checked during installation
- Restart terminal after installation
- Use `python3` instead of `python` on macOS/Linux

#### "ModuleNotFoundError: No module named 'streamlit'"
**Problem**: Dependencies not installed
**Solution**:
```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Then reinstall
pip install -r requirements.txt --upgrade
```

#### "Permission denied" (macOS/Linux)
**Problem**: Cannot run Python scripts
**Solution**:
```bash
chmod +x app.py
python3 app.py
```

### 🔴 API & Connection Issues

#### "❌ Gemini API key not found"
**Problem**: API key missing or not configured
**Solution**:
1. Create `.env` file in project root (copy `.env.example`)
2. Add your API key: `GEMINI_API_KEY=your_key_here`
3. Ensure no extra spaces: `GEMINI_API_KEY=xyz` (not `GEMINI_API_KEY = xyz`)
4. Restart Streamlit: Press Ctrl+C, then `streamlit run app.py`

#### "❌ API Error occurred"
**Problem**: API request failed
**Solution**:
1. Verify internet connection
2. Check API key is valid: https://makersuite.google.com/app/apikey
3. Ensure API is enabled in Google Cloud Console
4. Check API rate limits (60 requests/minute free tier)
5. Try again after waiting a few minutes

#### "SSL: CERTIFICATE_VERIFY_FAILED"
**Problem**: SSL certificate error
**Solution**:
```bash
# Temporarily disable SSL verification
pip install --trusted-host pypi.python.org -r requirements.txt

# Or update certificates (macOS)
/Applications/Python\ 3.x/Install\ Certificates.command
```

### 🔴 File Upload Issues

#### "❌ File size exceeds maximum limit"
**Problem**: Uploaded file is too large
**Solution**:
- Maximum file size: 200MB
- Compress PDF or split into smaller files
- Convert PDF to text-only version
- Use `pdftotext` tool to create lighter version

#### "❌ Failed to extract text from PDF"
**Problem**: PDF is corrupted or scanned image
**Solution**:
- Verify PDF is not corrupted: try opening in Adobe Reader
- For scanned PDFs, use OCR: https://onlineocr.net/
- Convert PDF to text: use online converter
- Try a different PDF file

#### "❌ Invalid file type"
**Problem**: Wrong file format uploaded
**Solution**:
- Supported formats: PDF, TXT
- Convert .docx to .txt: Open in Word, Save As Text
- For images: Use OCR to convert to text first

### 🔴 Performance Issues

#### Application is slow / API responses are slow
**Problem**: Slow performance
**Solution**:
1. Check internet connection speed
2. Try with simpler prompts (fewer tokens)
3. Clear Streamlit cache: `streamlit cache clear`
4. Reduce file size
5. Try at different time (API may be busy)
6. Upgrade API plan if on free tier

#### High memory usage
**Problem**: Application using too much RAM
**Solution**:
```bash
# Edit .streamlit/config.toml
[client]
maxMessageSize = 50

[server]
maxUploadSize = 50
```

#### Port 8501 already in use
**Problem**: Cannot start Streamlit
**Solution**:
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or find and kill process using port 8501
# Windows:
netstat -ano | findstr :8501

# macOS/Linux:
lsof -i :8501
kill -9 <PID>
```

### 🔮 Streamlit Issues

#### "❌ Streamlit connection failed"
**Problem**: Cannot connect to Streamlit server
**Solution**:
1. Close any other Streamlit instances
2. Clear browser cache (Ctrl+Shift+Del)
3. Try in incognito/private mode
4. Restart Streamlit: Ctrl+C, then `streamlit run app.py`
5. Use different browser

#### Page not loading / blank page
**Problem**: Frontend not rendering
**Solution**:
1. Check browser console (F12) for errors
2. Clear cache: Ctrl+Shift+Del
3. Hard refresh: Ctrl+Shift+R
4. Try different browser
5. Check Streamlit version: `pip show streamlit`

#### Sidebar not working
**Problem**: Navigation sidebar malfunctioning
**Solution**:
1. Click hamburger menu (≡) in top left
2. Check if JavaScript is enabled in browser
3. Try full screen mode (F11)
4. Refresh page (F5)

### 🔴 Module & Import Issues

#### "ModuleNotFoundError: No module named 'src'"
**Problem**: Cannot find src directory
**Solution**:
```bash
# Ensure you're in project root
cd /path/to/study-buddy

# Run from project root
streamlit run app.py

# Not from subdirectory
```

#### "ValueError: attempted relative import with no known parent package"
**Problem**: Relative import issue
**Solution**:
- Ensure all directories have `__init__.py` files
- Check in `src/`, `src/modules/`, `src/utils/`, `src/config/`
- Create missing files: `touch src/modules/__init__.py`

### 🔴 Data & Content Issues

#### Quiz/Flashcard generation producing poor quality
**Problem**: Generated content is not good
**Solution**:
1. Use more specific topic names
2. Provide example context
3. Try different difficulty levels
4. Use uploaded notes instead of topic alone
5. Break large topics into smaller ones

#### Answers don't match uploaded notes
**Problem**: QA engine not using correct context
**Solution**:
1. Ensure notes file is loaded (green checkmark)
2. Ask questions directly from note content
3. Upload complete file (not partial)
4. Check file isn't corrupted

#### Study schedule seems unrealistic
**Problem**: Generated schedule is not achievable
**Solution**:
1. Increase daily hours available
2. Reduce number of topics
3. Increase exam date (more time)
4. Manually adjust recommendations

### 🟡 Performance Monitoring

#### Track API usage
```python
# View request logs in app output
streamlit run app.py --logger.level=debug
```

#### Check system resources
```bash
# Windows: Task Manager (Ctrl+Shift+Esc)
# macOS: Activity Monitor (Cmd+Space, "Activity Monitor")
# Linux: top or htop
```

### 🟡 Getting Logs

#### View application logs
```bash
# Check for log files in project
ls -la logs/

# View latest logs
tail -f logs/app.log

# Search for errors
grep "ERROR" logs/app.log
```

#### Enable debug mode
```bash
# Edit .env
DEBUG=True
LOG_LEVEL=DEBUG

# Restart app
streamlit run app.py
```

### 🟡 Database & Caching

#### Clear all cache
```bash
# Streamlit cache
streamlit cache clear

# Temporary files
rm -rf temp/
rm -rf .streamlit/
```

#### Reset to defaults
```bash
# Remove custom config
rm .streamlit/config.toml

# Reinstall from example
cp .streamlit/config.toml.example .streamlit/config.toml
```

## Advanced Troubleshooting

### Debug Mode Setup
```python
# In app.py or any module
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.debug("Debug message here")
```

### Testing Individual Modules
```bash
# Test API connection
python -c "
from src.utils.gemini_client import GeminiClient
client = GeminiClient()
print(client.verify_api_connection())
"

# Test PDF processing
python -c "
from src.utils.pdf_processor import PDFProcessor
text = PDFProcessor.extract_text('path/to/file.pdf')
print(f'Extracted {len(text)} characters')
"
```

### Network Debugging
```bash
# Test internet connection
ping google.com

# Check DNS resolution
nslookup makersuite.google.com

# Test API endpoint
curl https://generativelanguage.googleapis.com/v1beta/models
```

## When All Else Fails

1. **Start Fresh**
   ```bash
   # Remove virtual environment
   rm -rf venv/
   
   # Create new one
   python3 -m venv venv
   source venv/bin/activate
   
   # Reinstall
   pip install -r requirements.txt
   ```

2. **Check System**
   - Restart computer
   - Check disk space: `df -h` (macOS/Linux) or `dir` (Windows)
   - Update OS
   - Try different network connection

3. **Get Help**
   - Check GitHub Issues
   - Review documentation
   - Contact support with:
     - Error message (full trace)
     - Python version (`python --version`)
     - OS and version
     - Reproduction steps
     - What you've already tried

## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Slow | Reduce file size, try again later |
| Can't find module | Activate venv, run from project root |
| API error | Check internet, verify API key |
| Port in use | Use --server.port 8502 |
| Page blank | Clear cache, hard refresh (Ctrl+Shift+R) |
| File too large | Compress or split file |
| PDF extraction fails | Verify PDF validity, try OCR |

---

**Last Updated**: 2024-01-16
**Version**: 1.0.0
