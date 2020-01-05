# Administrador de IAs para MicroEvoBrains por Omarsaurio 2020

"""
MicroEvoBrains ejecuta una simulacion de agentes en un entorno
competitivo, tiene sus propias IAs internas, pero puede tambien
utilizar IAs personalizadas externas, despues de que se respete
la trama de datos UDP, cualquier lenguaje o software puede
conectarse.
"""

# librerias indispensables para funcionamiento
import numpy as np
import matplotlib.pyplot as plt
import socket
import threading
import time

# librerias de los cerebros
from brainDMNN1 import brainAI as dmnn1
from brainDMNN2 import brainAI as dmnn2
from brainMLP1 import brainAI as mlp1
from brainMLP2 import brainAI as mlp2
from brainOmi1 import brainAI as omi1

# variables de configuracion
entradas = 23
salidas = 6
tipo = [dmnn1, dmnn2, omi1, mlp1, mlp2]
debugmode = False

# variables de funcionamiento
tareaTimeout = 3
limpiarTimeout = 6
pingTimeout = 2
ipport = ("", 0)
UDP = None
miport = 0
tareas = [] # id agente, tipo, acum fitness, segundos, entradas
cerebros = [] # id agente, tipo, objeto cerebro, tiempo uso
datines = []
patrones = []
mejor = [-1 for i in range(len(tipo))]
fatales = [0 for i in range(len(tipo))]
salir = False
# max cerebros, msj repetido, msj timeout, msj total, time inicio
lainfo = [0, 0, 0, 0, 0]

def main():
    global salir
    print("***Administrador IAs para MicroEvoBrains***")
    print("")
    iniciarUDP()
    print("")
    rx = threading.Thread(target=reciveUDP)
    rx.start()
    ci = threading.Thread(target=ciclo)
    ci.start()
    print("***Consola***")
    print("(ayuda)")
    print("")
    while not salir:
        consola()
    finalizarUDP()
    exit()

