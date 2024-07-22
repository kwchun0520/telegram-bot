from typing import Final
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from src.telegram_bot.constants import TELEGRAM_BOT_TOKEN, BOT_USER_NAME
from src.telegram_bot.config import CONFIG
from src.telegram_bot.client import ChatbotClient,SummarizationClient

TOKEN: Final = TELEGRAM_BOT_TOKEN
BOT: Final = BOT_USER_NAME


## commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Hello! I am {BOT}, your personal assistant! Welcome!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Please chat with me!")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"This is a custom command!")


async def summarize_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args>0:
        if context.args[0].startswith(r"http") or context.args[0].startswith(r"www"):
            url = context.args[0]
            try:
                await update.message.reply_text(f"Summarizing")
                result = SummarizationClient(CONFIG.CHATBOT).load(url)
            except Exception as e:
                result = f"Error: {str(e)}"
                
            await update.message.reply_text(result)
    else:
        await update.message.reply_text(f"No URL provided!")

## responses
def handle_response(text: str) -> str:

    return ChatbotClient(CONFIG.CHATBOT).chat(text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) sent a message in {message_type}: {text}")

    if message_type == "group":
        if BOT_USER_NAME in text:
            new_text: str = text.replace(BOT_USER_NAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return None
    else:
        response: str = handle_response(text)

    print(f"Bot response: {response}")
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update}. An error occurred: {context.error}")


def main():
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    ## commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(CommandHandler("summarize", summarize_command))

    ## responses
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    ## error handler
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()