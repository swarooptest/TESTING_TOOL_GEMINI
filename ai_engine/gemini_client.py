import google.generativeai as genai
from config import GEMINI_API_KEY

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        # Use a supported Gemini model
        self.model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    def generate_test_code(self, goal: str, base_url: str):
        prompt = f"""
        You are an expert Selenium + Python test automation engineer.
        Write a complete Pytest test for the goal: "{goal}"
        The website is: {base_url}
        Use Chrome WebDriver from Selenium.
        The code must be executable directly.
        Include locators and assertions.
        Save credentials in variables.
        """
        response = self.model.generate_content([prompt])
        return response.text