def consola():
    global salir
    global mejor
    global tareas
    global tipo
    global cerebros
    global lainfo
    global datines
    global patrones
    global fatales
    sel = input("-> ")
    if sel == "salir":
        salir = True
    elif sel == "grafica":
        guardado("rescate")
        grafica()
    elif sel == "informacion":
        todaInformacion()
    elif sel == "aleatorizar":
        for ce in cerebros:
            ce[2].__init__()
    elif sel == "abrir":
        abierto("cerebro")
    elif sel == "guardar":
        guardado("cerebro")
    elif sel == "resetear":
        mejor = [-1 for i in range(len(tipo))]
        fatales = [0 for i in range(len(tipo))]
        cerebros = []
        tareas = []
        datines = []
        patrones = []
        for i in range(len(lainfo)):
            lainfo[i] = 0
    elif sel == "limpgrafica":
        datines = []
    elif sel == "limpatrones":
        patrones = []
    elif sel == "limpinfo":
        fatales = [0 for i in range(len(tipo))]
        for i in range(len(lainfo)):
            lainfo[i] = 0
    elif sel == "patrones":
        ordenPatrones()
    elif sel == "dataset":
        guardaPatrones()
    elif sel == "conectar":
        conectar()
    elif sel == "configurar":
        configurar()
    elif sel == "t+":
        tempo(True)
    elif sel == "t-":
        tempo(False)
    elif sel == "alimento":
        alimento()
    elif sel == "seguir":
        ordenSeguir()
    elif sel == "visual":
        visual()
    elif sel == "reiniciar":
        reiniciar()
    elif sel == "cuantos":
        cuantos()
    elif sel == "renovar":
        renovar()
    elif sel == "demo":
        demo()
    elif sel == "savegrafi":
        saveGrafica()
    elif sel == "flags":
        flagsss()
    elif sel == "controles":
        print("***Controles Simulacion***")
        print("- Zoom con rueda del mouse")
        print("- Escape x2 salir")
        print("- Escape + Shift reiniciar")
        print("- F4 pantalla completa")
        print("- F10 foto de pantalla")
        print("- (+) acelerar, (-) desacelerar, simulacion")
        print("- Suprimir ver hijos o generaciones en agente")
        print("- Tab ver/no sensores")
        print("- (*) + demora (/) - demora, crear alimento")
        print("- P,O crear/eliminar muro en posicion mouse")
        print("- I,U crear/eliminar alimento en posicion mouse")
        print("***Manejo Manual***")
        print("- W,A,S,D o flechas Up,Left,Down,Right mover")
        print("- Q,E rotacion en sitio")
        print("- V,Espacio disparar")
        print("- B fecundar huevo cercano")
        print("- N donar alimento a cercano")
        print("- M gritar")
    elif sel == "acercade":
        print("***Acerca De***")
        print("Administrador de IAs para MicroEvoBrains")
        print("por Omarsaurio 2020, ojorcio@gmail.com")
        print("https://www.deviantart.com/omarsaurus")
        print("https://gamejolt.com/@PersonajeX")
        print("***Agente***")
        print("Sensores (23):")
        print("- de alimento: olor, tacto, vision, rayo")
        print("- de muros: tacto, vision, rayo")
        print("- de agentes: tacto")
        print("- de misma especie: olor, vision, rayo, calor, oido")
        print("- de otra especie: olor, vision, rayo, calor, oido")
        print("- de huevo: rastreo")
        print("- internos: calor, tiempo")
        print("       olor es concentracion de objetos en area")
        print("       tacto es direccion si izquierda o derecha")
        print("       vision es direccion del mas proximo en cono de vision")
        print("       rayo es distancia del mas proximo al frente")
        print("       calor es energia, si es de otro, segun rayo")
        print("       oido es direccion del promedio de sonidos en area")
        print("       rastreo es cercania al mas cercano en area")
        print("       tiempo es edad del agente, nacimiento a muerte")
        print("Actuadores (6):")
        print("  moverse hacia el frente, rotar izquierda o derecha,")
        print("  disparar, dar alimento, fretilizar huevo, gritar")
        print("Nota:")
        print("  la variable global 'tipo' tiene a las clases importadas")
        print("  de algoritmos IA, cambie alli los algoritmos a su gusto,")
        print("  respetando las reglas que contiene el archivo templateIA.py")
        print("Error:")
        print("  actualmente hay un bug al graficar, colapsa el codigo")
    elif sel == "ayuda":
        print("***Comandos***")
        print("acercade, salir, grafica, informacion, ayuda,")
        print("abrir, guardar, aleatorizar, resetear, patrones,")
        print("limpgrafica, limpatrones, limpinfo, dataset,")
        print("conectar, configurar, alimento, seguir, visual,")
        print("savegrafi, reiniciar, cuantos, renovar, demo,")
        print("flags, t+, t-, controles, diccionario")
    elif sel == "diccionario":
        print("***Comandos Descripcion***")
        print("acercade: muestra informacion del software")
        print("ayuda, diccionario: muestran comandos y su descripcion")
        print("informacion: UDP, algoritmos IA y estadisticas de funcionamiento")
        print("grafica, savegrafi: pinta la grafica de fitness y la guarda (txt)")
        print("guardar: en varios txt, los mejores algoritmos alcanzados")
        print("abrir: carga los mejores algoritmos con los txt antes salvados")
        print("aleatorizar: ejecuta de nuevo la inicializacion de algoritmos")
        print("resetear: reinicia los parametros internos de este software")
        print("patrones: define que tipo de agente enviara datos e/s cada 1s")
        print("dataset: guarda los patrones obtenidos a un txt")
        print("limpiagrafica, limpiapatrones, limpinfo: limpieza variables")
        print("conectar: envia a la simulacion la ip y puerto de este socket")
        print("configurar: elige tipo de algoritmo y cantidad de agentes")
        print("alimento: parametriza la taza de aparicion de alimento")
        print("seguir: define el tipo de agente que sera seguido por la camara")
        print("visual: flags visuales de la simulacion, uno es para ver sensores")
        print("reiniciar: reinicia la simulacion, no este software (resetear)")
        print("cuantos: cambia la cantidad inicial de agentes para un tipo")
        print("renovar: fuerza a la simulacion a relanzar")
        print("demo: valores por defecto para correr simulacion")
        print("flags: de simulacion, afectan el comportamiento global")
        print("t+,t-: aumento/disminucion de velocidad de simulacion")
        print("controles: comandos del software de simulacion")
    else:
        print("?")
    print("")

