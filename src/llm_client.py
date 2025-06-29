import os
import json
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Try to import Groq but don't fail if it doesn't work
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError as e:
    logger.error(f"Groq import failed: {str(e)}")
    GROQ_AVAILABLE = False
except Exception as e:
    logger.error(f"Unexpected import error: {str(e)}")
    GROQ_AVAILABLE = False

load_dotenv()

class LLMClient:
    def __init__(self):
        self.client = None
        self.initialized = False
        self.error_message = ""
        
        try:
            # Get API key
            api_key = self._get_api_key()
            
            # Initialize Groq client if available
            if GROQ_AVAILABLE:
                self.client = Groq(api_key=api_key)
                # Test connection
                self.client.models.list(limit=1)
                self.initialized = True
            else:
                self.error_message = "Groq library not available"
                
        except Exception as e:
            self.error_message = str(e)
            logger.exception("Groq initialization failed")
        
        # Set configuration parameters
        self.model = os.getenv("MODEL_NAME", "llama3-70b-8192")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "500"))

    def _get_api_key(self) -> str:
        """Retrieve API key from multiple sources"""
        api_key = os.getenv("GROQ_API_KEY")
        
        # Try Streamlit secrets if not found in env
        if not api_key:
            try:
                import streamlit as st
                if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
                    api_key = st.secrets['GROQ_API_KEY']
            except Exception:
                pass  # Streamlit not available or not initialized
        
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not found in environment variables or Streamlit secrets. "
                "Please set it in Streamlit secrets (for cloud) or .env file (for local)."
            )
        
        return api_key

    def is_initialized(self) -> bool:
        return self.initialized

    def get_error(self) -> str:
        return self.error_message

    async def generate_response(self, prompt: str, system_message: str = "") -> str:
        if not self.initialized:
            return self._fallback_response()
        
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
            logger.error(f"LLM request failed: {str(e)}")
            return self._fallback_response()

    def generate_response_sync(self, prompt: str, system_message: str = "") -> str:
        if not self.initialized:
            return self._fallback_response()
        
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
            logger.error(f"LLM request failed: {str(e)}")
            return self._fallback_response()

    def _fallback_response(self) -> str:
        return "I'm having trouble connecting to the career counseling service. Please try again later or contact support."

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
