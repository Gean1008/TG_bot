import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from helpers.texts import get_user_error_message
from services.openai_client import generate_playlist
from pathlib import Path
logger = logging.getLogger(__name__)

# Старт — выбор плейлиста
async def start_playlist_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        image_path = Path("images/music_intro.jpg")
        with open(image_path, "rb") as photo:
            await query.message.chat.send_photo(photo=photo)

        await asyncio.sleep(1)
        logger.info("playlist_conversation_started")

        context.user_data["playlist_step"] = "genre"

        await query.edit_message_text(
            "🎵 Enter your favorite genre:\n(Examples: Rock, Pop, Jazz, Rap, Classical, EDM)"
        )
    except Exception as e:
        logger.error(f"Error starting playlist conversation - {e}")
        await update.callback_query.message.reply_text(get_user_error_message())


# Основной обработчик плейлиста
async def playlist_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_data = context.user_data
        step = user_data.get("playlist_step")
        text = update.message.text.strip()

        if step == "genre":
            user_data["genre"] = text
            user_data["playlist_step"] = "mood"
            await update.message.reply_text(
                "😊 What mood do you want? (Examples: Happy, Sad, Energetic, Chill)"
            )

        elif step == "mood":
            user_data["mood"] = text
            user_data["playlist_step"] = "era"
            await update.message.reply_text(
                "🕰️ From which decade? (Examples: 80s, 90s, 2000s, 2010s, 2020s)"
            )

        elif step == "era":
            user_data["era"] = text
            user_data["playlist_step"] = "duration"
            await update.message.reply_text(
                "⏳ How long should the playlist be? (Examples: 30 mins, 1 hour, 2 hours)"
            )

        elif step == "duration":
            user_data["duration"] = text
            user_data["playlist_step"] = None

            await update.message.reply_text(
                f"<b>🎧 Let's make your playlist:</b>\n"
                f"Genre: {user_data['genre']}\n"
                f"Mood: {user_data['mood']}\n"
                f"Era: {user_data['era']}\n"
                f"Duration: {user_data['duration']}\n",
                parse_mode="HTML"
            )
            await update.message.reply_text("🎶 Generating your playlist...")

            # Вызови свою функцию для генерации плейлиста
            playlist = await generate_playlist(
                user_data["genre"],
                user_data["mood"],
                user_data["era"],
                user_data["duration"]
            )

            await update.message.reply_text(
                "<b>Your personalized playlist:</b>\n\n"
                f"{playlist}",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🏠 Back to menu", callback_data="main_menu")]]
                )
            )

        else:
            await update.message.reply_text(
                "If you want to create another playlist, press /start"
            )
    except Exception as e:
        logger.error(f"Error collecting playlist data - {e}")
        await update.message.reply_text(get_user_error_message())
