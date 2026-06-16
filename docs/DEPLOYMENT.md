# Deployment Guide - AI Study Buddy

## 🚀 Quick Start - Local Development

### Prerequisites
- Python 3.8+
- Git
- A Google Gemini API Key

### Setup Instructions

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/study-buddy.git
   cd study-buddy
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   # Copy example env file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key
   # GEMINI_API_KEY=your_key_here
   ```

5. **Run Application**
   ```bash
   streamlit run app.py
   ```
   Opens at http://localhost:8501

---

## ☁️ Streamlit Community Cloud Deployment

### Step 1: Prepare Repository

1. Create GitHub account and repository
2. Push code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/study-buddy.git
   git push -u origin main
   ```

3. Ensure files are in correct structure:
   ```
   study-buddy/
   ├── app.py
   ├── requirements.txt
   ├── README.md
   ├── .streamlit/
   │   └── config.toml
   └── src/
       ├── modules/
       ├── utils/
       └── config/
   ```

### Step 2: Streamlit Cloud Setup

1. **Create Streamlit Account**
   - Go to https://streamlit.io/cloud
   - Sign up with GitHub account
   - Authorize Streamlit access to repositories

2. **Deploy Application**
   - Click "New app"
   - Select repository: `study-buddy`
   - Select branch: `main`
   - Set main file path: `app.py`
   - Click "Deploy"

### Step 3: Configure Environment Variables

1. **Add API Key**
   - In Streamlit Cloud dashboard
   - Go to app settings (gear icon)
   - Click "Secrets"
   - Add:
     ```
     GEMINI_API_KEY = "your_api_key_here"
     ```
   - Click "Save"

2. **Advanced Settings** (Optional)
   ```
   DEBUG = "False"
   LOG_LEVEL = "INFO"
   MAX_UPLOAD_SIZE = "200"
   CACHE_ENABLED = "True"
   CACHE_TTL = "3600"
   ```

### Step 4: Configure Custom Domain (Optional)

1. Get a domain (e.g., from Namecheap, GoDaddy)
2. In Streamlit settings → Custom domain
3. Follow DNS configuration instructions
4. Wait for DNS propagation (up to 48 hours)

---

## 🔧 Environment Variables Reference

| Variable | Value | Description |
|----------|-------|-------------|
| `GEMINI_API_KEY` | Your API key | Google Gemini API authentication |
| `DEBUG` | False | Disable debug mode in production |
| `LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MAX_UPLOAD_SIZE` | 200 | Max file upload in MB |
| `CACHE_ENABLED` | True | Enable response caching |
| `CACHE_TTL` | 3600 | Cache time-to-live in seconds |

---

## 📊 Monitoring & Maintenance

### View Logs
1. Streamlit Cloud dashboard → App logs
2. Monitor for errors and performance issues

### Performance Monitoring
- Average response time: < 3 seconds
- API quota usage
- File upload sizes

### Update Application
```bash
git add .
git commit -m "Update: description"
git push origin main
```
(Automatically redeploys on main branch push)

---

## 🔒 Security Best Practices

### API Key Security
- ✅ Never commit `.env` file
- ✅ Use Streamlit Secrets for production
- ✅ Rotate API keys regularly
- ✅ Monitor API usage for anomalies

### Data Security
- Application is stateless (no server storage)
- All communications encrypted with HTTPS
- No sensitive data cached locally

### Dependency Security
```bash
# Check for vulnerabilities
pip-audit

# Update packages securely
pip install --upgrade package-name
```

---

## 🐛 Troubleshooting

### App won't deploy
- Check all files are pushed to GitHub
- Verify `app.py` in repository root
- Check `requirements.txt` syntax

### API key errors
- Verify key in Streamlit Secrets
- Check key is valid and not expired
- Confirm key has API access enabled

### Slow performance
- Check file upload sizes
- Monitor API response times
- Clear app cache if needed

### Module import errors
- Ensure all packages in `requirements.txt`
- Verify Python version compatibility (3.8+)
- Check file structure matches repository

---

## 📈 Scaling & Performance

### For Increased Usage
1. **Optimize API calls**
   - Implement caching
   - Batch requests when possible
   - Use prompt optimization

2. **Database integration** (Future)
   - User sessions
   - History tracking
   - Analytics

3. **Load balancing**
   - Consider cloud infrastructure
   - Implement CDN for assets

---

## 🔄 Continuous Integration/Deployment

### GitHub Actions Setup (Optional)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate requirements
        run: |
          pip install -r requirements.txt --dry-run
```

---

## 📞 Support

- Documentation: See README.md
- Issues: GitHub Issues
- API Help: [Google Gemini Docs](https://ai.google.dev)
- Streamlit Help: [Streamlit Docs](https://docs.streamlit.io)

---

**Last Updated**: 2024-01-16
**Version**: 1.0.0
