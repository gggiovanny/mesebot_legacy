import pyodbc
import re
from unicodedata import normalize

esRasp = False

#server = '192.168.0.3'
#server = '10.64.51.68'
server = 'localhost\SQLEXPRESS'

if esRasp:
    driver =  'FreeTDS'
else:
    driver = 'SQL Server'
database = 'PROYECTO'
username = 'SA'
password = 'ESMINOMBRE'
if esRasp:
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';TDS_Version = 7.2;Port=1433')
else:
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
conexion = cnxn.cursor()
dispositivo = 1
numPedido=0

class Item:
    nombreES = ""
    nombreEN = ""
    id = -1
    cantidad = 0;

def EnviarOrden(orden, seMuestra = False): #Se recibe un arreglo de la clase Item que es la orden
    #Se obtiene el numero de pedido
    conexion.execute("SELECT ISNULL(COUNT(*), 0) FROM ORDEN")
    fila = conexion.fetchone()
    numPedido = fila[0] + 1
    # Se crea una nueva orden
    sq1str = "INSERT INTO ORDEN (ordID, mesaDispositivo) VALUES (" + str(numPedido) + ", " + str(dispositivo) +")"
    if seMuestra:
        print('EJECUTANDO COMANDO SQL: ' + sq1str)
    conexion.execute(sq1str)
    #Se agregan los items de la orden
    for item in orden:
        sq1str = "INSERT INTO ORDEN_ITEM(ordID, itemID, ordCantidad) VALUES (" + str(numPedido) + ", " + str(item.id) + ", " + str(item.cantidad) + ")"
        if seMuestra:
            print('EJECUTANDO COMANDO SQL: ' + sq1str)
        conexion.execute(sq1str)
    cnxn.commit()
    print('Orden enviada correctamente!')
    return numPedido


def ObtenerMenu(seMuestra = False):
    menu = []

    conexion.execute("SELECT * FROM vObtenerMenu")
    row = conexion.fetchone()
    while row:
        item = Item()
        item.id = row[0]
        item.nombreES = row[1]
        item.nombreEN = row[2]
        item.precio = row[3]
        menu.append(item)
        row = conexion.fetchone()
    if seMuestra:
        print('[Menú obtenido correctamente!]')

    return menu

def enviarPreciototal(preciototal,  seMuestra = False):
    conexion.execute(" UPDATE ORDEN SET ordPrecio = preciototal  WHERE ordID = X ")



def Probar():
    print("server: %s" % server)
    print("database: %s" % database)
    print("username: %s" % username)

    conexion.execute("SELECT @@version;")
    row = conexion.fetchone()
    while row:
        print(row[0])
        row = conexion.fetchone()

def NormalizarTexto(texto):
    texto = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
        normalize("NFD", texto), 0, re.I
    )
    texto = normalize('NFC', texto)
    return texto.lower()

#Probar()