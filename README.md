# AI-Powered Study Buddy 📚✨

An AI-powered learning assistant that helps students understand complex concepts, summarize notes, generate quizzes and flashcards, create study plans, and answer questions from uploaded study materials.

## 🚀 Live Demo

🌐 **Live Application:**  
https://ai-powered-study-buddy-z8huccouu8ukxhm99tfu6k.streamlit.app/

## 📂 GitHub Repository

🔗 **Source Code:**  
https://github.com/kireeti01/AI-Powered-Study-Buddy

---

## 🎯 Features

### 📖 Topic Explainer
- AI-powered explanations for any topic
- Beginner, Intermediate, and Advanced levels
- Real-world examples and applications

### 📝 Notes Summarizer
- Upload PDF or text files
- Generate concise summaries
- Extract key concepts and important points

### ❓ Quiz Generator
- Generate MCQs
- True/False questions
- Short-answer questions
- Automatic answer explanations

### 🗂 Flashcard Generator
- Create flashcards from study notes
- Interactive revision support
- Quick concept review

### 📅 Study Planner
- Personalized study schedules
- Exam-focused preparation plans
- Daily study recommendations

### 🤖 Ask Questions From Notes
- Upload learning materials
- Ask context-aware questions
- Receive answers based on uploaded content

---

## 🛠️ Technology Stack

| Component | Technology |
|------------|------------|
| Frontend | Streamlit |
| Backend | Python |
| AI Model | Groq API (Llama 3.1) |
| PDF Processing | PyPDF2 |
| Data Handling | Pandas, NumPy |
| Environment Management | Python Dotenv |
| Version Control | Git & GitHub |
| Deployment | Streamlit Community Cloud |

---

## 📁 Project Structure

```text
AI-Powered-Study-Buddy/
│
├── app.py
├── requirements.txt
├── runtime.txt
├── README.md
├── .env
│
├── src/
│   ├── config/
│   │   └── settings.py
│   │
│   ├── modules/
│   │   ├── topic_explainer.py
│   │   ├── notes_summarizer.py
│   │   ├── quiz_generator.py
│   │   ├── flashcard_generator.py
│   │   ├── study_planner.py
│   │   └── qa_engine.py
│   │
│   └── utils/
│       ├── gemini_client.py
│       ├── pdf_processor.py
│       ├── text_processor.py
│       └── validators.py
│
└── assets/
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/kireeti01/AI-Powered-Study-Buddy.git
cd AI-Powered-Study-Buddy
```

### 2️⃣ Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create Environment File

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5️⃣ Run Application

```bash
streamlit run app.py
```

Application will start at:

```text
http://localhost:8501
```

---

## 📦 Requirements

```txt
streamlit==1.32.0
groq==1.4.0
pandas==2.2.2
numpy==1.26.4
PyPDF2==3.0.1
python-dotenv==1.0.1
requests==2.32.3
Pillow>=11.3.0
```

---

## 🔑 Groq API Setup

1. Create a free account at:
   https://console.groq.com

2. Generate an API key.

3. Add the API key to your `.env` file:

```env
GROQ_API_KEY=your_api_key
```

4. Restart the application.

---

## 🌐 Deployment

### Streamlit Community Cloud

1. Push code to GitHub
2. Login to Streamlit Cloud
3. Connect GitHub repository
4. Select:

```text
Repository: kireeti01/AI-Powered-Study-Buddy
Branch: main
Main File: app.py
```

5. Add Secret:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

6. Deploy Application

---

## 📸 Application Modules

- Topic Explainer
- Notes Summarizer
- Quiz Generator
- Flashcard Generator
- Study Planner
- Ask Questions from Notes

---

## 🚀 Future Enhancements

- Multi-language support
- Voice-based interaction
- Learning analytics dashboard
- Mobile application
- User authentication
- Cloud storage integration

---

## 👨‍💻 Author

### Nadiminti Kireeti

🎓 B.Tech CSE Student

🔗 GitHub: https://github.com/kireeti01

📧 Email: kireeti213@gmail.com

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- Groq API
- Streamlit
- PyPDF2
- Pandas
- NumPy
- Python Community

---

⭐ If you found this project useful, please give it a star on GitHub!
