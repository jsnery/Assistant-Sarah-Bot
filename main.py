import speech_recognition as sr # Biblioteca de reconhecimento de fala
from vosk import Model, KaldiRecognizer
# from gtts import gTTS, lang
# from playsound import playsound
import pyttsx3
import pyaudio
import requests
from os import system

# def read_audio(text='Não endtendi!', lang='pt-br'):
#     tts = gTTS(text=text, lang = lang, slow=False)
#     filename = 'read_audio.mp3'
#     tts.save(filename)
#     playsound(filename)

def read_audio(text='Não endtendi!', lang='pt-br'):
    pyttsx3.speak(text)
    
def check_online():
    try:
        requests.get('https://www.google.com')
        return True
    except requests.exceptions.ConnectionError:
        return False

def speech(): # Reconhecedor de Fala Online | import speech_recognition as sr
    def speech_vosk(): # Reconhecedor de Fala Online | from vosk import Model, KaldiRecognizer | import pyaudio
        model = Model('model') # Carregar o Modelo de Idioma
        system('cls')
        recognizer = KaldiRecognizer(model, 16000) # Reconhecedor de Voz

        # Reconhecer Microfone
        capture = pyaudio.PyAudio() # Capitura o Mic
        stream = capture.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream() # Iniciar reconhecimento

        while True:
            data = stream.read(4096) # Lendo os dados do mic | buffer de 4mb

            if recognizer.AcceptWaveform(data): # Se identificar a voz
                speech = eval(recognizer.Result())['text']
                if speech == '':
                    system('cls')
                    print("Ouvindo...")
                    continue
                return speech
        
    recognition = sr.Recognizer() # Reconhecedor de Voz
    microphone = sr.Microphone() # Microfone
    with microphone as mic: # Abrir|Ativar Microfone
        audio = recognition.listen(mic) # Capitando audio do Microfone
        while True:
            try:
                talk = recognition.recognize_google(audio, language="pt-BR") # Retrono em str
                break
            except sr.UnknownValueError:
                system('cls')
                talk = speech_vosk()
                break
        system('cls')
        return talk
    




print(speech())
read_audio('Olá, meu nome é Sara!')


