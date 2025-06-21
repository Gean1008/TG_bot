import logging
from pyexpat.errors import messages
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
from services.openai_client import get_chatgpt_response
import os

logger = logging.getLogger(__name__)


WAITING_FOR_MESSAGE = 1

CAPTION='''🤖 <b> ChatGPT Interface</b>\n\n
            Write any question or message, and I'll transmit it to ChatGPT\n
            💡 <b>Examples of questions:</b>\n
            • Explain quantum physics in simple words\n
            • Write a short story about cat\n
            • How to cook pasta carbonara?\n
            • Translate frase in English\n\n
            ✍ Just write your question in next message:'''


async def gpt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await gpt_start(update, context)


async def gpt_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        image_path = "images/chatgpt-logo-green.png"
        if os.path.exists(image_path):
            with open(image_path, 'rb') as photo:
                if update.callback_query:
                    await update.callback_query.message.reply_photo(
                        photo=photo,
                        caption=CAPTION,
                        parse_mode='HTML'
                    )
                else:
                    await update.message.reply_photo(
                        photo=photo,
                        caption=CAPTION,
                        parse_mode='HTML'
                    )
        else:
            message_text = CAPTION

            if update.callback_query:
                await update.callback_query.edit_message_text(message_text, parse_mode='HTML')
            else:
                await update.message.reply_text(message_text, parse_mode='HTML')

        if update.callback_query:
            await update.callback_query.answer()

        return WAITING_FOR_MESSAGE

    except Exception as e:
        logger.error(f"Error trying to run ChatGPT interface: {e}")
        error_text = "😟 Something wrong with running ChatGPT. Try later."

        if update.callback_query:
            await update.callback_query.edit_message_text(error_text)
        else:
            await update.message.reply_text(error_text)
        return -1

async def handle_gpt_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """"""
    logger.info("handle_gpt_message triggered!")
    try:
        user_message = update.message.text

        # show indicator about "typing"
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        # message about processing request
        processing_msg = await update.message.reply_text("🤔 Processing your request... ⏳")

        # get answer from ChatGPT
        gpt_response = await get_chatgpt_response(user_message)

        # create buttons
        keyboard = [
            [InlineKeyboardButton("💬 Ask another question", callback_data="gpt_continue")],
            [InlineKeyboardButton("🏠 Return to menu", callback_data="gpt_finish")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Delete messages about processing and send answer
        await processing_msg.delete()
        await update.message.reply_text(
            f"🤖 <b>ChatGPT response:</b>\n\n{gpt_response}",
            parse_mode='HTML',
            reply_markup=reply_markup
        )

        return WAITING_FOR_MESSAGE  # Keep the same status for the next question

    except Exception as e:
        logger.error(f"Error while processing message for ChatGPT: {e}")
        await update.message.reply_text(
            "😔 Something went wrong processing your message. Please try again or return to the main menu."
        )
        return WAITING_FOR_MESSAGE

































