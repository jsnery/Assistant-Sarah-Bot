import sqlite3
from data import *


try:
    system('cls')
    class BotStructure(ABC):

        def __init__(self):
            self.status = True

        @property    
        @abstractmethod
        def user_speech(self) -> str:...

        def bot_say(self, text, dir=BOTVOICE):
            
            try:
                speech_config = gTTS(text=text, lang='pt')
                speech_config.save(dir)
                playsound(f'{dir}')
                dir.unlink()
            except PlaysoundException as error:
                system('cls')
                bot_say2(text)
            
        def __learnig(self):
            self.bot_say('Me fale algo.')
            while True:
                learnQuestion = self.user_speech
                
                if learnQuestion == '':
                        continue
                break
                
            
            self.bot_say('O que espera que eu responda?')
            while True:
                learn = self.user_speech
                
                if learn == '':
                        continue
                break

            memory = sqlite3.connect(MEMORYDIR)
            cursor = memory.cursor()
            cursor.execute(f"INSERT INTO memory VALUES ('{learnQuestion}', '{learn}', '{learn}', '{learn}', '{learn}')")
            memory.commit()
            self.status = True

        def brain(self, user_speech, DIR=MEMORYDIR):

            if DIR.exists():
                memory = sqlite3.connect(DIR)
                cursor = memory.cursor()
                cursor.execute('SELECT * FROM memory')
                for user_say, *say in cursor.fetchall():
                    if user_speech == 'aprenda isso':
                        self.__learnig()
                        return 'Conhecimento obtido com sucesso'
                    
                    if user_speech == user_say:
                        return choice(say)
                    
                return 'Não aprendi isso ainda'


    class BotSara(BotStructure):

        @property
        def user_speech(self): # Reconhecimento de fala Offline | from vosk import Model, KaldiRecognizer | import pyaudio
            SetLogLevel(-1) # Desativar Log
            
            try:
                model = Model(f'{FULLLANGUAGE}') # Carregar o Modelo de Idioma
            except Exception:
                model = Model(f'{LIGHTLANGUAGE}') # Carregar o Modelo de Idioma

            recognizer = KaldiRecognizer(model, 16000) # Reconhecedor de Voz
            try:
                playsound(WARNINGSOUND)
            except PlaysoundException:
                system('cls')
                playsound(WARNINGSOUND)
            except:
                system('cls')
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

                        case 'sarah' if self.status:
                            self.status = False
                            self.bot_say('No que eu posso te ajudar?')
                            print('Escutando...')
                            speech = self.user_speech

                            if speech == '':
                                timeout = 3
                                continue
                            
                            system('cls')
                            return speech
                        
                        case 'depois nos falamos' | 'até mais' if not self.status:
                            self.status = True
                            self.bot_say('Certo, até mais!')

                        case _ if not self.status:
                            return speech

        

    if __name__ == '__main__':
        bot = BotSara()
        try:
            while True:
                bot.bot_say(bot.brain(bot.user_speech))
        except KeyboardInterrupt:
            print('Aplicação encerrada!')

except Exception as error:
    print(error)

sleep(5)