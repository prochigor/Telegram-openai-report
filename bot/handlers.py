import os

import openai
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

from db import user_is_exist, add_user, create_table
from keyboards import (
    location_keyboard,
    checklist_keyboard,
    comment_keyboard,
    report_keyboard,
    start_keyboard,
)
from messages import locations, checklist_question, checklist_clear

load_dotenv()
create_table()

# init bot
API_TOKEN = os.environ.get("TG_API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# saving selected locations and user checklist
user_data = {}


# Say hello at the startup
@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    user_id = message.from_user.id

    existing_user = user_is_exist(user_id)

    if existing_user is None:
        add_user(user_id)
        await message.answer("Привіт! Почнімо працювати.", reply_markup=start_keyboard)
    else:
        await message.answer("Давай продовжемо", reply_markup=start_keyboard)


# Start working with bot
@dp.message_handler(Text(equals=["Розпочнімо роботу"]))
async def start_working(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {"location": [], "checklist": {}}
    await message.answer("Обери локацію", reply_markup=location_keyboard)


# Choose location
@dp.message_handler(
    Text(equals=[locations[1], locations[2], locations[3], locations[4], locations[5]])
)
async def choose_location(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]["location"] = message.text
    await message.answer(
        "Добре, а тепер заповни чек-лист", reply_markup=checklist_keyboard
    )
    user_data[user_id]["checklist"]["question"] = 0
    await do_checklist(message)


# Checklist chooses
@dp.message_handler(Text(equals=["+", "-"]))
async def do_checklist(message: types.Message):
    user_id = message.from_user.id
    checklist = user_data[user_id]["checklist"]
    location = user_data[user_id]["location"]

    # first question
    if checklist["question"] == 0:
        await message.answer(checklist_question[location][0])
        checklist["question"] += 1
        return

    # Other questions
    choice = message.text == "+"
    if checklist["question"] < 5:
        checklist[checklist_question[location][checklist["question"]]] = choice
        await message.answer(checklist_question[location][checklist["question"]])
        checklist["question"] += 1
    else:
        await message.answer(
            "Прекрасно,тепер ти можеш залишити коментар або відправити запит.",
            reply_markup=comment_keyboard,
        )


# All clear
@dp.message_handler(Text(equals=[checklist_clear[1]]))
async def add_comment(message: types.Message):
    await message.answer(
        "Давай надішлемо звіт на обробку", reply_markup=report_keyboard
    )


# Leave the commentary
@dp.message_handler(Text(equals=[checklist_clear[2]]))
async def add_comment(message: types.Message):
    user_id = message.from_user.id

    # Save the state leave commentary and request commentary
    user_data[user_id]["leave_comment"] = message.text
    await message.answer("Залиш свій коментар!")


@dp.message_handler(
    lambda message: user_data[message.from_user.id].get("leave_comment")
    == checklist_clear[2]
)
async def save_commentary(message: types.Message):
    user_id = message.from_user.id

    # Save the commentary
    user_data[user_id]["commentary"] = message.text
    user_data[message.from_user.id].pop("leave_comment")

    await message.answer(
        "Чудово, тепер можеш завантажити фото, або відправити звіт.",
        reply_markup=report_keyboard,
    )


# Handle photo upload and save link
@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def save_photo(message: types.Message):
    user_id = message.from_user.id
    photo_url = message.photo[-1].file_id
    user_data[user_id]["photo_url"] = photo_url
    await message.answer("Фотографію збережено!")


# handle and send report
@dp.message_handler(Text(equals=["Надіслати"]))
async def openai_report(message: types.Message):
    # OpenAI API key
    openai.api_key = os.environ.get("API_KEY")

    user_id = message.from_user.id
    location = user_data[user_id]["location"]
    checklist = "\n".join(
        [
            f"{item}: {status}"
            for item, status in user_data[user_id]["checklist"].items()
        ]
    )
    comment = user_data[user_id].get("commentary")
    photo_url = user_data[user_id].get("photo_url")

    # Clear data
    user_data[user_id] = {"location": [], "checklist": {}}

    report = (
        f"Проаналізуй ллокацію: {location} та визнач місце яке варто відвідати"
        f" згідно чеклисту\nЧек-лист:\n{checklist}"
    )

    if comment:
        report += f"\nКоментар: {comment}"

    if photo_url:
        report += f"\nФото: {photo_url}"

    # Send report to OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", message=[{"role": "user", "content": report}]
        )

        # Send report to user
        await message.answer(f"{response['choices'][0]['message']['content']}")
    except openai.error.RateLimitError:
        await message.answer("Кількіь запитів перевищила ліміт, вибачте за незручності")

    await welcome(message)


if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
