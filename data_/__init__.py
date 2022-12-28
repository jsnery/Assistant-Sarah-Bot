from playsound import  PlaysoundException, playsound as playsound_  # type: ignore # noqa
from vosk import Model, KaldiRecognizer, SetLogLevel  # type: ignore # noqa
# Biblioteca de reconhecimento de fala Offline
from pyttsx3 import speak as bot_say2 # type: ignore # Leitor de texto  # noqa
from pyaudio import PyAudio, paInt16  # type: ignore # noqa
from os import system, path, mkdir, startfile  # noqa
from subprocess import run  # noqa
from webbrowser import open_new  # noqa
from random import choice  # noqa
from pathlib import Path  # noqa
from shutil import copy2  # noqa
from gtts import gTTS # type: ignore # Leitor de texto do google  # noqa
from sys import exit  # noqa
import speech_recognition as sr  # type: ignore # noqa
from googlesearch import search  # type: ignore # noqa


DATADIR = Path(__file__).parent  / 'data_'  # noqa

if (Path().absolute() / 'data_') != DATADIR:
    DATADIR = Path(__file__).parent

JSONDATA = Path(DATADIR) / 'memory.json'
MEMORYDIR = Path(DATADIR) / 'memory.db'
FULLLANGUAGE = Path(DATADIR) / 'full'
# Link: https://alphacephei.com/vosk/models/vosk-model-pt-fb-v0.1.1-pruned.zip
LIGHTLANGUAGE = Path(DATADIR) / 'lite'
WARNINGSOUND = Path(DATADIR) / 'sound.wav'
BOTVOICE = Path(DATADIR) / 'temp.mp3'

# CACHEDIR = path.join(path.expanduser("~"), "AppData/Roaming/SaraCache")

# if not path.isdir(CACHEDIR):
#     mkdir(CACHEDIR)

# copy2(WARNING, CACHEDIR)

# WARNINGSOUND = Path(CACHEDIR) / 'sound.wav'
# BOTVOICE = Path(CACHEDIR) / 'temp.mp3'
