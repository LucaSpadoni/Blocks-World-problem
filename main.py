import os
import time
import sys
import colorama
from colorama import Fore
from custom_search import breadth_first_graph_search, depth_first_graph_search, uniformed_cost_search, iterative_deepening_search, depth_limited_search, astar_search, recursive_best_first_search
from digitsdetector import get_state
from blocks_world import BlocksWorld

colorama.init(autoreset=True)

def main():
    search_algorithm = {    # Dizionario
        "bfs": breadth_first_graph_search,
        "dfs": depth_first_graph_search,
        "ucs": uniformed_cost_search,
        "ids": iterative_deepening_search,
        "dls": depth_limited_search,
        "astar": astar_search,
        "rbfs": recursive_best_first_search
    }

    bfs = "bfs"
    dfs = "dfs"
    ucs = "ucs"
    ids = "ids"
    dls = "dls"
    astar = "astar"
    rbfs = "rbfs"

    os.system('cls' if os.name == 'nt' else 'clear')

    print() 
    print(f"\t {Fore.BLUE}◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘ ") 
    print(f"\t {Fore.RED}░▒▓{Fore.YELLOW}               ╔═════╗╔═╗            ╔═╗       ╔═╗    ╔═╗          ╔═╗     ╔═╗              {Fore.RED} ▓▒░ ")
    print(f"\t {Fore.RED}░▒▓{Fore.YELLOW}      ┏━━━┓    ║ ╔═╗ ║║ ║            ║ ║       ║ ║    ║ ║          ║ ║     ║ ║    ┏━━━┓     {Fore.RED} ▓▒░ ")
    print(f"\t {Fore.RED}░▒▓{Fore.YELLOW}      ┃ 3 ┃    ║ ╚═╝ ╚╣ ║ ╔═════╦════╣ ║╔═╦════╣ ║ ╔╗ ║ ╠═════╦════╣ ║ ╔═══╝ ║    ┃ 5 ┃     {Fore.RED} ▓▒░ ")
    print(f"\t {Fore.RED}░▒▓{Fore.YELLOW}  ┏━━━╋━━━┫    ║ ╔══╗ ║ ║ ║ ╔═╗ ║ ╔══╣ ╚╝ ╣ ═══╣ ╚═╝╚═╝ ║ ╔═╗ ║ ╔══╣ ║ ║ ╔═╗ ║    ┣━━━╋━━━┓ {Fore.RED} ▓▒░ ")
    print(f"\t {Fore.RED}░▒▓{Fore.YELLOW}  ┃ 1 ┃ 2 ┃    ║ ╚══╝ ║ ╚═╣ ╚═╝ ║ ╚══╣ ╔╗ ╬═══ ╠═╗ ╔╗ ╔═╣ ╚═╝ ║ ║  ║ ╚═╣ ╚═╝ ║    ┃ 4 ┃ 6 ┃ {Fore.RED} ▓▒░ ")
    print(f"\t {Fore.RED}░▒▓{Fore.YELLOW}  ┗━━━┻━━━┛    ╚══════╩═══╩═════╩════╩═╝╚═╩════╝ ╚═╝╚═╝ ╚═════╩═╝  ╚═══╩═════╝    ┗━━━┻━━━┛ {Fore.RED} ▓▒░ ")
    print(f"\t {Fore.BLUE}◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘◘ ")
    print()

    time.sleep(2)

    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')

            initial_state_path = input("Insert the absolute path of the initial state: ")   
            initial_state = get_state(initial_state_path)
            print("\nThe relative initial state will be: ")

            for i in range(len(initial_state) - 1):
                print("Block ", initial_state[i][0], " in position (", initial_state[i][2], ",", initial_state[i][1], ")", sep='')

            print("The width will be:", initial_state[len(initial_state) -1]) 

            input("\Press enter to continue...")
            break

        except Exception as e:
            print(e)
            print("File not found!")
            time.sleep(2)

    while True:
        try:    
            os.system('cls' if os.name == 'nt' else 'clear')

            goal_state_path = input("insert the absolute path of the goal state: ")   
            goal_state = get_state(goal_state_path)
            print("\nThe relative goal state will be: ")

            for i in range(len(goal_state) - 1):
                print("Block ", goal_state[i][0], " in position (", goal_state[i][2], ",", goal_state[i][1], ")", sep='')

            print("The width will be:", goal_state[len(goal_state) -1]) 
            input("\nPress enter to continue...")

            break

        except Exception:
            print("\nFile not found!")    
            time.sleep(2)
        
    if initial_state == goal_state:
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.exit("\nThe initial state and goal state are the same\n")
        
    if len(initial_state) != len(goal_state):
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.exit("\nThe intial state and goal state must have the same number of blocks\n")

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Choose the search algorithm that you want to use (or exit the program): - bfs")
        print("                                                                        - dfs")
        print("                                                                        - ucs")
        print("                                                                        - dls")
        print("                                                                        - ids")
        print("                                                                        - astar")
        print("                                                                        - rbfs")
        print("------------------------------------------------------------------------------")
        print("                                                                        - exit")
        choice = input("--> ")
        
        print()

        if choice in (bfs, dfs, ucs, dls, ids, astar, rbfs):
            parameter_functions = {
                "ucs": lambda n: problem.f(n),
                "astar": lambda n: problem.h(n),
                "rbfs": lambda n: problem.h(n)
            }

            problem = BlocksWorld(initial_state, goal_state)

            if choice in (bfs, dfs, dls, ids):
                problem.solver(search_algorithm[choice](problem).solution())

            elif choice in (ucs, astar, rbfs):
                problem.solver(search_algorithm[choice](problem, parameter_functions[choice]).solution())

            print()
            input("Press enter to continue...")

        elif choice == "esci":
            break

        else:
            print("\nInsert a valid choice!")
            time.sleep(2)

if __name__ == '__main__':
    main()
