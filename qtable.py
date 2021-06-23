"""
Foi modificado a QTable para funcionar como aproximador de função.
Foi necessário a modificação das posições de [-2,2] sendo floats, por causa da transformação
numérica de decimal para binário
ao somar 0.2 a 0 o número se transforma em 1.9999996
Assim, estou remapeando os valores
-2 -> 0
-1.8 ->1
 e assim por diante, pois o passo é de 0.2.

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
    def __init__(self, alpha = 0.7 , discount = 0.99, egreedy = 1, decay_rate = 0.999, min_steps = 1000, actions = [0, 1, 2, 3], N = 8, goal_reward = 10):
        self.actions = actions
        self.N = N # matrix NxN
        self.QTable = {}
        self.goal_reward = goal_reward
        
        
        self.alpha = alpha # Taxa de aprendizado
        self.discount = discount # Taxa de desconto
        self.egreedy = egreedy # Epsilon Greedy
        self.decay_rate = decay_rate # Taxa de decaimento

        self.array_pos = [] # Array de posições
        self.create_positions()

        self.create_dictionary()

        # Dicionário que irá conter a quantidade de vezes que o agente passa pelo estado
        self.count_dict = {}
        self.create_count_dict()


        # As variáveis daqui para frente, são apenas para verificar performance

        self.trajectories = [] # Lista que conterá as trajetórias que irão conter cada estado percorrido
        self.stop_rate = 0.025 # Fator adicionado, quando a trajetória passar de fator, o algoritmo irá finalizar e irá printar a melhor trajetória e o seu melhor resultado
        self.min_steps = min_steps
        self.unique_trajectory = [] # Lista que contém as trajetórias sem repetição
        self.trajectories_score = {} # Dicionário que contém os scores de cada trajetória.
        self.n_best_values = 3 # 

    def create_positions(self):
        for i in range(self.N+1):
            for j in range(self.N+1):
                self.array_pos.append([i,j])

    def create_dictionary(self):
        """
        Para a criação dessa matriz, será necessário a passagem de uma lista
        que contém cada posição da matriz
        """
        for pos in self.array_pos:
            aux={}
            for j in self.actions:
                aux[j] = 0#rd.random()
                #aux[j] = rd.random()
            #pos_dict = self.pos_to_num(pos[0],pos[1]) # A posição não precisa ser convertida
            pos_dict = str(pos[0])+'-'+str(pos[1])
            self.QTable[pos_dict] = aux

    def create_count_dict(self):
        """
        Contagem de vezes que o agente esteve no estado
        """
        for pos in self.array_pos:
            pos_dict = str(pos[0])+'-'+str(pos[1])
            self.count_dict[pos_dict] = 0

    def print_count_dict(self):
        pp = pprint.PrettyPrinter(indent = 4)
        pp.pprint(self.count_dict)



    def print_qtable(self):

        df = pd.DataFrame(self.QTable)
        df = df.transpose
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print(df)
        #pp = pprint.PrettyPrinter(indent = 4)
        #pp.pprint(self.QTable)
        
    def explore(self, actions, cur_state):
        print("explorando")
        choice = rd.randint(0, len(actions) - 1)
        return actions[choice]


    def exploit(self, actions, cur_state):
        print("EXPLOITANDO")
        _, action = self.max_q_next_state(cur_state, actions)
        return action

    def max_q_next_state(self, cur_state, actions): # Essa função retorna a próxima ação a ser tomada e o valor da qtable
        """
        Essa função retorna o maior valor de q e a melhor ação, dado o estado
        """
        max_q = float('-inf') # Valor para debug
        best_action = -7 # Valor para debug
        for action in actions:
            #cur_q = self.QTable[(cur_state[0]*self.N+cur_state[1]-1)][action]
            cur_q = self.QTable[cur_state][action]
            if cur_q > max_q:
                max_q = cur_q
                best_action = action
        if max_q == float('-inf'):
            print('Bug no MAX Q NEXT STATE')
        return max_q, best_action

    def update_q_off(self, cur_state, action, cur_reward):
        self.QTable[cur_state][action] = cur_reward

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
        # qtable_pos = cur_state[0]*self.N + cur_state[1]
        # print('qtable pos:',str(qtable_pos))
        print('qtable pos', cur_state)
        print('taken action:', taken_action)
        print('value:'+str(self.QTable[cur_state][taken_action]))
        self.QTable[cur_state][taken_action] = (1-self.alpha)*self.QTable[cur_state][taken_action] + self.alpha*(l_value)

    def update_trajectory_list(self, last_trajectory, score):
        if last_trajectory in self.unique_trajectory: # Verifica se a trajetória já está na lista de trajetórias
            self.trajectories_score[self.unique_trajectory.index(last_trajectory)]["count"] += 1 # Se estiver aumenta um no contador
        else:
            self.unique_trajectory.append(last_trajectory) # Se não estiver adiciona na lista
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

        


    def pos_to_num(self, x, y):
        """
        Essa função mapeia uma tupla (x,y) dentro do domínio para um valor z
        Como os passos são de 0.2, entre -2 e 2, então irei mapear os 2 primeiros
        digitos para o valor em y e os 2 maiores digitos para o valor de x
        ou seja [-1.8, -1.8]
        se transformara em
        1-1
        """
        new_y = round(y+2)/0.2
        
        new_x = round(x+2)/0.2
        print('old x:',x,'new x:',new_x)
        """
        if (new_x < 10):
            str_x = '0' + str(new_x)
        else:
            str_x = str(new_x)
        if (new_y < 10):
            str_y = '0' + str(new_y)
        else:
            str_y = str(new_y)
        """
        str_x = str(new_x)
        str_y = str(new_y)
        array_value  = str_x +'-'+ str_y
        return array_value

    def num_to_pos(self, num):
        """
        Esse valor retorna o número que mapeia a tupla
        No entanto, não sei se vai ser necessário a utilização dessa função
        """
        print("valor inicial:",num)
        x, y = num.split('-')
        x = int(x)
        y = int(y)
        x = x*0.2 - 2.0
        y = y*0.2 - 2.0
        print('O valor de x é:',x,' o valor de y é:',y) 


if __name__ == "__main__":
    table = qtable()