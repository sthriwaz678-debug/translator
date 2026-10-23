import speech_recognition as sr
import requests
from gtts import gTTS
from playsound import playsound
import os
import uuid

def speak(text,lang='hi'):
    print('speaking...')
    filename = f'voice_{uuid.uuid4()}.mp3'
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone()as source:
        print('pls speak now in english...')
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print('recording speech...')
        text = recognizer.recognize_google(audio, language= 'en-US')
        print(f'you said: {text}')
        return text

    except sr.UnknownValueError:
        print('could not understand the audio')
    except sr.RequestsError as e:
        print(f'api error: {e}')

    return ""

def translate_text(text,target_language='hi'):
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client' : 'gtx',
            'sl' : 'en',
            'tl' :target_language,
            'dt' : 't',
            'q' : text
        }
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        translated = result[0][0][0]
        print(f'translated text: {translated}')
        return translated
    except Exception as e :
        print('translation failed:', e)
        return text
def display_language_options():
    print('\n choose translation language')

    print('1.German (de)')
    print('2. spanish')
    print('3. french')
    print('4. italian')
    print('5. portuguese')
    print('6. russian')
    print('7. chinese')
    print('8. japanese')
    print('9. arabic')
    print('10. urdu')
    choice = input('enter your choice (1-10): ')
    language_map = {
    '1': 'de',
    '2': 'es',
    '3': 'fr',
    '4': 'it',
    '5': 'pt',
    '6': 'ru',
    '7': 'zh-CN',
    '8': 'ja',
    '9': 'ar',
    '10': 'ur'
         }
    return language_map.get(choice, 'hi')
def main():
    while True:
            target_language = display_language_options()
            original_text = speech_to_text()
            if original_text:
                translated_text = translate_text(original_text, target_language)
                speak(translated_text, lang=target_language)
                print(f'Translated text: {translated_text}')
if __name__ == "__main__":
    main()
           