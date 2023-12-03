# Implementazione dei vari algoritmi di ricerca visti a lezione presi dal file search.py di AIMA ed usati per la risoluzione del BlocksWorld

import sys
from collections import deque
import time
import numpy as np
from utils import memoize, PriorityQueue
from search import Node

FRONTIER_DIMENSION = 0  # Dimensione della frontiera temporanea
EXPANDED_NODES = 0  # Numero di nodi espansi durante la ricerca
FRONTIER_LENGTH = 0     # Massimo numero di nodi presenti nella frontiera durante la ricerca
START_TIME = 0     # Tempo di esecuzione dell'algoritmo
START_TIME_IDS = 0     # Tempo di esecuzione dell'algoritmo

# __________________________________________________________________________________________________________________________
# Uninformed Search algorithms

# BFS
def breadth_first_graph_search(problem):
    global FRONTIER_DIMENSION, EXPANDED_NODES, FRONTIER_LENGTH, START_TIME
    FRONTIER_DIMENSION = 0
    EXPANDED_NODES = 0
    FRONTIER_LENGTH = 0
    START_TIME = 0 
    START_TIME = time.time()

    node = Node(problem.initial)
    frontier = deque([node])
    FRONTIER_DIMENSION += 1
    explored = set()

    while frontier:
        EXPANDED_NODES += 1
        node = frontier.popleft()
        FRONTIER_DIMENSION -= 1
        explored.add(node.state)

        if problem.goal_test(node.state):
            running_time = time.time() - START_TIME

            print("Numero nodi espansi: ", EXPANDED_NODES)
            print("Massima dimensione della frontiera: ", FRONTIER_LENGTH)
            print("Tempo di esecuzione dell'algoritmo: ", running_time)
            return node

        for child in node.expand(problem):  # Le azioni possibili
            if child.state not in explored and child not in frontier:
                frontier.append(child)
                FRONTIER_DIMENSION += 1
                FRONTIER_LENGTH = max(FRONTIER_DIMENSION, FRONTIER_LENGTH)

# DFS
def depth_first_graph_search(problem):
    global FRONTIER_DIMENSION, EXPANDED_NODES, FRONTIER_LENGTH, START_TIME
    FRONTIER_DIMENSION = 0
    EXPANDED_NODES = 0
    FRONTIER_LENGTH = 0
    START_TIME = 0 
    START_TIME = time.time()

    frontier = deque([Node(problem.initial)])   # Stack
    FRONTIER_DIMENSION += 1
    explored = set()

    while frontier:
        node = frontier.pop()   # LIFO
        FRONTIER_DIMENSION -= 1
        EXPANDED_NODES += 1

        if problem.goal_test(node.state):
            running_time = time.time() - START_TIME
            print("Numero nodi espansi: ", EXPANDED_NODES)
            print("Massima dimensione della frontiera: ", FRONTIER_LENGTH)
            print("Tempo di esecuzione dell'algoritmo: ", running_time)
            return node

        explored.add(node.state)

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
                FRONTIER_DIMENSION += 1
                FRONTIER_LENGTH = max(FRONTIER_DIMENSION, FRONTIER_LENGTH)


# UCS
def uniformed_cost_search(problem, f):
    """Search the nodes with the lowest f scores first. You specify the function f(node) that you want to minimize; for example, if f is a heuristic estimate 
    to the goal, then we have greedy best first search; if f is node.depth then we have breadth-first search. There is a subtlety: the line "f = memoize(f, 'f')" 
    means that the f values will be cached on the nodes as they are computed. So after doing a best first search you can examine the f values of the path returned."""
    
    global FRONTIER_DIMENSION, EXPANDED_NODES, FRONTIER_LENGTH, START_TIME
    FRONTIER_DIMENSION = 0
    EXPANDED_NODES = 0
    FRONTIER_LENGTH = 0
    START_TIME = 0 
    START_TIME = time.time()

    node = Node(problem.initial)

    if problem.goal_test(node.state):
        running_time = time.time() - START_TIME
        print("Numero nodi espansi: ", EXPANDED_NODES)
        print("Massima dimensione della frontiera: ", FRONTIER_LENGTH)
        print("Tempo di esecuzione dell'algoritmo: ", running_time)
        return node

    f = memoize(f, 'f')     # Aggiunge al nodo l'attributo nodo.f = f(nodo)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    FRONTIER_DIMENSION += 1
    explored = set()

    while frontier:
        node = frontier.pop()   # Estrae il nodo con costo più basso
        FRONTIER_DIMENSION -= 1

        expand = node.expand(problem)
        EXPANDED_NODES += len(expand)

        if problem.goal_test(node.state):
            running_time = time.time() - START_TIME
            print("Numero nodi espansi: ", EXPANDED_NODES)
            print("Massima dimensione della frontiera: ", FRONTIER_LENGTH)
            print("Tempo di esecuzione dell'algoritmo: ", running_time)
            return node
        
        explored.add(node.state)

        for child in expand:
            if child.state not in explored and child not in frontier:
                frontier.append(child)
                FRONTIER_DIMENSION += 1
                FRONTIER_LENGTH = max(FRONTIER_DIMENSION, FRONTIER_LENGTH)
                    
            elif child in frontier:
                incumbent = frontier.get_item(child)
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)

