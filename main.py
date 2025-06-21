import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from config import TG_BOT_TOKEN
from handlers import basic, random_fact, chatgpt_client

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    try:
        application = Application.builder().token(TG_BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", basic.start))
        application.add_handler(CommandHandler("random", random_fact.random_fact))
        application.add_handler(CommandHandler("gpt", chatgpt_client.gpt_command))

        gpt_conversation = ConversationHandler(
            entry_points=[CallbackQueryHandler(chatgpt_client.gpt_start, pattern="^gpt_client$")],
            states={
                chatgpt_client.WAITING_FOR_MESSAGE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt_client.handle_gpt_message)
                ],
            },
            fallbacks=[
                CommandHandler("start", basic.start),
                CallbackQueryHandler(basic.menu_callback, pattern="^(gpt_finish|main_menu)$")
            ],
            # per_message=True,
        )

        application.add_handler(gpt_conversation)
        application.add_handler(CallbackQueryHandler(random_fact.random_fact_callback, pattern="^random_"))
        application.add_handler(CallbackQueryHandler(basic.menu_callback))

        logger.info("Bot has started")
        application.run_polling()

    except Exception as e:
        logger.error(f"Oops... Something went wrong - {e}")

if __name__ == "__main__":
    main()

        # application.add_handler(CallbackQueryHandler(button))
        # application.run_polling()



