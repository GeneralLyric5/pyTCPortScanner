import threading
import socket
from datetime import datetime
import multiprocessing
import os
import random
import time
'''
class servicioTCP(object):
    def __init__(self, puerto) -> None:
        self.puerto = puerto
'''    


def escribirFichero(autor, lista, fich):
        lock_acceso_log.acquire()
        fichero = open(fich,"a")
        tcp = "TCP service:"
        fichero.write(f'-----------------------\n{autor}\n')
        for contenido in lista:
            fichero.write(f'{tcp} {contenido}\n')
        fichero.close()
        lock_acceso_log.release()

#Añade los puertos

def animacion():
    fecha_inicio = datetime.today()
    lock_animacion.acquire()
    myOs = os.name
    listaAnimada = ["OwO","-w-","^w^"]
    comando = ""
    if myOs == "nt":
        comando = "cls"
    else:
        comando = "clear"
    
    numero = len(listaAnimada)
    while flagAnimacion:
        os.system(comando)
        fechaAhora = datetime.today() - fecha_inicio
        print(f"TCP Scan just started be pacient \nStart time: {fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')}\nTime elapsed: {fechaAhora.seconds}  seconds ")

        print(listaAnimada[random.randint(0,numero-1)])
        time.sleep(1)
    os.system(comando)
    fechaAhora = datetime.today() - fecha_inicio
    print(f"Scanner duration {fechaAhora.seconds} seconds")
    lock_animacion.release()

def anadirServiciosLista( lista,listaDePuertos):
        lock_acceso_lista_servicios.acquire()
        listaDePuertos += lista
        lock_acceso_lista_servicios.release()

def escanando(inf,super, fich,flag,listaGuardado):
    lista = []
    #print(f"{threading.current_thread().name}-{inf}-{super}")
    for puerto in range(inf,super):
        miServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        miServer.settimeout(0.12)
       
        if (0 >= miServer.connect_ex((server_ip,puerto))):
            #print(f"Servicio TCP corriendo en puerto: {puerto}")
            miServer.send("https://github.com/RustinceHD".encode("utf-8"))
            #lista.append(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}-Servicio TCP corriendo en el puerto: {puerto}\n")
            lista.append(puerto)
        else:
            pass
            #print(f"NO hay servicio TCP corriendo en puerto: {puerto}")    
        miServer.close()
    anadirServiciosLista(lista,listaGuardado)
    #escribirFichero(f"{threading.current_thread().name}" ,lista,fich)
    if flag == True:
        #print(f"Fin hilo {threading.current_thread().name} ")
        barrera.wait()
        #print(f"Barrera PASADA {threading.current_thread().name} ")
try:
    domain = input("Introduzca la dominio del serveidor: ")
    #domain = "fr1.cheetahost.com"
    server_ip = socket.gethostbyname(domain)
    PORT1 =  int(input("Introduzca el puerto inferior: "))
    PORT2 =  int(input("Introduzca el puerto superior: "))
    fich = input("Introduzca el nombre del fichero de log: ")
    fich = f"{datetime.today().strftime('%Y-%m-%d')}"+fich +".txt"
    f = open(fich,"w")
    f.write(f"---------------------------------\nDominio: {domain}\nIp Servidor: {server_ip}\nRango de puertos: {PORT1}-{PORT2}\nLog OutPut: {fich}\n---------------------------------\n")
    f.close()
except ValueError:
    print("La entrada no es un número entero válido.")
    exit(-1)


n = 0
listaDePuertos = []
multiplayer = 20
num_cores = multiprocessing.cpu_count()
print("Number of CPU cores:", num_cores)
lock_acceso_lista_servicios = threading.Lock()
lock_acceso_log = threading.Lock()
lock_animacion = threading.Lock()


flagAnimacion = True
procesos = num_cores  

animacioChula =  hilo = threading.Thread(target=animacion)
animacioChula.start()
if ((len(range(PORT1,PORT2+1)) // (num_cores*multiplayer)) >= 1 ):
    rangoPuertos = (len(range(PORT1,PORT2+1)) // (num_cores*multiplayer))

    if ((len(range(PORT1,PORT2+1)) % (num_cores*multiplayer)) == 0):
        #print(f"ESTADO EXACTO SIN HILO EXTRA {len(range(PORT1,PORT2+1))}-{rangoPuertos}")
        numHilos = (num_cores*multiplayer) + 1
    else:
        #print(f"ESTADO HILO EXTRA?? {(len(range(PORT1,PORT2+1)))}-{rangoPuertos + 1}")
        numHilos = (num_cores*multiplayer) + 2
    #print(f"{numHilos}_____________")
    barrera = threading.Barrier(numHilos)

    for n in range(num_cores*multiplayer):
        print(f"{(PORT1 + rangoPuertos*n)}-{(PORT1 + rangoPuertos*(n+1))}--{threading.current_thread().name}--{n}")
        hilo = threading.Thread(target=escanando, args = ((PORT1 + rangoPuertos*n),(PORT1 + rangoPuertos*(n+1)), fich, True,listaDePuertos))
        hilo.start()
    
    if (rangoPuertos*(n+1) < PORT2 ):
        n +=1
        print(f"{(PORT1 + rangoPuertos*(n+1))}-{(PORT2)}--{threading.current_thread().name}--{n}")
        hilo = threading.Thread(target=escanando, args = ((PORT1 + rangoPuertos*(n+1)),(PORT2), fich, True,listaDePuertos))
        hilo.start()
    barrera.wait()
    flagAnimacion = False
    lock_animacion.acquire()

else:
     pass
        #print(f"{(PORT1 )}-{(PORT2)}--{threading.current_thread().name}--{n}")
        #escanando(PORT1 ,PORT2 + 1, fich, False,listaDePuertos)

listaDePuertos.sort()
escribirFichero(f"{threading.current_thread().name}" ,listaDePuertos,fich)
print(f"---------------------------------\nDomain: {domain}\nServer Ip : {server_ip}\nPorts range: {PORT1}-{PORT2}\nLog OutPut: {fich}\n---------------------------------\n") 
print(f"--TCP scan finished--")
for puertoCOnsola in listaDePuertos:
     print(f"TCP service running in: {puertoCOnsola}")
lock_animacion.release()
'''
for hilo in threading.enumerate ():
  print (f"{hilo.name} Hilo activo")
'''
