from vosk import Model, KaldiRecognizer, SetLogLevel  # Biblioteca de reconhecimento de fala Offline
from pyttsx3 import speak as bot_say2 # Leitor de texto
from pyaudio import PyAudio, paInt16
from playsound import playsound
from gtts import gTTS, gTTSError
from abc import ABC, abstractmethod
from pathlib import Path
from os import system
import sqlite3

system('cls')
MEMORYDIR = Path(__file__).parent / 'data' / 'memory.db'
MODELDIR = Path(__file__).parent / 'data' / 'full' # Baixar pelo Link: https://alphacephei.com/vosk/models/vosk-model-pt-fb-v0.1.1-pruned.zip
MODELLITEDIR = Path(__file__).parent / 'data' / 'lite'
TEMPTALK = Path(__file__).parent / 'data' / 'temp.mp3'
SOUNDDIR = Path(__file__).parent / 'data' / 'sound.wav'


class BotStructure(ABC):

    def __init__(self):
        self.status = True

    @property    
    @abstractmethod
    def user_speech(self) -> str:...


    def bot_say(self, text, dir=TEMPTALK):
        try:
            speech_config = gTTS(text=text, lang='pt')
            speech_config.save(dir)
            playsound(dir)
            dir.unlink()
        except gTTSError:
            bot_say2(text)
        

    def brain(self, user_speech, DIR=MEMORYDIR):

        if DIR.exists():
            memory = sqlite3.connect(DIR)
            cursor = memory.cursor()
            cursor.execute('SELECT * FROM memory')
            for user_say, say in cursor.fetchall():
                if user_speech == user_say:
                    return say
        
        # self.bot_say('Não sei o que dizer, pode me ensinar?')

        # while True:
        #     answer = self.user_speech
        #     match answer:
        #         case 'sim' | 'claro' | 'posso' | 'ok':
        #             self.bot_say('O que eu tenho que falar?')
        #             bot_speech = self.user_speech
        #             break
        #         case 'não' | 'não posso' | 'não quero' | 'melhor não' | 'deixe pra lá':
        #             self.status = True
        #             return 'Ok, eu entendo...'
        #         case 'que burra' | 'ia burra' | 'idiota' | 'burra' | 'sua idiota' | 'mas é burra viu':
        #             self.status = True
        #             return 'Você é muito babaca!'
        #         case _:
        #             self.bot_say('Não entendi, pode me ajudar?')

        # memory = sqlite3.connect(DIR)
        # cursor = memory.cursor()
        # cursor.execute("CREATE TABLE IF NOT EXISTS memory (user TEXT NOT NULL, answer TEXT NOT NULL)")
        # cursor.execute(f"INSERT INTO memory VALUES ('{user_speech}', '{bot_speech}')")
        # memory.commit()
        # self.status = True
        # return 'Obrigada por me ensinar!"'


class BotSara(BotStructure):

    @property
    def user_speech(self): # Reconhecimento de fala Offline | from vosk import Model, KaldiRecognizer | import pyaudio
        SetLogLevel(-1) # Desativar Log
        
        try:
            model = Model(f'{MODELDIR}') # Carregar o Modelo de Idioma
        except Exception:
            model = Model(f'{MODELLITEDIR}') # Carregar o Modelo de Idioma

        recognizer = KaldiRecognizer(model, 16000) # Reconhecedor de Voz
        playsound(SOUNDDIR)

        # Reconhecer Microfone
        capture = PyAudio() # Capitura o Mic
        stream = capture.open(format=paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream() # Iniciar reconhecimento
        
        while True:
            data = stream.read(16384) # Lendo os dados do mic | buffer de 16mb

            if recognizer.AcceptWaveform(data): # Se identificar a voz
                speech = eval(recognizer.Result())['text']
                
                if speech == '':
                    continue

                elif speech == 'sara pode me ouvir' and self.status:
                    self.status = False
                    self.bot_say('No que eu posso te ajudar?')
                    print('Escutando...')
                    speech = self.user_speech

                    if speech == '':
                        continue
                    
                    system('cls')
                    return speech
                
                elif (speech == 'sara depois nos falamos' or speech == 'sara até mais') and not self.status:
                    self.status = True
                    self.bot_say('Certo, até mais!')
                elif not self.status:
                    return speech

    

if __name__ == '__main__':
    bot = BotSara()
    try:
        playsound(SOUNDDIR)
        while True:
            print('É só falar, "Olá Sara!"...')
            bot.bot_say(bot.brain(bot.user_speech))
    except KeyboardInterrupt:
        print('Aplicação encerrada!')

