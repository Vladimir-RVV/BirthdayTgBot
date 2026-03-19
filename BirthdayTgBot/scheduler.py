import asyncio
from datetime import datetime
import storage

async def check_birthdays(bot):
    """Проверяет и отправляет напоминания о днях рождениях"""
    print("⏰ Планировщик напоминаний запущен")
    
    while True:
        now = datetime.now()
        
        if now.hour == 9 and now.minute == 0:
            today = now.strftime("%d.%m")
            print(f"🔍 Проверяю день {today}...")
            
            try:
                all_data = storage.get_all_birthdays()
                sent_count = 0
                
                for user_id_str, birthdays in all_data.items():
                    user_id = int(user_id_str)
                    today_birthdays = []
                    
                    for b in birthdays:
                        if b['date'] == today:
                            today_birthdays.append(b)
                    
                    if today_birthdays:
                        if len(today_birthdays) == 1:
                            b = today_birthdays[0]
                            message = (
                                f"🎉 **Сегодня день рождения!** 🎉\n\n"
                                f"👤 {b['name']}\n\n"
                                f"✨ Не забудьте поздравить! ✨"
                            )
                        else:
                            message = "🎉 **Сегодня дни рождения празднуют:** 🎉\n\n"
                            for b in today_birthdays:
                                message += f"• {b['name']}\n"
                            message += "\n✨ Поздравляем! ✨"
                        
                        try:
                            await bot.send_message(user_id, message, parse_mode="Markdown")
                            sent_count += 1
                            print(f"✅ Отправлено напоминание пользователю {user_id}")
                        except Exception as e:
                            print(f"❌ Ошибка отправки пользователю {user_id}: {e}")
                
                if sent_count > 0:
                    print(f"📨 Отправлено {sent_count} уведомлений")
                else:
                    print("😴 Сегодня нет дней рождения")
               
                await asyncio.sleep(60)
                
            except Exception as e:
                print(f"❌ Ошибка в планировщике: {e}")

        await asyncio.sleep(60)