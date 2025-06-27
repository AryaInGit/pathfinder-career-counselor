#!/usr/bin/env python3
"""
PathFinder CLI - AI Career Counseling Platform
Run this file to start the command-line interface version
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli_interface import CLIInterface

def main():
    """Main entry point for CLI application"""
    try:
        # Check for Groq API key
        if not os.getenv("GROQ_API_KEY"):
            print("❌ Error: GROQ_API_KEY environment variable not set")
            print("Please add your Groq API key to your environment variables or .env file")
            print("Example: export GROQ_API_KEY='your_api_key_here'")
            sys.exit(1)
        
        # Initialize and run CLI interface
        cli = CLIInterface()
        cli.run()
        
    except KeyboardInterrupt:
        print("\n👋 Thanks for using PathFinder! Good luck with your career journey!")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
