import logging
from PIL.SpiderImagePlugin import loadImageSeries
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.basic import start_menu_again
from services.openai_client import get_random_fact
from helpers.keyboards import get_main_menu_keyboard,get_one_more_fact_keyboard

logger = logging.getLogger(__name__)


async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Random fact handler"""
    await send_fact(update)


async def random_fact_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "random_more":
        await send_fact(update)
    elif query.data == "random_exit":
        reply_markup = get_main_menu_keyboard()

        await query.edit_message_text(
            "🤖 <b>Welcome to ChatGPT bot</b> 🤖\n\n"
            "🟢 Choose option from menu to continue:",
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    elif query.data == "random_fact":
        await send_fact(update)

async def send_fact(update: Update):
    try:
        if update.message:
            loading_message = await update.message.reply_text("🤖 Generating fact, please wait...🤖 ")
        elif update.callback_query:
            loading_message = await update.callback_query.message.reply_text("🤖 Generating fact, please wait...🤖 ")
        else:
            logger.warning("Update has no message or callback_query")
            return
        fact = await get_random_fact()

        reply_markup = get_one_more_fact_keyboard()

        await loading_message.edit_text(
            f"🧠🧠🧠<b>Interesting fact:</b>🧠🧠🧠\n\n{fact}",
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"An error occurred while generating fact - {e}")
        await loading_message.edit_text(
            f"🛑🛑🛑<b>AI services are unavailable now, please try again later</b>🛑🛑🛑",
            parse_mode='HTML',
            reply_markup=reply_markup
        )
