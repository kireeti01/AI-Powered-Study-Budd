# Contributing to AI Study Buddy

We love your input! We want to make contributing to AI Study Buddy as easy and transparent as possible.

## 📋 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Pledge
In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
Examples of behavior that contributes to creating a positive environment include:
- Using welcoming and inclusive language
- Being respectful of differing opinions, viewpoints, and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior include:
- The use of sexualized language or imagery and unwelcome sexual attention or advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Conduct which could reasonably be considered inappropriate in a professional setting

## 🚀 Getting Started

### Fork & Clone
1. Fork the repository on GitHub
2. Clone your fork locally
3. Add upstream remote: `git remote add upstream https://github.com/yourusername/study-buddy.git`

### Set Up Development Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

## 🔍 Types of Contributions

### 🐛 Reporting Bugs
Before creating a bug report, check the issue list to avoid duplicates. Provide:
- Clear, descriptive title
- Detailed description of the unexpected behavior
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)
- Python version and OS
- Full error traceback

**Example Bug Report:**
```markdown
**Title**: Flashcard export fails for large decks

**Description**: When exporting flashcards with more than 100 cards to CSV, the process fails.

**Steps to Reproduce**:
1. Create flashcard deck with 150+ cards
2. Click "Export CSV"
3. Observe error

**Expected**: CSV file downloads successfully
**Actual**: Error message appears

**Environment**:
- Python: 3.10.5
- OS: Windows 11
- Streamlit: 1.28.0
```

### 🎨 Suggesting Enhancements
Enhancements include:
- New features
- Improvements to existing features
- Performance optimizations
- Code structure improvements

**Example Feature Request:**
```markdown
**Title**: Add voice input for questions

**Description**: Students could speak questions instead of typing them.

**Use Case**: Hands-free study while multitasking

**Implementation**: Use browser's Web Speech API

**Alternatives**: Always required to type currently
```

### 📝 Improving Documentation
- Fix typos and grammatical errors
- Clarify confusing sections
- Add examples
- Update outdated information
- Improve API documentation

### 💻 Code Contributions

#### Code Style Guidelines
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to all functions
- Add type hints where possible
- Write comments for complex logic

**Example Well-Written Function:**
```python
def generate_flashcards(
    text: str,
    num_cards: int = 15,
    difficulty: str = "medium"
) -> List[Dict[str, str]]:
    """
    Generate flashcards from provided text.
    
    Args:
        text: Source text for flashcard generation
        num_cards: Number of cards to generate (5-50)
        difficulty: Card difficulty level (easy, medium, hard)
        
    Returns:
        List of flashcard dictionaries with 'front' and 'back' keys
        
    Raises:
        ValueError: If num_cards out of range or text invalid
        
    Example:
        >>> cards = generate_flashcards("Python is a programming language")
        >>> len(cards)
        15
        >>> 'front' in cards[0]
        True
    """
    if not text or not isinstance(text, str):
        raise ValueError("Text must be a non-empty string")
    
    if not (5 <= num_cards <= 50):
        raise ValueError("num_cards must be between 5 and 50")
    
    # Implementation here
    return flashcards
```

#### Testing Requirements
- Write unit tests for new features
- Ensure existing tests still pass
- Maintain > 80% code coverage

```bash
# Run tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=src/
```

#### Commit Messages
Write clear, descriptive commit messages:
```
[FEATURE] Add voice input for questions

- Integrate Web Speech API
- Add voice recording button to UI
- Implement error handling for unsupported browsers

Closes #123
```

**Format:**
- Use `[FEATURE]`, `[BUG]`, `[DOCS]`, `[REFACTOR]`, `[TEST]` prefixes
- Keep first line under 50 characters
- Reference related issues: `Closes #123`
- Provide detailed description of changes

#### Pull Request Process

1. **Update from Main**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Commit Your Changes**
   ```bash
   git commit -am "Clear commit message"
   ```

3. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request**
   - Go to GitHub and create PR
   - Fill in the PR template
   - Link related issues
   - Describe changes clearly

5. **PR Template:**
   ```markdown
   ## Description
   Brief explanation of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation
   - [ ] Performance improvement
   
   ## Related Issues
   Closes #123
   
   ## Testing
   How to test these changes
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] No new warnings generated
   ```

### ✅ Review Process

Your PR will be reviewed by maintainers. They may:
- Request changes
- Ask clarifying questions
- Suggest improvements
- Approve and merge

Be patient and responsive during review. Once approved, PR will be merged.

## 📚 Development Workflow

### Project Structure
```
study-buddy/
├── app.py                  # Main application
├── src/
│   ├── modules/           # Feature modules
│   ├── utils/             # Utilities
│   └── config/            # Configuration
├── tests/                 # Tests
├── docs/                  # Documentation
└── requirements.txt       # Dependencies
```

### Adding New Features

1. **Create Feature Module**
   ```python
   # src/modules/new_feature.py
   
   class NewFeature:
       """Description of the feature"""
       
       def __init__(self):
           """Initialize the feature"""
           pass
       
       def do_something(self, param: str) -> str:
           """Do something with the parameter
           
           Args:
               param: Input parameter
               
           Returns:
               Result of the operation
           """
           return result
   ```

2. **Add Tests**
   ```python
   # tests/test_new_feature.py
   
   class TestNewFeature(unittest.TestCase):
       def test_do_something(self):
           feature = NewFeature()
           result = feature.do_something("input")
           self.assertEqual(result, "expected")
   ```

3. **Update Streamlit App**
   ```python
   # In app.py
   def show_new_feature(self):
       st.header("✨ New Feature")
       # UI implementation
   ```

4. **Update Documentation**
   - README.md with feature description
   - Code comments
   - User guide if needed

### Performance Optimization

- Profile before optimizing: `python -m cProfile app.py`
- Use caching appropriately
- Minimize API calls
- Optimize file I/O

### Security Considerations

- Never commit secrets (API keys, tokens)
- Validate all user input
- Use parameterized queries
- Keep dependencies updated
- Follow security best practices

## 🎓 Learning Resources

- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Google Gemini API Docs](https://ai.google.dev)

## 📞 Getting Help

- Check existing issues
- Read documentation
- Ask in discussions
- Email maintainers

## 🎉 Recognition

Contributors will be recognized in:
- README.md Contributors section
- GitHub contributors page
- Release notes

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

---

Thank you for contributing to AI Study Buddy! Together, we're making learning better for everyone. 📚✨
