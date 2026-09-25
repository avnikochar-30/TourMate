from deep_translator import GoogleTranslator

def translate(text, dest_lang):

    try:
        return GoogleTranslator(source='auto', target=dest_lang).translate(text)
    except:
        return text