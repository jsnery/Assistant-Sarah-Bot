# import speech_recognition as sr # Biblioteca de reconhecimento de fala Online
from vosk import Model, KaldiRecognizer, SetLogLevel  # Biblioteca de reconhecimento de fala Offline
from pyttsx3 import speak as hear # Leitor de texto
import sqlite3
from pathlib import Path
from abc import ABC, abstractmethod
import pyaudio
from os import system

DIR = Path(__file__).parent / 'memory.db'

class BotStructure(ABC):

    def __init__(self):...

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

    @property
    def say(self): # Reconhecimento de fala Offline | from vosk import Model, KaldiRecognizer | import pyaudio
        SetLogLevel(-1)
        model = Model('model') # Carregar o Modelo de Idioma
        system('cls')
        recognizer = KaldiRecognizer(model, 16000) # Reconhecedor de Voz

        # Reconhecer Microfone
        capture = pyaudio.PyAudio() # Capitura o Mic
        stream = capture.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream() # Iniciar reconhecimento

        while True:
            data = stream.read(16384) # Lendo os dados do mic | buffer de 16mb

            if recognizer.AcceptWaveform(data): # Se identificar a voz
                speech = eval(recognizer.Result())['text']
                if speech == '':
                    system('cls')
                    continue
                return speech

    


bot = BotSara()
try:
    while True:
        hear(bot.brain(bot.say))
except KeyboardInterrupt:
    print('Aplicação encerrada!')

