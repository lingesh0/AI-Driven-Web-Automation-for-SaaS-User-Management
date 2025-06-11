import logging
import sys
import os
from src.scrapers.user_scraper import UserScraper
from src.utils.config import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    """Main automation workflow"""
    
    # Create necessary directories
    os.makedirs('data/extracted', exist_ok=True)
    os.makedirs('data/logs', exist_ok=True)
    
    # Configuration
    platform_name = input("Enter platform name (trello/notion): ").lower()
    base_url = input("Enter platform URL: ")
    
    if platform_name not in ['trello', 'notion']:
        logging.error("Unsupported platform. Please add configuration.")
        return
    
    # Initialize scraper
    scraper = UserScraper(platform_name, base_url)
    
    try:
        # Initialize browser
        logging.info("Initializing browser...")
        scraper.initialize()
        
        # Login
        logging.info("Attempting login...")
        if not scraper.login():
            logging.error("Login failed")
            return
        
        logging.info("Login successful!")
        
        # Extract users
        logging.info("Starting user extraction...")
        users = scraper.extract_users()
        
        if users:
            logging.info(f"Extracted {len(users)} users")
            
            # Save data
            csv_file = scraper.save_users_data(users, 'csv')
            json_file = scraper.save_users_data(users, 'json')
            
            print(f"\n✅ Extraction completed!")
            print(f"📊 Users extracted: {len(users)}")
            print(f"📁 CSV file: {csv_file}")
            print(f"📁 JSON file: {json_file}")
            
        else:
            logging.warning("No users extracted")
    
    except Exception as e:
        logging.error(f"Automation failed: {e}")
        
    finally:
        # Cleanup
        scraper.close()
        logging.info("Browser closed")

if __name__ == "__main__":
    main()