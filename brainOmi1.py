# Template for AI competition simulation by Omarsaurio ojorcio@gmail.com 2020
# brainOmi1 by Omarsaurio

"""
Introduction:
This is an IA template to handle an agent that live in a simulation, it should
survive searching energy (food) and interacting with the environment, can exist
agents of other species with their own IA systems, all they can perform social
collaboration or aggressive actions, spawn child to evolve or not.
This code requires other Python code (the administrator) to connect with the
simulation, it will be with UDP and the simulation runs in GameMakerStudio
video game engine (for now, Godot in view)
"""

"""
Rules:
- don't use print functions, the main administrator code will decide what show
- don't use communications like sockets TCP or UDP, HTTP, serial, etc
- don't use the file system like .txt to transport or save information
- don't use threads or blocking functions like GUI's or graphic plotters
- don't make infinite loops, main loop execution is handle by the administrator
- don't access to PC sensors or web services
- maintain the structure of the prime functions
- you can delete all the informative text of the template, except: Introduction,
  Rules, Agent Description and the first line of the document
"""

"""
Agent Description:
Is a creature that can eat, attack (shoot), give energy charitably, scream and
spawn child, this spawn can be asexual if the creature reach the maximum energy,
will put an egg and lost the half energy, other creature of the same specie can
fertilize the egg making a sexual reproduction.
SEN (23 sensors):
0 - smell food: -1 no food, 0 to 1, some food to lots of food
1 - smell same specie: -1 no one, 0 to 1, someone to many others
2 - smell other specie: -1 no one, 0 to 1, someone to many others
3 - touch food: -1 no food, 0 to 1, left to right (don't care back or front)
4 - touch wall: -1 no wall, 0 to 1, left to right (don't care back or front)
5 - touch another agent: -1 no one, 0 to 1, left to right (don't care back or front)
6 - vision food: -1 no food, 0 to 1, left to right (in the angle and distance to view)
7 - vision wall: -1 no wall, 0 to 1, left to right (in the angle and distance to view)
8 - vision same specie: -1 no one, 0 to 1, left to right (in the angle and distance to view)
9 - vision other specie: -1 no one, 0 to 1, left to right (in the angle and distance to view)
10 - ray food: -1 no food, 0 to 1, far ahead to close in front
11 - ray wall: -1 no wall, 0 to 1, far ahead to close in front
12 - ray same specie: -1 no one, 0 to 1, far ahead to close in front
13 - ray other specie: -1 no one, 0 to 1, far ahead to close in front
14 - warm same specie: -1 no one, 0 to 1, low energy to high energy (same seen by ray)
15 - warm other specie: -1 no one, 0 to 1, low energy to high energy (same seen by ray)
16 - hearing same specie: -1 no one, 0 to 1, left to right (average point of screams)
17 - hearing other specie: -1 no one, 0 to 1, left to right (average point of screams)
18 - hearing same specie: -1 no one, 0 to 1, back to front (average point of screams)
19 - hearing other specie: -1 no one, 0 to 1, back to front (average point of screams)
20 - tracking fertile egg: -1 no egg, 0 to 1, far to close (don't care direction)
21 - energy: -1 to 1, low to high (at -1 will die)
22 - age: -1 to 1, birth and eld (at 1 will die)
ACT (6 actuators):
0 - move to front: -1 to 0 is quiet, 0 to 1 is run with proportionally speed
1 - rotate: -1 to 1, left to right with proportionally angle speed (0 is quiet)
2 - attack: -1 to 0 is not, 0 to 1 is true and will shoot at front (has sleep time)
3 - give: -1 to 0 is not, 0 to 1 is true and will pass energy to nearby front agent
4 - fertilize: -1 to 0 is not, 0 to 1 is true and will fecundate nearby egg
5 - scream: -1 to 0 is not, 0 to 1 is true and will emit sound
"""

import numpy as np

class brainAI(object):

    def __init__(self):
        # de configuracion
        self.time_cambio = 50
        # de funcionamiento
        self.reloj_cambio = 0
        self.direccion = 0.0
        self.cambialado = -1

    def copy(self):
        new = brainAI()
        new.time_cambio = self.time_cambio
        return new

    def execute(self, SEN, C):
        ACT = np.zeros(6, dtype=float) - 1
        self.relojes()
        # cambiar sentido de giro al chocar con paredes
        if SEN[4] == -1:
            self.cambialado = (-1 if np.random.rand(1)[0] > 0.5 else 1)
        # ver si hay comida cerca rayo
        if SEN[10] > -1:
            ACT[0] = 1
            ACT[1] = 0
        # ver si hay comida cerca vision
        elif SEN[6] > -1:
            ACT[0] = 1
            if SEN[6] < 0.5:
                ACT[1] = -1
            else:
                ACT[1] = 1
        # ver si olfatea comida
        elif SEN[0] > 0.2 and abs(self.direccion) < 0.25:
            ACT[0] = 0
            ACT[1] = 1
        # andar evitando muros
        else:
            # acelerar si no hay comida cerca
            ACT[0] = np.clip(1 - SEN[0], 0.75, 1)
            # ver colision con muros
            if SEN[4] > -1:
                if SEN[4] < 0.25:
                    self.direccion = 1.0
                elif SEN[4] > 0.75:
                    self.direccion = -1.0
                elif SEN[11] > 0.8:
                    self.direcion = float(self.cambialado)
            ACT[1] = self.direccion
        # acciones si hay energia
        if SEN[21] > 0.75:
            # dar ayuda
            if SEN[12] > 0.8 and SEN[14] < 0.25:
                ACT[3] = 1
            # disparar
            if SEN[13] > -1 and SEN[15] < 0.5 and SEN[12] == -1 and SEN[8] == -1:
                ACT[2] = 1
            # fertilizar
            if SEN[20] > 0.8:
                ACT[4] = 1
        return ACT

    def exportIA(self):
        data = str(self.time_cambio)
        return data

    def importIA(self, data):
        self.time_cambio = int(data)

    def spawn(self, mother, father):
        c = (-1.0 + np.random.rand(1)[0] * 2.0) * 10
        quien = (mother if father == None else
                 (mother if np.random.rand(1)[0] < 0.5 else father))
        self.time_cambio = int(np.clip(quien.time_cambio + c, 10, 200))

    def about(self):
        message = "brainOmi1 by Omarsaurio, ojorcio@gmail.com 2020\n" \
                  "un cerebro basico y experto, igual al presente en\n" \
                  "MicroEvoBrains de GMS, no cambiara mayormente en\n" \
                  "cuanto a performance durante la simulacion"
        return message

    def relojes(self):
        self.reloj_cambio -= 1
        if self.reloj_cambio <= 0:
            self.reloj_cambio = self.time_cambio
            self.direccion = (-1.0 + np.random.rand(1)[0] * 2.0)

"""
Work:
- 
"""
