import speech_recognition as sr # Biblioteca de reconhecimento de fala Online
from vosk import Model, KaldiRecognizer  # Biblioteca de reconhecimento de fala Offline
from pyttsx3 import speak as hear # Leitor de texto
import sqlite3
from pathlib import Path
from abc import ABC, abstractmethod
import pyaudio
from os import system

DIR = Path(__file__).parent / 'memory.db'

class BotStructure(ABC):

    def __init__(self) -> None:
        pass

    @property    
    @abstractmethod
    def say(self) -> str:...

    def brain(self, user_speech, DIR=DIR):

        if DIR.exists():
            memory = sqlite3.connect(DIR)
            cursor = memory.cursor()
            cursor.execute('SELECT * FROM memory')
            for user_say, bot_say in cursor.fetchall():
                if user_speech == user_say:
                    return bot_say
        while True:
            hear('Não sei o que dizer, pode me ensinar?')
            answer = self.say
            match answer:
                case 'sim' | 'claro' | 'posso' | 'ok':
                    hear('O que eu tenho que falar?')
                    bot_speech = self.say
                    break
                case 'não' | 'não posso' | 'não quero' | 'melhor não' | 'deixe pra lá':
                    return 'Ok, eu entendo...'
                case 'Que burra' | 'ia burra' | 'idiota':
                    return 'Você é babaca!'
                case _:
                    hear('Não entendi, pode me ajudar?')

        memory = sqlite3.connect(DIR)
        cursor = memory.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS memory (user TEXT NOT NULL, answer TEXT NOT NULL)")
        try:    
            cursor.execute(f"INSERT INTO memory VALUES ('{user_speech}', '{bot_speech}')")
        except sqlite3.NotSupportedError:
            print('deu erro')
        memory.commit()
        return 'Obrigada por me ensinar"'


class BotSara(BotStructure):

    def __speech_vosk(self): # Reconhecedor de Fala Online | from vosk import Model, KaldiRecognizer | import pyaudio
        
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
                    continue
                return speech

    @property
    def say(self): # Reconhecedor de Fala Online | import speech_recognition as sr
        
        recognition = sr.Recognizer() # Reconhecedor de Voz
        microphone = sr.Microphone() # Microfone
        with microphone as mic: # Abrir|Ativar Microfone
            audio = recognition.listen(mic, timeout=1000) # Capitando audio do Microfone
            while True:
                try:
                    talk = recognition.recognize_google(audio, language="pt-BR") # Retrono em str
                    break
                except sr.UnknownValueError:
                    system('cls')
                    talk = self.__speech_vosk()
                    break
            system('cls')
            return talk
    


bot = BotSara()
try:
    while True:
        hear(bot.brain(bot.say))
except KeyboardInterrupt:
    print('Aplicação encerrada!')

