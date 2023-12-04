# Blocks World problem: a revised version

Blocks World is a typical AI domain in which one imagines having a number of blocks (in our case a maximum of 6) identified by a number and a mechanical arm capable of performing certain actions that allow these blocks to be moved. This domain is typically used in search and planning problems in which, starting from an initial configuration, one is asked to find the actions to be performed by the mechanical arm so that an end state called goal is reached.

This program takes as input two images, one representing the initial state and one representing the goal state, from which it is able to extract configurations related to the blocks world. Once the states have been acquired, it allows the user to choose the search algorithm by which the set of moves necessary to move from one state to another will be found. At the end of the process, using the MatPlotLib library, an animation is created showing how the agent performs the required moves in order to go from the initial state to the goal state.

![animation](https://github.com/LucaSpadoni/blocks_world_problem/blob/main/images/animation/animation.gif)


# Constraints

The constraints with which this specific version of the problem was configured are listed below:
- blocks must be square;
- the blocks must all have the same size;
- each block can have at most one block directly above it (although there is no limit for the size of a block column (except the maximum height));
- the maximum number of blocks that can be used is 6;
- blocks are identified by a number sequentially starting with 1;
- blocks must only be placed on top of other blocks or on the surface (base) of the world (they cannot float);
- the world is a two-dimensional grid with finite width and height;
- width and height of the world can vary in each instance of it;
- width is an integer indicating the number of areas on which a block can be placed (maximum number of blocks placed on the floor);
- height is an integer that sets the maximum attainable height, forming a column that uses all the blocks in the current instance (maximum 6);
- each block must belong to only one zone;
- the mechanical arm can grab only one block at a time;
- the mechanical arm can only grab blocks that have no other blocks above them.


# Structure of the program

The program revolves mainly around 5 python files:
- the neuralnetwork.py file, in which we build, train and evaluate a convolutional neural network model (CNN) based on the MNIST handwritten digits dataset;
- the digitsdetector.py file, with which, through the OpenCV library, we extract the block digits from the two images passed as input to construct the two states;
- the custom_search.py file, which consists of the various search algorithms taken from the [AIMA-PYTHON](https://github.com/aimacode/aima-python) module that will be used to solve the problem;
- the blocks_world.py file, which is a class derived from Problem contained in AIMA and which defines the actions and various intermediate states to go from the initial state to the goal state;
- the main.py file, which takes care of the program execution.

The search algorithms that can be used to solve the problem are:
- uninformed algorithms:
    - BFS
    - DFS
    - UCS
    - IDS
    - DLS
- informed algorithms:
    - A*
    - RBFS

The pictures of the two states the program uses as input can be seen  and put in [images](https://github.com/LucaSpadoni/blocks_world_problem/tree/main/images). Under [states](https://github.com/LucaSpadoni/blocks_world_problem/tree/main/images/states) more samples of initial and goal states can be found (remember). These images can be either hand-written like in this case or digital-made since OpenCV seems to work well with both. For

![initial](https://github.com/LucaSpadoni/blocks_world_problem/blob/main/images/states/initial4.jpg)
![goal](https://github.com/LucaSpadoni/blocks_world_problem/blob/main/images/states/goal4.jpg)

We represent each state as a list of individual blocks, where each one is represented by the block number, its y-coordinate, its x-coordinate and the width of the world instance. For example the state relative to the previous image would be:
goal_state: ((1, 0, 0), (2, 0, 1), (3, 1, 1), (4, 0, 2), 3)


# How to run

First of all main.py must be launched by command line. During the execution you will be asked to enter the absolute path relative to the two images depicting the initial and goal states. After having processed the images, if the two configurations coincide or if they have a different number of blocks, the program will return an error and stop. Finally, you will be asked to choose the search algorithm with which you want to find the solution. 

