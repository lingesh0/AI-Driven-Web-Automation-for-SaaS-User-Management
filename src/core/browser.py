from playwright.sync_api import sync_playwright
from src.utils.config import config
import time
import logging

class BrowserManager:
    def __init__(self, platform='chromium'):
        self.playwright = None
        self.browser = None
        self.page = None
        self.platform = platform
        
    def launch(self):
        """Launch browser and create new page"""
        self.playwright = sync_playwright().start()
        self.browser = getattr(self.playwright, self.platform).launch(
            headless=config.headless,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        self.page = self.browser.new_page()
        
        # Set default timeout
        self.page.set_default_timeout(config.timeout)
        
        # Set user agent to avoid detection
        self.page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        return self.page
    
    def close(self):
        """Close browser and cleanup"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def wait_for_manual_action(self, message="Complete manual action", timeout=60):
        """Wait for manual user action (like MFA)"""
        print(f"\n{message}")
        print("Press Enter after completing the action...")
        input()