import sqlite3
from data import *


class Brain(ABC):

    def __init__(self):
        self.status = True
        self._farewell = ('Certo, até mais!', 'Até depois então', 'Falo com você mais tarde!', 'Estarei aqui!')
        self._salutation = ('No que eu posso te ajudar?', 'Precisando de mim?', 'Chamou chamou', 'Estou aqui!')
        self._commands = {
            'abrir google': lambda: open_new('https://www.google.com/'),
            'abrir youtube': lambda: open_new('https://www.youtube.com/'),
        }

    @property
    @abstractmethod
    def voice_detection(self): ...

    def bot_say(self, text, dir_=BOTVOICE):
        try:
            speech_config = gTTS(text=text, lang='pt')
            speech_config.save(dir_)
            try:
                playsound_(dir_)
            except PlaysoundException: # Corrigi o bug de execução de som
                system('cls')
                playsound_(dir_)
            dir_.unlink()
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
        try:
            cursor.execute(f"INSERT INTO memory VALUES ('{asking}', '{answer}', '{answer}', '{answer}', '{answer}')")
            memory.commit()
            self.status = True
            return 'Conhecimento obtido com sucesso'
        except sqlite3.OperationalError:
            self.status = True
            return 'Acho que já conheço isso! Se quiser me ensinar outra coisa fale "Aprenda Isso"'

    def discourse(self, user_speech, DIR_=MEMORYDIR):
        memory = sqlite3.connect(DIR_)
        cursor = memory.cursor()
        cursor.execute('SELECT * FROM memory')

        for user_say, *bot_say in cursor.fetchall():
            if user_speech == 'aprenda isso':
                return self.__learnig()
            
            if user_speech in list(self._commands.keys()):
                self._commands.get(user_speech)()
                return 'Abrindo...'
            
            if user_speech == user_say:
                return choice(bot_say)
            
        return 'Eu não entendi isso!'


class BotSara(Brain):

    @property
    def voice_detection(self): # Reconhecimento de fala Offline | from vosk import Model, KaldiRecognizer | import pyaudio
        
        # speech_recognition
        srrecognizer = sr.Recognizer() 
        mic = sr.Microphone()

        # vosk   
        try:
            SetLogLevel(-1)
            model = Model(f'{FULLLANGUAGE}') # Carregar o Modelo de Idioma Cheio
        except Exception:
            system('cls')
            SetLogLevel(-1)
            model = Model(f'{LIGHTLANGUAGE}') # Carregar o Modelo de Idioma Leve

        recognizer = KaldiRecognizer(model, 16000) # Reconhecedor de Voz

        try:
            playsound_(WARNINGSOUND)
        except PlaysoundException: # Corrigi o bug de execução de som
            system('cls')
            playsound_(WARNINGSOUND)
        
        timeout = 3
        while True:
            system('cls')
            try: # speech_recognition
                with mic as source:
                    audio = srrecognizer.listen(source)
                    speech = srrecognizer.recognize_google(audio, language='pt-BR').lower()
                    system('cls')

            except (sr.UnknownValueError, sr.RequestError): # vosk
                system('cls')
                # Reconhecer Microfone
                capture = PyAudio() # Capitura o Mic
                stream = capture.open(format=paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192) # Configurando Captura
                stream.start_stream() # Iniciar reconhecimento

                data = stream.read(16384) # Lendo os dados do mic | buffer de 16mb

                if recognizer.AcceptWaveform(data): # Se identificar a voz
                    speech = eval(recognizer.Result())['text']

            try:
                match speech:
                    case '' if timeout > 0:
                        timeout -= 1
                        if timeout == 0:
                            self.status = True 
                        continue

                    case 'sarah' | 'sara' | 'testando' if self.status:
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
            
            except UnboundLocalError:
                continue
        


if __name__ == '__main__':
    bot = BotSara()
    bot.bot_say(' ') # Corrigi a leitura de voz | Armengo temporario
    while True:
        bot.bot_say(bot.discourse(bot.voice_detection))
