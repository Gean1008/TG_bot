import asyncio
import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.openai_client import generate_quiz_themes, generate_question, generate_answers_for_question, verify_answer_AI
from helpers.keyboards import get_buttons_for_themes,get_difficulty_buttons, get_answers_buttons, get_main_menu_keyboard, continue_quiz_exit
from helpers.texts import get_main_text_menu,get_user_error_message

from pathlib import Path

logger = logging.getLogger(__name__)

async def start_quiz_with_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        context.user_data["correct_quiz_answers"] = 0
        context.user_data["wrong_quiz_answers"] = 0
        user_id = update.effective_user.id

        quiz_themes_raw = await generate_quiz_themes()
        quiz_themes = [
            line.strip("1234567890.- ").strip()
            for line in quiz_themes_raw.splitlines()
            if line.strip()
        ]
        logger.info(f"📋 Raw themes from OpenAI: {quiz_themes_raw}")
        context.user_data["quiz_themes"] = quiz_themes

        if type(quiz_themes) is list:
            await query.answer()

        await query.message.edit_text(f"<b>Choose theme</b> - \n\n ", parse_mode='HTML', reply_markup=get_buttons_for_themes(quiz_themes))
    except Exception as e:
        logger.error(f"🛑🛑🛑An error occurred while AI generated response to user - {e}🛑🛑🛑")
        await query.message.edit_text(get_user_error_message())

async def generate_theme_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        query = update.callback_query
        await query.answer()

        data = query.data

        theme_index = int(data.replace("quiz_theme_", ""))
        theme_list = context.user_data.get("quiz_themes", [])

        if 0 <= theme_index < len(theme_list):
            theme = theme_list[theme_index]
            context.user_data["theme_selected"] = theme
            await query.message.edit_text(
                f"<b>You've selected - {theme}. Great choice</b>\n\n"
                "<b>Select question difficulty</b>\n" ,parse_mode='HTML', reply_markup=get_difficulty_buttons())
        else:
            await query.message.edit_text("⚠️ Invalid theme selected")

    except Exception as e:
        logger.error(f"🛑🛑🛑An error occurred while AI generated response to user - {e}🛑🛑🛑")
        await query.message.edit_text(get_user_error_message())

async def generate_question_by_difficulty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        difficulty = query.data.replace("difficulty_", "")
        theme = context.user_data.get("theme_selected")
        logger.info(f"Theme - {theme}, difficulty - {difficulty}")

        question = await generate_question(theme, difficulty)
        logger.info(f"Question - {question}")
        context.user_data["quiz_question"] = question

        raw_answers = await generate_answers_for_question(question)
        answers = [
            line.strip("1234567890.- ").strip()
            for line in raw_answers.splitlines()
            if line.strip()
        ]
        logger.info(f"Answers - {answers}")

        correct_answers = context.user_data.get("correct_quiz_answers")
        wrong_answers = context.user_data.get("wrong_quiz_answers")

        await query.message.edit_text(
            f"<b>Correct answers - {correct_answers}.     Wrong answers - {wrong_answers}.</b>\n\n"
            f"<b>{question}</b>",
            reply_markup=get_answers_buttons(answers),
            parse_mode='HTML'
        )

    except Exception as e:
        logger.error(f"🛑🛑🛑An error occurred while AI generated question by difficulty - {e}🛑🛑🛑")
        await query.message.edit_text(get_user_error_message())


async def verify_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        question = context.user_data.get("quiz_question")
        answer = query.data.replace("question_answer_","")

        result = await verify_answer_AI(question, answer)

        logger.info(result)
        if result is True:
            context.user_data["correct_quiz_answers"] +=1
            await query.edit_message_text("Congratulations!")

            await asyncio.sleep(3)

            await query.edit_message_text(
                "Choose option:",
                reply_markup=continue_quiz_exit()
            )
        else:
            context.user_data["wrong_quiz_answers"] += 1
            await query.edit_message_text("Wrong answer!")

            await asyncio.sleep(3)

            await query.edit_message_text(
                "Choose option:",
                reply_markup=continue_quiz_exit()
            )

    except Exception as e:
        logger.error(f"🛑🛑🛑An error occurred while AI verified answer - {e}🛑🛑🛑")
        await query.message.edit_text(get_user_error_message())

async def quiz_query_handler(update: Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        if query.data == "continue_quiz":
            await generate_question_by_difficulty(update, context)
        elif query.data == "quiz_exit":
            await quiz_exit(update, context)
        elif query.data == "select_quiz_theme":
            await choose_new_quiz_theme(update,context)

    except Exception as e:
        logger.error(f"🛑🛑🛑An error occurred in quiz query handler - {e}🛑🛑🛑")
        await query.message.edit_text(get_user_error_message())

async def quiz_exit(update: Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        context.user_data["quiz_question"] = None
        context.user_data["theme_selected"] = None

        correct_answers = context.user_data.get("correct_quiz_answers")
        wrong_answers = context.user_data.get("wrong_quiz_answers")

        await query.edit_message_text(
            f"<b>QUIZ finished. TOTAL CORRECT ANSWERS - {correct_answers}. WRONG ANSWERS - {wrong_answers}</b>",
           parse_mode='HTML'
        )

        context.user_data["correct_quiz_answers"] = 0
        context.user_data["wrong_quiz_answers"] = 0

        await asyncio.sleep(3)

        main_text = get_main_text_menu()
        await query.edit_message_text(
            f"{main_text}",
            parse_mode='HTML',
            reply_markup=get_main_menu_keyboard()
        )
    except Exception as e:
        logger.error(f"🛑🛑🛑An error occurred in quiz exit - {e}🛑🛑🛑")
        await query.message.edit_text(get_user_error_message())


async def choose_new_quiz_theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        quiz_themes_raw = await generate_quiz_themes()
        quiz_themes = [
            line.strip("1234567890.- ").strip()
            for line in quiz_themes_raw.splitlines()
            if line.strip()
        ]
        logger.info(f"📋 Raw themes from OpenAI: {quiz_themes_raw}")
        context.user_data["quiz_themes"] = quiz_themes

        if type(quiz_themes) is list:
            await query.answer()

        await query.message.edit_text(f"<b>Choose theme</b> - \n\n ", parse_mode='HTML', reply_markup=get_buttons_for_themes(quiz_themes))
    except Exception as e:
        logger.error(f"🛑🛑🛑An error occurred while AI generated response to user - {e}🛑🛑🛑")
        await query.message.edit_text(get_user_error_message())