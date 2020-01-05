# Cerebro Neurotico by Omarsaurio 2019 (ojorcio@gmail.com)
"""
v1.0.2 cambiar cuando se valla a publicar
La funcion de este codigo es brindar las herramientas para crear y administrar
redes neuronales DMNN y MLP, enfocadas en algoritmos heuristicos como lo son
los evolutivos, por ello aun no tiene funciones de backpropagation, en cambio
ofrece reproduccion sexual con aumento o disminucion de neuronas/dendritas, fue
pensado para enfrentar a las dos redes en simulacion de agentes evolutivos
donde en lugar de optimizar fenotipos, se optimiza el comportamiento.
Las clases a usar son: redDMNN y redMLP (las otras serian privadas).
"""
import numpy as np

class redDMNN(object):

    def __init__(self, entradas, salidas, limite, numdend):
        self.limite = limite
        self.neuras = []
        sal = max(1, salidas)
        for n in range(sal):
            self.neuras.append(neuronaDMNN(max(1, entradas), limite,
                                           int(max(1, np.ceil(numdend / sal)))))

    def numunits(self):
        nd = 0
        for neu in self.neuras:
            nd += len(neu.dendras)
        return nd

    def exportar(self, archivo):
        if archivo != "":
            txt = self.guardar()
            if ".txt" in archivo:
                fff = open(archivo, "w")
            else:
                fff = open(archivo + ".txt", "w")
            fff.write(txt)
            fff.close()
            return True
        else:
            return False

    def guardar(self):
        info = self.informacion(False)
        txt = "Red DMNN by Omarsaurio:\n"
        txt += "limite, entradas, salidas, dendritas, pesos\n"
        txt += "{},{},{},{},{}\n".format(info[0], info[1], info[2],
                                         info[3], info[4])
        for neu in self.neuras:
            txt += neu.guardar()
        return txt

    def importar(self, archivo):
        if archivo != "":
            if ".txt" in archivo:
                fff = open(archivo, "r")
            else:
                fff = open(archivo + ".txt", "r")
            dat = fff.read()
            fff.close()
            return self.abrir(dat)
        else:
            return False

    def abrir(self, texto):
        if "DMNN" in texto:
            dat = texto.split("neurona")
            info = dat[0].split("\n")
            info = info[2].split(",")
            self.limite = float(info[0])
            self.neuras = []
            for n in range(len(dat) - 1):
                self.neuras.append(neuronaDMNN(int(info[1]), self.limite, 1))
                self.neuras[-1].abrir(dat[n + 1])
            return True
        else:
            return False

    def informacion(self, ver):
        info = []
        info.append(self.limite)
        info.append(self.neuras[0].dendras[0].oriW.size)
        info.append(len(self.neuras))
        info.append(self.numunits())
        info.append(info[3] * info[1] * 2)
        if ver:
            print("Red DMNN by Omarsaurio:\nlimite: {}\n".format(info[0]) +
                  "entradas: {}\nsalidas: {}\ndendritas: {}\npesos: {}".format(
                      info[1], info[2], info[3], info[4]))
        return info

    def copiar(self, origen):
        self.limite = origen.limite
        ent = origen.neuras[0].dendras[0].oriW.size
        neuronas = []
        for neu in origen.neuras:
            neuronas.append(neuronaDMNN(ent, self.limite, 1))
            neuronas[-1].copiar(neu)
        self.neuras = neuronas

    def copy(self):
        aux = redDMNN(1, 1, 1, 1)
        aux.copiar(self)
        return aux

    def ejecutar(self, datos, activ):
        res = np.zeros(len(self.neuras), dtype=float)
        for n in range(len(self.neuras)):
            res[n] = self.neuras[n].ejecutar(datos, activ)
        return res

    def competir(self, datos, activ):
        vec = np.reshape(self.ejecutar(datos, False), (2, -1))
        if activ:
            return activacion(np.subtract(vec[0, :], vec[1, :]))
        else:
            return np.subtract(vec[0, :], vec[1, :])

    def clasificar(self, datos):
        return np.argmax(self.ejecutar(datos, False))

    def subclasificar(self, datos):
        vec = np.reshape(self.ejecutar(datos, False), (2, -1))
        return np.argmax(vec, axis=0)

    def probabilidad(self):
        vec = np.zeros(len(self.neuras), dtype=float)
        for n in range(len(self.neuras)):
            vec[n] = len(self.neuras[n].dendras)
        return vec / vec.sum()

    def editar(self, proba, vacio=0):
        if np.random.rand(1)[0] < proba:
            if np.random.rand(1)[0] < 0.5:
                self.reducir()
            else:
                self.aumentar()

    def reducir(self):
        dado = np.random.rand(1)[0]
        prob = self.probabilidad()
        for n in range(prob.size):
            if dado < prob[:(n + 1)].sum():
                self.neuras[n].reducir()
                break

    def aumentar(self):
        dado = np.random.rand(1)[0]
        prob = 1.0 - self.probabilidad()
        prob /= max(1.0, prob.sum())
        for n in range(prob.size):
            if dado < prob[:(n + 1)].sum():
                self.neuras[n].aumentar(self.limite)
                break

    def aleatorizar(self):
        for neu in self.neuras:
            neu.aleatorizar(self.limite)

    def dividir(self, madre, fuerza, cantidad, full):
        self.copiar(madre)
        self.mutar(fuerza, cantidad, full)

    def mutar(self, fuerza, cantidad, full):
        for neu in self.neuras:
            neu.mutar(fuerza, cantidad, self.limite, full)

    def combinar(self, madre, padre, relleno, full):
        self.limite = madre.limite
        ent = madre.neuras[0].dendras[0].oriW.size
        self.neuras = []
        for n in range(len(madre.neuras)):
            self.neuras.append(neuronaDMNN(ent, self.limite, 1))
            self.neuras[-1].combinar(madre.neuras[n], padre.neuras[n], relleno, full)

    def grafica2D(self, clasi):
        xx = []
        yy = []
        cc = []
        if self.neuras[0].dendras[0].oriW.size == 2:
            for x in range(int(-self.limite), int(self.limite + 1)):
                for y in range(int(-self.limite), int(self.limite + 1)):
                    xx.append(x)
                    yy.append(y)
                    if clasi:
                        cc.append(self.clasificar(np.array([x, y], dtype=float)))
                    else:
                        res = self.ejecutar(np.array([x, y], dtype=float), True)
                        if res.size > 1:
                            if res[0] >= 0:
                                if res[1] >= 0:
                                    cc.append('red')
                                else:
                                    cc.append('orange')
                            else:
                                if res[1] >= 0:
                                    cc.append('yellow')
                                else:
                                    cc.append('blue')
                        else:
                            if res[0] >= 0:
                                cc.append('red')
                            else:
                                cc.append('blue')
        # plt.scatter(xx, yy, c=cc)
        # plt.show()
        return xx, yy, cc

