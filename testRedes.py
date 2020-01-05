# Administrador de Cerebro Neurotico by Omarsaurio 2019

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from cerebroNeurotico import redDMNN as dmnn
from cerebroNeurotico import redMLP as mlp

class testeoRedes(object):

    def __init__(self):
        # del problema
        self.entreno = 20
        self.valida = 5
        self.test = 5
        self.ruid = 2.25
        # evolucion
        self.pobla = 10
        self.numadres = 0.2
        self.genera = 100
        self.varias = False
        self.reintentar = 10
        self.muta = 1.0
        self.recomb = 0.1
        self.relleno = 0.5
        self.sexual = True
        self.genfull = True
        # arqui redes
        self.dendritas = 20
        self.editdmnn = 0.8
        self.editmlp = 0.2
        self.edineunocap = 1.0
        self.capas = 3
        self.neurons = 10
        # internas
        self.P = np.array([])
        self.V = np.array([])
        self.T = np.array([])

    def defectoDMNN(self):
        self.muta = 2.0
        self.recomb = 0.3
        self.editdmnn = 0.8
        self.dendritas = 20

    def defectoMLP(self):
        self.muta = 0.5
        self.recomb = 0.1
        self.editmlp = 0.2
        self.edineunocap = 1.0
        self.capas = 3
        self.neurons = 10

    def defectoEvo(self):
        self.pobla = 10
        self.numadres = 0.2
        self.genera = 100
        self.varias = False
        self.reintentar = 10
        self.muta = 1.0
        self.recomb = 0.1
        self.relleno = 0.5
        self.sexual = True
        self.genfull = True

    def prueba(self, dendral, graficar):
        if self.P.size > 0:
            print("")
            print("Go...")
            hoy = dt.datetime.today()
            red = self.poblacionRedes(dendral, self.P)
            if dendral:
                elite = dmnn(1, 1, 1, 1)
            else:
                elite = mlp(1, 1, 1, 1, 1)
            elite.copiar(red[0])
            mejor = 1
            eee = [-1, 1, 1, 0, 0, 0]
            curva = []
            units = []
            mad = []
            emad = []
            top = 0
            cont = 0
            for v in range(self.genera):
                if dendral:
                    mad, emad = self.evolucion(mad, emad, red, self.editdmnn)
                else:
                    mad, emad = self.evolucion(mad, emad, red, self.editmlp)
                vali = self.error(red[mad[0]], self.V)
                if vali <= mejor:
                    mejor = vali
                    elite.copiar(red[mad[0]])
                curva.append([emad[0], vali])
                units.append(red[mad[0]].numunits())
                if eee[0] == -1:
                    eee[0] = emad[0]
                    eee[1] = mejor
                    eee[2] = self.error(elite, self.T)
                cont += 1
                if cont >= top:
                    if dendral:
                        print("d{:.0f}% ... {:.3f}".format((top / self.genera) * 100,
                                                           emad[0]))
                    else:
                        print("p{:.0f}% ... {:.3f}".format((top / self.genera) * 100,
                                                           emad[0]))
                    top += int(self.genera / 10)
                if mejor == 0 and emad[0] == 0:
                    break
            eee[3] = emad[0]
            eee[4] = mejor
            eee[5] = self.error(elite, self.T)
            self.informacion(eee, elite, curva, units, hoy, graficar)
            return elite
        else:
            return None

    def optimizar(self, dendral, iter):
        print("")
        print("Go...")
        self.entreno = 6
        self.valida = 1
        self.test = 1
        self.ruid = 2.25
        self.problema1()
        self.genera = 40
        # crear los parametros iniciales
        # madres, muta, recomb, relleno, editdmnn, editmlp
        genes = np.array([0.4, 0.2, 0.1, 0.5, 0.8, 0.2])
        originales = self.poblacionRedes(dendral, self.P)
        red = []
        for r in originales:
            if dendral:
                red.append(dmnn(1, 1, 1, 1))
            else:
                red.append(mlp(1, 1, 1, 1, 1))
        mejor = 1
        top = 0
        cont = 0
        # ciclo de optimizacion
        for i in range(iter):
            prueba = genes.copy()
            prueba = prueba + (-1.0 + np.random.rand(prueba.size) * 2.0) * 0.2
            prueba = np.clip(prueba, 0.0, 1.0)
            self.fenotipo(prueba)
            for r in range(len(originales)):
                red[r].copiar(originales[r])
            mad = []
            emad = []
            # ciclo evolutivo interno
            for v in range(self.genera):
                if dendral:
                    mad, emad = self.evolucion(mad, emad, red, self.editdmnn)
                else:
                    mad, emad = self.evolucion(mad, emad, red, self.editmlp)
                if emad[0] == 0:
                    break
            # analizar la solucion
            if emad[0] <= mejor:
                mejor = emad[0]
                genes = prueba.copy()
            # ver como va la cosa
            cont += 1
            if cont >= top:
                print("{:.0f}% ... {:.3f}".format((top / iter) * 100, mejor))
                top += int(iter / 10)
        self.fenotipo(genes)
        self.infoParametros()

    def fenotipo(self, genes):
        self.numadres = genes[0] * 0.5
        self.muta = genes[1] * 5.0
        self.recomb = genes[2]
        self.relleno = genes[3]
        self.editdmnn = genes[4]
        self.editmlp = genes[5]

    def informacion(self, eee, elite, curva, units, hoy, graficar):
        print(dt.datetime.today() - hoy)
        print("errores iniciales:")
        print("ent: {}".format(eee[0]))
        print("val: {}".format(eee[1]))
        print("tes: {}".format(eee[2]))
        print("errores finales:")
        print("ent: {}".format(eee[3]))
        print("val: {}".format(eee[4]))
        print("tes: {}".format(eee[5]))
        elite.informacion(True)
        if graficar:
            plt.subplot(2, 2, 1)
            plt.title("Patrones Problema")
            if self.P.shape[0] == 3:
                plt.scatter(self.P[0, :], self.P[1, :], c=self.P[2, :], linewidths=0.1)
            else:
                plt.plot([])
            plt.subplot(2, 2, 2)
            plt.title("Superficie Decision")
            xx, yy, cc = elite.grafica2D(True)
            plt.scatter(xx, yy, c=cc)
            plt.subplot(2, 2, 3)
            plt.title("Descenso Error (azul:entreno, nar:val)")
            plt.plot(curva)
            plt.scatter([0, 0], [0, 1], c=['white', 'white'])
            plt.subplot(2, 2, 4)
            plt.title("Unidades Procesamiento")
            plt.plot(units)
            plt.scatter([0], [0], c=['white'])
            plt.show()

    def infoDatos(self):
        if self.P.size > 0:
            print("entradas: " + str(self.P.shape[0] - 1))
            print("salidas: " + str(int(self.P[-1, :].max() + 1)))
            print("entreno: " + str(self.P.shape[1]))
            print("validacion: " + str(self.V.shape[1]))
            print("testeo: " + str(self.T.shape[1]))
        else:
            print("no hay patrones")

    def infoParametros(self):
        print("entreno: " + str(self.entreno))
        print("validacion: " + str(self.valida))
        print("testeo: " + str(self.test))
        print("ruido: " + str(self.ruid))
        print("poblacion: " + str(self.pobla))
        print("madres: " + str(self.numadres))
        print("generaciones: " + str(self.genera))
        print("variar inicio: " + str(self.varias))
        print("reintentos iniciales: " + str(self.reintentar))
        print("mutacion: " + str(self.muta))
        print("recombinacion: " + str(self.recomb))
        print("relleno: " + str(self.relleno))
        print("sexual: " + str(self.sexual))
        print("genfull: " + str(self.genfull))
        print("dendritas DMNN: " + str(self.dendritas))
        print("edicion DMNN: " + str(self.editdmnn))
        print("edicion MLP: " + str(self.editmlp))
        print("edi neu vs cap MLP: " + str(self.edineunocap))
        print("capas MLP: " + str(self.capas))
        print("neuronas MLP: " + str(self.neurons))

    def problema1(self):
        XX = [-7.5, -2.5, 2.5, 2.5, 7.5, 7.5, -7.5, -7.5, -5, -5, 0, 2.5, 5]
        YY = [-7.5, -2.5, 2.5, -7.5, 5, -5, 5, -2.5, -5, -7.5, 5, -5, 0]
        CC = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
        self.P = self.aleatorizar(XX, YY, CC, self.entreno)
        self.V = self.aleatorizar(XX, YY, CC, self.valida)
        self.T = self.aleatorizar(XX, YY, CC, self.test)

    def problema2(self):
        XX = []
        YY = []
        CC = []
        print("digite: x, y, clase")
        print("x,y entre -10y10, clase 0,1,2,...")
        i = 1
        while True:
            txt = input(str(i) + ": ")
            if txt == "":
                break
            else:
                try:
                    while "  " in txt:
                        txt = txt.replace("  ", " ")
                    txt = txt.replace(", ", ",")
                    txt = txt.replace(" ", ",")
                    txt = txt.split(",")
                    x = float(txt[0])
                    y = float(txt[1])
                    c = float(txt[2])
                    XX.append(max(-10.0, min(10.0, x)))
                    YY.append(max(-10.0, min(10.0, y)))
                    CC.append(c)
                    i += 1
                except:
                    pass
        if len(XX) == 0:
            XX = [0]
            YY = [0]
            CC = [0]
        self.P = self.aleatorizar(XX, YY, CC, self.entreno)
        self.V = self.aleatorizar(XX, YY, CC, self.valida)
        self.T = self.aleatorizar(XX, YY, CC, self.test)

    def problema3(self):
        archivo = input("archivo: ")
        try:
            fff = open(archivo, "r")
            txt = fff.read()
            fff.close()
            txt = txt.split("\n")
            txt = txt[3:]
            Qe = []
            for t in txt:
                if t != "":
                    dat = t.split(",")
                    if len(Qe) == 0:
                        for e in range(len(dat)):
                            Qe.append([])
                    for e in range(len(dat)):
                        Qe[e].append(float(dat[e]))
            # agregar validacion
            tot = len(Qe[0])
            val = np.floor((self.valida / (self.entreno + self.valida + self.test)) * tot)
            Qv = []
            for v in range(len(Qe)):
                Qv.append([])
            while len(Qv[0]) < val:
                ind = np.random.randint(len(Qe[0]))
                for v in range(len(Qe)):
                    Qv[v].append(Qe[v].pop(ind))
            # agregar testeo
            tes = np.floor((self.test / (self.entreno + self.valida + self.test)) * tot)
            Qt = []
            for t in range(len(Qe)):
                Qt.append([])
            while len(Qt[0]) < tes:
                ind = np.random.randint(len(Qe[0]))
                for t in range(len(Qe)):
                    Qt[t].append(Qe[t].pop(ind))
            # formar los cosos
            self.P = np.array(Qe, dtype=float)
            self.V = np.array(Qv, dtype=float)
            self.T = np.array(Qt, dtype=float)
            # limitar a talla 10
            mi = np.min(self.P[:-1, :])
            ma = np.max(self.P[:-1, :])
            self.P[:-1, :] = (2.0 * ((self.P[:-1, :] - mi) / (ma - mi)) - 1.0) * 10.0
            self.V[:-1, :] = (2.0 * ((self.V[:-1, :] - mi) / (ma - mi)) - 1.0) * 10.0
            self.T[:-1, :] = (2.0 * ((self.T[:-1, :] - mi) / (ma - mi)) - 1.0) * 10.0
            # verificar que todos tengan la misma anchura
            ok = False
            if self.P.shape[0] == self.V.shape[0] and self.P.shape[0] == self.T.shape[0]:
                sal = max(self.P[-1, :].max(), self.V[-1, :].max(), self.T[-1, :].max()) + 1
                ok = True
                for s in range(int(sal)):
                    if not (s in self.P[-1, :]):
                        ok = False
                        break
            if not ok:
                self.P = np.array([])
                print("error")
        except:
            print("error")

    def problema4(self):
        # AND
        XX = [-5, -5, 5, 5]
        YY = [5, -5, 5, -5]
        CC = [0, 0, 1, 0]
        self.P = self.aleatorizar(XX, YY, CC, self.entreno)
        self.V = self.aleatorizar(XX, YY, CC, self.valida)
        self.T = self.aleatorizar(XX, YY, CC, self.test)

    def problema5(self):
        # OR
        XX = [-5, -5, 5, 5]
        YY = [5, -5, 5, -5]
        CC = [1, 0, 1, 1]
        self.P = self.aleatorizar(XX, YY, CC, self.entreno)
        self.V = self.aleatorizar(XX, YY, CC, self.valida)
        self.T = self.aleatorizar(XX, YY, CC, self.test)

    def problema6(self):
        # XOR
        XX = [-5, -5, 5, 5]
        YY = [5, -5, 5, -5]
        CC = [1, 0, 0, 1]
        self.P = self.aleatorizar(XX, YY, CC, self.entreno)
        self.V = self.aleatorizar(XX, YY, CC, self.valida)
        self.T = self.aleatorizar(XX, YY, CC, self.test)

    def aleatorizar(self, XX, YY, CC, num):
        Qx = []
        Qy = []
        Qc = []
        for i in range(len(CC)):
            for r in range(num):
                while True:
                    x = (-1.0 + np.random.rand(1)[0] * 2.0) * self.ruid
                    y = (-1.0 + np.random.rand(1)[0] * 2.0) * self.ruid
                    if np.sqrt(np.power(x, 2.0) + np.power(y, 2.0)) < self.ruid:
                        break
                Qx.append(XX[i] + x)
                Qy.append(YY[i] + y)
                Qc.append(CC[i])
        Q = np.vstack((Qx, Qy, Qc))
        return Q

    def poblacionRedes(self, dendral, datos):
        red = []
        ent = int(datos.shape[0] - 1)
        sal = int(datos[-1, :].max() + 1)
        lim = np.ceil(np.abs(datos[:-1, :]).max() * 1.1)
        for n in range(self.pobla):
            if dendral:
                if self.varias:
                    ddd = int((0.5 + np.random.rand(1)[0] * 1.5) * self.dendritas)
                else:
                    ddd = self.dendritas
                red.append(dmnn(ent, sal, lim, ddd))
            else:
                if self.varias:
                    nnn = int((0.5 + np.random.rand(1)[0] * 1.5) * self.neurons)
                else:
                    nnn = self.neurons
                red.append(mlp(ent, sal, lim, self.capas, nnn))
        if self.reintentar > 0:
            if dendral:
                otrared = dmnn(1, 1, 1, 1)
            else:
                otrared = mlp(1, 1, 1, 1, 1)
            otrared.copiar(red[0])
            mejor = self.error(otrared, self.P)
            for r in range(self.reintentar):
                otrared.aleatorizar()
                err = self.error(otrared, self.P)
                if err < mejor:
                    mejor = err
                    red[0].copiar(otrared)
        return red

    def evolucion(self, md, emd, red, edit):
        # seleccionar a las potenciales madres
        fit = self.evaluacion(md, emd, self.P, red)
        madres = max(1, int(self.pobla * self.numadres))
        mad = []
        emad = []
        for m in range(madres):
            e = 1000
            n = 0
            for f in range(fit.size):
                if fit[f] < e:
                    e = fit[f]
                    n = f
            mad.append(n)
            emad.append(fit[n])
            fit[n] = 1000
        # crear a los hijos
        hijos = int(self.pobla / madres)
        actu = 0
        cont = 0
        for n in range(self.pobla):
            if not n in mad:
                red[n].dividir(red[mad[actu]], self.muta, self.recomb, self.genfull)
                red[n].editar(edit, self.edineunocap)
                cont += 1
                if cont >= hijos:
                    actu += 1
                    cont = 0
        if len(mad) > 2 and self.sexual:
            red[mad[-1]].combinar(red[mad[0]], red[mad[1]], self.relleno, self.genfull)
            mad.pop(len(mad) - 1)
        return mad, emad

    def evaluacion(self, mad, emad, datos, red):
        res = []
        mad.append(-1)
        m = 0
        for r in range(len(red)):
            if r == mad[m]:
                res.append(emad[m])
                m += 1
            else:
                res.append(self.error(red[r], datos))
        return np.array(res, dtype=float)

    def error(self, lared, datos):
        e = 0.0
        for i in range(datos.shape[1]):
            if lared.clasificar(datos[:-1, i]) != datos[-1, i]:
                e += 1.0
        return e / datos.shape[1]

    def velocidad(self, lared, datos, escala):
        if datos.size > 0:
            print("Go...")
            hoy = dt.datetime.today()
            for e in range(max(1, escala)):
                self.error(lared, datos)
            ret = dt.datetime.today() - hoy
            print("demora: " + str(ret))

    def graficaRed(self, dendral, lared=None):
        if lared != None:
            mired = lared
        elif dendral:
            mired = dmnn(2, 2, 20.0, self.dendritas)
        else:
            mired = mlp(2, 2, 20.0, self.capas, self.neurons)
        plt.subplot(1, 2, 1)
        plt.title("Competencia Clasificadora")
        xx, yy, cc = mired.grafica2D(True)
        plt.scatter(xx, yy, c=cc)
        plt.subplot(1, 2, 2)
        plt.title("Zonas (azul:negativo, rojo:positivo)")
        xx, yy, cc = mired.grafica2D(False)
        plt.scatter(xx, yy, c=cc)
        plt.show()

