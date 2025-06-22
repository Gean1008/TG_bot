from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

logger = logging.getLogger(__name__)

def get_main_menu_keyboard():
    buttons = [
            [InlineKeyboardButton("🎲 Random fact", callback_data="random_fact")],
            [InlineKeyboardButton("💬 Chat with AI", callback_data="chat_gpt")],
            [InlineKeyboardButton("🌟 Chat with celebrity", callback_data="chat_with_celebrity")],
            [InlineKeyboardButton("🧠 Quiz", callback_data="start_quiz_with_user")],
            [InlineKeyboardButton("🎧 Playlist generator", callback_data="playlist_gen")],
            [InlineKeyboardButton("📄 Assistant in writing CV", callback_data="generate_cv")]
            # [InlineKeyboardButton("🎥 Suggest an interesting movie for the evening (soon)", callback_data="movie_soon")]
    ]
    return InlineKeyboardMarkup(buttons)

def get_one_more_fact_keyboard():
    buttons = [
            [InlineKeyboardButton("🔁 One more fact", callback_data="random_more")],
            [InlineKeyboardButton("❌ END", callback_data="random_exit")]
    ]
    return InlineKeyboardMarkup(buttons)

def get_buttons_for_themes(list):
    buttons = [
            [InlineKeyboardButton(f"🧠  {value} ", callback_data=f"quiz_theme_{index}")]
        for index, value in enumerate(list)
    ]
    return InlineKeyboardMarkup(buttons)

def get_difficulty_buttons():
    buttons = [
        [InlineKeyboardButton("🟢 Easy", callback_data="difficulty_easy")],
        [InlineKeyboardButton("🟡 Medium", callback_data="difficulty_medium")],
        [InlineKeyboardButton("🔴 Hard", callback_data="difficulty_hard")]
    ]
    return InlineKeyboardMarkup(buttons)

def get_answers_buttons(list):
    buttons = [
        [InlineKeyboardButton(f"{index}. {value}", callback_data=f"question_answer_{value}")]
        for index, value in enumerate(list)
    ]
    return InlineKeyboardMarkup(buttons)

def continue_quiz_exit():
    buttons = [
        [InlineKeyboardButton("🔁 One more question", callback_data="continue_quiz")],
        [InlineKeyboardButton("🔁 Select other quiz theme", callback_data="select_quiz_theme")],
        [InlineKeyboardButton("❌ END", callback_data="quiz_exit")]
    ]
    return InlineKeyboardMarkup(buttons)