class neuronaDMNN(object):

    def __init__(self, entradas, limite, numdend):
        self.dendras = []
        for d in range(numdend):
            self.dendras.append(dendritaDMNN(entradas, limite))

    def guardar(self):
        txt = "neurona\n"
        for den in self.dendras:
            txt += den.guardar()
        return txt

    def abrir(self, txt):
        self.dendras = []
        dat = txt.replace("neurona", "").split("\n")
        for d in dat:
            if d != "":
                self.dendras.append(dendritaDMNN(1, 1))
                self.dendras[-1].abrir(d)

    def copiar(self, origen):
        self.dendras = []
        for den in origen.dendras:
            self.dendras.append(dendritaDMNN(1, 1))
            self.dendras[-1].copiar(den)

    def ejecutar(self, datos, activ):
        S = np.zeros(len(self.dendras), dtype=float)
        for d in range(S.size):
            S[d] = self.dendras[d].ejecutar(datos)
        if activ:
            return activacion(np.max(S))
        else:
            return np.max(S)

    def reducir(self):
        dend = len(self.dendras)
        if dend > 1:
            self.dendras.pop(np.random.randint(dend))

    def aumentar(self, limite):
        ent = self.dendras[0].oriW.size
        self.dendras.append(dendritaDMNN(ent, limite))

    def aleatorizar(self, limite):
        ent = self.dendras[0].oriW.size
        for den in self.dendras:
            den.aleatorizar(ent, limite)

    def mutar(self, fuerza, cantidad, limite, full):
        if full:
            for den in self.dendras:
                den.remutar(fuerza, cantidad, limite)
        else:
            for den in self.dendras:
                den.mutar(fuerza, cantidad, limite)

    def combinar(self, madre, padre, relleno, full):
        self.dendras = []
        for dm in madre.dendras:
            igual = None
            for dp in padre.dendras:
                if dm.id == dp.id:
                    igual = dp
                    break
            if igual != None:
                self.dendras.append(dendritaDMNN(1, 1))
                if full:
                    self.dendras[-1].recombinar(dm, igual)
                else:
                    self.dendras[-1].combinar(dm, igual)
            elif np.random.rand(1)[0] < relleno:
                self.dendras.append(dendritaDMNN(1, 1))
                self.dendras[-1].copiar(dm)
        for dp in padre.dendras:
            igual = None
            for dm in madre.dendras:
                if dp.id == dm.id:
                    igual = dm
                    break
            if igual == None and np.random.rand(1)[0] < relleno:
                self.dendras.append(dendritaDMNN(1, 1))
                self.dendras[-1].copiar(dp)
        if len(self.dendras) == 0:
            self.dendras.append(dendritaDMNN(1, 1))
            self.dendras[-1].copiar(madre.dendras[0])

