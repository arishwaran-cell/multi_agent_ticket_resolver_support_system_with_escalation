import os
from dotenv import load_dotenv

load_dotenv()


llm_config={
            "temperature": 0,
            "config_list": [
                {
                    "model": "llama3:8b",  # This should match your deployment name
                    "base_url": "http://localhost:11434/v1",
                    "api_type": "openai",
                    "api_key": "NULL"
                }
                ]
        }