def todaInformacion():
    global tipo
    global cerebros
    global tareas
    global lainfo
    global patrones
    global datines
    global fatales
    resel = input("0-UDP, 1-Cerebros, 2-General: ")
    if resel == "0":
        informacionUDP()
    elif resel == "1":
        print("***Tipos de Cerebro***")
        for i in range(len(tipo)):
            try:
                print(tipo[i]().about())
                print("...")
            except:
                print("Void slot...")
                print("...")
    elif resel == "2" or resel == "":
        print("***Informacion General***")
        print("cerebros: " + str(len(cerebros)) + " / " + str(lainfo[0]) + "max")
        print("ordenes: " + str(len(tareas)) + " / " + str(lainfo[3]) + "tot")
        z = round((lainfo[1] / max(1, lainfo[3])) * 10000.0) / 100
        print("   repetidas: " + str(z) + "%")
        z = round((lainfo[2] / max(1, lainfo[3])) * 10000.0) / 100
        print("   timeout: " + str(z) + "%")
        print("Tiempo: " + str(round(time.time() - lainfo[4])) + "s")
        print("Patrones: " + str(len(patrones)))
        print("Grafica: " + str(len(datines)))
        print("Errores de cada IA (0 a 9):")
        print("  e: " + str(fatales))

def saveGrafica():
    global datines
    nn = input("? nombre archivo (guardar grafica): ")
    if nn != "":
        if ".txt" in nn:
            fff = open(nn, "w")
        else:
            fff = open(nn + ".txt", "w")
        txt = "Grafica de MicroEvoBrains\n" \
              "muestreo 1s sin contar escala de simulacion (x1)\n"
        for d in datines:
            v = ""
            for i in d:
                v += str(i) + ","
            txt += v[:-1] + "\n"
        fff.write(txt)
        fff.close()

def guardado(titulo):
    global mejor
    for i in range(len(mejor)):
        mic = buscaCerebro(mejor[i], i, False)
        if mic != None:
            try:
                txt = mic[2].exportIA()
                fff = open(titulo + str(i) + ".txt", "w")
                fff.write(txt)
                fff.close()
            except:
                debug("guardando cerebro")

def abierto(titulo):
    global mejor
    for i in range(len(mejor)):
        mic = buscaCerebro(mejor[i], i, False)
        if mic != None:
            try:
                fff = open(titulo + str(i) + ".txt", "r")
                txt = fff.read()
                fff.close()
                mic[2].importIA(txt)
            except:
                debug("abriendo cerebro")

def alimento():
    global UDP
    global ipport
    buf = bytearray(3)
    buf[0] = 13
    f = teclado(True, "? digite probabilidad agrupar alimento (vacio 0.25): ", 0.25)
    buf[1] = int(min(1, max(0, f)) * 255)
    buf[2] = int(teclado(True, "? digite demora crear alimento (vacio 20): ", 20))
    UDP.sendto(buf, ipport)

def configurar():
    global UDP
    global ipport
    global tipo
    buf = bytearray(1 + 2 * len(tipo))
    buf[0] = 12
    for i in range(len(tipo)):
        print("agente " + str(i) + ":")
        buf[7 + i * 2] = int(teclado(True, "? digite 0-UDP, 1-MLP, 2-Basic, 3-manual: ", 0))
        buf[8 + i * 2] = int(teclado(True, "? digite cantidad de agentes: ", 0))
    UDP.sendto(buf, ipport)

def flagsss():
    global UDP
    global ipport
    global tipo
    buf = bytearray(7)
    buf[0] = 21
    buf[1] = int(teclado(True, "? digite 0 si No envejecer (vacio 1): ", 1))
    buf[2] = int(teclado(True, "? digite 0 si No desnutrir (vacio 1): ", 1))
    buf[3] = int(teclado(True, "? digite 0 si No procrear (vacio 1): ", 1))
    buf[4] = int(teclado(True, "? digite 0 si No fitness edad (vacio 0): ", 0))
    buf[5] = int(teclado(True, "? digite 0 si No forzar reinicio (vacio 1): ", 1))
    buf[6] = int(teclado(True, "? digite id para, donde aparecen los agentes\n"
                               "  0-azar, 1-esquinas, 2-origen, 3-centro,\n"
                               "  4-agrupados (vacio 0): ", 0))
    UDP.sendto(buf, ipport)

