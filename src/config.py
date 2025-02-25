# src/config.py
from pydantic import BaseSettings
from typing import Dict

class Settings(BaseSettings):
    # API Configuration
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # OpenAI Configuration
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4"

    # Vector Store Configuration
    VECTOR_STORE_PATH: str = "vector_store"

    # Topic Namespaces
    NAMESPACE_MAP: Dict[str, str] = {
        "General Services": "general",
        "Property Tax": "property_tax",
        "Water Supply": "water",
        "Solid Waste": "waste",
        "Roads": "roads"
    }

    class Config:
        env_file = ".env"