class dendritaDMNN(object):

    def __init__(self, entradas, limite):
        self.aleatorizar(entradas, limite)
        self.id = np.random.rand(1)[0]

    def guardar(self):
        txt = str(self.id) + ":"
        for n in self.oriW:
            txt += str(n) + ","
        txt = txt[:-1] + "|"
        for n in self.cajW:
            txt += str(n) + ","
        txt = txt[:-1] + "\n"
        return txt

    def abrir(self, txt):
        dat = txt.replace("\n", "").split(":")
        self.id = float(dat[0])
        dat = dat[1].split("|")
        ori = dat[0].split(",")
        caj = dat[1].split(",")
        self.oriW = np.array(ori, dtype=float)
        self.cajW = np.array(caj, dtype=float)

    def copiar(self, origen):
        self.oriW = origen.oriW.copy()
        self.cajW = origen.cajW.copy()
        self.id = origen.id

    def ejecutar(self, datos):
        L = datos - (self.oriW - self.cajW)
        H = (self.oriW + self.cajW) - datos
        return np.min(np.minimum(L, H))

    def aleatorizar(self, entradas, limite):
        self.oriW = (-1.0 + np.random.rand(entradas) * 2.0) * limite
        self.cajW = (0.5 + np.random.rand(entradas) * 0.5) * limite * 0.15

    def mutar(self, fuerza, cantidad, limite):
        if np.random.rand(1)[0] < cantidad:
            movesc = np.random.rand(1)[0]
            if movesc < 0.7:
                self.oriW = np.clip(self.oriW +
                                    (-1.0 + np.random.rand(self.oriW.size) * 2.0) *
                                    fuerza, -limite, limite)
            if movesc > 0.3:
                self.cajW = np.clip(self.cajW +
                                    (-1.0 + np.random.rand(self.cajW.size) * 2.0) *
                                    fuerza, limite * 0.001, limite)

    def remutar(self, fuerza, cantidad, limite):
        for i in range(self.oriW.size):
            if np.random.rand(1)[0] < cantidad:
                self.oriW[i] = np.clip(self.oriW[i] +
                                       (-1.0 + np.random.rand(1)[0] * 2.0) *
                                       fuerza, -limite, limite)
        for i in range(self.cajW.size):
            if np.random.rand(1)[0] < cantidad:
                self.cajW[i] = np.clip(self.cajW[i] +
                                       (-1.0 + np.random.rand(1)[0] * 2.0) *
                                       fuerza, limite * 0.001, limite)

    def combinar(self, madre, padre):
        self.id = madre.id
        if np.random.rand(1)[0] < 0.5:
            self.oriW = madre.oriW.copy()
        else:
            self.oriW = padre.oriW.copy()
        if np.random.rand(1)[0] < 0.5:
            self.cajW = madre.cajW.copy()
        else:
            self.cajW = padre.cajW.copy()

    def recombinar(self, madre, padre):
        self.id = madre.id
        prob = np.random.rand(madre.oriW.size) < 0.5
        self.oriW = np.where(prob, madre.oriW, padre.oriW)
        prob = np.random.rand(madre.cajW.size) < 0.5
        self.cajW = np.where(prob, madre.cajW, padre.cajW)

