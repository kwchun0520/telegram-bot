import yaml
from src.telegram_bot.constants import CONFIG_PATH
from pydantic import BaseModel,Field

class Config(BaseModel):
    OPENAI_MODEL: str = Field(str)
    GEMINI_MODEL: str = Field(str)
    CHATBOT: str = Field(str)


def load_config() -> Config:
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
        return Config(**config)
    
CONFIG = load_config()