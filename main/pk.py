import base64
import requests
import os
from mistralai import Mistral

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None

# Path to your image
image_path = "main\\image\\unknown_2024.10.10-14.13.png"

# Getting the base64 string
base64_image = encode_image(image_path)

# Retrieve the API key from environment variables
api_key = "T3renkSMSM6FUEX1Q3JksvSrFJMElW9H"

# Specify model
model = "pixtral-12b-2409"

# Initialize the Mistral client
client = Mistral(api_key=api_key)

message = """На картинке представлен браузер с сайтом, на котором проходится тест. Необходимо, чтобы ты сказал, какой вопрос был задан и какой ответ выбран.
Вопрос идёт между текстом "Вопрос №" и вариантами ответа. Не изменяй слова и не добавляй свои! Цитируй вопрос слово в слово, буква в букву, прям как написано на картинке.
Ответ, который был выбран, помечается синим кружочком слева от текста.
От тебя я ожидаю такой формат ответа, отвечай только так, не отклоняйся от формата:
"
Вопрос: вопрос
Вариант ответа: ответ
"
"""

# Define the messages for the chat
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": message
            },
            {
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_image}" 
            }
        ]
    }
]

# Get the chat response
chat_response = client.chat.complete(
    model=model,
    messages=messages
)

# Print the content of the response
print(chat_response.choices[0].message.content)