class redMLP(object):

    def __init__(self, entradas, salidas, limite, numcap, numneu):
        self.limite = limite
        self.capas = []
        caps = max(1, numcap)
        numn = max(1, numneu)
        for c in range(caps):
            if c == caps - 1:
                if c == 0:
                    self.capas.append(capaMLP(salidas, entradas))
                else:
                    self.capas.append(capaMLP(salidas, numn))
            else:
                if c == 0:
                    self.capas.append(capaMLP(numn, entradas))
                else:
                    self.capas.append(capaMLP(numn, numn))

    def numunits(self):
        nn = 0
        for cap in self.capas:
            nn += len(cap.neuras)
        return nn

    def exportar(self, archivo):
        if archivo != "":
            txt = self.guardar()
            if ".txt" in archivo:
                fff = open(archivo, "w")
            else:
                fff = open(archivo + ".txt", "w")
            fff.write(txt)
            fff.close()
            return True
        else:
            return False

    def guardar(self):
        info = self.informacion(False)
        txt = "Red MLP by Omarsaurio:\n"
        txt += "limite, entradas, salidas, neuronas, cappas, pesos\n"
        txt += "{},{},{},{},{},{}\n".format(info[0], info[1], info[2],
                                            info[3], info[4], info[5])
        for cap in self.capas:
            txt += cap.guardar()
        return txt

    def importar(self, archivo):
        if archivo != "":
            if ".txt" in archivo:
                fff = open(archivo, "r")
            else:
                fff = open(archivo + ".txt", "r")
            dat = fff.read()
            fff.close()
            return self.abrir(dat)
        else:
            return False

    def abrir(self, texto):
        if "MLP" in texto:
            dat = texto.split("capa")
            info = dat[0].split("\n")
            info = info[2].split(",")
            self.limite = float(info[0])
            self.capas = []
            for c in range(len(dat) - 1):
                self.capas.append(capaMLP(1, int(info[1])))
                self.capas[-1].abrir(dat[c + 1])
            return True
        else:
            return False

    def informacion(self, ver):
        info = []
        info.append(self.limite)
        info.append(self.capas[0].neuras[0].pesW.size - 1)
        info.append(len(self.capas[-1].neuras))
        info.append(self.numunits())
        info.append(len(self.capas))
        info.append(0)
        for cap in self.capas:
            info[-1] += len(cap.neuras) * cap.neuras[0].pesW.size
        if ver:
            print("Red MLP by Omarsaurio:\nlimite: {}\n".format(info[0]) +
                  "entradas: {}\nsalidas: {}\n".format(info[1], info[2]) +
                  "neuronas: {}\ncapas: {}\npesos: {}".format(info[3],
                                                              info[4], info[5]))
        return info

    def copiar(self, origen):
        self.limite = origen.limite
        ent = origen.capas[0].neuras[0].pesW.size - 1
        capotas = []
        for cap in origen.capas:
            capotas.append(capaMLP(1, ent))
            capotas[-1].copiar(cap)
        self.capas = capotas

    def copy(self):
        aux = redMLP(1, 1, 1, 1, 1)
        aux.copiar(self)
        return aux

    def ejecutar(self, datos, activ, sigm):
        res = datos
        cps = len(self.capas)
        for c in range(cps):
            if c == cps - 1:
                res = self.capas[c].ejecutar(res, False)
            else:
                res = self.capas[c].ejecutar(res, sigm)
        if activ:
            return activacion(res)
        else:
            return res

    def competir(self, datos, activ):
        vec = np.reshape(self.ejecutar(datos, False, True), (2, -1))
        if activ:
            return activacion(np.subtract(vec[0, :], vec[1, :]))
        else:
            return np.subtract(vec[0, :], vec[1, :])

    def clasificar(self, datos):
        return np.argmax(self.ejecutar(datos, False, True))

    def subclasificar(self, datos):
        vec = np.reshape(self.ejecutar(datos, False, True), (2, -1))
        return np.argmax(vec, axis=0)

    def probabilidad(self):
        cps = len(self.capas)
        if cps > 1:
            vec = np.zeros(cps - 1, dtype=float)
            for c in range(vec.size):
                vec[c] = len(self.capas[c].neuras)
            return vec / vec.sum()
        else:
            return np.array([])

    def editar(self, proba, soloneuras):
        if np.random.rand(1)[0] < proba:
            if np.random.rand(1)[0] < soloneuras:
                if np.random.rand(1)[0] < 0.5:
                    self.reducir()
                else:
                    self.aumentar()
            else:
                if np.random.rand(1)[0] < 0.5:
                    self.reducirfull()
                else:
                    self.aumentarfull()

    def reducir(self):
        dado = np.random.rand(1)[0]
        prob = self.probabilidad()
        if prob.size > 0:
            ind = -1
            cap = 0
            for c in range(prob.size):
                if dado < prob[:(c + 1)].sum():
                    ind = self.capas[c].reducir()
                    cap = c
                    break
            if ind != -1:
                for neu in self.capas[cap + 1].neuras:
                    neu.pesW = np.delete(neu.pesW, ind + 1)

    def aumentar(self):
        dado = np.random.rand(1)[0]
        prob = self.probabilidad()
        if prob.size > 0:
            prob = 1.0 - prob
            prob /= max(1.0, prob.sum())
            cap = -1
            for c in range(prob.size):
                if dado < prob[:(c + 1)].sum():
                    self.capas[c].aumentar()
                    cap = c
                    break
            if cap != -1:
                for neu in self.capas[cap + 1].neuras:
                    neu.pesW = np.append(neu.pesW, 0.0)

    def reducirfull(self):
        dado = np.random.rand(1)[0]
        prob = self.probabilidad()
        if prob.size > 0:
            prob = 1.0 - prob
            prob /= max(1.0, prob.sum())
            cap = -1
            ent = 0
            for c in range(prob.size):
                if dado < prob[:(c + 1)].sum():
                    cap = c
                    ent = self.capas[c].neuras[0].pesW.size - 1
                    self.capas.pop(c)
                    break
            if cap != -1:
                for neu in self.capas[cap].neuras:
                    neu.regulatalla(ent + 1)

    def aumentarfull(self):
        dado = np.random.rand(1)[0]
        prob = self.probabilidad()
        if prob.size > 0:
            cap = -1
            for c in range(prob.size):
                if dado < prob[:(c + 1)].sum():
                    cap = c
                    ent = self.capas[c].neuras[0].pesW.size - 1
                    self.capas.insert(c, capaMLP(1, ent))
                    self.capas[c].copiar(self.capas[c + 1])
                    break
            if cap != -1:
                ent = len(self.capas[cap].neuras)
                for neu in self.capas[cap + 1].neuras:
                    neu.regulatalla(ent + 1)
                    neu.id = np.random.rand(1)[0]

    def aleatorizar(self):
        for cap in self.capas:
            cap.aleatorizar()

    def dividir(self, madre, fuerza, cantidad, full):
        self.copiar(madre)
        self.mutar(fuerza, cantidad, full)

    def mutar(self, fuerza, cantidad, full):
        for cap in self.capas:
            cap.mutar(fuerza, cantidad, self.limite, full)

    def combinar(self, madre, padre, relleno, full):
        self.limite = madre.limite
        ent = madre.capas[0].neuras[0].pesW.size - 1
        self.capas = []
        for c in range(len(madre.capas)):
            self.capas.append(capaMLP(1, ent))
            if c < len(padre.capas):
                self.capas[-1].combinar(madre.capas[c], padre.capas[c], relleno, full)
            else:
                self.capas[-1].copiar(madre.capas[c])
        self.adecuar(madre)

    def adecuar(self, madre):
        ent = madre.capas[0].neuras[0].pesW.size - 1
        for neu in self.capas[0].neuras:
            neu.regulatalla(ent + 1)
        sal = len(madre.capas[-1].neuras)
        while sal > len(self.capas[-1].neuras):
            self.capas[-1].aumentar()
        while sal < len(self.capas[-1].neuras):
            self.capas[-1].reducir()
        cps = len(self.capas)
        if cps > 1:
            for c in range(cps - 1):
                ent = len(self.capas[c].neuras)
                for neu in self.capas[c + 1].neuras:
                    neu.regulatalla(ent + 1)

    def grafica2D(self, clasi):
        xx = []
        yy = []
        cc = []
        if self.capas[0].neuras[0].pesW.size - 1 == 2:
            for x in range(int(-self.limite), int(self.limite + 1)):
                for y in range(int(-self.limite), int(self.limite + 1)):
                    xx.append(x)
                    yy.append(y)
                    if clasi:
                        cc.append(self.clasificar(np.array([x, y], dtype=float)))
                    else:
                        res = self.ejecutar(np.array([x, y], dtype=float), True, True)
                        if res.size > 1:
                            if res[0] >= 0:
                                if res[1] >= 0:
                                    cc.append('red')
                                else:
                                    cc.append('orange')
                            else:
                                if res[1] >= 0:
                                    cc.append('yellow')
                                else:
                                    cc.append('blue')
                        else:
                            if res[0] >= 0:
                                cc.append('red')
                            else:
                                cc.append('blue')
        # plt.scatter(xx, yy, c=cc)
        # plt.show()
        return xx, yy, cc

