from function import Funcao
from qtable import qtable
import matplotlib.pyplot as plt
import time
import numpy as np

# Quantidade de episódios que devem ocorrer
num_steps = 1000

fun = Funcao()

score_y = []

N = round(fun.limite_x/fun.tamanho_passo)*2

print(N)

QTable = qtable(N = N)
#QTable.print_qtable()

qtd_vezes = {}

# Contador que contém a quantidade de episódios
cur_step = 0
# Esse array que contém as trajetórias
trajectories = np.array([])
# Contém a melhor pontuação
best_score = 0
# Array que contém as ações
actions = [0, 1, 2, 3]
eixo_x = []
eixo_y = []

while QTable.egreedy > 0.01:
    GG = False
    # Conta a quantidade de passos dentro dos episódios
    step = 0
    # Contém as ações tomadas dentro de um episódio
    trajectory = []
    fun.reset()
    # Limitando a quantidade de passos máximos para 100
    while (GG == False) and step < 100:
        step+=1
        print('esta na pos:',fun.px,fun.py)
        # Contém o estado e um array que contém as possíveis ações
        next_s_a = []
        # Transformando a posição no plano cartesiano para valores inteiros(Mapeamento)
        old_cur_state = fun.pos_to_num(fun.px, fun.py)
        eixo_x.append(fun.px)
        eixo_y.append(fun.py)

        # Incrementando no dicionário a quantidade de vezes que o algoritmo passou pelo estado
        QTable.count_dict[old_cur_state] += 1
        
        print('old_cur_state', old_cur_state)
        action = QTable.choose_action(actions,old_cur_state)
        #action = int(input("Escolha a ação de 0 a 3"))
        # Executa próxima ação
        new_pos = fun.get_next_pos(action)
        # Obtendo o valor de Z, para a recompensa
        fun.update_pos(new_pos[0], new_pos[1])
        fun.update_z()
        #print('new_pos',new_pos)
        reward = fun.get_reward()
        print("Recompensa: ",reward)
        GG = fun.terminate()
        if GG == False:
            cur_state = fun.pos_to_num(fun.px, fun.py)
            next_s_a.append([cur_state, actions])
            cur_state = fun.pos_to_num(fun.px, fun.py)
            print('next_s_a:',next_s_a,'action',action,'curstate',cur_state,'reward',reward)
            QTable.update_q(next_s_a, action, old_cur_state,reward)
        else:
            # Tem que criar uma função nova para quando o agente sai dos limites da função
            # Pois não há mapeamento quando isso ocorre.
            #print('reward',reward)
            #input('entrou no fim')
            QTable.update_q_off(old_cur_state, action, reward)

    cur_step += 1


plt.hist2d(eixo_x,eixo_y, bins=[np.arange(-2,2,0.2),np.arange(-2,2,0.2)])

plt.show()