import os
from pathlib import Path
from typing import Any

class Config:
    _instance = None
    _dictionary = {}

    def __new__(cls):
        if cls._instance is None:
            #вызываем __new__ родительского класса (object)
            cls._instance = super(Config, cls).__new__(cls)

            #parents[4] позволяет подниматься по родительским папкам 
            config_path = Path(__file__).parents[4] / 'resources' / 'urls.properties'

            if not config_path.exists():
                raise FileNotFoundError(f"Config path not found: {config_path}")

            with open(config_path, "r") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.split("=")
                        cls._dictionary[key] = value.strip()

        return cls._instance

    @staticmethod
    def fetch(key: str, default_value: Any = None) -> Any:

        env_variables = {
            "backendUrl": "BACKEND_URL",
            "dataBaseUrl": "DATABASE_URL",
        }

        env_name = env_variables.get(key)

        if env_name:
            env_value = os.getenv(env_name)

            if env_value:
                return env_value

        return Config()._dictionary.get(key, default_value)