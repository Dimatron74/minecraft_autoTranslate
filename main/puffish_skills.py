import json
from deep_translator import GoogleTranslator
from pathlib import Path
import os



def translate_text(text, target_lang, original_language):
    """
    Переводит текст на указанный язык с использованием GoogleTranslator.
    """
    translator = GoogleTranslator(source=original_language, target=target_lang)
    translated_text = translator.translate(text)
    return translated_text

def translate_fields(item, target_lang, original_language):
    """
    Рекурсивно переводит поля 'title' и 'description' в JSON объекте.
    """
    if isinstance(item, dict):
        for key, value in item.items():
            if key == 'title':
                item[key] = translate_text(value, target_lang, original_language)
            elif key == 'description':
                item[key] = translate_text(value, target_lang, original_language)
            elif isinstance(value, (dict, list)):
                item[key] = translate_fields(value, target_lang, original_language)
    elif isinstance(item, list):
        for i, value in enumerate(item):
            item[i] = translate_fields(value, target_lang, original_language)
    return item

def translate_json_file(input_file_path, output_file_path, target_lang, original_language):
    """
    Переводит поля 'title' и 'description' в JSON файле.
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            data = json.load(input_file)
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в файле {input_file_path}: {e}")
        return

    translated_data = translate_fields(data, target_lang, original_language)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(translated_data, output_file, ensure_ascii=False, indent=4)

def process_file(file_path, lang_to, original_language, file_index, total_files, base_output_dir):
    """
    Обрабатывает один JSON файл, подготавливает целевую папку для переведённого файла и вызывает функцию перевода
    """
    quest_path = Path(file_path)
    relative_path = quest_path.relative_to(base_output_dir)
    target_translated = base_output_dir.parent / (base_output_dir.name + '_translated')
    translated_path = target_translated / relative_path

    if not os.path.isdir(target_translated):
        os.mkdir(target_translated)

    translated_path.parent.mkdir(parents=True, exist_ok=True)

    print(f'Файл {file_index}/{total_files}: Подготовка к обработке файла {quest_path}')
    print(f'\tПереводится файл: {quest_path}')
    translate_json_file(file_path, translated_path, lang_to, original_language)
    print(f'\tПеревод файла {quest_path} завершён.')

def process_files_in_directory(directory_path, lang_to = 'ru', original_language = 'en'):
    """
    Обрабатывает все JSON файлы в указанной директории и её поддиректориях.
    """
    # Использование pathlib для рекурсивного поиска файлов с расширением .json
    directory_path = Path(directory_path)
    json_files = list(directory_path.rglob("*.json"))
    total_files = len(json_files)

    print(f"Всего файлов с расширением .json в папке: {total_files}")

    # Перебор файлов с расширением .json
    for file_index, file_path in enumerate(json_files, start=1):
        process_file(file_path, lang_to, original_language, file_index, total_files, directory_path)

    print("Перевод всех файлов окончен.")



input_json_file = 'main\\files\\originals' # Папка, где искать оригинальные файлы для перевода
target_language = 'ru' # Язык, на который нужно перевести файлы
original_language = 'en' # Язык оригинальных файлов (можно установить auto, если языков несколько)
process_files_in_directory(input_json_file, target_language, original_language) # Вызов основной программы

