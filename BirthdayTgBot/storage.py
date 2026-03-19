import json
import os
from config import FILE_NAME

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_birthday(user_id, name, date):
    data = load_data()
    user_id = str(user_id)

    if user_id not in data:
        data[user_id] = []
    
    data[user_id].append({
        "name": name,
        "date": date
    })

    save_data(data)
    return True

def get_user_birthdays(user_id):
    data = load_data()
    user_id = str(user_id)
    result = data.get(user_id, [])
    
    if not isinstance(result, list):
        return []
    
    return result

def delete_birthday_by_name(user_id, name_to_delete):
    data = load_data()
    user_id = str(user_id)
    deleted_count = 0
    
    if user_id in data:
        original_length = len(data[user_id])
        data[user_id] = [b for b in data[user_id] if b['name'] != name_to_delete]
        deleted_count = original_length - len(data[user_id])
        
        if deleted_count > 0:
            save_data(data)
    
    return deleted_count

def get_all_birthdays():
    return load_data()