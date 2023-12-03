# Classe che risolve il problema del BlocksWorld dati gli stati iniziale e goal (istanza di Problem), basato sugli esempi dei file search.py e planning.py di AIMA

import time
import os
import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np
import imageio
from search import Problem

class BlocksWorld(Problem):

    def __init__(self, initial, goal):
        """ Define goal state and initialize the problem"""

        super().__init__(initial, goal)

    # Lista delle possibili azioni per lo stato attuale. Le azioni sono rappresentate come una tripla (numero blocco, nuova posizione asse y e nuova posizione asse x)
    def actions(self, state):
        """Return the actions that can be executed in the given state"""

        blocks = [*state[0:-1]]     # Prende tutti i blocchi contenuti nello stato dove -1 (che è escluso) è la larghezza
        choices = {}
        movable_blocks = []

        for block in blocks:
            block_number, x, y = block
            if y not in choices:    # Uso la y per controllare se il blocco è sopra un altro blocco o sul piano
                choices[y] = (block_number, x, y)
            else:
                if x > choices[y][1]:
                    choices[y] = (block_number, x, y)

        for choice in choices:
            movable_blocks.append(choices[choice])

        size = state[-1]    # Larghezza
        actions = []    # Lista contenente tutte le possibili azioni

        for block in movable_blocks:
            block_number, x, y = block
            for choice in range(size):      # Utilizzo la larghezza per definirmi quante zone sono utilizzabili per posizionare un blocco sul piano (o sopra di un altro)
                if choice != y:
                    if choice in choices:
                        actions.append((block_number, choices[choice][1] + 1, choice))  # Appendo le azioni possibili per quel blocco
                    else:
                        actions.append((block_number, 0, choice))   # Il blocco è messo sul piano
        return actions

    # Ritorna un nuovo stato dato uno stato e un'azione
    def result(self, state, actions):
        """Given state and action, returns a new state that is the result of the action. Action is assumed to be a valid action in the state"""

        blocks = [*state[0:-1]]     # Prende tutti i blocchi compresi nello stato
        size = state[-1]    # Prende la larghezza
        tmp = ()

        for block in blocks:
            if block[0] == actions[0]:  # Se il numero del blocco (nella lista dei blocchi) corrisponde al numero del blocco nella lista delle azioni, mi salvo il blocco
                tmp = block

        blocks.remove(tmp)  # Rimuove il blocco su cui è possibile l'azione 
        blocks.append((actions))    # Aggiunge la tripla che corrisponde alla nuova posizione del blocco secondo l'azione possibile
        blocks.append(size)

        return tuple(blocks)

    # Controlla se lo stato attuale è quello goal
    def goal_test(self, state):
        """Given a state, return True if state is a goal state or False, otherwise"""

        current = [*state[0:-1]]
        current.sort(key=lambda l: l[0])
        goal = [*self.goal[0:-1]]
        goal.sort(key=lambda l: l[0])

        return str(current) == str(goal)    # Se lo stato corrente è formato nello stesso modo dello stato goal

    # Rappresentazione animata del passaggio tra i vari stati, partendo dall'iniziale e arrivando a quello goal
    def solver(self, actions):
        """Creates a sequence of images that represent the shift between two states"""

        if len(actions) is None:
            return

        state = self.initial
        successor = None
        n = 1
        i = 0
        j = 0
        size = (len(actions) - 1)   # Mi serve per trovarmi l'azione che porta allo stato goal

        print("Stati creati: " + str(len(actions) - 1))     # Le azioni necessarie per arrivare al goal state
        print()
        print("Mosse necessarie:")

        for action in actions:
            i += 1

            if j != size:
                if n < 9:
                    print(f"Stato {n + 1}:    Sposta il blocco ", action[0], " in posizione (",action[2], ",",action[1],")" , sep='')
                else:
                    print(f"Stato {n + 1}:   Sposta il blocco ", action[0], " in posizione (",action[2], ",",action[1],")" , sep='')
            else:
                print("Stato Goal: Sposta il blocco ", action[0], " in posizione (",action[2], ",",action[1],")" , sep='')

            successor = self.result(state, action)
            img = self.graphical_representation(state)

            if n == 1:
                axis = plt.subplot(111)
                axis.imshow(img, cmap=plt.cm.binary)
                axis.set_xticks([])
                axis.set_yticks([])
                axis.text(10, 20, 'Sequenza degli stati\n', fontsize = 18, color = 'b')
                axis.set_xlabel('\nStato Iniziale\n')
       
            else:
                axis = plt.subplot(111)
                axis.imshow(img, cmap=plt.cm.binary)
                axis.set_xticks([])
                axis.set_yticks([])
                axis.text(10, 20, 'Sequenza degli stati\n', fontsize = 18, color = 'b')
                axis.set_xlabel(f'\nStato {n}')

            plt.savefig(r'C:\Users\spado\source\repos\ProgettoBlocksWorld\images\animation\frames\img_' + str(i) + '.png')   # Salva la figura creata come file png

            state = successor
            n += 1
            j += 1
        
        state = self.result(state, actions[size])
        img = self.graphical_representation(state)
        axis = plt.subplot(111)
        axis.imshow(img, cmap=plt.cm.binary)
        axis.set_xticks([])
        axis.set_yticks([])
        axis.text(10, 20, 'Sequenza degli stati\n', fontsize = 18, color = 'b')
        axis.set_xlabel(f'\nStato Goal')

        plt.savefig(r'C:\Users\spado\source\repos\ProgettoBlocksWorld\images\animation\frames\img_' + str(size + 2) + '.png')

        i = 0
        images = []

        for action in actions:
            i += 1
            images.append(imageio.imread(r'C:\Users\spado\source\repos\ProgettoBlocksWorld\images\animation\frames\img_' + str(i) + '.png'))

        images.append(imageio.imread(r'C:\Users\spado\source\repos\ProgettoBlocksWorld\images\animation\frames\img_' + str(size + 2) + '.png'))
        imageio.mimsave(r'C:\Users\spado\source\repos\ProgettoBlocksWorld\images\animation\animation.gif', images,  duration = 1.5)
        animation = imageio.mimread(r'C:\Users\spado\source\repos\ProgettoBlocksWorld\images\animation\animation.gif')
        
        nums = len(animation)
        range2 = (len(animation) + 1)
        num = range(range2)
        imgs = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in animation]  # Converte da RGB a BGR
        
        i = 0
        for j in num:
            cv2.waitKey(2000)
            cv2.imshow("Animazione", imgs[i])
            i = (i+1)%nums
        
        time.sleep(3)
        cv2.destroyAllWindows()

        files = glob.glob(r'C:\Users\spado\source\repos\ProgettoBlocksWorld\images\animation\frames\*')    
        for f in files:     # Elimina le immagini per la creazione dell'animazione dalla directory 'frames' per fare pulizia
            os.remove(f)

     # Rappresentazione grafica dello stato in input
    def graphical_representation(self, state):
        """Given a state, returns its graphical representation"""

        blocks = [*state[0:-1]]
        size = state[-1]    # Facendo così mi prendo la larghezza del mondo (cioè il numero massimo di blocchi presenti nell'istanza)
        blocks.sort(key=lambda l: l[1], reverse=True)
        height = blocks[0][1]    # Facendo così mi prendo l'altezza del mondo (cioè il numero massimo di blocchi presenti nell'istanza)

        img = np.zeros(((height + 1)*100, size*100), np.uint8)

        for block in blocks:
            block_number, x, y = block
            x = height - x
            digit = cv2.imread("./images/digits/" + str(block_number) + ".png", 0)
            digit = cv2.resize(digit, (100, 100))
            img[x*100:x*100 + 100, y*100:y*100 + 100] = ~digit  # '~' è il complenmento bit a bit

        size2 = (len(state) - 1)*100    # Per un'immagine abbastanza grande, sia altezza che larghezza sono moltiplicate per 100
        new_img = np.zeros((size2, size*100), np.uint8)
        new_img[size2 - (height + 1)*100 : size2, :] = img

        return new_img

    # Funzione di valutazione usata dall'UCS
    def f(self, node):
        """Evaluation function for the UCS algorithm that simply returns the depth of the current node (its distance from the starting node)"""
        
        distance = node.depth

        return distance

    # Euristica che calcola il numero dei blocchi attualmente non nella corretta posizione rispetto allo stato goal
    def h(self, node):
        """Heuristic - this heuristic calculates the number of blocks that are currently not in the correct position"""

        blocks = [*node.state[0:-1]]
        goal = [*self.goal[0:-1]]
        goal.sort(key = lambda l: l[0])
        res = 0

        for block in blocks:
            n, i, y = block
            if goal[n - 1][1:3] != (i, y):
                res += 1

        return res