def demo():
    global UDP
    global ipport
    global tipo
    buf = bytearray(1 + 2 * len(tipo))
    buf[0] = 12
    for i in range(len(tipo)):
        buf[7 + i * 2] = 0
        buf[8 + i * 2] = 5
    buf[12] = 1
    UDP.sendto(buf, ipport)
    buf = bytearray(7)
    buf[0] = 21
    buf[1] = 1
    buf[2] = 1
    buf[3] = 1
    buf[4] = 0
    buf[5] = 1
    buf[6] = 0
    UDP.sendto(buf, ipport)

def visual():
    global UDP
    global ipport
    buf = bytearray(3)
    buf[0] = 15
    buf[1] = int(teclado(True, "? digite 0 para que el numero sobre los agentes\n"
                               "  sea la generacion, sino hijos (vacio 0): ", 0))
    buf[2] = int(teclado(True, "? digite 0 si No mostrar sensores (vacio 0): ", 0))
    UDP.sendto(buf, ipport)

def tempo(subir):
    global UDP
    global ipport
    buf = bytearray(1)
    buf[0] = (16 if subir else 17)
    UDP.sendto(buf, ipport)

def renovar():
    global UDP
    global ipport
    buf = bytearray(1)
    buf[0] = 20
    UDP.sendto(buf, ipport)

def conectar():
    global UDP
    global ipport
    buf = bytearray(1)
    buf[0] = 11
    UDP.sendto(buf, ipport)

def reiniciar():
    global UDP
    global ipport
    buf = bytearray(1)
    buf[0] = 18
    UDP.sendto(buf, ipport)

def ordenSeguir():
    global UDP
    global ipport
    buf = bytearray(2)
    buf[0] = 14
    buf[1] = int(teclado(True, "? digite indice de criatura que sera seguida\n"
                               "  por la camara, vacio ninguna (modo mouse) y\n"
                               "  254 para seguir a cualquiera: ", 255))
    UDP.sendto(buf, ipport)

def cuantos():
    global UDP
    global ipport
    buf = bytearray(3)
    buf[0] = 19
    buf[1] = int(teclado(True, "? digite indice de criaturas a editar su poblacion\n"
                               "  inicial, (vacio ninguna): ", 255))
    if buf[1] == 255:
        buf[2] = 0
    else:
        buf[2] = int(teclado(True, "? digite cantidad de agentes: ", 0))
    UDP.sendto(buf, ipport)

def ordenPatrones():
    global UDP
    global ipport
    buf = bytearray(2)
    buf[0] = 10
    buf[1] = int(teclado(True, "? digite indice de criatura que dara patrones\n"
                               "  solo una enviara / s, (vacio ninguna): ", 255))
    UDP.sendto(buf, ipport)

def guardaPatrones():
    global patrones
    nn = input("? nombre archivo (guardar patrones): ")
    if nn != "":
        if ".txt" in nn:
            fff = open(nn, "w")
        else:
            fff = open(nn + ".txt", "w")
        txt = "Patrones: Agente Evolutivo de MicroEvoBrains\n" \
            "Salidas: move, rotate, attack, give, fertilize, scream\n" \
            "Entradas: smellfood, smellsame, smellother, touchfood, " \
            "touchwall, touchagent, visionfood, visionwall, visionsame, " \
            "visionother, rayfood, raywall, raysame, rayother, warmsame, " \
            "warmother, hearsamex, hearotherx, hearsamey, hearothery, " \
            "trackingegg, energy, age\n"
        for p in patrones:
            v = ""
            for i in p:
                v += str(i) + ","
            txt += v[:-1] + "\n"
        fff.write(txt)
        fff.close()

def grafica():
    global datines
    dat = np.array(datines, dtype=float)
    col = ['r', 'm', 'y', 'c', 'b']
    for c in range(len(col)):
        plt.plot(dat[:, c], c=col[c])
    plt.show()

