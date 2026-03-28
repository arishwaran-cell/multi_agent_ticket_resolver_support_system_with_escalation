import os
from dotenv import load_dotenv

load_dotenv()


llm_config={
            "temperature": 0,
            "config_list": [
                {
                    "model": os.getenv("OLLAMA_MODEL"),  # This should match your deployment name
                    "base_url": os.getenv("OLLAMA_BASE_URL"),
                    "api_type": "openai",
                    "api_key": os.getenv("OLLAMA_API_KEY")
                }
            ],
        }

