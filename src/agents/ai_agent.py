from langchain.agents import create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from src.utils.config import config
import logging

class UIAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=config.openai_api_key,
            model="gpt-4",
            temperature=0
        )
        
    def detect_ui_changes(self, page, expected_selectors):
        """Detect UI changes and suggest new selectors"""
        try:
            # Get current page HTML
            html_content = page.content()
            
            # Create prompt for UI analysis
            prompt = f'''
            Analyze this HTML and determine if the expected selectors are still valid.
            Expected selectors: {expected_selectors}
            
            Current HTML (first 2000 chars): {html_content[:2000]}
            
            If selectors are invalid, suggest new ones in the same format.
            Return result as JSON with "valid": true/false and "suggestions": {{}}
            '''
            
            response = self.llm.invoke(prompt)
            return self._parse_ui_response(response.content)
            
        except Exception as e:
            logging.error(f"UI detection failed: {e}")
            return {"valid": False, "suggestions": {}}
    
    def _parse_ui_response(self, response):
        """Parse AI response for UI analysis"""
        try:
            import json
            return json.loads(response)
        except:
            return {"valid": False, "suggestions": {}}
    
    def find_elements_intelligently(self, page, element_description):
        """Use AI to find elements based on description"""
        try:
            html_content = page.content()
            
            prompt = f'''
            Find CSS selectors for: {element_description}
            
            HTML content (first 3000 chars): {html_content[:3000]}
            
            Return the most specific CSS selector that would reliably identify this element.
            Return only the selector, no explanation.
            '''
            
            response = self.llm.invoke(prompt)
            return response.content.strip()
            
        except Exception as e:
            logging.error(f"Intelligent element finding failed: {e}")
            return None