import logging

import helpers.keyboards
from services.openai_client import responce_to_user_message
from telegram import Update
from telegram.ext import ContextTypes
from helpers.keyboards import get_main_menu_keyboard
from chat_history.chat_with_user import chat_with_user

logger = logging.getLogger(__name__)

async def response_to_user(update: Update, context:ContextTypes.DEFAULT_TYPE):

    try:
        if not context.user_data.get("chat_mode"):
            await update.message.reply_text("🟢 Choose option from menu. Use 🚀 /start to return to main menu.")
            return

        user_id = update.effective_user.id
        user_message = update.message.text

        if user_id not in chat_with_user:
            chat_with_user[user_id] = [{"role": "system", "content": "You are like a friend to user, response him in russian"}]

        chat_with_user[user_id].append({"role": "user", "content": user_message})
        ai_response = await responce_to_user_message(chat_with_user[user_id])

        await update.message.reply_text(ai_response)
        chat_with_user[user_id].append({"role": "assistant", "content": ai_response})
        await update.message.reply_text("Use ❌ /exit if you want to exit chat mode")
    except Exception as e:
        logger.error(f"An error occurred while AI generated response to user - {e}")
        return "🛑🛑🛑 AI services are unavailable now, try again later 🛑🛑🛑"

async def stop_chat_mode(update: Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data["chat_mode"] = False

    reply_markup = get_main_menu_keyboard()

    try:
        chat_with_user.clear()
    except Exception as e:
        logger.error(f"🛑🛑🛑 An error occurred while AI generated response to user - {e} 🛑🛑🛑")

    await update.message.reply_text(
        "🤖 <b>Chat with AI deactivated.</b>\n\n"
        "🟢 Choose option from menu to continue:",
        parse_mode='HTML',
        reply_markup=reply_markup
    )
