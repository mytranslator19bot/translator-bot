import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def translate(text):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": f"Detect whether the following text is Russian or English. If Russian, translate to English. If English, translate to Russian. Reply with ONLY the translation, no explanations.\n\n{text}"}]
    )
    return response.content[0].text.strip()

async def start(update, context):
    await update.message.reply_text("👋 Hi! Send me any message in Russian or English and I'll translate it!\n\n🇷🇺 Russian → English\n🇬🇧 English → Russian")

async def handle_message(update, context):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        translation = translate(update.message.text.strip())
        await update.message.reply_text(translation)
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("⚠️ Something went wrong, please try again.")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
logger.info("Bot running...")
app.run_polling()
