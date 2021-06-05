from maze import Maze
from qtable import qtable
import matplotlib.pyplot as plt
import time
import numpy as np

num_steps = int(input("Digite o número de episódios que devem ocorrer\n"))
N = int(input("Digite o tamanho do labirinto:\n"))
#actions = input("Digite as ações que o agente pode tomar:\n")
#actions = ["down", "up", "left", "right"]
actions = [0, 1 ,2 ,3]

# Cria a instância do jogo
maze = Maze(N)
goal_reward = 10
goal_pos_matrix = maze.get_cricket_pos()
goal_pos_array = N * goal_pos_matrix[1] + goal_pos_matrix[0]


score_y = []

QTable = qtable(actions=actions, N=N, min_steps=num_steps,decay_rate=0.98, goal_pos=goal_pos_array, goal_reward=goal_reward) # Criando a qtable
QTable.print_qtable()

cur_step = 0
trajectories = np.array([])
best_score = 0

while cur_step < num_steps:
    GG = False
    next_s_a = []
    step_maze = 0
    trajectory = []
    while(GG == False) and step_maze < 1000:
        # Renderizando o ambiente
        #maze.render()

        print("Possíveis ações: "+str(maze.posible_actions(maze.get_lizard_pos())))
        # Decidindo qual ação irá tomar
        action = QTable.choose_action(maze.posible_actions(maze.get_lizard_pos()), maze.get_lizard_pos())
        print("Posicao Matriz: "+str(maze.lizard_pos))
        print("Posicao array: " +str(maze.lizard_pos[0]*N + maze.lizard_pos[1] ))
        print("Ação tomada: "+str(action))
        

        new_pos = maze.get_next_pos(action)
        
        candidates_next_action = maze.posible_actions(new_pos)
        next_s_a.append([new_pos, candidates_next_action])
        QTable.update_q(next_s_a, action,maze.get_lizard_pos(), maze.get_reward())
        #maze.update_pos(new_pos)
        trajectory.append(action)
        QTable.print_qtable()
        maze.update_lizard_pos(new_pos)
        #input("esperando a resposta")
        #print("Sua recompensa foi: "+str(maze.get_reward()))
        maze.render()
        #print("Pos lagarto: "+str(maze.get_lizard_pos()))
        #print("pos cricket: "+str(maze.cricket_pos))
        #print(str(maze.cricket_pos.shape))
        #print(str(maze.lizard_pos.shape))
        #QTable.print_qtable()
        #import pdb; breakpoint()
        GG = maze.terminate()
        #if (step_maze > 50):
        #    GG = True
        step_maze += 1
    maze.last_reward()
    cur_score = maze.get_sum_reward()
    if cur_score > best_score:
        best_score = cur_score
    score_y.append(cur_score)    
    QTable.update_trajectory_list(trajectory, maze.get_sum_reward()) # Só adiciona na lista de trajetórias se convergiu
    maze.reset()
    
    cur_step += 1
    print("\n\n\n cur step ="+str(cur_step))

print(str(QTable.trajectories_score))
print('best score' + str(best_score))
for key, value in QTable.trajectories_score.items():
    print('key: ' + str(key))
    print('value: ' + str(value))
    if value['score'] == best_score:
        best_key = key
#print(str(QTable.unique_trajectory[best_key]))
plt.plot(score_y,"r")
plt.show()
print("best key: " + str(best_key))
print(str(QTable.unique_trajectory[best_key]))
maze.render_best_trajectory(QTable.unique_trajectory[best_key])
maze.mainloop()

#QTable.print_qtable()

