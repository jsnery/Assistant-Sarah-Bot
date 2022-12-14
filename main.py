import sqlite3
from data import *


class Brain(ABC):

    def __init__(self):
        self.status = True
        self._farewell = ('Certo, até mais!', 'Até depois então', 'Falo com você mais tarde!', 'Estarei aqui!')
        self._salutation = ('No que eu posso te ajudar?', 'Precisando de mim?', 'Chamou chamou', 'Estou aqui!')
    
    @property
    @abstractmethod
    def voice_detection(self): ...

    def bot_say(self, text, dir=BOTVOICE):
        try:
            speech_config = gTTS(text=text, lang='pt')
            speech_config.save(dir)
            try:
                playsound(dir)
            except PlaysoundException: # Corrigi o bug de execução de som
                system('cls')
                playsound(dir)
            dir.unlink()
        except Exception:
            system('cls')
            bot_say2(text)

    def __learnig(self):
        self.bot_say('Me fale algo o que vou ouvir.')
        while True:
            asking = self.voice_detection
            if asking == '':
                    continue
            break
            
        self.bot_say('Me fale o que devo responder')
        while True:
            answer = self.voice_detection
            if answer == '':
                    continue
            break

        memory = sqlite3.connect(MEMORYDIR)
        cursor = memory.cursor()
        cursor.execute(f"INSERT INTO memory VALUES ('{asking}', '{answer}', '{answer}', '{answer}', '{answer}')")
        memory.commit()
        self.status = True

    def discourse(self, user_speech, DIR=MEMORYDIR):
        memory = sqlite3.connect(DIR)
        cursor = memory.cursor()
        cursor.execute('SELECT * FROM memory')

        for user_say, *bot_say in cursor.fetchall():
            if user_speech == 'aprenda isso':
                self.__learnig()
                return 'Conhecimento obtido com sucesso'
            
            if user_speech == user_say:
                return choice(bot_say)
            
        return 'Não aprendi isso ainda, se quiser me ensinar fale: Aprenda Isso!'

class BotSara(Brain):

    @property
    def voice_detection(self): # Reconhecimento de fala Offline | from vosk import Model, KaldiRecognizer | import pyaudio
        SetLogLevel(-1) # Desativar Log
        
        try:
            model = Model(f'{FULLLANGUAGE}') # Carregar o Modelo de Idioma
        except Exception:
            system('cls')
            model = Model(f'{LIGHTLANGUAGE}') # Carregar o Modelo de Idioma

        recognizer = KaldiRecognizer(model, 16000) # Reconhecedor de Voz
        try:
            playsound(WARNINGSOUND)
        except PlaysoundException: # Corrigi o bug de execução de som
            system('cls')
            playsound(WARNINGSOUND)

        # Reconhecer Microfone
        capture = PyAudio() # Capitura o Mic
        stream = capture.open(format=paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream() # Iniciar reconhecimento
        
        timeout = 3
        while True:
            data = stream.read(16384) # Lendo os dados do mic | buffer de 16mb

            if recognizer.AcceptWaveform(data): # Se identificar a voz
                speech = eval(recognizer.Result())['text']

                match speech:
                    case '' if timeout > 0:
                        timeout -= 1
                        if timeout == 0:
                            self.status = True 
                        continue

                    case 'sarah' | 'sara' if self.status:
                        self.status = False
                        self.bot_say(choice(self._salutation))
                        speech = self.voice_detection

                        if speech == '':
                            timeout = 3
                            continue
        
                        return speech
                    
                    case 'vá dormir' | 'até mais' | 'até depois' if not self.status:
                        self.status = True
                        self.bot_say(choice(self._farewell))

                    case 'desligar':
                        self.bot_say('Tchau Tchau!')
                        exit(0)

                    case _ if not self.status:
                        return speech
        

if __name__ == '__main__':
    bot = BotSara()
    while True:
        bot.bot_say(bot.discourse(bot.voice_detection))
