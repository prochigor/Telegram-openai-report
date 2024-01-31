from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from messages import locations

location_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=locations[1]),
            KeyboardButton(text=locations[2]),
            KeyboardButton(text=locations[3]),
        ],
        [
            KeyboardButton(text=locations[4]),
            KeyboardButton(text=locations[5]),
        ]
    ],
    resize_keyboard=True
)

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Розпочнімо роботу"),
        ]
    ],
    resize_keyboard=True
)

checklist_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="+"),
            KeyboardButton(text="-"),
        ]
    ],
    resize_keyboard=True
)

comment_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Все чисто"),
            KeyboardButton(text="Залишити коментар"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

report_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Надіслати"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
