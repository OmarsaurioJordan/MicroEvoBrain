# Template for AI competition simulation by Omarsaurio ojorcio@gmail.com 2020
# write here a line about your work (similar to mine)

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

"""
import the libraries you want, for example numpy, obviously you don't need PyQt5
"""
import numpy as np

class brainAI(object):
    """
    This class contains all the necessary methods to handle the IA agent, some
    functions must be write for accomplish the requirements, other can be
    created if you need, don't change the class name
    """

    def __init__(self):
        """
        your main variables must be here, start the system
        """

    def copy(self):
        """
        To can duplicate the system, this is important for we, especially
        when systems evolve with time
        :return: a new object of this same class
        """
        return new

    def execute(self, SEN, C):
        """
        Here go all the IA logic, you don't make the infinite loop, only one cycle
        use the sensed data to generate te actuation signals, for example, you
        can create an artificial neural network that make it. In the other hand, you
        have the fitness points, it in case that you can create your own optimizing
        algorithm in one generation, so the spawn system can do it evolutionarily
        - Note: to see the sensors / actuators structure, read the Agent Description
        :param SEN: sensors, numpy float array between -1 and 1, size 23
        :param C: float points of fitness, accumulate it will be fitness
        :return: ACT: actuators, numpy float array between -1 and 1, size 6
        """
        return ACT

    def exportIA(self):
        """
        This is to save the state of the system, if you need to do it
        :return: string ready to be saved in a .txt file
        """
        return data

    def importIA(self, data):
        """
        This is for open a saved state of the system, is the inverse
        operation of exportIA, if you need save the state at all
        :param data: string that was read from the .txt file
        """

    def spawn(self, mother, father):
        """
        Similar to copy, but here you can make this class be some different to
        the original, like genetic mutations, optionally you can perform
        recombination using another optional original object
        :param mother: always be a reference to another object of this same class
        :param father: another object reference like mother, or None
        """

    def about(self):
        """
        Write some about you, your code, version, year, contact, etc
        don't contains blank line breaks, all in one paragraph, this
        because the main administration code, could show different abouts
        separated by blank line breaks, to look good
        :return: string with the adequate line breaks
        """
        return message

    """
    Add down the other functions you need, the up functions are obligatory 
    """

    def exampleFunction(self, input):
        output = input * 2
        return output

"""
Work:
- write here future ideas or unfinished things
- separated by hyphen
- like: make to emerge conscience
"""
