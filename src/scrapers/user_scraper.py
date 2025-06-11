import pandas as pd
import json
import time
from src.core.browser import BrowserManager
from src.core.auth import AuthHandler
from src.agents.ai_agent import UIAgent
from src.utils.captcha_solver import CaptchaSolver
from src.utils.config import config
import logging

class UserScraper:
    def __init__(self, platform_name, base_url):
        self.platform_name = platform_name
        self.base_url = base_url
        self.browser_manager = BrowserManager()
        self.page = None
        self.auth_handler = None
        self.ai_agent = UIAgent()
        self.captcha_solver = CaptchaSolver()
        self.selectors = config.get_platform_selectors(platform_name)
        
    def initialize(self):
        """Initialize browser and authentication"""
        self.page = self.browser_manager.launch()
        self.auth_handler = AuthHandler(self.page, self.platform_name)
        
        # Navigate to platform
        self.page.goto(self.base_url)
        
    def login(self, username=None, password=None):
        """Perform login"""
        return self.auth_handler.login(username, password)
    
    def extract_users(self):
        """Extract user data from the platform"""
        users = []
        page_number = 1
        
        try:
            # Navigate to user management page
            self._navigate_to_users_page()
            
            while True:
                logging.info(f"Extracting users from page {page_number}")
                
                # Extract users from current page
                page_users = self._extract_users_from_current_page()
                users.extend(page_users)
                
                # Check if there's a next page
                if not self._go_to_next_page():
                    break
                    
                page_number += 1
                time.sleep(2)  # Respectful delay
                
        except Exception as e:
            logging.error(f"User extraction failed: {e}")
            
        return users
    
    def _navigate_to_users_page(self):
        """Navigate to user management page"""
        # This would be platform-specific
        # For now, we'll assume we're already on the right page
        time.sleep(3)
    
    def _extract_users_from_current_page(self):
        """Extract users from current page"""
        users = []
        user_mgmt_selectors = self.selectors.get('user_management', {})
        
        try:
            # Wait for user table to load
            user_table = user_mgmt_selectors.get('users_table')
            if user_table:
                self.page.wait_for_selector(user_table, timeout=10000)
            
            # Get all user rows
            user_row_selector = user_mgmt_selectors.get('user_row')
            if not user_row_selector:
                # Use AI to find user rows
                user_row_selector = self.ai_agent.find_elements_intelligently(
                    self.page, "user rows in a table or list"
                )
            
            if user_row_selector:
                user_elements = self.page.query_selector_all(user_row_selector)
                
                for element in user_elements:
                    user_data = self._extract_user_data_from_element(element, user_mgmt_selectors)
                    if user_data:
                        users.append(user_data)
                        
        except Exception as e:
            logging.error(f"Failed to extract users from page: {e}")
            
        return users
    
    def _extract_user_data_from_element(self, element, selectors):
        """Extract individual user data from element"""
        try:
            # Extract using configured selectors
            name = self._safe_extract_text(element, selectors.get('name_selector'))
            email = self._safe_extract_text(element, selectors.get('email_selector'))
            role = self._safe_extract_text(element, selectors.get('role_selector'))
            
            # Try to find last login if available
            last_login = self._safe_extract_text(element, selectors.get('last_login_selector', ''))
            
            return {
                'name': name,
                'email': email,
                'role': role,
                'last_login': last_login,
                'extracted_at': pd.Timestamp.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Failed to extract user data: {e}")
            return None
    
    def _safe_extract_text(self, element, selector):
        """Safely extract text from element"""
        if not selector:
            return ''
            
        try:
            sub_element = element.query_selector(selector)
            return sub_element.inner_text().strip() if sub_element else ''
        except:
            return ''
    
    def _go_to_next_page(self):
        """Navigate to next page if available"""
        user_mgmt_selectors = self.selectors.get('user_management', {})
        next_button_selector = user_mgmt_selectors.get('next_button')
        
        if not next_button_selector:
            # Use AI to find next button
            next_button_selector = self.ai_agent.find_elements_intelligently(
                self.page, "next page button or pagination next"
            )
        
        if next_button_selector:
            try:
                next_button = self.page.query_selector(next_button_selector)
                if next_button and next_button.is_enabled():
                    next_button.click()
                    time.sleep(3)  # Wait for page load
                    return True
            except:
                pass
                
        return False
    
    def save_users_data(self, users, format='csv'):
        """Save extracted users data"""
        if not users:
            logging.warning("No users to save")
            return
            
        df = pd.DataFrame(users)
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        
        if format == 'csv':
            filename = f"data/extracted/users_{self.platform_name}_{timestamp}.csv"
            df.to_csv(filename, index=False)
        elif format == 'json':
            filename = f"data/extracted/users_{self.platform_name}_{timestamp}.json"
            df.to_json(filename, orient='records', indent=2)
        
        logging.info(f"Saved {len(users)} users to {filename}")
        return filename
    
    def close(self):
        """Close browser and cleanup"""
        self.browser_manager.close()