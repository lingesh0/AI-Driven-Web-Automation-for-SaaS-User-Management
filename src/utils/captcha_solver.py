import requests
import time
from src.utils.config import config

class CaptchaSolver:
    def __init__(self):
        self.api_key = config.captcha_api_key
        self.base_url = "http://2captcha.com"
    
    def solve_captcha(self, captcha_image_path=None, site_key=None, page_url=None):
        """Solve CAPTCHA using 2Captcha API"""
        if not self.api_key:
            print("No CAPTCHA API key provided. Please solve manually.")
            input("Press Enter after solving CAPTCHA...")
            return None
            
        try:
            if captcha_image_path:
                return self._solve_image_captcha(captcha_image_path)
            elif site_key and page_url:
                return self._solve_recaptcha(site_key, page_url)
        except Exception as e:
            print(f"CAPTCHA solving failed: {e}")
            print("Please solve CAPTCHA manually.")
            input("Press Enter after solving CAPTCHA...")
            return None
    
    def _solve_image_captcha(self, image_path):
        """Solve image-based CAPTCHA"""
        # Submit CAPTCHA
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {'key': self.api_key, 'method': 'post'}
            response = requests.post(f"{self.base_url}/in.php", files=files, data=data)
        
        if not response.text.startswith('OK|'):
            raise Exception(f"CAPTCHA submission failed: {response.text}")
        
        captcha_id = response.text.split('|')[1]
        
        # Get result
        return self._get_captcha_result(captcha_id)
    
    def _solve_recaptcha(self, site_key, page_url):
        """Solve reCAPTCHA"""
        data = {
            'key': self.api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': page_url
        }
        response = requests.post(f"{self.base_url}/in.php", data=data)
        
        if not response.text.startswith('OK|'):
            raise Exception(f"reCAPTCHA submission failed: {response.text}")
        
        captcha_id = response.text.split('|')[1]
        return self._get_captcha_result(captcha_id)
    
    def _get_captcha_result(self, captcha_id):
        """Get CAPTCHA solution result"""
        for _ in range(60):  # Wait up to 5 minutes
            time.sleep(5)
            response = requests.get(f"{self.base_url}/res.php", params={
                'key': self.api_key,
                'action': 'get',
                'id': captcha_id
            })
            
            if response.text == 'CAPCHA_NOT_READY':
                continue
            elif response.text.startswith('OK|'):
                return response.text.split('|')[1]
            else:
                raise Exception(f"CAPTCHA solving failed: {response.text}")
        
        raise Exception("CAPTCHA solving timeout")