def teclado(encabezado, mensaje, defecto):
    if encabezado != "":
        print(encabezado)
    try:
        cad = ""
        for de in defecto:
            cad += str(de) + " "
    except:
        cad = str(defecto)
    print("  def: " + cad)
    while True:
        txt = input(mensaje)
        if txt == "":
            return defecto
        else:
            try:
                while "  " in txt:
                    txt = txt.replace("  ", " ")
                txt = txt.replace(", ", ",")
                txt = txt.replace(" ", ",")
                txt = txt.split(",")
                dat = []
                for t in range(len(txt)):
                    dat.append(float(txt[t]))
                if len(dat) == 1:
                    try:
                        if len(defecto) == 1:
                            return dat
                    except:
                        return dat[0]
                elif len(dat) > 1:
                    try:
                        if len(dat) == len(defecto):
                            return dat
                    except:
                        pass
            except:
                pass

def abrirRed():
    archivo = input("archivo de red: ")
    if archivo != "":
        red = dmnn(1, 1, 1, 1)
        if red.importar(archivo):
            return red
        else:
            red = mlp(1, 1, 1, 1, 1)
            if red.importar(archivo):
                return red
            else:
                return None
    else:
        return None

def main():
    master = testeoRedes()
    print("***Software Evolucion DMNN y MLP by Omarsaurio 2019***")
    print("(digite ayuda)")
    anterior = ""
    while True:
        print("")
        sel = input("-> ").lower()
        if sel == " ":
            if anterior != "" and anterior != " ":
                sel = anterior
                print("-> " + sel)
        if sel == "arquidmnn":
            master.dendritas = int(teclado("# el total de dendritas al inicializar",
                                           "  dendritas: ", 20))
            master.editdmnn = teclado("# (0a1) probabilidad aumento/disminucion dendritas",
                                      "  edicion: ", 0.8)
        elif sel == "arquimlp":
            master.capas = int(teclado("# el total de capas al inicializar",
                                       "  capas: ", 3))
            master.neurons = int(teclado("# el total de neuronas por capa al inicializar",
                                         "  neuronas: ", 10))
            master.editmlp = teclado("# (0a1) probabilidad aumento/disminucion neuronas",
                                     "  edicion: ", 0.2)
            master.edineunocap = teclado("# (0a1) probabilidad edicion afecte neuronas, sino capas",
                                         "  edi neu vs cap: ", 1)
        elif sel == "paraevo":
            master.pobla = int(teclado("# la cantidad de poblacion para cada generacion",
                                       "  poblacion: ", 10))
            master.numadres = teclado("# (0a1) porcentaje de individuos seleccionados para procrear",
                                      "  madres: ", 0.2)
            master.genera = int(teclado("# cuantas generaciones/iteraciones se haran",
                                        "  generaciones: ", 100))
            master.varias = teclado("# digite 0 para no variar dendritas/neuronas al iniciar poblacion",
                                    "  variar: ", 0) != 0
            master.reintentar = int(teclado("# la cantidad de intentos que hara una red al inicializar",
                                            "  reintentos: ", 10))
        elif sel == "paragen":
            master.muta = teclado("# fuerza del cambio en cada gen modificado",
                                  "  mutacion: ", 1)
            master.recomb = teclado("# (0-1) probabilidad de modificar cada gen, 1 es que todos cambian",
                                    "  recombinacion: ", 0.1)
            master.relleno = teclado("# (0-1) probabilidad aplicar genes sin par en reproduccion sexual",
                                     "  relleno: ", 0.5)
            master.sexual = teclado("# digite 0 para deshabilitar la reproduccion sexual (una por generacion)",
                                    "  sexual: ", 1) != 0
            master.genfull = teclado("# digite 0 para que la recombinacion afecte unidades logicas, no genes",
                                     "  genfull: ", 1) != 0
        elif sel == "and":
            master.ruid = teclado("# radio para poner puntos alrededor de cada punto base",
                                  "  ruido: ", 4.5)
            master.problema4()
        elif sel == "or":
            master.ruid = teclado("# radio para poner puntos alrededor de cada punto base",
                                  "  ruido: ", 4.5)
            master.problema5()
        elif sel == "xor":
            master.ruid = teclado("# radio para poner puntos alrededor de cada punto base",
                                  "  ruido: ", 4.5)
            master.problema6()
        elif sel == "dataset":
            master.problema3()
        elif sel == "ejemplo":
            master.ruid = teclado("# radio para poner puntos alrededor de cada punto base",
                                  "  ruido: ", 2.25)
            master.problema1()
        elif sel == "manual":
            master.ruid = teclado("# radio para poner puntos alrededor de cada punto base",
                                  "  ruido: ", 1.0)
            master.problema2()
        elif sel == "paraproblem":
            print("nota: con datasets .txt, los valores aqui generaran porcentajes")
            master.entreno = int(teclado("# numero de puntos para entreno",
                                         "  entreno: ", 20))
            master.valida = int(teclado("# numero de puntos para validacion",
                                        "  validacion: ", 5))
            master.test = int(teclado("# numero de puntos para testeo",
                                      "  testeo: ", 5))
        elif sel == "defectodmnn":
            master.defectoDMNN()
        elif sel == "defectomlp":
            master.defectoMLP()
        elif sel == "defectoevo":
            master.defectoEvo()
        elif sel == "evodmnn":
            ed = master.prueba(True, True)
            if ed != None:
                print("desea guardar la red?")
                ed.exportar(input("archivo (dmnn): "))
        elif sel == "evomlp":
            ep = master.prueba(False, True)
            if ep != None:
                print("desea guardar la red?")
                ep.exportar(input("archivo (mlp): "))
        elif sel == "enfrentamiento":
            ed = master.prueba(True, False)
            ep = master.prueba(False, False)
            if ed != None and ep != None:
                print("desea guardar las redes?")
                ed.exportar(input("archivo (dmnn): "))
                ep.exportar(input("archivo (mlp): "))
        elif sel == "demo":
            if master.P.size == 0:
                master.entreno = 20
                master.valida = 5
                master.test = 5
                master.ruid = 2.25
                master.problema1()
            master.defectoEvo()
            master.defectoDMNN()
            master.prueba(True, True)
            master.defectoMLP()
            master.prueba(False, True)
        elif sel == "infored":
            red = abrirRed()
            if red != None:
                red.informacion(True)
        elif sel == "optidmnn":
            iter = int(teclado("# numero de iteraciones para ajustar parametros generales",
                               "  iteraciones: ", 40))
            master.optimizar(True, iter)
        elif sel == "optimlp":
            iter = int(teclado("# numero de iteraciones para ajustar parametros generales",
                               "  iteraciones: ", 40))
            master.optimizar(False, iter)
        elif sel == "limpiar":
            master.P = np.array([])
        elif sel == "infodatos":
            master.infoDatos()
        elif sel == "infoparam":
            master.infoParametros()
        elif sel == "demora":
            red = abrirRed()
            if red != None:
                esc = int(teclado("# cuantas veces calcular el error de patrones de entreno",
                                  "  escala: ", 100))
                master.velocidad(red, master.P, esc)
        elif sel == "grafired":
            red = abrirRed()
            if red != None:
                master.graficaRed(True, red)
        elif sel == "grafidmnn":
            master.graficaRed(True)
        elif sel == "grafimlp":
            master.graficaRed(False)
        elif sel == "acercade":
            print("***Acerca De***")
            print("software evolutivo para DMNN y MLP")
            print("desarrollado por Omar Jordan Jordan, ojorcio@gmail.com")
            print("v1.0.1 de 2019, consta de 2 archivos Python")
            print("visite los siguientes links para mas trabajos")
            print("https://www.dropbox.com/sh/plhbo1ornjah8jb/AAAOdaSe5JArLE1XRo--Eh_7a?dl=0")
            print("https://www.deviantart.com/omarsaurus")
        elif sel == "formato":
            print("***ejemplo archivo dataset TXT***")
            print("Patrones: compuerta XOR")
            print("Salidas: false, true")
            print("Entradas: A, B")
            print("-5,-5,0")
            print("-5,5,1")
            print("5,5,0")
            print("5,-5,1")
        elif sel == "ayuda":
            print("***Comandos***")
            print("arquidmnn, arquimlp, ayuda, salir, paraevo, paragen,")
            print("and, or, xor, dataset, ejemplo, paraproblem, formato,")
            print("defectodmnn, defectomlp, evodmnn, evomlp, enfrentamiento,")
            print("infored, infodatos, manual, defectoevo, demo, limpiar,")
            print("demora, infoparam, optidmnn, optimlp, grafired, grafidmnn,")
            print("grafimlp, acercade")
            print("  nota: espacio para comando anterior")
        elif sel == "salir":
            print("***Finalizado***")
            break
        anterior = sel

main()
