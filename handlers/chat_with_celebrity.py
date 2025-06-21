import logging
from telegram import Update
from telegram.ext import ContextTypes
from chat_history.chat_with_celebrity import celebrity_chats
from services.openai_client import generate_celebrity_prompt, responce_to_user_message
from helpers.keyboards import get_main_menu_keyboard
from helpers.texts import get_main_text_menu
from services.image_search import get_celebrity_image_url
from pathlib import Path
from helpers.texts import get_user_error_message

logger = logging.getLogger(__name__)

async def start_chat_with_celebrity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        user_text = update.message.text.strip()
        loading_gif_path = Path("images/Loading_icon.gif")

        if context.user_data.get("awaiting_celebrity_name"):
            name = user_text.title()
            loading_message = await update.message.reply_animation(
                animation=loading_gif_path.open("rb"),
                caption="⏳ Loading..."
            )

            system_prompt = await generate_celebrity_prompt(name)

            await loading_message.delete()

            if not system_prompt:
                await update.message.reply_text("🔁 Unable to retrieve information about this person. Try another one.🔁")
                return

            context.user_data["awaiting_celebrity_name"] = False
            context.user_data["celebrity_name"] = name
            context.user_data["celebrity_chat_active"] = True

            celebrity_chats[user_id] = [{"role": "system", "content": system_prompt}]

            loading_message = await update.message.reply_animation(
                animation=loading_gif_path.open("rb"),
                caption="⏳ Loading..."
            )

            photo_url = await get_celebrity_image_url(name)

            await loading_message.delete()

            if photo_url:
                await update.message.reply_photo(
                    photo=photo_url,
                    caption=f"🌟🌟🌟 Now you are discussing with {name}. Ask something.🌟🌟🌟"
                )
            else:
                await update.message.reply_text(f"🌟🌟🌟 Now you are discussing with {name}. Ask something.🌟🌟🌟")
            return

        if context.user_data.get("celebrity_chat_active"):
            user_message = update.message.text.strip()

            if user_id not in celebrity_chats:
                await update.message.reply_text("🛑🛑🛑Message history not found🛑🛑🛑")
                return

            celebrity_chats[user_id].append({"role": "user", "content": user_message})
            ai_response = await responce_to_user_message(celebrity_chats[user_id])
            celebrity_chats[user_id].append({"role": "assistant", "content": ai_response})

            await update.message.reply_text(ai_response)
            await update.message.reply_text("🔚 If you want to exit from this chat, write or press ❌ /exit_celebrity")
            return

        await update.message.reply_text("🟢Choose from main menu or use 🚀 /start")

    except Exception as e:
        logger.error(f"🛑🛑🛑An error occurred while AI generated response to user - {e}🛑🛑🛑")
        await update.message.reply_text(get_user_error_message())

async def exit_chat_with_celebrity(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    context.user_data["awaiting_celebrity_name"] = False
    context.user_data["celebrity_name"] = None
    context.user_data["celebrity_chat_active"] = False

    if user_id in celebrity_chats:
        del celebrity_chats[user_id]

    welcome_text = get_main_text_menu()
    reply_markup = get_main_menu_keyboard()

    await update.message.reply_text(
        "🔚<b>You've exit chat with celebrity</b>🔚\n\n\n"
        + welcome_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

