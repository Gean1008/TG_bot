import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler,MessageHandler,filters
from config import TG_BOT_TOKEN
from handlers import basic, random_fact,chat_with_AI,chat_with_celebrity,Quiz_handler,message_router,playlist_generator


#Adding basic configuration for log actions in console
logging.basicConfig(
    format="%(asctime)s - %(name)s -%(levelname)s -%(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    try:
        application = Application.builder().token(TG_BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", basic.start))

        application.add_handler(CommandHandler("random", random_fact.random_fact))
        application.add_handler(CallbackQueryHandler(random_fact.random_fact_callback, pattern="random_"))

        application.add_handler(CallbackQueryHandler(Quiz_handler.generate_theme_questions, pattern="quiz_theme_"))
        application.add_handler(CallbackQueryHandler(Quiz_handler.generate_question_by_difficulty, pattern="difficulty_"))
        application.add_handler(CallbackQueryHandler(Quiz_handler.verify_answer, pattern="question_answer_"))

        application.add_handler(CallbackQueryHandler(Quiz_handler.quiz_query_handler, pattern="^continue_quiz$"))
        application.add_handler(CallbackQueryHandler(Quiz_handler.quiz_query_handler, pattern="^quiz_exit$"))
        application.add_handler(CallbackQueryHandler(Quiz_handler.quiz_query_handler, pattern="^select_quiz_theme$"))

        application.add_handler(CallbackQueryHandler(playlist_generator.start_playlist_conversation, pattern="^playlist_gen"))

        application.add_handler(CallbackQueryHandler(basic.menu_callback))

        application.add_handler(MessageHandler(filters.TEXT | filters.AUDIO | filters.VOICE, message_router.message_router))

        application.add_handler(CommandHandler("exit", chat_with_AI.stop_chat_mode))

        application.add_handler(CommandHandler("exit_celebrity", chat_with_celebrity.exit_chat_with_celebrity))

        logger.info("Chat bot was successfully started")
        application.run_polling()
    except Exception as e:
        logger.info(f"An error occurred while starting bot - {e}")

if __name__  == "__main__":
    main()