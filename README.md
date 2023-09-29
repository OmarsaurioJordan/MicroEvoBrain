# MicroEvoBrain:

## DESCRIPTION:

This project is an evolutionary simulator for artificial intelligence algorithm competition. The simulator was created in Game Maker Studio, and the source code is included in the "MicroEvo.gmx" folder. All these files are also included in the executable "MicroEvoBrain.exe."

It consists of a 2D virtual world with randomly generated food. Walls can be added to complicate navigation. You can select 1 to 5 species of agents, differentiated by color. Each species can have its own artificial intelligence algorithm.

An agent requires energy to function and reproduce. It has a point counter that serves as fitness. There are 23 inputs or sensors from the environment and 6 outputs or actions (walk, rotate, shoot, donate energy, fertilize egg, scream). The inputs include smell, touch, hearing, vision, contact beam, energy from others and oneself, perception of time, and proximity to the egg.

The simulation software can run on its own, although limitedly. It includes a basic expert algorithm, an evolutionary MLP neural network, a manual mode to control the agent, and the UDP mode, which is the main feature.

In summary, UDP connects the Game Maker software with the Python code that manages external artificial intelligence algorithms. This manager is named "MicroEvoAdmin.py". Essentially, Game Maker Studio sends the agent's inputs. External algorithms process these inputs and send back the outputs through the manager, which are then received by the respective agent.

## FILES:

1. "MicroEvo.gmx":
Source code of the simulator created in Game Maker Studio.

2. "cerebroNeurotico.py":
General-purpose library for using MLP (Multi-Layer Perceptron) and DMNN (Dendral Morphological Neural Network) neural networks. These networks are fully configurable, exportable, and graphable in 2D. They currently do not have gradient descent algorithms for use but instead use genetic mutation and recombination. You can increase or decrease the number of logical units during training (neurons/layers, dendrites). This is done to compare these two neural network architectures under equal conditions and for unsupervised problems (without patterns).

3. "MicroEvoAdmin.py":
IA manager for "MicroEvoBrain.exe" or any other software that uses UDP communication. When executed, type the "help" command to get a list of all commands. You will find information about the code, command descriptions, simulator software controls, etc.

4. "brainDMNN1.py", "brainDMNN2.py", "brainMLP1.py", "brainMLP2.py":
Examples of AI algorithms to be managed by the manager. They all use the "cerebroNeurotico.py" library included here.

5. "brainOmi1.py":
Another example of an AI algorithm to be managed by the manager. This algorithm is the same one internally used by the code created in Game Maker, mentioned as the basic expert algorithm.

6. "templateAI.py":
This blank document serves as the foundation for creating your own AI following the rules and protocols written there. Following these guidelines ensures proper connection to the simulator. The document contains all the information regarding the agent's inputs and outputs.

7. "testRedes.py":
Raw test code for the "cerebroNeurotico.py" library. Here, classification problems in txt format can be imported and tested. The code includes internal examples such as gates or handpicked noisy points. This classification software uses most evolutionary functions of the library, demonstrating the capabilities of both types of networks and the viability of solving problems stochastically.

8. "mlp_ejemplote.png", "dmnn_ejemplote.png":
Two images resulting from the "testRedes.py" code, showing the decision surface of both types of networks for a 2D problem with a demanding geometric shape. This problem is included by default in the mentioned code. To view the images, execute the code and enter the "demo" command.

9. "ejemplito.txt", "espiral2.txt", "glass.txt", "iris.txt":
Datasets to use with "testRedes.py". Iris and glass datasets are classic and represent real-world problems. Ejemplito and espiral2 are synthetic 2D datasets created to push the networks to their limits.

## TEST:

To test the library, run "testRedes.py" and then enter the command "demo". This will allow you to verify its functionality. You can access all the commands by typing "help".

For the simulation software, follow these steps:

1. Run "MicroEvoBrain.exe" (or the editable version from GMS). Observe how it functions on its own.

2. Execute "MicroEvoAdmin.py" (the order doesn't matter). Enter the command "demo" to verify the joint functionality. You can do this by typing "information" and then "2".

3. Finally, type "help" to access all the available commands. Enjoy exploring the various functionalities!

## OPERATION:

In the GMS simulation, cycles are performed where each agent senses the environment, executes the AI, and obtains the outputs. These outputs are used to calculate collisions, shots, deaths, and fitness (refer to "EvoPID.exe," another creation by the author).

When characters reproduce asexually, an egg with information is created. Upon hatching, it generates the new agent. If the egg is fertilized, reproduction can be sexual if the algorithm supports it.

During world reset, the best AIs are saved to mentor a new generation.

The Python administrator receives various commands. The UDP protocol details can be found in the "help.rtf" file inside the GMS folder. If there isn't an associated AI class for the agent's ID, a new one is created. If input data is sent, the administrator creates a thread to execute the AI and return the output.

The received execution data is queued, and a thread is responsible for traversing the queue to obtain the latest data if it hasn't expired. This thread also checks if an AI has been inactive for a while and doesn't belong to the best group. In such a case, it is removed to free up memory (likely because its agent has died).

In the case of reproduction, GMS sends the command, and the administrator locates the corresponding AI classes to instruct them on recombination or mutation. Many try statements are used to prevent failures from the code of each AI.

## FUTURE WORK:

The GMS software is complete, but there's room for enhancements, such as adding sounds or additional flags. For example, flags could be added to disable violent shots or add fitness for such actions.

Nevertheless, both the GMS simulation and the Python administrator are self-sufficient. For instance, a simulation could be created in Godot, which is open-source and supports 3D, to replace GMS. Conversely, a better administrator with a graphical user interface (GUI) could be developed.

Additionally, in Godot, an extra software could be created that allows various human players to have limited visibility of the environment (similar to how an agent sees it) and act within it. This setup would enable the comparison of human brains with neural networks, eliminating the powerful human ability to see the simulation screen when controlling manually. This interaction could also happen via UDP, creating a third independent software. This software might even turn the project into an engaging game, providing better patterns for supervised training.

The "cerebroNeurotico.py" library (if I can call it that) contains a list of future work and improvements.

Lastly, thorough testing should be conducted to identify and correct any errors.

## INTENTION:

What if we challenge our fellow programmers to create the best AI? One that, for instance, creates an internal map of the environment (similar to mobile robotics). Competitions could be organized, involving groups, universities, etc., with juicy prizes included.

## CREATOR:

Omwekiatl (Omar Jordan Jordan)

Colombia 2020

mail: [ojorcio@gmail.com]

Link: [https://linktr.ee/omwekiatl]

Indie game developer in free time, as well as creator of various software. In the link, you'll find my art and other links to my projects (check Dropbox).

I recommend looking for "SoftwareDMNN.exe" to understand DMNN. It's somewhere out there and was my thesis work, so it's well-documented (and with accents), and it's open source.

## LICENSE:

The finished software is free and open source. It can be used and modified as long as attribution to the creator is retained. Be free, honey.
