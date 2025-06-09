import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start"""
    keyboard=[
        [InlineKeyboardButton("🎲 Some random fact",callback_data="random_fact")],
        [InlineKeyboardButton("🤖 chatGPT(coming soon)", callback_data="gpt_coming_soon")],
        [InlineKeyboardButton("💬 Chat with celebrity(coming soon)", callback_data="talk_coming_soon")],
        [InlineKeyboardButton("🧠 Quiz(coming soon)", callback_data="quiz_coming_soon")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "🎉 <b>Welcome to ChatGpt Bot</b>\n\n"
        "🚀 <b>Available options</b>\n"
        "Random fact - get some random facts\n"
        "ChatGPT - talk to AI (coming soon)\n"
        "Chat with Celebrity (coming soon)\n"
        "Quiz - test your knowledge (coming soon)\n\n"
        "Choose your option from menu:"
    )

    await  update.message.reply_text(welcome_text, parse_mode="HTML", reply_markup=reply_markup)

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "random_fact":
        # This case work in random_fact.py
        pass
    elif query.data in ["gpt_coming_soon","talk_coming_soon","quiz_coming_soon"]:
        await query.edit_message_text(
            "<b>Option in progress</b>\n\n",
            parse_mode="HTML"
        )
        #Through 3s function will sleep
        await asyncio.sleep(3)
        await start_menu_again(query)


async def start_menu_again(query):
    """Returne to home menu /start"""
    keyboard = [
        [InlineKeyboardButton("🎲 Some random fact", callback_data="random_fact")],
        [InlineKeyboardButton("🤖 chatGPT(coming soon)", callback_data="gpt_coming_soon")],
        [InlineKeyboardButton("💬 Chat with celebrity(coming soon)", callback_data="talk_coming_soon")],
        [InlineKeyboardButton("🧠 Quiz(coming soon)", callback_data="quiz_coming_soon")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "🎉 <b> Wellcome to ChatGPT bot</b>\n\n"
        "Choose one enabled option",
        parse_mode = "HTML",
        reply_markup = reply_markup
    )

