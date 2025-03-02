# src/utils.py
from functools import lru_cache
from src.config import Settings

@lru_cache()
def get_settings():
    return Settings()