def ciclo():
    global salir
    global pingTimeout
    global UDP
    global miport
    ping = time.time()
    while not salir:
        asignarTareas()
        limpieza()
        # hacer ping a el mismo
        acpin = time.time()
        if acpin - ping >= pingTimeout:
            ping = acpin
            buf = bytearray(1)
            buf[0] = 7
            UDP.sendto(buf, ("127.0.0.1", miport))

def limpieza():
    global cerebros
    global UDP
    global ipport
    for cer in cerebros:
        if time.time() - cer[3] >= limpiarTimeout:
            cer[3] = time.time()
            buf = bytearray(5)
            buf[0] = 5
            buf[1:5] = (int(cer[0])).to_bytes(4, byteorder="little", signed=False)
            UDP.sendto(buf, ipport)

def asignarTareas():
    global tareas
    global tareaTimeout
    global lainfo
    try:
        tll = len(tareas)
        if tll > 0:
            # buscar primera tarea en lista, cualquier agente
            una = tareas.pop(0)
            tll -= 1
            t = 0
            # verificar que sea la tarea mas reciente para ese agente
            while t < tll:
                if tareas[t][0] == una[0]:
                    una = tareas.pop(t)
                    lainfo[1] += 1
                    tll -= 1
                else:
                    t += 1
            # verificar no sea orden vieja
            if time.time() - una[3] < tareaTimeout:
                # buscar cerebro del agente
                mic = buscaCerebro(una[0], una[1], True)
                if mic != None:
                    # asignar ejecucion al cerebro
                    tx = threading.Thread(target=ejecutar, args=[mic, una[4], una[2]])
                    tx.start()
            else:
                lainfo[2] += 1
    except:
        debug("asignando tarea")

def ejecutar(quien, inputs, fitness):
    global salidas
    global UDP
    global ipport
    global fatales
    try:
        try:
            res = quien[2].execute(inputs, fitness)
        except:
            res = None
            fatales[quien[1]] = min(9, fatales[quien[1]] + 1)
        quien[3] = time.time()
        if res.size == salidas:
            res = np.clip(np.round(res * 100.0), -100, 100)
            buf = bytearray(5 + salidas)
            buf[0] = 1
            buf[1:5] = (int(quien[0])).to_bytes(4, byteorder="little", signed=False)
            for s in range(salidas):
                e = (int(res[s])).to_bytes(1, byteorder="little", signed=True)
                buf[5 + s] = (int).from_bytes(e, byteorder="little", signed=False)
            UDP.sendto(buf, ipport)
        else:
            fatales[quien[1]] = min(9, fatales[quien[1]] + 1)
    except:
        debug("ejecutando tarea")

def reproduccion(hijo, ti, madre, padre):
    try:
        mic = buscaCerebro(hijo, ti, True)
        if mic != None:
            ma = buscaCerebro(madre, ti, False)
            if ma != None:
                pa = buscaCerebro(padre, ti, False)
                mic[2].spawn(ma, pa)
    except:
        debug("en reproduccion")

def ancestral(hijo, ti, mut):
    global mejor
    try:
        mic = buscaCerebro(hijo, ti, True)
        if mic != None:
            elite = buscaCerebro(mejor[ti], ti, False)
            if elite != None:
                if mut == 0:
                    mic[2] = elite[2].copy()
                else:
                    mic[2].spawn(elite[2], None)
    except:
        debug("en ancestral")

def buscaCerebro(ind, ti, crear):
    global cerebros
    global tipo
    global lainfo
    # buscar cerebro del agente
    mic = None
    for cer in cerebros:
        if cer[0] == ind:
            mic = cer
            break
    # crear cerebro si no existe
    if mic == None and tipo[ti] != None and crear:
        mic = []
        mic.append(ind)
        mic.append(ti)
        mic.append(tipo[ti]())
        mic.append(time.time())
        cerebros.append(mic)
        tot = len(cerebros)
        if tot > lainfo[0]:
            lainfo[0] = tot
    return mic

