from src.utils.config import config
import time
import logging

class AuthHandler:
    def __init__(self, page, platform_name):
        self.page = page
        self.platform_name = platform_name
        self.selectors = config.get_platform_selectors(platform_name)
        
    def login(self, username=None, password=None):
        """Handle login process"""
        username = username or config.saas_username
        password = password or config.saas_password
        
        login_selectors = self.selectors.get('login', {})
        
        try:
            # Fill email
            email_field = login_selectors.get('email_field')
            if email_field:
                self.page.fill(email_field, username)
                
            # Fill password
            password_field = login_selectors.get('password_field')
            if password_field:
                self.page.fill(password_field, password)
                
            # Click submit
            submit_button = login_selectors.get('submit_button')
            if submit_button:
                self.page.click(submit_button)
                
            # Wait for navigation
            time.sleep(3)
            
            # Check if MFA is required
            if self._is_mfa_required():
                self._handle_mfa()
                
            logging.info("Login successful")
            return True
            
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False
    
    def _is_mfa_required(self):
        """Check if MFA verification is required"""
        mfa_indicators = [
            'text=Enter verification code',
            'text=Two-factor authentication',
            'input[name="code"]',
            '.mfa-form'
        ]
        
        for indicator in mfa_indicators:
            try:
                if self.page.is_visible(indicator, timeout=5000):
                    return True
            except:
                continue
        return False
    
    def _handle_mfa(self):
        """Handle MFA verification"""
        print("\n🔐 MFA Required!")
        print("Please complete the MFA verification manually.")
        print("Press Enter after completing MFA...")
        input()
        
        # Wait for MFA completion
        time.sleep(5)