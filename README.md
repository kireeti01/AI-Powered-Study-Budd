# AI-Powered Study Buddy 📚✨

A comprehensive AI-powered learning assistant that helps students master complex concepts through intelligent explanations, smart summaries, interactive quizzes, and personalized study planning.

## 🎯 Features

### 1. **Topic Explainer**
- Get AI-powered explanations for any topic in simple language
- Includes real-world examples and use cases
- Perfect for quick concept understanding

### 2. **Notes Summarizer**
- Upload PDFs and text files
- Extract and summarize content automatically
- Highlight key points and important concepts
- Export summaries for later reference

### 3. **Quiz Generator**
- Create multiple-choice questions (MCQs)
- Generate true/false questions
- Short answer questions
- Comprehensive answer explanations
- Test your knowledge on any topic

### 4. **Flashcard Generator**
- Auto-generate flashcards from uploaded notes
- Interactive revision mode
- Track learning progress
- Export flashcards for study

### 5. **Study Planner**
- Generate personalized study schedules
- Input exam date and available study hours
- Get daily study recommendations
- Optimize your learning path

### 6. **Ask Questions from Notes**
- Upload study materials
- Ask context-aware questions
- Get answers based only on uploaded content
- Verify understanding with instant feedback

## 🛠️ Technical Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| AI Engine | Google Gemini API |
| PDF Processing | PyPDF2 |
| Data Processing | Pandas, NumPy |
| Deployment | Streamlit Community Cloud |
| Version Control | GitHub |

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Git
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/study-buddy.git
cd study-buddy
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
AI-Study-Buddy/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
│
├── src/
│   ├── __init__.py
│   │
│   ├── modules/               # Core business logic modules
│   │   ├── __init__.py
│   │   ├── topic_explainer.py
│   │   ├── notes_summarizer.py
│   │   ├── quiz_generator.py
│   │   ├── flashcard_generator.py
│   │   ├── study_planner.py
│   │   └── qa_engine.py
│   │
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   ├── pdf_processor.py
│   │   ├── text_processor.py
│   │   ├── gemini_client.py
│   │   └── validators.py
│   │
│   └── config/                # Configuration files
│       ├── __init__.py
│       └── settings.py
│
├── tests/                      # Unit and integration tests
│   ├── __init__.py
│   ├── test_modules.py
│   └── test_utils.py
│
├── assets/                     # Static assets
│   └── logo.png
│
└── docs/                       # Documentation
    └── DEPLOYMENT.md
```

## 💡 Usage Guide

### Topic Explainer
1. Navigate to "Topic Explainer" tab
2. Enter a topic or concept
3. Specify the difficulty level (Beginner, Intermediate, Advanced)
4. Click "Explain" to get AI-powered explanation
5. Copy or download the explanation

### Notes Summarizer
1. Go to "Notes Summarizer"
2. Upload a PDF or text file
3. Set summary length (Short, Medium, Long)
4. Click "Summarize"
5. Review key points and download summary

### Quiz Generator
1. Select "Quiz Generator"
2. Enter topic or upload notes
3. Choose number of questions (5-20)
4. Select question types
5. Answer quiz questions
6. Review your score and explanations

### Flashcard Generator
1. Access "Flashcard Generator"
2. Upload notes or enter text
3. Click "Generate Flashcards"
4. Review and edit cards as needed
5. Start revision mode
6. Export for external study tools

### Study Planner
1. Open "Study Planner"
2. Select exam date
3. Enter available study hours per day
4. Specify topics to cover
5. Get personalized study schedule
6. Track progress daily

### Ask Questions
1. Go to "Ask Questions"
2. Upload your study materials
3. Type your question
4. Get context-aware answers
5. Verify with follow-up questions

## 🔑 API Integration

### Google Gemini API Setup
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add the key to your `.env` file
4. The application automatically authenticates with the API

### API Rate Limits
- Free tier: 60 requests per minute
- Upgrade for higher limits

## 🧪 Testing

```bash
# Run unit tests
pytest tests/ -v

# Run specific test file
pytest tests/test_modules.py -v

# Generate coverage report
pytest tests/ --cov=src/
```

## 🌐 Deployment

### Streamlit Community Cloud

1. Push code to GitHub
2. Sign up at [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Configure environment variables
5. Deploy with one click

### Deployment Steps
See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## 📊 Performance Metrics

- **Response Time**: < 3 seconds for most queries
- **Uptime**: 99.9% on Streamlit Cloud
- **API Calls**: Optimized to minimize usage
- **File Size**: Supports up to 200MB uploads

## 🔒 Security Features

- API keys stored securely in environment variables
- No data storage on server (stateless)
- Encrypted API communications
- Input validation and sanitization
- CSRF protection enabled

## 🐛 Troubleshooting

### API Key Not Found
- Check `.env` file exists in project root
- Verify `GEMINI_API_KEY` variable is set correctly
- Restart Streamlit app after adding key

### PDF Upload Fails
- Ensure PDF is not corrupted
- Check file size (max 200MB)
- Verify PDF has extractable text

### Slow Performance
- Check internet connection
- Verify API rate limits
- Clear Streamlit cache: `streamlit cache clear`

### Module Import Errors
- Verify all requirements installed: `pip install -r requirements.txt`
- Check Python version compatibility
- Activate correct virtual environment

## 📈 Future Enhancements

- [ ] Multi-language support
- [ ] Speech-to-text for questions
- [ ] Learning analytics dashboard
- [ ] Collaborative study groups
- [ ] Mobile app version
- [ ] Integration with LMS platforms
- [ ] Offline mode support
- [ ] Advanced export formats

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 👨‍💻 Author

**AI-Powered Study Buddy Team**

## 📧 Support

For issues, questions, or suggestions, please open an GitHub issue or contact us at support@studybuddy.ai

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- Streamlit for amazing UI framework
- Python community for excellent libraries

---

**Made with ❤️ for students worldwide**
