import os
import json
from typing import Dict, Any
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        # 1. Initialize api_key with environment variable first
        api_key = os.getenv("GROQ_API_KEY")
        
        # 2. Try to import Streamlit and check secrets
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
                api_key = st.secrets['GROQ_API_KEY']
        except ImportError:
            pass  # Streamlit not available, use env var
        
        # 3. If still not found, raise explicit error
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not found. "
                "Please set it in Streamlit secrets (for cloud) or .env file (for local)."
            )
        
        # 4. Initialize Groq client
        self.client = Groq(api_key=api_key)
        self.model = os.getenv("MODEL_NAME", "llama3-70b-8192")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "500"))

    # ... rest of your methods unchanged ...
