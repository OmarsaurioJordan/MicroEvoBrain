# Template for AI competition simulation by Omarsaurio ojorcio@gmail.com 2019
# Multi Layer Perceptron with Genetic Evolution by Omarsaurio

import numpy as np
from cerebroNeurotico import redMLP as mlp

class brainAI(object):

    def __init__(self):
        self.master = mlp(23, 6, 1.1, 3, 46)
        self.muta = 0.01
        self.recomb = 0.1
        self.relleno = 0.5
        self.full = True
        self.editmlp = 0.2
        self.edineunocap = 1.0

    def copy(self):
        new = brainAI()
        new.master = self.master.copy()
        return new

    def execute(self, SEN, C):
        ACT = self.master.ejecutar(SEN, True, True)
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
        self.master.editar(self.editmlp, self.edineunocap)

    def about(self):
        message = "MLP with Evolution, by Omarsaurio\n" +\
            "this use a basic MLP execution, so out is continuous\n" +\
            "v1.0.0, 2020 - ojorcio@gmail.com"
        return message
