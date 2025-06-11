VS Code Setup Guide for SaaS Automation Project
🚀 Quick Start in VS Code
Step 1: Initial Setup

Open Terminal in VS Code (Ctrl+``  or View > Terminal)
Run the setup commands:

bash# Create project directory
mkdir saas-automation
cd saas-automation

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Create directory structure
mkdir -p src/core src/scrapers src/agents src/utils config data/extracted data/logs tests .vscode
Step 2: Install Dependencies
bash# Create requirements.txt
cat > requirements.txt << 'EOF'
playwright==1.40.0
langchain==0.1.0
openai==1.3.0
python-dotenv==1.0.0
pyyaml==6.0.1
pandas==2.1.0
requests==2.31.0
beautifulsoup4==4.12.2
schedule==1.2.0
EOF

# Install Python packages
pip install -r requirements.txt
playwright install chromium

# Install Node.js dependencies for Playwright
npm init -y
npm install playwright
Step 3: VS Code Configuration
Create .vscode/settings.json:
json{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.analysis.extraPaths": ["./src"],
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "files.associations": {
        "*.yaml": "yaml",
        "*.yml": "yaml"
    },
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"]
}
Create .vscode/launch.json:
json{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run Demo",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/main.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Run Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/"],
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
Step 4: Essential Files
Create config/credentials.env:
env# OpenAI API Key (Get from https://platform.openai.com/api-keys)
OPENAI_API_KEY=your_openai_api_key_here

# 2Captcha API Key (Optional - Get from https://2captcha.com)
CAPTCHA_API_KEY=your_2captcha_api_key_here

# Default SaaS Platform Credentials
SAAS_USERNAME=your_username
SAAS_PASSWORD=your_password

# Browser Settings
HEADLESS=False
TIMEOUT=30000
Create config/selectors.yaml:
yamlplatforms:
  trello:
    login:
      email_field: 'input[name="user"]'
      password_field: 'input[name="password"]'
      submit_button: 'input[type="submit"]'
    user_management:
      users_table: '.board-members-list'
      user_row: '.board-member'
      name_selector: '.board-member-name'
      email_selector: '.board-member-email'
      role_selector: '.board-member-role'
      next_button: '.pagination-next'
  
  notion:
    login:
      email_field: 'input[type="email"]'
      password_field: 'input[type="password"]'
      submit_button: 'button[type="submit"]'
    user_management:
      users_table: '.workspace-members'
      user_row: '.member-row'
      name_selector: '.member-name'
      email_selector: '.member-email'
      role_selector: '.member-role'
      next_button: '.load-more'
Step 5: Create Core Files
Create src/utils/config.py:
pythonimport os
import yaml
from dotenv import load_dotenv

load_dotenv('config/credentials.env')

class Config:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.captcha_api_key = os.getenv('CAPTCHA_API_KEY')
        self.saas_username = os.getenv('SAAS_USERNAME')
        self.saas_password = os.getenv('SAAS_PASSWORD')
        self.headless = os.getenv('HEADLESS', 'False').lower() == 'true'
        self.timeout = int(os.getenv('TIMEOUT', 30000))
        
        try:
            with open('config/selectors.yaml', 'r') as file:
                self.selectors = yaml.safe_load(file)
        except FileNotFoundError:
            self.selectors = {'platforms': {}}
    
    def get_platform_selectors(self, platform_name):
        return self.selectors['platforms'].get(platform_name, {})

config = Config()
Create empty __init__.py files:
bashtouch src/__init__.py
touch src/core/__init__.py
touch src/scrapers/__init__.py
touch src/agents/__init__.py
touch src/utils/__init__.py
Step 6: Test Your Setup
Create tests/test_setup.py:
pythonimport unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.config import config

class TestSetup(unittest.TestCase):
    def test_config_loading(self):
        self.assertIsNotNone(config)
        self.assertIsInstance(config.selectors, dict)

if __name__ == '__main__':
    unittest.main()
Step 7: Install VS Code Extensions
Install these extensions in VS Code:

Python (Microsoft)
Playwright Test for VS Code (Microsoft)
YAML (Red Hat)
Python Docstring Generator (Nils Werner)
GitLens (GitKraken)

Step 8: Run Your First Test

Open VS Code in your project folder:
bashcode .

Select Python Interpreter:

Press Ctrl+Shift+P
Type "Python: Select Interpreter"
Choose ./venv/bin/python (or ./venv/Scripts/python.exe on Windows)


Run the demo:

Press F5 or go to Run > Start Debugging
Select "Run Demo" configuration


Run tests:
bashpython tests/test_setup.py


🔧 Development Workflow in VS Code
Running Code

F5: Run with debugger
Ctrl+F5: Run without debugger
Terminal: python src/main.py

Debugging

Set breakpoints by clicking left of line numbers
Use Debug Console for variable inspection
Step through code with F10/F11

Testing

Use Test Explorer in Activity Bar
Run individual tests with right-click
View test results in Test Output

Git Integration

Initialize repo: git init
Stage changes in Source Control panel
Commit with meaningful messages

📋 Daily Development Checklist
Before Starting

 Activate virtual environment
 Pull latest changes (if using git)
 Check environment variables are set

During Development

 Write tests for new features
 Use descriptive commit messages
 Keep requirements.txt updated
 Add logging for debugging

Before Committing

 Run all tests
 Check for sensitive data in commits
 Update documentation
 Verify code formatting

🎯 Next Development Steps

Start with Demo: Run the simple demo to understand the flow
Add Platform Support: Extend config/selectors.yaml for your target SaaS
Implement AI Features: Add OpenAI API key and test intelligent selectors
Add Error Handling: Implement retry logic and better error messages
Create Tests: Write comprehensive tests for your features
Add Scheduling: Implement automated execution with schedule
Deploy: Set up cloud deployment for production use

🚨 Common Issues & Solutions
Python Interpreter Not Found

Solution: Press Ctrl+Shift+P, select "Python: Select Interpreter", choose ./venv/bin/python

Module Import Errors

Solution: Ensure PYTHONPATH includes your project root
Check .vscode/settings.json has correct python.analysis.extraPaths

Playwright Installation Issues

Solution: Run playwright install chromium after pip install

Permission Errors

Solution: Run VS Code as administrator (Windows) or check file permissions

Environment Variables Not Loading

Solution: Verify config/credentials.env exists and has correct format
Check file is not named credentials.env.txt

🔐 Security Best Practices

Never commit config/credentials.env to version control
Use .gitignore to exclude sensitive files
Store API keys in environment variables
Test only on development/staging accounts
Use separate credentials for different environments
