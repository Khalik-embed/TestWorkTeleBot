import hashlib
from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from config.config import CONFIG
from handlers.menu_processing import get_menu_content
from keyboards.inline import MenuCallBack
from lexicon import NAVIGATION, ANSWERS
from database.orm_query import (
   orm_get_question_from_faq,
   orm_get_answer_from_faq,
   orm_add_question_to_faq
)

inline_router = Router()

@inline_router.inline_query()
async def get_in(inline_query : InlineQuery, bot : Bot):

    user_text = inline_query.query
    if not user_text:
        return

    filtered_question = await get_autocompletion(text = user_text)
    answer = await get_answers(filtered_question = filtered_question)
    message_text = answer_template(
        answer = answer,
        filtered_question = filtered_question,
        in_text = user_text)

    input_content = InputTextMessageContent(message_text = message_text)
    result_id = hashlib.md5(message_text.encode()).hexdigest()

    if answer:
        item = InlineQueryResultArticle(
            input_message_content = input_content,
            id = result_id,
            description = filtered_question[0],
            title = NAVIGATION['prompt'])
    else :
        item = InlineQueryResultArticle(
            input_message_content = input_content,
            id = result_id,
            description = user_text,
            title = NAVIGATION['prompt'])
    await bot.answer_inline_query(inline_query_id = inline_query.id, results=[item])

async def get_autocompletion(text : str) -> [str]:
    questions : [str] = await orm_get_question_from_faq()
    filtered_question : [str] = [question for question in questions if text.lower()  in question.lower() ]
    return filtered_question

async def get_answers(filtered_question : list[str] | str | None) -> str:
    answer : str = []
    if filtered_question:
        filtered_question = filtered_question[0]
        answer = await orm_get_answer_from_faq(text = filtered_question)
    return answer

def answer_template(answer : list[str] | None,
                    filtered_question : list[str] | None,
                    in_text : str | None) -> str:
    if answer:
        message_text = filtered_question[0] + "\n\n" + answer[0] + "!"
    else :
        message_text = in_text + "\n\n" + ANSWERS['no_answer_to_the_question'] + "!"
    return message_text

async def set_new_question(question : str) -> None:
    await orm_add_question_to_faq(question = question)