"""

Essa implementação é a mesma que a do LizardGame da outra pasta. Houve apenas a modificação na denominação dos valores da qtable
de self.values para self.QTable, para maior entendimento.   

Autor: Felipe Churuyuki Chinen
"""

import numpy as np
import random as rd
import pprint
import pandas as pd

class qtable:
    """
    v0 are the initial values for the Q-Table.
    """
    def __init__(self, alpha = 0.7 , discount = 0.99, egreedy = 1, decay_rate = 0.93, min_steps = 1000, actions = [1, 2], N =2, goal_pos = 1, goal_reward = 10):
        self.actions = actions
        self.N = N # matrix N,N
        self.QTable = {}
        self.goal_pos = goal_pos
        self.goal_reward = goal_reward
        self.create_dictionary()
        self.alpha = alpha # Taxa de aprendizado
        self.discount = discount # Taxa de desconto
        self.egreedy = egreedy # Epsilon Greedy
        self.decay_rate = decay_rate # Taxa de decaimento


        # As variáveis daqui para frente, são apenas para verificar performance

        self.trajectories = [] # Lista que conterá as trajetórias que irão conter cada estado percorrido
        self.stop_rate = 0.025 # Fator adicionado, quando a trajetória passar de fator, o algoritmo irá finalizar e irá printar a melhor trajetória e o seu melhor resultado
        self.min_steps = min_steps
        self.unique_trajectory = [] # Lista que contém as trajetórias sem repetição
        self.trajectories_score = {} # Dicionário que contém os scores de cada trajetória.
        self.n_best_values = 3 # 

    def create_dictionary(self):
        """
        Há a criação da QTable dentro da QTable.
        Para cada posição da matriz de estados, haverá um valor chave no dicionário.
        Para cada valor de estado, haverá um valor que contera uma dupla chave e valor, a primeira indicando a ação
        e a segunda indicando o valor.
        """
        for i in range(0, (self.N*self.N)):
            aux={}
            for j in self.actions:
                aux[j] = rd.random()
            self.QTable[i] = aux
            if i == self.goal_pos:
                aux[j] = self.goal_reward
                self.QTable[i] = aux[j]


    def print_qtable(self):

        df = pd.DataFrame(self.QTable)
        df = df.transpose
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print(df)
        #pp = pprint.PrettyPrinter(indent = 4)
        #pp.pprint(self.QTable)
        
    def explore(self, actions, cur_state):
        choice = rd.randint(0, actions.size - 1)
        return actions[choice]


    def exploit(self, actions, cur_state):
        _, action = self.max_q_next_state(cur_state, actions)
        return action

    def max_q_next_state(self, cur_state, actions): # Essa função retorna a próxima ação a ser tomada e o valor da qtable
        max_q = float('-inf') # Valor para debug
        best_action = -7 # Valor para debug
        for action in actions:
            cur_q = self.QTable[(cur_state[0]*self.N+cur_state[1])][action]
            if cur_q > max_q:
                max_q = cur_q
                best_action = action
        if max_q == float('-inf'):
            print('Bug no MAX Q NEXT STATE')
        return max_q, best_action

    def update_q(self, next_s_a, taken_action, cur_state, cur_reward):

        best_q = float('-inf')
        for candidate_best_states in next_s_a:
            s, a = candidate_best_states
            best_q_aux, _ = self.max_q_next_state(s, a)
            if (best_q_aux > best_q):
                best_q = best_q_aux
        # Obtendo o valor do Valor aprendido(Learning Value)
        l_value = cur_reward + best_q 

        # Equação: new Q = 1 - alpha & old Q + alfa * learned value
        # cur_state[0]*self.N + cur_state[1] - 1
        self.QTable[cur_state[0]*self.N + cur_state[1] - 1][taken_action] = (1-self.alpha)*self.QTable[cur_state[0]*self.N + cur_state[1] - 1][taken_action] + self.alpha*(l_value)

    def update_trajectory_list(self, last_trajectory, score):
        if last_trajectory in self.unique_trajectory: # Verifica se a trajetória já está na lista de trajetórias
            self.trajectories_score[self.unique_trajectory.index(last_trajectory)]["count"] += 1 # Se estiver aumenta um no contador
        else:
            self.unique_trajectory.append(last_trajectory) # Se não estiver adicinoa na lista
            self.trajectories_score[self.unique_trajectory.index(last_trajectory)] = {"score" : 0, "count" : 0} # Adiciona um novo valor para a trajetória
            self.trajectories_score[self.unique_trajectory.index(last_trajectory)]["score"] = score # Atribui o valor da sua pontuação
            self.trajectories_score[self.unique_trajectory.index(last_trajectory)]["count"] = 1 # Inicializa o contador como 1


    def print_trajectories(self):
        pp = pprint.PrettyPrinter(indent = 4)
        pp.pprint(self.trajectories_score)

    def choose_action(self, actions, cur_state):
        self.egreedy *= self.decay_rate # Multiplicando pela taxa de decaimento, aumentando a chance do agente explorar ao invés de aprender
        rng = rd.random()
        print('rng = '+str(rng)+' egreedy = '+str(self.egreedy))
        if rng < self.egreedy: # Compara o fator egreedy com um valor aleatório.
            
            return self.explore(actions, cur_state) # Aprende no caso de ser menor que egreedy
        else:
            return self.exploit(actions, cur_state) # Explora caso seja maior