def iniciarUDP():
    global UDP
    global ipport
    global miport
    print("***Server UDP***")
    try:
        port = input("Mi Puerto (vacio 2020): ")
        if port == "":
            port = 2020
        else:
            port = int(port)
        UDP = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDP.bind(("127.0.0.1", port))
        miport = port
        port = input("Puerto Simulacion (vacio 2021): ")
        if port == "":
            port = 2021
        else:
            port = int(port)
        ip = input("IP Simulacion (vacio local): ")
        if ip == "":
            ip = "127.0.0.1"
        ipport = (ip, port)
        print("Server Go...")
    except:
        UDP = None
        print("Error...")
        exit()

def informacionUDP():
    global ipport
    global miport
    print("***Informacion UDP***")
    print("IP Simulacion: " + ipport[0])
    print("Puerto Simulacion: " + str(ipport[1]))
    print("Mi IP: " + socket.gethostbyname(socket.gethostname()))
    print("Mi Puerto: " + str(miport))

def reciveUDP():
    global UDP
    global tareas
    global entradas
    global salidas
    global mejor
    global cerebros
    global salir
    global lainfo
    global datines
    global patrones
    time.sleep(0.5)
    bt = np.array([1, 256, 65536, 16777216], dtype=int)
    while not salir:
        try:
            buf = bytearray(256)
            UDP.recv_into(buf)
            ind = int(buf[0])
            # significa que recibe entradas
            if ind == 0:
                vec = []
                vec.append(np.sum(np.array(buf[1:5], dtype=np.uint8) * bt))
                vec.append(int(buf[5]))
                vec.append(np.array(buf[6:10], dtype=np.uint8).view(dtype=np.float32)[0])
                vec.append(time.time())
                ent = []
                for e in range(entradas):
                    ent.append(np.array(buf[10 + e], dtype=np.int8))
                vec.append(np.array(ent, dtype=float) / 100.0)
                tareas.append(vec)
                lainfo[3] += 1
                if lainfo[4] == 0:
                    lainfo[4] = time.time()
            # significa que recibe reproduccion
            elif ind == 2:
                hijo = np.sum(np.array(buf[1:5], dtype=np.uint8) * bt)
                ti = int(buf[5])
                madre = np.sum(np.array(buf[5:9], dtype=np.uint8) * bt)
                padre = np.sum(np.array(buf[9:13], dtype=np.uint8) * bt)
                reproduccion(hijo, ti, madre, padre)
            # significa que recibe a los mejores
            elif ind == 3:
                for m in range(len(mejor)):
                    mejor[m] = np.sum(np.array(buf[(1 + m * 4):(5 + m * 4)],
                                               dtype=np.uint8) * bt)
            # significa que recibe ancestral
            elif ind == 4:
                hijo = np.sum(np.array(buf[1:5], dtype=np.uint8) * bt)
                ti = int(buf[5])
                mut = int(buf[10])
                ancestral(hijo, ti, mut)
            # significa que recibe eliminacion
            elif ind == 6:
                eli = np.sum(np.array(buf[1:5], dtype=np.uint8) * bt)
                for c in range(len(cerebros)):
                    if cerebros[c][0] == eli:
                        cerebros.pop(c)
                        break
            # significa que recibe un simple ping
            elif ind == 7:
                pass
            # significa que recibe puntos para graficar
            elif ind == 8:
                vec = np.zeros(len(mejor), dtype=float)
                for m in range(len(mejor)):
                    vec[m] = np.array(buf[(1 + m * 4):(5 + m * 4)],
                                      dtype=np.uint8).view(dtype=np.float32)[0]
                datines.append(vec)
            # significa que recibe patrones
            elif ind == 9:
                pat = []
                for p in range(entradas + salidas):
                    pat.append(np.array(buf[1 + p], dtype=np.int8))
                patrones.append(np.array(pat, dtype=float) / 100.0)
        except:
            debug("recibiendo mensaje UDP")

def finalizarUDP():
    global UDP
    UDP.close()
    print("Server Off...")

def teclado(esnum, mensaje, defecto):
    while True:
        txt = input(mensaje)
        if txt == "":
            return defecto
        elif esnum:
            try:
                num = float(txt)
                return num
            except:
                pass
        else:
            return txt

def debug(mensaje):
    global debugmode
    if debugmode:
        print("error: " + mensaje)

main()

"""
Tareas:
- al graficar, tiempo despues aparece error fatal con hilos
  guarda cerebros en txt por si acaso
"""