class capaMLP(object):

    def __init__(self, numneu, entradas):
        self.neuras = []
        for n in range(max(1, numneu)):
            self.neuras.append(neuronaMLP(entradas))

    def guardar(self):
        txt = "capa\n"
        for neu in self.neuras:
            txt += neu.guardar()
        return txt

    def abrir(self, txt):
        self.neuras = []
        dat = txt.replace("capa", "").split("\n")
        for d in dat:
            if d != "":
                self.neuras.append(neuronaMLP(1))
                self.neuras[-1].abrir(d)

    def copiar(self, origen):
        self.neuras = []
        for neu in origen.neuras:
            self.neuras.append(neuronaMLP(1))
            self.neuras[-1].copiar(neu)

    def ejecutar(self, datos, sigm):
        res = np.zeros(len(self.neuras), dtype=float)
        for n in range(res.size):
            res[n] = self.neuras[n].ejecutar(datos, sigm)
        return res

    def reducir(self):
        neu = len(self.neuras)
        if neu > 1:
            ind = np.random.randint(neu)
            self.neuras.pop(ind)
            return ind
        else:
            return -1

    def aumentar(self):
        ent = self.neuras[0].pesW.size - 1
        self.neuras.append(neuronaMLP(ent))

    def aleatorizar(self):
        ent = self.neuras[0].pesW.size - 1
        for neu in self.neuras:
            neu.aleatorizar(ent)

    def mutar(self, fuerza, cantidad, limite, full):
        if full:
            for neu in self.neuras:
                neu.remutar(fuerza, cantidad, limite)
        else:
            for neu in self.neuras:
                neu.mutar(fuerza, cantidad, limite)

    def combinar(self, madre, padre, relleno, full):
        self.neuras = []
        for dm in madre.neuras:
            igual = None
            for dp in padre.neuras:
                if dm.id == dp.id:
                    igual = dp
                    break
            if igual != None:
                self.neuras.append(neuronaMLP(1))
                if full:
                    self.neuras[-1].recombinar(dm, igual)
                else:
                    self.neuras[-1].combinar(dm, igual)
            elif np.random.rand(1)[0] < relleno:
                self.neuras.append(neuronaMLP(1))
                self.neuras[-1].copiar(dm)
        for dp in padre.neuras:
            igual = None
            for dm in madre.neuras:
                if dp.id == dm.id:
                    igual = dm
                    break
            if igual == None and np.random.rand(1)[0] < relleno:
                self.neuras.append(neuronaMLP(1))
                self.neuras[-1].copiar(dp)
        if len(self.neuras) == 0:
            self.neuras.append(neuronaMLP(1))
            self.neuras[-1].copiar(madre.neuras[0])

