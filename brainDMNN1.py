# Template for AI competition simulation by Omarsaurio ojorcio@gmail.com 2019
# Dendral Morphologycal Neural Network with Genetic Evolution by Omarsaurio

import numpy as np
from cerebroNeurotico import redDMNN as dmnn

class brainAI(object):

    def __init__(self):
        self.master = dmnn(23, 6 * 2, 1.1, 230)
        self.muta = 0.01
        self.recomb = 0.1
        self.relleno = 0.5
        self.full = True
        self.editdmnn = 0.8

    def copy(self):
        new = brainAI()
        new.master = self.master.copy()
        return new

    def execute(self, SEN, C):
        ACT = np.where(self.master.subclasificar(SEN) == 0, -1.0, 1.0)
        return ACT

    def exportIA(self):
        data = self.master.guardar()
        return data

    def importIA(self, data):
        self.master.abrir(data)

    def spawn(self, mother, father):
        if father == None:
            self.master.dividir(mother, self.muta, self.recomb, self.full)
        else:
            self.master.combinar(mother, father, self.relleno, self.full)
        self.master.editar(self.editdmnn)

    def about(self):
        message = "DMNN with Evolution, by Omarsaurio\n" +\
            "this use sub-classifier algorithm, discrete out\n" +\
            "v1.0.0, 2020 - ojorcio@gmail.com"
        return message
