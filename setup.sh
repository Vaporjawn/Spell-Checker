#!/bin/bash

# Python Spell Checker Setup Script
# Author: Victor Williams
# Description: Automated setup and run script for the Python Spell Checker

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python installation
check_python() {
    print_status "Checking Python installation..."

    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
        print_success "Python $PYTHON_VERSION found"

        # Check if Python version is 3.8+
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            print_success "Python version is compatible (3.8+)"
        else
            print_error "Python 3.8+ is required. Current version: $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8 or higher."
        exit 1
    fi
}

# Setup virtual environment
setup_venv() {
    print_status "Setting up virtual environment..."

    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi

    print_status "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."

    # Upgrade pip first
    print_status "Upgrading pip..."
    python -m pip install --upgrade pip

    # Install requirements
    print_status "Installing project dependencies..."
    pip install -r requirements.txt

    print_success "All dependencies installed successfully"
}

# Run tests
run_tests() {
    print_status "Running test suite..."

    python -m pytest tests/ -v

    if [ $? -eq 0 ]; then
        print_success "All tests passed!"
    else
        print_error "Some tests failed. Please check the output above."
        exit 1
    fi
}

# Test spell checker functionality
test_spell_checker() {
    print_status "Testing spell checker functionality..."

    python3 -c "
from lib.checker import Checker
print('Testing spell corrections:')
checker = Checker()
test_words = ['teh', 'helo', 'wrold', 'spellling', 'correct']
for word in test_words:
    corrected = checker.correct(word)
    print(f'  {word} -> {corrected}')
print('Spell checker functionality verified!')
"

    if [ $? -eq 0 ]; then
        print_success "Spell checker functionality test passed!"
    else
        print_error "Spell checker functionality test failed."
        exit 1
    fi
}

# Show usage information
show_usage() {
    echo
    print_success "Setup completed successfully!"
    echo
    echo "To run the spell checker web application:"
    echo "  1. Activate the virtual environment: source venv/bin/activate"
    echo "  2. Start the web server: python main.py"
    echo "  3. Open your browser to: http://localhost:5000"
    echo
    echo "To run tests:"
    echo "  pytest tests/ -v"
    echo
    echo "To use the spell checker programmatically:"
    echo "  python3 -c \"from lib.checker import Checker; c = Checker(); print(c.correct('teh'))\""
    echo
    echo "For development:"
    echo "  - Install dev dependencies: pip install -r requirements-dev.txt"
    echo "  - Format code: black ."
    echo "  - Check code style: flake8 lib/ tests/ main.py"
    echo
}

# Main setup function
main() {
    echo "=================================="
    echo "Python Spell Checker Setup"
    echo "=================================="
    echo

    check_python
    setup_venv
    install_dependencies
    run_tests
    test_spell_checker
    show_usage

    print_success "Setup completed successfully! 🎉"
}

# Run setup if this script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi