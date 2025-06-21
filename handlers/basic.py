import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from helpers.keyboards import get_main_menu_keyboard,get_one_more_fact_keyboard
from helpers.texts import get_main_text_menu
from handlers.Quiz_handler import start_quiz_with_user

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for start"""

    if update.message:
        await update.message.delete()

    await asyncio.sleep(0.5)

    reply_markup = get_main_menu_keyboard()

    welcome_text = get_main_text_menu()

    await update.message.reply_text(welcome_text, parse_mode='HTML', reply_markup=reply_markup)


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for selection"""
    query = update.callback_query

    await query.answer()

    if query.data == "random_fact":
        """Call from random_fact.py"""
        pass
    elif query.data == "chat_gpt":
        context.user_data["chat_mode"] = True
        await query.edit_message_text(
            "🤖 <b>ChatGpt activated</b>\n\n"
            "💬 Asc me anything"
            , parse_mode='HTML'
        )
    elif query.data == "chat_with_celebrity":
        context.user_data["awaiting_celebrity_name"] = True
        await query.edit_message_text("🌟 <b>Enter celebrity name.</b>\n\n\n",
                                      parse_mode='HTML')
    elif query.data == "start_quiz_with_user":
        await query.edit_message_text(
            "<b>🧠 QUIZ was selected</b>\n\n",
            parse_mode='HTML'
        )
        await start_quiz_with_user(update, context)
    # elif query.data == "start_translator":
    #     await query.edit_message_text(
    #         "<b>🌐 Translator </b> - function started\n\n"
    #         "Give me an audio",
    #         parse_mode='HTML'
    #     )
    else:
        await start_menu_again(query)


async def start_menu_again(query):
    """Return back start menu"""

    reply_markup = get_main_menu_keyboard()

    await query.edit_message_text(
        "👋 <b>Welcome to ChatGPT bot</b>\n\n"
        "🟢 Choose option from menu to continue:",
        parse_mode='HTML',
        reply_markup=reply_markup
    )