import os
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
        
        # Load UI selectors
        with open('config/selectors.yaml', 'r') as file:
            self.selectors = yaml.safe_load(file)
    
    def get_platform_selectors(self, platform_name):
        return self.selectors['platforms'].get(platform_name, {})

config = Config()