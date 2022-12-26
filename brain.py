import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass
from json import 
import data_


@dataclass
class Brain(ABC):

    _farewell = (
                'Certo, até mais!',
                'Até depois então',
                'Falo com você mais tarde!',
                'Estarei aqui!'
                )
    _salutation = (
                'No que eu posso te ajudar?',
                'Precisando de mim?',
                'Chamou chamou',
                'Estou aqui!'
                )

    @property
    @abstractmethod
    def voice_detection(self): ...

    def bot_say(self, text, dir_=data_.BOTVOICE):
        try:
            data_.gTTS(text=text, lang='pt').save(dir_)
            try:  # Corrigi o bug de execução de som
                data_.playsound_(dir_)
            except data_.PlaysoundException:
                data_.system('cls')
                data_.playsound_(dir_)
            dir_.unlink()

        except Exception:
            data_.system('cls')
            data_.bot_say2(text)

    def __learnig(self, DIR_=data_.MEMORYDIR):
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
            cursor.execute(f"INSERT INTO memory VALUES ('{asking}', '{answer}', '{answer}', '{answer}', '{answer}')")  # noqa
            memory.commit()
            return 'Consegui aprender isso! Obrigada.'
        except sqlite3.OperationalError:
            return 'Já possuo essa informação em minha memória!'

    def discourse(self, user_speech, DIR_=data_.MEMORYDIR):
        memory = sqlite3.connect(DIR_)
        cursor = memory.cursor()
        cursor.execute('SELECT * FROM memory')

        for user_say, *bot_say in cursor.fetchall():
            if user_speech == 'aprenda isso':
                return self.__learnig()

            if 'abrir' in user_speech:
                search_ = "+".join(user_speech.split()[1:])
                data_.open_new(*[i for i in data_.search(search_, stop=1, lang='br')])  # noqa
                return 'Abrindo...'

            if 'pesquisar' in user_speech:
                search_ = "+".join(user_speech.split()[1:])
                data_.open_new(f'https://www.google.com/search?q={search_}')
                return 'Pesquisando...'

            if user_speech == user_say:
                return data_.choice(bot_say)

        return 'Eu não entendi isso!'