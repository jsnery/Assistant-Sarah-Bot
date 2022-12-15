from playsound import  PlaysoundException, playsound as playsound_
from vosk import Model, KaldiRecognizer, SetLogLevel  # Biblioteca de reconhecimento de fala Offline
from pyttsx3 import speak as bot_say2 # Leitor de texto
from pyaudio import PyAudio, paInt16
from abc import ABC, abstractmethod
from os import system, path, mkdir, startfile
from subprocess import run
from webbrowser import open_new
from random import choice
from pathlib import Path
from shutil import copy2
from gtts import gTTS # Leitor de texto do google
from sys import exit
import speech_recognition as sr
from googlesearch import search


DATADIR = Path(__file__).parent  / 'data'

if (Path().absolute() / 'data') != DATADIR:
    DATADIR = Path(__file__).parent

MEMORYDIR = Path(DATADIR) / 'memory.db'
FULLLANGUAGE = Path(DATADIR)  / 'full' # Baixar pelo Link: https://alphacephei.com/vosk/models/vosk-model-pt-fb-v0.1.1-pruned.zip
LIGHTLANGUAGE = Path(DATADIR)  / 'lite'
WARNINGSOUND = Path(DATADIR) / 'sound.wav'
BOTVOICE = Path(DATADIR) / 'temp.mp3'

# CACHEDIR = path.join(path.expanduser("~"), "AppData/Roaming/SaraCache")

# if not path.isdir(CACHEDIR):
#     mkdir(CACHEDIR)

# copy2(WARNING, CACHEDIR)

# WARNINGSOUND = Path(CACHEDIR) / 'sound.wav'
# BOTVOICE = Path(CACHEDIR) / 'temp.mp3'