from mistralai import Mistral
from mistralai.models import UserMessage
import os
import re
from pathlib import Path



def run_mistral(user_message, model_choice, file_path, directory_path_rus, file_index, total_files):
    if model_choice == 1:
        model="mistral-large-latest" #умнее
    elif model_choice == 2:
        model="pixtral-12b-2409" #бесплатна и быстра
    else:
        raise ValueError("Неверный выбор модели. Пожалуйста, выберите 1 или 2.")
    
    api_key = "T3renkSMSM6FUEX1Q3JksvSrFJMElW9H"
    client = Mistral(api_key=api_key)
    
    messages = [
        {
            "role": "user", "content": user_message
        }
    ]
    chat_response = client.chat.complete(
        model=model,
        messages=messages,
    )
    filename = os.path.basename(file_path)
    with open(f"{directory_path_rus}\\{filename}", 'w', encoding='utf-8') as output_file:
        rawanswer = chat_response.choices[0].message.content
        lines = rawanswer.splitlines()
        if len(lines) > 2:
            lines = lines[1:-1]
        else:
            lines = []  # Если в файле меньше двух строк, очистим список

        clearanswer = '\n'.join(lines)
        output_file.write(clearanswer)

    print(f"Файл {file_index}/{total_files}: Файл {file_path} переведён успешно.")
    return



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

def process_file(file_path, lang_to, file_index, total_files):
    quest_path = Path(file_path)
    target_translated = quest_path.parent.with_name(quest_path.parent.name + '_translated')
    if not os.path.isdir(target_translated):
        os.mkdir(target_translated)
    print(f'Файл {file_index}/{total_files}: Подготовка к обработке файла {quest_path}')
    with open(f'{quest_path}'.replace("\\", "/"), encoding='utf-8') as file:
        # Создаем путь для переведенного файла
        translated_path = target_translated / quest_path.name
        translated_path.parent.mkdir(parents=True, exist_ok=True)
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
        process_file(file_path, lang_to, file_index, total_files)

    print("Перевод всех файлов окончен.")


directory_path = 'main\\new_try'
lang_to = 'ru'
process_files_in_directory(directory_path, lang_to)







# def run_mistral(user_message, model_choice, file_path, directory_path_rus, file_index, total_files):
#     if model_choice == 1:
#         model="mistral-large-latest" #умнее
#     elif model_choice == 2:
#         model="pixtral-12b-2409" #бесплатна и быстра
#     else:
#         raise ValueError("Неверный выбор модели. Пожалуйста, выберите 1 или 2.")
    
#     api_key = "T3renkSMSM6FUEX1Q3JksvSrFJMElW9H"
#     client = Mistral(api_key=api_key)
    
#     messages = [
#         {
#             "role": "user", "content": user_message
#         }
#     ]
#     chat_response = client.chat.complete(
#         model=model,
#         messages=messages,
#     )
#     filename = os.path.basename(file_path)
#     with open(f"{directory_path_rus}\\{filename}", 'w', encoding='utf-8') as output_file:
#         rawanswer = chat_response.choices[0].message.content
#         lines = rawanswer.splitlines()
#         if len(lines) > 2:
#             lines = lines[1:-1]
#         else:
#             lines = []  # Если в файле меньше двух строк, очистим список

#         clearanswer = '\n'.join(lines)
#         output_file.write(clearanswer)

#     print(f"Файл {file_index}/{total_files}: Файл {file_path} переведён успешно.")
#     return

# def process_file(file_path, directory_path_rus, file_index, total_files):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         content = file.read()
#     retrieved_chunk = content
#     prompt = f"""
#     Информация из файла, который используется в игре, приведена ниже.

#     {retrieved_chunk}

#     Формат файла snbt.
#     Переведи строчки с английского на русский, которые увидит игрок.
#     Обычно эти строчки являются description:, title:, subtitle:.
#     Также у текста в строчках есть символ &, а после этого символа обычно идёт один символ-модификатор - это не переводи, не учитывай.
#     Остальные строчки оставь без изменения.
#     Ответ оформи в таком же формате snbt, в котором и была предоставлена информация.
#     Не применяй никакого дополнительного форматирования своего ответа.
#     Дополнительная информация по переводу:
#     mods, mod и его произвольные переводи как моды, мод и так далее.
#     questbook переводи как книга заданий.
#     """
#     run_mistral(prompt, 2, file_path, directory_path_rus, file_index, total_files)

# def process_files_in_directory(directory_path, directory_path_rus):
#     # Перебор файлов в папке
#     files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
#     total_files = len(files)

#     print(f"Всего файлов в папке: {total_files}")

#     # Перебор файлов в папке
#     for file_index, filename in enumerate(files, start=1):
#         file_path = os.path.join(directory_path, filename)
#         process_file(file_path, directory_path_rus, file_index, total_files)
#     print("Перевод всех файлов окончен.")

# directory_path = 'main\\files'
# directory_path_rus = 'main\\files\\rus'
# process_files_in_directory(directory_path, directory_path_rus)