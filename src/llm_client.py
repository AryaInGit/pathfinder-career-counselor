import os
import json
import logging
from typing import Dict, Any
from groq import Groq
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import streamlit as st
    logger.info("Streamlit imported successfully")
except ImportError:
    st = None
    logger.warning("Streamlit not available in this environment")

load_dotenv()

class LLMClient:
    def __init__(self):
        # Get API key with comprehensive fallback logic
        api_key = None
        key_source = "Not found"
        
        # 1. Check Streamlit secrets
        if st and hasattr(st, 'secrets'):
            if 'GROQ_API_KEY' in st.secrets:
                api_key = st.secrets['GROQ_API_KEY']
                key_source = "Streamlit secrets"
            elif 'groq' in st.secrets and 'api_key' in st.secrets['groq']:
                api_key = st.secrets['groq']['api_key']
                key_source = "Streamlit secrets (nested)"
        
        # 2. Check environment variables
        if not api_key:
            if os.getenv("GROQ_API_KEY"):
                api_key = os.getenv("GROQ_API_KEY")
                key_source = "Environment variable"
            elif os.getenv("GROQ_API_KEY"):
                api_key = os.getenv("GROQ_API_KEY")
                key_source = "Alternative environment variable"
        
        # 3. Check for common CI/CD environment variables
        if not api_key:
            for var in ["SECRETS_GROQ_API_KEY", "ENV_GROQ_API_KEY", "GROQ_API_KEY"]:
                if os.getenv(var):
                    api_key = os.getenv(var)
                    key_source = f"CI/CD variable ({var})"
                    break
        
        # Final check and error handling
        if not api_key:
            error_msg = (
                "GROQ_API_KEY not found in any sources. "
                "Check your Streamlit secrets or environment variables."
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        logger.info(f"Using Groq API key from: {key_source}")
        
        try:
            # Initialize Groq client with validation
            self.client = Groq(api_key=api_key)
            logger.info("Groq client initialized successfully")
        except Exception as e:
            error_msg = f"Groq client initialization failed: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
        
        # Get configuration with defaults
        self.model = os.getenv("MODEL_NAME", "llama3-70b-8192")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "500"))
        logger.info(f"Model: {self.model}, Temp: {self.temperature}, Max tokens: {self.max_tokens}")

class LLMClient:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("MODEL_NAME", "llama3-70b-8192")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "500"))

    async def generate_response(self, prompt: str, system_message: str = "") -> str:
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again."

    def generate_response_sync(self, prompt: str, system_message: str = "") -> str:
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again."

    def extract_structured_data(self, text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        Extract the following information from the text below and return it as JSON:

        Schema: {json.dumps(schema, indent=2)}

        Text: {text}

        Return only valid JSON that matches the schema. If information is not available, use null or empty arrays as appropriate.
        """

        try:
            response = self.generate_response_sync(prompt)
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {}
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error extracting structured data: {e}")
            return {}

    def analyze_career_match(self, student_info: str, career_info: str) -> Dict[str, Any]:
        prompt = f"""
        Analyze how well this career matches the student's profile:

        Student Information:
        {student_info}

        Career Information:
        {career_info}

        Return a JSON object with:
        {{
            "match_score": 0.85,
            "explanation": "Brief explanation of the match",
            "strengths": ["strength1", "strength2"],
            "considerations": ["consideration1", "consideration2"]
        }}

        Match score should be between 0.0 and 1.0.
        """

        response = self.generate_response_sync(prompt)
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except (json.JSONDecodeError, Exception):
            pass

        return {
            "match_score": 0.5,
            "explanation": "Unable to analyze match at this time.",
            "strengths": [],
            "considerations": []
        }
