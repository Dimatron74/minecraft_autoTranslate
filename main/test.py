from deep_translator import YandexTranslator

translated = YandexTranslator('b1g394q49o6nsje338sk').translate(source="auto", target="en", text='Hallo, Welt')
print(f"translated text: {translated}")