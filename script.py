import playsound
import speech_recognition as sr
from gtts import gTTS
from datetime import datetime, date, time, timedelta
import SQL


preciototal = 0


""" VARIABLES GLOBALES """
MENU = []
NUMEROS = {
    "uno" : 1,
    "una" : 1,
    "unos": 1,
    "unas": 1,
    "dos": 2,
    "tres": 3,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10
}
recognizer = sr.Recognizer()
microphone = sr.Microphone()
RUTA = "media//"

class ClaseResultado:
    correcto = True
    transcripcion = ""

""" FUNCIONES """
def decir(frase):
    tts = gTTS(text=frase, lang='es')
    tts.save(RUTA + "frase.mp3")
    playsound.playsound(RUTA + 'frase.mp3')

def generarTTSMenu():
    frase = "El menu de hoy es: "
    for item in MENU:
        frase += item.nombreES + " ,"
    tts = gTTS(text=frase, lang='es')
    tts.save(RUTA + "menu.mp3")
    print('[TTS del menú generado correctamente!]')

def DecirSaludo():
    #Saliudo personalizado segun horario de atención
    hora1 = time(4, 0, 0) #4:00:00 am
    hora2 = time(12,0,0) #12:00:00 pm
    hora3 = time(19,0,0) #7:00:00 pm
    hora_act = datetime.now().time()
    if hora_act > hora1 and hora_act < hora2:
        print("DECIR: Buenos dias")
        playsound.playsound(RUTA + "buenos_dias.mp3")
    else:
        if hora_act>hora2 and hora_act < hora3:
            print("DECIR: Buenas tardes")
            playsound.playsound(RUTA + "buenas_tardes.mp3")
        else:
            print("DECIR: Buenas noches")
            playsound.playsound(RUTA + "buenas_noches.mp3")

def DecirMenu():
    print('MOSTRAR MENÚ:')
    for item in MENU:
        print("\tid: %s, nombre: %s, Precio: %s" % (item.id, item.nombreES, item.precio))
    playsound.playsound(RUTA + 'menu.mp3')

def PedirOrden():
    print('DECIR: ¿Qué desea ordenar?')
    playsound.playsound(RUTA + "pedir_orden.mp3")

def ReconocerVoz(seMuestra = False, tiempo_limite = 10):
    """"  Graba la voz y la reconoce, y lidia con los errores de reconocimiento """
    resultado = ClaseResultado
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.1) #tomar muestreo del ruido ambiental
        if seMuestra:
            print("[Escuchando...]")
        audio = recognizer.listen(source, phrase_time_limit=tiempo_limite) #escuchar
    try:
        if seMuestra:
            print("[Reconociendo...]")
        resultado.transcripcion = recognizer.recognize_google(audio, language='es-MX')
    except sr.RequestError:
        # No se pudo conectar a la API o esta no responde
        print('DECIR: No se ha podido establecer conexión a la red. Favor de contactar al administrador.')
        playsound.playsound(RUTA + "no_API.mp3")
        resultado.correcto = False
    except sr.UnknownValueError:
        # No se entiende lo que el cliente dice
        print("DECIR: No pude entender lo que ha dicho, ¿podría repetirlo?")
        playsound.playsound(RUTA + "no_entiendo.mp3")
        resultado = ReconocerVoz(seMuestra)

    if seMuestra:
        print('TEXTO RECONOCIDO: %s' % resultado.transcripcion)
    return resultado

def ConfirmarOrden(orden):

    texto_pedido = ""
    if len(orden) == 1:
        texto_pedido += str(orden[0].cantidad) + " " + orden[0].nombreES
    if len(orden) == 2:
        texto_pedido += str(orden[0].cantidad) + " " + orden[0].nombreES + " y " + str(orden[1].cantidad) + " " + orden[1].nombreES
    if len(orden) >= 3:
        for i in range(len(orden)-2):
            texto_pedido += str(orden[i].cantidad) + " " + orden[i].nombreES + ", "
        texto_pedido += str(orden[len(orden) - 2].cantidad) + " " + orden[len(orden) - 2].nombreES + " y " + str(orden[len(orden) - 1].cantidad) + " " + orden[len(orden) - 1].nombreES
    ordencompleta= "Usted ha ordenado %s" % texto_pedido
    print('DECIR ORDEN: ' + ordencompleta)
    decir((ordencompleta))
    playsound.playsound(RUTA + 'confirmacion_orden.mp3')
    resultado = ReconocerVoz(True, 5)
    if 'si' in SQL.NormalizarTexto(resultado.transcripcion):
        return True
    if 'no' in SQL.NormalizarTexto(resultado.transcripcion):
        return False

def ProcesarOrden(transcripcion):
    """ Recibe una transcripcion de la orden y regresa una lista de tipo Item con los elementos reconocidos en el menu"""
    orden = []

    cantidad = 1
    cantidad_vigente = False

    preciototal=0
    frase = SQL.NormalizarTexto(transcripcion).split()
    for palabra in frase:

        if not cantidad_vigente:
            #se verifica que la palabra sea cantidad
            for numNombre in NUMEROS:
                #print("nombreES: %s numero: %s" % (nombreES, NUMEROS[nombreES]))
                if numNombre == palabra or str(NUMEROS[numNombre]) == palabra:
                    cantidad = NUMEROS[numNombre]
                    cantidad_vigente = True
                    break

        for item in MENU:
            if SQL.NormalizarTexto(item.nombreES) in palabra or SQL.NormalizarTexto(item.nombreEN) in palabra :
                item.cantidad = cantidad
                orden.append(item)
                cantidad_vigente = False
                cantidad = 1
                break


    for item in orden:
            print("id: %s, nombre: %s, cantidad: %s, precio : %s" % (item.id, item.nombreES, item.cantidad, item.precio))
            cant= int(item.cantidad)
            prec=int(item.precio)
            preciosubtotal= cant * prec

            preciototal+=preciosubtotal
    print("La cuenta total es de $ %s" % preciototal)
    return orden


if __name__ == "__main__":

    MENU = SQL.ObtenerMenu(True)
    generarTTSMenu()

    DecirSaludo()
    DecirMenu()
    PedirOrden()
    resultado = ReconocerVoz(True)
    orden = ProcesarOrden(resultado.transcripcion)
    while len(orden) == 0:
        # No se entiende lo que el cliente dice
        playsound.playsound(RUTA + "no_entiendo.mp3")
        print("DECIR: No entiendo lo que has dicho, podrias repetirlo?")
        resultado = ReconocerVoz(True)
        orden = ProcesarOrden(resultado.transcripcion)
    if ConfirmarOrden(orden) == True:
        SQL.EnviarOrden(orden)
        playsound.playsound(RUTA + 'orden_enviada.mp3')
    else:
        playsound.playsound(RUTA + 'pedido_cancelado.mp3')