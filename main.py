import speech_recognition as sr # Biblioteca de reconhecimento de fala

# Reconhecedor de Voz
r = sr.Recognizer()


# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f'Microphone with name "{name}" found for `Microphone(device_index={index})`')

# Abrir o microfone
with sr.Microphone() as mic: # device_index=5
    audio = r.listen(mic) # Define mic como fonte de audio
    
    print(r.recognize_google(audio))
    

