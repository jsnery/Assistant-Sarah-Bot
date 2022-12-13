# import speech_recognition as sr # Biblioteca de reconhecimento de fala Online
from vosk import Model, KaldiRecognizer, SetLogLevel  # Biblioteca de reconhecimento de fala Offline
from pyttsx3 import speak as bot_say # Leitor de texto
from pathlib import Path
from abc import ABC, abstractmethod
from os import system
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
import sqlite3, pyaudio

system('cls')
MEMORYDIR = Path(__file__).parent / 'data' / 'memory.db'
MODELDIR = Path(__file__).parent / 'data' / 'model'
SOUNDDIR = Path(__file__).parent / 'data' / 'sound.wav'

class BotStructure(ABC):

    def __init__(self):
        self._song = AudioSegment.from_wav(SOUNDDIR)
        self.status = True

    @property    
    @abstractmethod
    def user_speech(self) -> str:...

    def brain(self, user_speech, DIR=MEMORYDIR):

        if DIR.exists():
            memory = sqlite3.connect(DIR)
            cursor = memory.cursor()
            cursor.execute('SELECT * FROM memory')
            for user_say, say in cursor.fetchall():
                if user_speech == user_say:
                    return say
        
        bot_say('Não sei o que dizer, pode me ensinar?')
        while True:
            answer = self.user_speech
            match answer:
                case 'sim' | 'claro' | 'posso' | 'ok':
                    bot_say('O que eu tenho que falar?')
                    bot_speech = self.user_speech
                    break
                case 'não' | 'não posso' | 'não quero' | 'melhor não' | 'deixe pra lá':
                    self.status = True
                    return 'Ok, eu entendo...'
                case 'Que burra' | 'ia burra' | 'idiota' | 'burra':
                    self.status = True
                    return 'Você é babaca!'
                case _:
                    bot_say('Não entendi, pode me ajudar?')

        memory = sqlite3.connect(DIR)
        cursor = memory.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS memory (user TEXT NOT NULL, answer TEXT NOT NULL)")
        try:    
            cursor.execute(f"INSERT INTO memory VALUES ('{user_speech}', '{bot_speech}')")
        except sqlite3.NotSupportedError:
            print('deu erro')
        memory.commit()
        self.status = True
        return 'Obrigada por me ensinar"'


class BotSara(BotStructure):

    @property
    def user_speech(self): # Reconhecimento de fala Offline | from vosk import Model, KaldiRecognizer | import pyaudio
        SetLogLevel(-1) # Desativar Log
        model = Model(f'{MODELDIR}') # Carregar o Modelo de Idioma
        recognizer = KaldiRecognizer(model, 16000) # Reconhecedor de Voz
        play(self._song)

        # Reconhecer Microfone
        capture = pyaudio.PyAudio() # Capitura o Mic
        stream = capture.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream() # Iniciar reconhecimento
        
        while True:
            data = stream.read(16384) # Lendo os dados do mic | buffer de 16mb

            if recognizer.AcceptWaveform(data): # Se identificar a voz
                speech = eval(recognizer.Result())['text']
                
                if speech == '':
                    continue

                elif speech == 'olá sara' and self.status:
                    self.status = False
                    bot_say('No que eu posso te ajudar?')
                    speech = self.user_speech

                    if speech == '':
                        continue

                    return speech
                
                elif speech == 'depois nos falamos' and not self.status:
                    self.status = True
                    bot_say('Certo, até mais!')
                elif not self.status:
                    return speech

    


bot = BotSara()
try:
    while True:
        bot_say(bot.brain(bot.user_speech))
except KeyboardInterrupt:
    print('Aplicação encerrada!')

