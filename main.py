import speech_recognition as sr # Biblioteca de reconhecimento de fala
from os import system

# Reconhecedor de Voz
r = sr.Recognizer()

# Abrir o microfone
with sr.Microphone() as mic: # device_index=5
    audio = r.listen(mic) # Define mic como fonte de audio
    speech = r.recognize_google(audio, language="pt-BR")
    system('cls')
    print(speech)
    