# DLS
def depth_limited_search(problem, limit = 10):
    global FRONTIER_DIMENSION, EXPANDED_NODES, FRONTIER_LENGTH, START_TIME, START_TIME_IDS
    FRONTIER_DIMENSION = 0
    EXPANDED_NODES = 0
    FRONTIER_LENGTH = 0 
    START_TIME = 0 
    START_TIME = time.time()

    def recursive_dls(node, problem, limit):
        global FRONTIER_DIMENSION, EXPANDED_NODES, FRONTIER_LENGTH, START_TIME, START_TIME_IDS
        
        EXPANDED_NODES += 1

        if problem.goal_test(node.state):
            if START_TIME_IDS == 0:
                running_time = 0
                running_time = time.time() - START_TIME
                print("Numero nodi espansi: ", EXPANDED_NODES)
                print("Massima dimensione della frontiera: ", FRONTIER_LENGTH)
                print("Tempo di esecuzione dell'algoritmo: ", running_time)
            elif START_TIME_IDS != 0:
                running_time = 0
                running_time = time.time() - START_TIME_IDS
                print("Numero nodi espansi: ", EXPANDED_NODES)
                print("Massima dimensione della frontiera: ", FRONTIER_LENGTH)
                print("Tempo di esecuzione dell'algoritmo: ", running_time)
                START_TIME_IDS = 0 
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                FRONTIER_DIMENSION += 1
                FRONTIER_LENGTH = max(FRONTIER_DIMENSION, FRONTIER_LENGTH)
                result = recursive_dls(child, problem, limit - 1)
                FRONTIER_DIMENSION -= 1

                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    # Body of depth_limited_search:
    return recursive_dls(Node(problem.initial), problem, limit)

# IDS
def iterative_deepening_search(problem):
    global FRONTIER_DIMENSION, EXPANDED_NODES, START_TIME_IDS
    FRONTIER_DIMENSION = 0
    EXPANDED_NODES = 0
    n_nodes = 0
    START_TIME_IDS = 0 
    START_TIME_IDS = time.time()

    for depth in range(sys.maxsize):
        FRONTIER_DIMENSION += 1
        result = depth_limited_search(problem, depth)
        n_nodes = EXPANDED_NODES
        FRONTIER_DIMENSION = 0

        if result != 'cutoff':
            return result

# __________________________________________________________________________________________________________________________
# Informed (Heuristic) Search algorithms

# A*
def astar_search(problem, h):
    """A* search is uniformed_cost graph search with f(n) = g(n)+h(n). You need to specify the h function when you call astar_search, or else in your Problem subclass."""
    h = memoize(h or problem.h)
    return uniformed_cost_search(problem, lambda n: n.path_cost + h(n))

# RBFS
def recursive_best_first_search(problem, h):
    global FRONTIER_DIMENSION, EXPANDED_NODES, FRONTIER_LENGTH, START_TIME
    FRONTIER_DIMENSION = 0
    EXPANDED_NODES = 0
    FRONTIER_LENGTH = 0  
    START_TIME = 0 
    START_TIME = time.time()

    f = memoize(lambda n: g(n) + h(n),'f')
    g = memoize(lambda n: n.path_cost, 'g')
    h = memoize(h or problem.h, 'h')

    def RBFS(problem, node, flimit=np.inf):
        global FRONTIER_DIMENSION, EXPANDED_NODES, FRONTIER_LENGTH

        EXPANDED_NODES += 1

        if problem.goal_test(node.state):
            running_time = time.time() - START_TIME            
            print("Numero nodi espansi: ", EXPANDED_NODES)
            print("Massima dimensione della frontiera: ", FRONTIER_LENGTH)
            print("Tempo di esecuzione dell'algoritmo: ", running_time)
            return node, 0  # The second value is immaterial

        successors = [*node.expand(problem)]
        FRONTIER_DIMENSION += len(successors)
        FRONTIER_LENGTH = max(FRONTIER_DIMENSION, FRONTIER_LENGTH)

        if len(successors) == 0:
            return None, np.inf

        for s in successors:
            s.f = max(f(s), node.f)

        while True:
            # Order by lowest f value
            successors.sort(key=lambda x: x.f)
            best = successors[0]

            if best.f > flimit:
                FRONTIER_DIMENSION -= len(successors)
                return None, best.f

            alternative = successors[1].f if len(successors) > 1 else np.inf
            # IMPORTANTE sovrascrivere best.f
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            # Return result
            if result is not None:
                FRONTIER_DIMENSION -= len(successors)
                return result, best.f

    node = Node(problem.initial) 
    f(node)
    FRONTIER_DIMENSION += 1

    return RBFS(problem, node)[0]