class neuronaMLP(object):

    def __init__(self, entradas):
        self.aleatorizar(entradas)
        self.id = np.random.rand(1)[0]

    def guardar(self):
        txt = str(self.id) + ":"
        for n in self.pesW:
            txt += str(n) + ","
        txt = txt[:-1] + "\n"
        return txt

    def abrir(self, txt):
        dat = txt.replace("\n", "").split(":")
        self.id = float(dat[0])
        dat = dat[1].split(",")
        self.pesW = np.array(dat, dtype=float)

    def copiar(self, origen):
        self.pesW = origen.pesW.copy()
        self.id = origen.id

    def ejecutar(self, datos, sigm):
        X = np.append(1.0, datos)
        if sigm:
            return self.sigmoide(np.sum(X * self.pesW))
        else:
            return np.sum(X * self.pesW)

    def sigmoide(self, num):
        n = np.clip(num, -700.0, 700.0)
        return 1.0 / (1.0 + np.exp(-n))

    def aleatorizar(self, entradas):
        self.pesW = -1.0 + np.random.rand(entradas + 1) * 2.0

    def mutar(self, fuerza, cantidad, limite):
        if np.random.rand(1)[0] < cantidad:
            self.pesW = np.clip(self.pesW +
                                (-1.0 + np.random.rand(self.pesW.size) * 2.0) *
                                fuerza, -limite, limite)

    def remutar(self, fuerza, cantidad, limite):
        for i in range(self.pesW.size):
            if np.random.rand(1)[0] < cantidad:
                self.pesW[i] = np.clip(self.pesW[i] +
                                       (-1.0 + np.random.rand(1)[0] * 2.0) *
                                       fuerza, -limite, limite)

    def combinar(self, madre, padre):
        self.id = madre.id
        if np.random.rand(1)[0] < 0.5:
            self.pesW = madre.pesW.copy()
        else:
            self.pesW = padre.pesW.copy()

    def recombinar(self, madre, padre):
        self.id = madre.id
        prob = np.random.rand(madre.pesW.size) < 0.5
        pa = padre.pesW.copy()
        while madre.pesW.size > pa.size:
            pa = np.append(pa, -1.0 + np.random.rand(1)[0] * 2.0)
        while madre.pesW.size < pa.size:
            pa = pa[:-1]
        self.pesW = np.where(prob, madre.pesW, pa)

    def regulatalla(self, ind):
        while ind > self.pesW.size:
            self.pesW = np.append(self.pesW, -1.0 + np.random.rand(1)[0] * 2.0)
        while ind < self.pesW.size:
            self.pesW = self.pesW[:-1]

def activacion(num):
    n = np.clip(num, -700.0, 700.0)
    return 1.0 - (2.0 / (1.0 + np.exp(n)))

"""
Tareas:
- aumentar dendrita duplicando alguna
- aumentar dendrita entre dos existentes
- aumentar dendrita lejos de otras
- reducir dendrita segun volumen
- reducir dendrita segun cercania a otra
- graficar almenos dos dimensiones siempre
- hacer SGD para MLP
- hacer SGD para DMNN
- hacer Kmedias para DMNN
- hacer PSO para MLP
- hacer PSO para DMNN
"""
