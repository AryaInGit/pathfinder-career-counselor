import os
import json
from typing import Dict, Any
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        # Get API key from environment variables first
        api_key = os.getenv("GROQ_API_KEY")
        
        # If not found, try to get from Streamlit secrets (but only if Streamlit is available)
        if not api_key:
            api_key = self._get_streamlit_secret()
        
        # Validate API key
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not found. "
                "Please set it in Streamlit secrets (for cloud) or .env file (for local)."
            )
        
        if len(api_key) < 30 or not api_key.startswith("gsk_"):
            raise ValueError(
                "Invalid API key format. "
                "Groq API keys typically start with 'gsk_' and are 40+ characters."
            )
        
        # Initialize Groq client
        try:
            self.client = Groq(api_key=api_key)
            # Simple validation request
            self.client.models.list(limit=1)
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Groq client: {str(e)}\n"
                "Please verify your GROQ_API_KEY at https://console.groq.com"
            ) from e
        
        # Set configuration parameters
        self.model = os.getenv("MODEL_NAME", "llama3-70b-8192")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "500"))

    def _get_streamlit_secret(self) -> str:
        """Safely get Streamlit secret at runtime"""
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
                return st.secrets['GROQ_API_KEY']
        except ImportError:
            pass  # Streamlit not available
        except Exception as e:
            print(f"Warning: Could not access Streamlit secrets: {str(e)}")
        return None

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
