from os import replace
from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from datetime import datetime

import storage
from keyboards import get_main_keyboard, get_birthday_list_keyboard, get_cancel_keyboard
from my_calendar import YearlessCalendar

calendar = YearlessCalendar()
class AddBirthday(StatesGroup):
    waiting_for_name = State()
    waiting_for_date = State()


async def cmd_start(message: types.Message):
    await message.delete()
    await message.answer(
        "👋 **Привет! Я бот для напоминания о днях рождения!**\n\n"
        "🎂 Я помогу тебе не забыть поздравить друзей и близких.\n"
        "📅 Просто добавь дни рождения, и я буду напоминать о них каждый день!\n\n"
        "Используй кнопки ниже 👇",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )
    


async def help_handler(message: types.Message):
    await message.delete()
    await message.answer(
        "❓ **Как пользоваться ботом:**\n\n"
        "📅 **Добавить день рождения**\n"
        "• Нажми кнопку «Добавить день рождения»\n"
        "• Введи имя человека\n"
        "• Выбери дату в календаре\n\n"
        "📋 **Мои дни рождения**\n"
        "• Показывает список всех добавленных дней рождения\n"
        "• Можно удалить запись, нажав на кнопку\n\n"
        "⏰ **Напоминания**\n"
        "• Я проверяю каждый день в 9:00 утра\n"
        "• Если сегодня чей-то день рождения - пришлю уведомление",
        parse_mode="Markdown"
    )
    


async def add_start(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer(
        "👤 **Введите имя человека:**\n\n"
        "Например: `Анна Смирнова`\n\n"
        "Или нажмите кнопку ниже для отмены",
        parse_mode="Markdown",
        reply_markup=get_cancel_keyboard()
    )
    
    await state.set_state(AddBirthday.waiting_for_name)


async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    await message.delete()
    
    if len(name) < 2:
        await message.answer("❌ Имя слишком короткое. Введите ещё раз:")
        return
    
    await state.update_data(name=name)
    
    await message.answer(
        "📅 **Выберите дату рождения:**\n\n"
        "Используйте кнопки календаря для навигации",
        parse_mode="Markdown",
        reply_markup=await calendar.start_calendar()
    )
    await state.set_state(AddBirthday.waiting_for_date)


async def process_calendar_callback(callback: types.CallbackQuery, state: FSMContext):
    
    result = await calendar.process_selection(callback.data)
    
    if result[0] is False and result[1] is not None:
        # Навигация по месяцам
        year, month = result[1]
        await callback.message.edit_reply_markup(
            reply_markup=await calendar.start_calendar(year, month)
        )
        
    elif result[0] is True:
        # Выбрана дата
        selected_date = result[1]
        formatted_date = selected_date.strftime("%d.%m")
        
        data = await state.get_data()
        name = data.get('name')
        
        storage.add_birthday(
            user_id=callback.from_user.id,
            name=name,
            date=formatted_date
        )
        
        await callback.message.edit_text(
            f"✅ **День рождения добавлен!**\n\n"
            f"👤 {name}\n"
            f"📅 {formatted_date}\n\n"
            f"Я напомню о нём в нужный день! 🎂",
            parse_mode="Markdown"
        )
        await state.clear()
    
    await callback.answer()





async def cancel_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Добавление отменено")
    await callback.answer()


async def show_list(message: types.Message):
    await message.delete()
    birthdays = storage.get_user_birthdays(message.from_user.id)
    
    if not birthdays:
        await message.answer(
            "📭 **У тебя пока нет дней рождения**\n\n"
            "Нажми «📅 Добавить день рождения», чтобы начать!",
            parse_mode="Markdown"
        )
        return
    

    birthdays.sort(key=lambda x: x['date'][3:] + x['date'][:2])
    
    months = {
        "01": "Январь", "02": "Февраль", "03": "Март", "04": "Апрель",
        "05": "Май", "06": "Июнь", "07": "Июль", "08": "Август",
        "09": "Сентябрь", "10": "Октябрь", "11": "Ноябрь", "12": "Декабрь"
    }
    
    text = "📋 **Твои дни рождения:**\n\n"
    current_month = ""
    
    for b in birthdays:
        month_num = b['date'][3:]
        month_name = months.get(month_num, month_num)
        
        if month_name != current_month:
            current_month = month_name
            text += f"\n**{month_name}**\n"
        
        text += f"• {b['date']} - {b['name']}\n"
    
    await message.answer(text, parse_mode="Markdown")


async def delete_list(message: types.Message):
    await message.delete()
    birthdays = storage.get_user_birthdays(message.from_user.id)
    if birthdays:
        keyboard = get_birthday_list_keyboard(birthdays)
        await message.answer(
            "🗑 **Выберите запись для удаления:**",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    else:
        await message.answer(
            "😴 Ваш список дней рождений пуст",
            parse_mode="Markdown",
            )

async def delete_callback(callback: types.CallbackQuery):
    try:
        # Получаем индекс из callback_data (формат: "del_0", "del_1" и т.д.)
        index = int(callback.data.split('_')[1])
        user_id = callback.from_user.id
        
        # Получаем все birthdays пользователя
        birthdays = storage.get_user_birthdays(user_id)
        
        # Проверяем, что индекс существует
        if 0 <= index < len(birthdays):
            birthday_to_delete = birthdays[index]
            name = birthday_to_delete['name']
            date = birthday_to_delete['date']
            
            # Удаляем запись
            storage.delete_birthday_by_name(user_id, name)  # Удаляем все с таким именем
            
            await callback.message.edit_text(
                f"✅ Удалено: {name} - {date}"
            )
        else:
            await callback.message.edit_text("❌ Запись не найдена")
            
    except (ValueError, IndexError):
        await callback.message.edit_text("❌ Ошибка при удалении")
    
    await callback.answer()


# Регистрация всех обработчиков
def register_handlers(dp):
    # Команды
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(help_handler, F.text == "❓ Помощь")
    dp.message.register(add_start, F.text == "📅 Добавить день рождения")
    dp.message.register(show_list, F.text == "📋 Мои дни рождения")
    dp.message.register(delete_list, F.text == "❌ Удалить день рождения")
    
    # FSM состояния
    dp.message.register(process_name, AddBirthday.waiting_for_name)
    
    # Callback запросы
    dp.callback_query.register(process_calendar_callback, F.data.startswith("calendar:"))
    dp.callback_query.register(cancel_callback, F.data == "cancel")
    dp.callback_query.register(delete_callback, F.data.startswith("del_"))