import playsound
from gtts import gTTS

RUTA = "media//"
nombre_archivo = 'no_API.mp3'

tts = gTTS(text='No se ha podido establecer conexión a la red. Favor de contactar al administrador.', lang='es')
tts.save(RUTA + nombre_archivo)
playsound.playsound(RUTA + nombre_archivo, True)

