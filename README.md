# Blocks World problem: a revised version

Blocks World is a typical AI domain in which one imagines having a number of blocks (in our case a maximum of 6) identified by a number and a mechanical arm capable of performing certain actions that allow these blocks to be moved. This domain is typically used in search and planning problems in which, starting from an initial configuration, one is asked to find the actions to be performed by the mechanical arm so that an end state called goal is reached.

This program takes as input two images, one representing the initial state and one representing the goal state, from which it is able to extract configurations related to the blocks world. Once the states have been acquired, it allows the user to choose the search algorithm by which the set of moves necessary to move from one state to another will be found. At the end of the process, using the MatPlotLib library, an animation is created showing how the agent performs the required moves in order to go from the initial state to the goal state.

![animation](https://github.com/LucaSpadoni/blocks_world_problem/blob/main/images/animation/animation.gif)


# Structure of the program

The program revolves mainly around 5 python files:
- the neuralnetwork.py file, in which we build, train and evaluate a convolutional neural network model (CNN) based on the MNIST handwritten digits dataset;
- the digitsdetector.py file, with which, through the OpenCV library, we extract the block digits from the two images passed as input to construct the two states;
- the custom_search.py file, which consists of the various search algorithms taken from the [AIMA-PYTHON](https://github.com/aimacode/aima-python) module that will be used to solve the problem;
- the blocks_world.py file, which is a class derived from Problem contained in AIMA and which defines the actions and various intermediate states to go from the initial state to the goal state;
- the main.py file, which takes care of the program execution.




This program takes as input two images, one representing the initial state and one representing the goal state, from which it is able to extract configurations related to the blocks world. Once the states have been acquired
![initial](https://github.com/LucaSpadoni/blocks_world_problem/blob/main/images/initial.jpg)
![goal](https://github.com/LucaSpadoni/blocks_world_problem/blob/main/images/goal.jpg)
