import speech_recognition as sr
r = sr.Recognizer()

harvard = sr.AudioFile("media//harvard.wav")

with harvard as source:
    audio = r.record(source)
print(type(audio))

print(r.recognize_google(audio))
