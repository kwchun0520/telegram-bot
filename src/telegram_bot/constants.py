from dotenv import load_dotenv
import os

load_dotenv()

# Telegram bot token
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
BOT_USER_NAME = os.environ["BOT_USER_NAME"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
OPENAI_MODEL = "gpt-4-turbo"
CONFIG_PATH = './config/config.yaml'

