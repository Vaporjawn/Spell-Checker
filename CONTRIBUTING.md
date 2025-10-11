# Contributing to Python Spell Checker

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to the Python Spell Checker. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots if applicable**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain the behavior you expected to see instead**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Include screenshots and animated GIFs in your pull request whenever possible
- Follow the Python coding standards
- Include thoughtfully-worded, well-structured tests
- Document new code based on the Documentation Standards
- End all files with a newline

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Vaporjawn/Spell-Checker.git
   cd Spell-Checker
   ```

2. **Run the automated setup:**
   ```bash
   ./setup.sh
   ```

### Manual Setup

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development tools
   ```

3. **Run tests to verify setup:**
   ```bash
   pytest tests/ -v
   ```

### Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes and test them:**
   ```bash
   # Run tests
   pytest tests/ -v

   # Format code
   black .

   # Check code style
   flake8 lib/ tests/ main.py
   ```

3. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add your descriptive commit message"
   ```

4. **Push to your fork and submit a pull request**

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [flake8](https://flake8.pycqa.org/) for linting
- Line length: 88 characters (Black default)

### Code Formatting

Run these commands before committing:

```bash
# Format code with Black
black .

# Check code style with flake8
flake8 lib/ tests/ main.py

# Sort imports with isort (if installed)
isort .
```

### Naming Conventions

- **Functions and variables:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_CASE`
- **Private methods:** `_leading_underscore`
- **Files and modules:** `lowercase_with_underscores`

### Documentation

- Use docstrings for all public functions, classes, and methods
- Follow [Google Style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for docstrings
- Include type hints for function parameters and return values
- Add inline comments for complex logic

Example:
```python
def correct(self, word: str) -> str:
    """Return the most likely correct spelling of word.

    Args:
        word: The word to be spell-checked.

    Returns:
        The corrected word if a better spelling is found,
        otherwise returns the original word.

    Example:
        >>> checker = Checker()
        >>> checker.correct("teh")
        "the"
    """
```

## Testing Guidelines

### Test Structure

- Tests are located in the `tests/` directory
- Use pytest as the testing framework
- Follow the naming convention: `test_*.py`
- Test functions should be named `test_*`

### Writing Tests

- Write tests for all new functionality
- Include edge cases and error conditions
- Use descriptive test names that explain what is being tested
- Keep tests simple and focused on one aspect
- Use fixtures for common test setup

Example:
```python
def test_correct_known_word():
    """Test that known words are returned unchanged."""
    checker = Checker()
    assert checker.correct("hello") == "hello"

def test_correct_unknown_word():
    """Test that unknown words are corrected."""
    checker = Checker()
    corrected = checker.correct("teh")
    assert corrected == "the"
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_checker.py -v

# Run with coverage
pytest --cov=lib tests/

# Run tests in watch mode (if pytest-watch is installed)
ptw
```

## Pull Request Process

1. **Ensure any install or build dependencies are removed** before the end of the layer when doing a build.

2. **Update the README.md** with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.

3. **Increase the version numbers** in any examples files and the README.md to the new version that this Pull Request would represent.

4. **Ensure all tests pass** and code coverage is maintained or improved.

5. **Your PR will be merged** once you have the sign-off of at least one maintainer.

### PR Template

When creating a pull request, please include:

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests that you ran to verify your changes.

## Checklist:
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

## Issue Reporting

### Bug Reports

Use the following template for bug reports:

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
- OS: [e.g. macOS, Windows, Linux]
- Python Version: [e.g. 3.11.6]
- Browser [if applicable]: [e.g. Chrome, Safari]

**Additional context**
Add any other context about the problem here.
```

### Feature Requests

Use the following template for feature requests:

```markdown
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

## Project Structure

Understanding the project structure will help you navigate the codebase:

```
Spell-Checker/
├── lib/                    # Core spell checker modules
│   ├── checker.py         # Main spell checker class
│   └── trainer.py         # Language model trainer
├── data/                  # Training corpus files
│   ├── corpus.txt        # Full training corpus
│   └── corpus_test.txt   # Test corpus (smaller)
├── tests/                # Test suite
│   ├── test_checker.py   # Checker tests
│   ├── test_trainer.py   # Trainer tests
│   └── test_main.py      # Web app tests
├── templates/            # Flask templates
├── static/              # Static web assets
├── main.py             # Flask web application
├── requirements.txt    # Production dependencies
├── requirements-dev.txt # Development dependencies
├── setup.sh           # Automated setup script
└── README.md          # Project documentation
```

## Getting Help

- **Documentation:** Check the [README.md](README.md) first
- **Issues:** Browse existing [GitHub Issues](https://github.com/Vaporjawn/Spell-Checker/issues)
- **Discussions:** Start a [GitHub Discussion](https://github.com/Vaporjawn/Spell-Checker/discussions)
- **Email:** Contact victor.williams.dev@gmail.com for questions

## Recognition

Contributors will be recognized in:
- The project README
- Release notes for significant contributions
- Special recognition for first-time contributors

Thank you for contributing! 🚀