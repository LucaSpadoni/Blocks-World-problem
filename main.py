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

            initial_state_path = input("Inserisci il path dell'immagine dell'initial state: ")   # C:\Users\spado\source\repos\ProgettoBlocksWorld\images\initial.jpg
            initial_state = get_state(initial_state_path)
            #initial_state = get_state(r"C:\Users\spado\source\repos\ProgettoBlocksWorld\images\initial.jpg")
            print("\nLo stato iniziale relativo sarà: ")

            for i in range(len(initial_state) - 1):
                print("Blocco ", initial_state[i][0], " in posizione (", initial_state[i][2], ",", initial_state[i][1], ")", sep='')

            print("La larghezza sarà:", initial_state[len(initial_state) -1]) 

            input("\nPremi invio per continuare...")
            break

        except Exception as e:
            print(e)
            print("File non trovato!")
            time.sleep(2)

    while True:
        try:    
            os.system('cls' if os.name == 'nt' else 'clear')

            goal_state_path = input("Inserisci il path dell'immagine del goal state: ")   # C:\Users\spado\source\repos\ProgettoBlocksWorld\images\goal.jpg
            goal_state = get_state(goal_state_path)
            #goal_state = get_state(r"C:\Users\spado\source\repos\ProgettoBlocksWorld\images\goal.jpg")
            print("\nLo stato goal relativo sarà: ")

            for i in range(len(goal_state) - 1):
                print("Blocco ", goal_state[i][0], " in posizione (", goal_state[i][2], ",", goal_state[i][1], ")", sep='')

            print("La larghezza sarà:", goal_state[len(goal_state) -1]) 
            input("\nPremi invio per continuare...")

            break

        except Exception:
            print("\nFile non trovato!")    
            time.sleep(2)
        
    if initial_state == goal_state:
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.exit("\nLo stato iniziale e lo stato goal corrispondono!\n")
        
    if len(initial_state) != len(goal_state):
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.exit("\nLo stato iniziale e lo stato goal devono avere lo stesso numero di blocchi!\n")

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Inserisci l'algoritmo di ricerca che vuoi utilizzare (oppure esci): - bfs")
        print("                                                                    - dfs")
        print("                                                                    - ucs")
        print("                                                                    - dls")
        print("                                                                    - ids")
        print("                                                                    - astar")
        print("                                                                    - rbfs")
        print("---------------------------------------------------------------------------")
        print("                                                                    - esci")
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
            input("Premi invio per continuare...")

        elif choice == "esci":
            break

        else:
            print("\nInserire una scelta valida!")
            time.sleep(2)

if __name__ == '__main__':
    main()
