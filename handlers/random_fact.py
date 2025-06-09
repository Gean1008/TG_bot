import logging
from PIL.SpiderImagePlugin import loadImageSeries
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from handlers.basic import start_menu_again
from services.openai_client import get_random_fact

logger = logging.getLogger(__name__)


async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """"""
    try:
        loading_msg = await update.message.reply_text("🎲 Generating fact ...⏳")
        fact = await get_random_fact()
        keyboard = [
            [InlineKeyboardButton("🎲 Want another one!",callback_data="random_more")],
            [InlineKeyboardButton("🏠 End", callback_data="random_finish")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await loading_msg.edit_text(
            f"🧠 <b>Interesting fact:</b>\n\n{fact}",
            parse_mode="HTML",
            reply_markup=reply_markup
        )

    except Exception as e:
        logger.error(f"Error trying generate random fact from OpenAI: {e}")
        await update.message.reply_text("🤔 Unfortunately Chat can't generate fact right now! Try latter!")

async def random_fact_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """"""
    query = update.callback_query
    await query.answer()

    if query.data == "random_more":
        try:
            await query.edit_message_text("🎲 Generating fact ...⏳")

            fact = await get_random_fact()
            keyboard = [
                [InlineKeyboardButton("🎲 Want another one!", callback_data="random_more")],
                [InlineKeyboardButton("🏠 End", callback_data="random_finish")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                f"🧠 <b>Interesting fact:</b>\n\n{fact}",
                parse_mode="HTML",
                reply_markup=reply_markup
            )

        except Exception as e:
            logger.error(f"Error trying generate random fact from OpenAI: {e}")
            await query.edit_message_text(
                "😔 Unfortunately Chat can't generate fact right now! Try latter!"
                "Use /start to return menu."
            )

    elif query.data == "random_finish":
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
            parse_mode="HTML",
            reply_markup=reply_markup
        )

    elif query.data == "random_fact":
        try:
            await query.edit_message_text("🎲 Generating fact ...⏳")

            fact = await get_random_fact()
            keyboard = [
                [InlineKeyboardButton("🎲 Want another one!", callback_data="random_more")],
                [InlineKeyboardButton("🏠 End", callback_data="random_finish")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                f"🧠 <b>Interesting fact:</b>\n\n{fact}",
                parse_mode="HTML",
                reply_markup=reply_markup
            )
        except Exception as e:
            logger.error(f"Error trying generate random fact from OpenAI: {e}")
            await query.edit_message_text(
                "Unfortunately Chat can't generate fact right now! Try latter!"
                "Use /start to return menu."
            )

        # await start_menu_again(query)
