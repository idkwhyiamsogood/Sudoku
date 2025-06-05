import json
from pathlib import Path

def get_value_from_json(file_path: str, key_path: str):
    file = Path(file_path)
    if not file.exists():
        return f'Файл {file_path} не найден.'

    with file.open(encoding='utf-8') as f:
        data = json.load(f)

    keys = key_path.split('.')
    value = data
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return f'Путь {key_path} не найден в {file_path}'

def change_json_value(file_path: str, key_path: str, new_value):
    if not get_value_from_json("app/settings.json", "Settings.Collect Statistics"):
        return

    file = Path(file_path)
    if not file.exists():
        return f'Файл {file_path} не найден.'

    with file.open(encoding='utf-8') as f:
        data = json.load(f)

    keys = key_path.split('.')
    value = data
    
    try:
        for key in keys[:-1]:
            value = value[key]
        value[keys[-1]] = new_value
    except (KeyError, TypeError):
        return f'Путь {key_path} не найден в {file_path}'

    with file.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return f'Значение по пути {key_path} успешно изменено на {new_value}.'

def get_file(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return file.read()