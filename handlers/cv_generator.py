import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from helpers.texts import get_user_error_message
from services.openai_client import generate_user_cv
from pathlib import Path
logger = logging.getLogger(__name__)

async def start_cv(update:Update,context:ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        image_path = Path("images/person_image.png")
        with open(image_path, "rb") as photo:
            await query.message.chat.send_photo(photo=photo)

        await asyncio.sleep(1)

        context.user_data["cv_counter_step"] = "name"

        await query.edit_message_text("️🤔 Enter your name: ")

    except Exception as e:
        logger.error(f"🛑🛑🛑An error occurred while cv generator starting - {e}🛑🛑🛑")
        await update.callback_query.message.reply_text(get_user_error_message())


async def cv_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_data = context.user_data
        step = user_data.get("cv_counter_step")
        text = update.message.text.strip()

        if step == "name":
            user_data["name"] = text
            user_data["cv_counter_step"] = "education"
            await update.message.reply_text("📚 Enter your education: ")
        elif step == "education":
            user_data["education"] = text
            user_data["cv_counter_step"] = "experience"
            await update.message.reply_text("️💡 Enter your work experience: ")

        elif step == "experience":
            user_data["experience"] = text
            user_data["cv_counter_step"] = "stack"
            await update.message.reply_text("🛠 Enter your technology stack: ")

        elif step == "stack":
            user_data["stack"] = text
            user_data["cv_counter_step"] = None


            await update.message.reply_text(
                f"<b>Excellent!</b> Your education - {user_data["education"]} 📚\n"
                f"Your work experience - {user_data["experience"]} 💡\n"
                f"Your technology stack - {user_data["stack"]} 🛠\n",
                parse_mode='HTML'
            )

            await update.message.reply_text("Generating your CV...")

            result = await generate_user_cv(
                user_data["name"],
                user_data["education"],
                user_data["experience"],
                user_data["stack"])

            await update.message.reply_text(
                "<b>Your CV:</b>\n\n"
                f"{result}",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("❌ exit to main menu ❌", callback_data="/exit")]]
                )
            )

        else:
            await update.message.reply_text(
                "If you want to create another CV, press /start"
            )
    except Exception as e:
        logger.error(f"🛑🛑🛑An error occurred while collecting meal data - {e}🛑🛑🛑")
        await update.message.reply_text(get_user_error_message())



