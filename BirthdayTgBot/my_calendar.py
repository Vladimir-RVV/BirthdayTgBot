from aiogram_calendar import SimpleCalendar
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import calendar
from typing import Tuple, Optional

class YearlessCalendar:
     async def start_calendar(
        self,
        year: int = None,
        month: int = None
    ) -> InlineKeyboardMarkup:
        
        now = datetime.now()
        if year is None:
            year = now.year
        if month is None:
            month = now.month
        
        month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                      "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        
        week_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        
        keyboard = []
        
        
        keyboard.append([
            InlineKeyboardButton(
                text=f"📅 {month_names[month-1]}",
                callback_data="ignore"
            )
        ])
        
        # Навигация по месяцам
        keyboard.append([
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"calendar:prev:{year}:{month}"
            ),
            InlineKeyboardButton(
                text=" ",
                callback_data="ignore"
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"calendar:next:{year}:{month}"
            )
        ])
        
        # Дни недели
        week_row = []
        for day in week_days:
            week_row.append(
                InlineKeyboardButton(text=day, callback_data="ignore")
            )
        keyboard.append(week_row)
        
        # Числа месяца
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            row = []
            for day in week:
                if day == 0:
                    row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
                else:
                    row.append(
                        InlineKeyboardButton(
                            text=str(day),
                            callback_data=f"calendar:day:{year}:{month}:{day}"
                        )
                    )
            keyboard.append(row)
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
     async def process_selection(
        self, 
        callback_data: str
       ) -> Tuple[bool, Optional[datetime]]:
       
        if not callback_data.startswith("calendar:"):
            return False, None
        
        parts = callback_data.split(":")
        if len(parts) < 2:
            return False, None
        
        action = parts[1]
        
        if action == "prev":
            year = int(parts[2])
            month = int(parts[3])
            
            if month == 1:
                month = 12
                year -= 1
            else:
                month -= 1
            
            return False, (year, month)
            
        elif action == "next":
            year = int(parts[2])
            month = int(parts[3])
            
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
            
            return False, (year, month)
            
        elif action == "day":
            year = int(parts[2])
            month = int(parts[3])
            day = int(parts[4])
            
            selected_date = datetime(year, month, day)
            return True, selected_date
        
        return False, None