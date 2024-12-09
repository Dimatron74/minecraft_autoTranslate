import os
from deep_translator import GoogleTranslator
import re
from pathlib import Path

def translate_to(text, lang_to, src_lang='en'):
    if text == '':
        return ''
    translator = GoogleTranslator(source=src_lang, target=lang_to)
    # Найти все символы форматирования
    formatting_symbols = re.findall(r'&[a-zA-Z0-9]', text)

    # Найти все экранированные символы
    escaped_symbols = re.findall(r'\\.', text)

    # Заменить символы форматирования на уникальные метки
    placeholders_formatting = [f'PLACEHOLDER_F_{i}' for i in range(len(formatting_symbols))]
    text_with_placeholders = text
    for symbol, placeholder in zip(formatting_symbols, placeholders_formatting):
        text_with_placeholders = text_with_placeholders.replace(symbol, placeholder)

    # Заменить экранированные символы на уникальные метки
    placeholders_escaped = [f'PLACEHOLDER_E_{i}' for i in range(len(escaped_symbols))]
    for symbol, placeholder in zip(escaped_symbols, placeholders_escaped):
        text_with_placeholders = text_with_placeholders.replace(symbol, placeholder)

    # Перевести текст
    translated_text = translator.translate(text_with_placeholders)

    # Вернуть символы форматирования на место
    for symbol, placeholder in zip(formatting_symbols, placeholders_formatting):
        translated_text = translated_text.replace(placeholder, symbol)

    # Вернуть экранированные символы на место
    for symbol, placeholder in zip(escaped_symbols, placeholders_escaped):
        translated_text = translated_text.replace(placeholder, symbol)

    return translated_text

def translate_line(i, file, translated_file, lang_to):
    if file[i].strip().startswith('"{'):
        translated_file.write(file[i])
        return i + 1

    indexes = [index for index, element in enumerate(file[i]) if element == '"']
    if len(indexes) < 2:
        translated_file.write(file[i])
        return i + 1

    string = translate_to(file[i][indexes[0] + 1:indexes[-1]], lang_to)
    translated_file.write(file[i][:indexes[0] + 1] + string + file[i][indexes[-1]:])
    return i + 1

def find_and_translate(file, translated_file, lang_to):
    file = file.readlines()
    line = 0
    total_lines = len(file)
    while line < total_lines:
        if 'description: [' in file[line] and not ']' in file[line]:
            translated_file.write(file[line])
            line += 1
            while ']' not in file[line]:
                line = translate_line(line, file, translated_file, lang_to)
            translated_file.write(file[line])
            line += 1
        elif 'description: [' in file[line] and ']' in file[line]:
            line = translate_line(line, file, translated_file, lang_to)
        elif 'title:' in file[line]:
            line = translate_line(line, file, translated_file, lang_to)
        else:
            translated_file.write(file[line])
            line += 1

def process_file(file_path, lang_to, file_index, total_files, base_output_dir):
    quest_path = Path(file_path)
    relative_path = quest_path.relative_to(base_output_dir)
    target_translated = base_output_dir.parent / (base_output_dir.name + '_translated')
    translated_path = target_translated / relative_path

    if not os.path.isdir(target_translated):
        os.mkdir(target_translated)
    
    translated_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f'Файл {file_index}/{total_files}: Подготовка к обработке файла {quest_path}')
    with open(f'{quest_path}'.replace("\\", "/"), encoding='utf-8') as file:
        with open(translated_path, 'w', encoding='utf-8') as translated_file:
            print(f'\tПереводится файл: {quest_path}')
            find_and_translate(file, translated_file, lang_to)
            print(f'\tПеревод файла {quest_path} завершён.')

def process_files_in_directory(directory_path, lang_to):
    # Использование pathlib для рекурсивного поиска файлов с расширением .snbt
    directory_path = Path(directory_path)
    snbt_files = list(directory_path.rglob("*.snbt"))
    total_files = len(snbt_files)

    print(f"Всего файлов с расширением .snbt в папке: {total_files}")

    # Перебор файлов с расширением .snbt
    for file_index, file_path in enumerate(snbt_files, start=1):
        process_file(file_path, lang_to, file_index, total_files, directory_path)

    print("Перевод всех файлов окончен.")


directory_path = 'main\\files\\originals' # Папка, где искать оригинальные файлы для перевода
lang_to = 'ru' # Язык, на который нужно перевести файлы
process_files_in_directory(directory_path, lang_to) # Вызов основной программы