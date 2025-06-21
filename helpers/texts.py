import logging

logger = logging.getLogger(__name__)

def get_main_text_menu() -> str:
    return ("👋 <b>Welcome to ChatGpt bot</b>\n\n"
        "<b>Available options</b>\n"
        "🎲 Random fact - get a random fact from AI\n"
        "💬 ChatGPT - take a talk with AI(soon)\n"
        "🌟 Chat with celebrity - take a talk with a celebrity(soon)\n"
        "🧠 Quiz - check your knowledge(soon)\n"
        "Choose option from menu to continue:"
            )

def get_user_error_message() -> str:
    return ("🛑🛑🛑 An error occurred - try later. Use 🚀 /start to follow main menu🛑🛑🛑")