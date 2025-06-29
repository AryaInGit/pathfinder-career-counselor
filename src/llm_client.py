import os
import json
from typing import Dict, Any
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        # Get API key with detailed validation
        api_key = self._get_api_key()
        
        # Initialize Groq client with extra validation
        try:
            self.client = Groq(api_key=api_key)
            # Test connection immediately
            self._test_connection()
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Groq client: {str(e)}\n"
                "Please verify your GROQ_API_KEY at https://console.groq.com"
            ) from e
        
        # Set configuration parameters
        self.model = os.getenv("MODEL_NAME", "llama3-70b-8192")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "500"))

    def _get_api_key(self) -> str:
        """Retrieve and validate API key from multiple sources"""
        api_key = None
        sources = []
        
        # 1. Check environment variables
        if os.getenv("GROQ_API_KEY"):
            api_key = os.getenv("GROQ_API_KEY")
            sources.append("environment variable")
        
        # 2. Check Streamlit secrets
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
                api_key = st.secrets['GROQ_API_KEY']
                sources.append("Streamlit secrets")
        except ImportError:
            pass
        
        # 3. Validate key format
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not found in any source. "
                "Please set it in Streamlit secrets or environment variables."
            )
        
        if len(api_key) < 30 or not api_key.startswith("gsk_"):
            raise ValueError(
                f"Invalid API key format from source(s): {', '.join(sources)}\n"
                "Groq API keys typically start with 'gsk_' and are 40+ characters."
            )
        
        return api_key

    def _test_connection(self):
        """Verify the API key works with a simple request"""
        try:
            # Simple validation request
            self.client.models.list(limit=1)
        except Exception as e:
            raise ConnectionError(
                f"Groq API connection failed: {str(e)}\n"
                "Please check your API key and network connection."
            ) from e

    # ... rest of your methods unchanged ...
