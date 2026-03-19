from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Добавить день рождения"), KeyboardButton(text="❌ Удалить день рождения")],
            [KeyboardButton(text="📋 Мои дни рождения")],
            [KeyboardButton(text="❓ Помощь")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_birthday_list_keyboard(birthdays):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for i, b in enumerate(birthdays):
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"❌ {b['date']} - {b['name']}",
                callback_data=f"del_{i}"
            )
        ])
    return keyboard

def get_cancel_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ]
    )
    return keyboard