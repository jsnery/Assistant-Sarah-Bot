from brain import Brain
import data_


class BotSara(Brain):
    @property
    def voice_detection(self):  # Reconhecimento de fala Offline
        # from vosk import Model, KaldiRecognizer | import pyaudio
        # Speech Recognition
        srrecognizer = data_.sr.Recognizer()
        mic = data_.sr.Microphone()

        # vosk
        data_.SetLogLevel(-1)
        try:
            model = data_.Model(f'{data_.FULLLANGUAGE}')
            # Carregar o Modelo de Idioma Cheio
        except Exception:
            data_.system('cls')
            model = data_.Model(f'{data_.LIGHTLANGUAGE}')
            # Carregar o Modelo de Idioma Leve

        recognizer = data_.KaldiRecognizer(model, 16000)  # Reconhecedor de Voz

        try:  # Corrigi o bug de execução de som
            data_.playsound_(data_.WARNINGSOUND)
        except data_.PlaysoundException:
            data_.system('cls')
            data_.playsound_(data_.WARNINGSOUND)
        except Exception:
            ...

        timeout = 3
        while True:
            data_.system('cls')
            try:  # Speech Recognition
                with mic as source:
                    audio = srrecognizer.listen(source)
                    speech = srrecognizer.recognize_google(audio, language='pt-BR').lower()  # type: ignore # noqa
                    data_.system('cls')
            except (data_.sr.UnknownValueError, data_.sr.RequestError):  # Vosk
                capture = data_.PyAudio()  # Capiturando o Mic
                stream = capture.open(format=data_.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)  # Configurando Captura  # noqa
                stream.start_stream()  # Iniciar reconhecimento
                data = stream.read(16384)  # Lendo os dados do mic

                if recognizer.AcceptWaveform(data):  # Se identificar a voz
                    speech = eval(recognizer.Result())['text']

            data_.system('cls')
            try:
                match speech:  # type: ignore
                    case '' if timeout > 0:
                        timeout -= 1
                        if timeout == 0:
                            self.status = True
                        continue

                    case 'sarah' | 'sara' | 'testando' if self.status:
                        self.status = False
                        self.bot_say(data_.choice(self._salutation))
                        speech = self.voice_detection

                        if speech == '':
                            timeout = 3
                            continue

                        return speech

                    case 'vá dormir' | 'até mais' | 'até depois' if not self.status:  # noqa
                        self.status = True
                        self.bot_say(data_.choice(self._farewell))

                    case 'desligar':
                        self.bot_say('Tchau Tchau!')
                        exit(0)

                    case _ if not self.status:
                        return speech   # type: ignore

            except UnboundLocalError:
                continue


if __name__ == '__main__':
    bot = BotSara()
    bot.bot_say(' ')
    while True:
        bot.bot_say(bot.discourse(bot.voice_detection))
