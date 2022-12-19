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

    def bot_say(self, text, dir_=BOTVOICE):
        try:
            gTTS(text=text, lang='pt').save(dir_)
            try: # Corrigi o bug de execução de som
                playsound_(dir_)
            except PlaysoundException:
                system('cls')
                playsound_(dir_)
            dir_.unlink()

        except Exception:
            system('cls')
            bot_say2(text)

    def __learnig(self, DIR_=MEMORYDIR):
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

        memory = sqlite3.connect(DIR_)
        cursor = memory.cursor()
        try:
            cursor.execute(f"INSERT INTO memory VALUES ('{asking}', '{answer}', '{answer}', '{answer}', '{answer}')")
            memory.commit()
            return 'Consegui aprender isso! Obrigada.'
        except sqlite3.OperationalError:
            return 'Já possuo essa informação em minha memória!'

    def discourse(self, user_speech, DIR_=MEMORYDIR):
        memory = sqlite3.connect(DIR_)
        cursor = memory.cursor()
        cursor.execute('SELECT * FROM memory')

        for user_say, *bot_say in cursor.fetchall():
            if user_speech == 'aprenda isso':
                return self.__learnig()

            if 'abrir' in user_speech:
                search_ = "+".join(user_speech.split()[1:])
                open_new(*[i for i in search(search_, stop=1, lang='br')])
                return 'Abrindo...'
            
            if 'pesquisar' in user_speech:
                search_ = "+".join(user_speech.split()[1:])
                open_new(f'https://www.google.com/search?q={search_}')
                return 'Pesquisando...'
            
            if user_speech == user_say:
                return choice(bot_say)
            
        return 'Eu não entendi isso!'


class BotSara(Brain):

    @property
    def voice_detection(self): # Reconhecimento de fala Offline | from vosk import Model, KaldiRecognizer | import pyaudio
        
        # Speech Recognition
        srrecognizer = sr.Recognizer() 
        mic = sr.Microphone()

        # vosk   
        SetLogLevel(-1)
        try:
            model = Model(f'{FULLLANGUAGE}') # Carregar o Modelo de Idioma Cheio
        except Exception:
            system('cls')
            model = Model(f'{LIGHTLANGUAGE}') # Carregar o Modelo de Idioma Leve

        recognizer = KaldiRecognizer(model, 16000) # Reconhecedor de Voz

        try: # Corrigi o bug de execução de som
            playsound_(WARNINGSOUND)
        except PlaysoundException:
            system('cls')
            playsound_(WARNINGSOUND)
        except Exception:
            ...
        
        timeout = 3
        while True:
            system('cls')
            try: # Speech Recognition
                with mic as source:
                    audio = srrecognizer.listen(source)
                    speech = srrecognizer.recognize_google(audio, language='pt-BR').lower()
                    system('cls')
            except (sr.UnknownValueError, sr.RequestError): # Vosk
                capture = PyAudio() # Capiturando o Mic
                stream = capture.open(format=paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192) # Configurando Captura
                stream.start_stream() # Iniciar reconhecimento
                data = stream.read(16384) # Lendo os dados do mic | buffer de 16mb

                if recognizer.AcceptWaveform(data): # Se identificar a voz
                    speech = eval(recognizer.Result())['text']
            
            system('cls')
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
    bot.bot_say(' ')
    while True:
        bot.bot_say(bot.discourse(bot.voice_detection))
