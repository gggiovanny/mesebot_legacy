import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone()

print("Di algo...")
with mic as source:
    r.adjust_for_ambient_noise(source, duration=0.5)
    audio = r.listen(source)

print(r.recognize_google(audio, language='es-MX'))
