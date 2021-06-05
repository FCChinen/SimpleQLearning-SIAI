"""
Labirinto no qual o lagarto deve evitar os obstáculos(Árvores) até chegar no ponto final, a fim de tentar encontrar o melhor caminho.
O labirinto é uma matriz NxN, no qual N é passado por parâmetro pelo usuário, no qual N deve ser maior ou igual a 4. Pois senão, não é possivel adicionar obstáculos para obstruir a passagem do agente.

Orientação dos eixos do labirinto:
    -> x (Cresce para direita)
    \/ y (Cresce para baixo)

Autor: Felipe Churuyuki Chinen
"""
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class Maze(tk.Tk, object):
    def __init__(self, pixels = 40, p0_lizard = [1,3]):
        super(Maze, self).__init__()
        # Tamanho do labirinto
        self.N = 5
        # Quantos pixels terão cada quadrado
        self.pixels = pixels
        self.sum_reward = 0
        # Informações sobre os obstáculos/árvores
        self.trees = np.array([]) # Lista que contém a tupla [x,y] da posição de cada árvore
        self.trees_widgets = [] # Contém o widget de cada árvore
        self.img_tree = None
        self.create_trees() # Função que popula a lista self.trees
        # self.img_treeobstacle = None # 

        # Informações sobre o grilo
        self.cricket_pos = np.array([1, 1])
        self.img_cricket = None
        self.cricket_widget = None

        # Informações sobre os 5 grilos
        self.five_cricket_pos = np.array([3, 3]) #!! Precisa modificar
        self.img_five_cricket = None
        self.five_cricket_widget = None

        # Informações sobre o pássaro
        self.bird_pos = np.array([2, 2]) #!!
        self.img_bird = None
        self.bird_widget = None
        

        # Informações sobre o lagarto
        self.lizard_pos = np.array(p0_lizard)
        self.lizard_p0 = np.array(p0_lizard)
        self.lizard_widget = None
        self.img_lizard = None

        self.img_step = []
        self.step_widget = []
        self.step_pos = p0_lizard

        # Criando o ambiente visual
        self.create_visual()
        
    # PARTE GRÁFICA

    def print_trees(self):
        print(str(self.trees))

    def create_visual_trees(self):
        img_tree = Image.open("imgs/treeconverted.png")
        self.img_treeobstacle = ImageTk.PhotoImage(img_tree)
        for tree_pos in self.trees:
            tree_widget = self.canvas_widget.create_image(self.pixels * tree_pos[0], self.pixels * tree_pos[1], anchor = 'nw', image=self.img_treeobstacle)
            self.trees_widgets.append(tree_widget)

    def create_visual_cricket(self):
        self.img_cricket = Image.open("imgs/cricketconverted.png")
        self.img_cricket = ImageTk.PhotoImage(self.img_cricket)
        self.cricket_widget = self.canvas_widget.create_image(self.pixels * self.cricket_pos[0], self.pixels * self.cricket_pos[1], anchor = 'nw', image=self.img_cricket)

    def create_visual_five_cricket(self):
        self.img_five_cricket = Image.open("imgs/5cricketsconverted.png")
        self.img_five_cricket = ImageTk.PhotoImage(self.img_five_cricket)
        self.cricket_widget = self.canvas_widget.create_image(self.pixels * self.five_cricket_pos[0], self.pixels * self.five_cricket_pos[1], anchor = 'nw', image=self.img_five_cricket)

    def create_visual_bird(self):
        self.img_bird = Image.open("imgs/birdconverted.png")
        self.img_bird = ImageTk.PhotoImage(self.img_bird)
        self.cricket_widget = self.canvas_widget.create_image(self.pixels * self.bird_pos[0], self.pixels * self.bird_pos[1], anchor = 'nw', image=self.img_bird)

    def create_visual_lizard(self):
        img_lizard = Image.open("imgs/lizardconverted.png")
        self.img_lizard = ImageTk.PhotoImage(img_lizard)
        self.lizard_widget = self.canvas_widget.create_image(self.pixels * self.lizard_pos[0], self.pixels * self.lizard_pos[1], anchor = 'nw', image=self.img_lizard)

    def create_visual_step(self, best_trajectory):
        count = 0
        
        for action in best_trajectory:
            self.img_step.append(ImageTk.PhotoImage(Image.open("imgs/footstepconverted.png")))
            #self.step_widget
            if action == 0: # Para cima
                print('cima')
                self.step_pos[1] += 1

            elif action == 1: # Para baixo
                print('baixo')
                self.step_pos[1] -= 1

            elif action == 2: # Para esquerda
                print('esquerda')
                self.step_pos[0] -= 1

            else: # para direita
                print('direita')
                self.step_pos[0] += 1

            print(str(self.step_pos))
            self.step_widget.append(self.canvas_widget.create_image(self.pixels * self.step_pos[0], self.pixels * self.step_pos[1], anchor = 'nw', image=self.img_step[count]))
            count+=1
            #if count == len(best_trajectory) - 1:
            #    break
        

    def create_visual(self):
        self.canvas_widget = tk.Canvas(self,  bg='white',
                                       height=self.N * self.pixels,
                                       width=self.N * self.pixels)

        # Creating grid lines
        self.create_visual_trees()
        self.create_visual_cricket()
        self.create_visual_lizard()
        self.create_visual_five_cricket()
        self.create_visual_bird()
        for column in range(0, self.N * self.pixels, self.pixels):
            x0, y0, x1, y1 = column, 0, column, self.N * self.pixels
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')
        for row in range(0, self.N * self.pixels, self.pixels):
            x0, y0, x1, y1 = 0, row, self.N * self.pixels, row
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')
        
        # Packing everything
        self.canvas_widget.pack()

    def create_trees(self):
        """
        Como o labirinto é uma matriz quadrada, devemos definir quais ações são possíveis em cada quadrado.
        Estou definindo que nas bordas do labirinto, haverá árvores, assim como na em sua diagonal
        """
        trees = []
        for tree in range(0, self.N):
            trees.append([tree, 0]) # Criando árvores da borda inferior
            trees.append([tree, self.N-1]) # Criando árvores da borda superior
            trees.append([self.N-1, tree]) # Criando árvores da borda lateral direita
            trees.append([0, tree]) # Criando árvores da borda lateral da esquerda
        self.trees = trees # Tirando as duplicatas


    # A função que atualiza o ambiente
    def render(self):
        self.update()

    # Reseta o ambiente após a finalização do jogo(No final de cada episódio).
    def reset(self):
        
        self.sum_reward = 0
        # Updating agent
        self.canvas_widget.delete(self.lizard_widget)
        self.lizard_pos = self.lizard_p0
        self.lizard_widget = self.canvas_widget.create_image(self.pixels * self.lizard_pos[0], self.pixels * self.lizard_pos[1], anchor = 'nw', image=self.img_lizard)
        self.update()

        # Return observation
        #return self.canvas_widget.coords(self.agent)

    def render_best_trajectory(self, best_trajectory):
        self.canvas_widget.delete(self.lizard_widget)
        self.create_visual_step(best_trajectory)

    # LÓGICA DO JOGO

    def get_next_pos(self, action):
        a = np.array([0, 0])
        if action == 0: # Para cima
            a[1] += self.pixels
            self.canvas_widget.move(self.lizard_widget,a[0], a[1])
            return self.lizard_pos + [0,1]
        elif action == 1: # Para baixo
            a[1] -= self.pixels
            self.canvas_widget.move(self.lizard_widget,a[0], a[1])
            return self.lizard_pos - [0,1]
        elif action == 2: # Para esquerda
            a[0] -= self.pixels
            self.canvas_widget.move(self.lizard_widget,a[0], a[1])
            return self.lizard_pos - [1,0]
        else: # para direita
            a[0] += self.pixels
            self.canvas_widget.move(self.lizard_widget,a[0], a[1])
            return self.lizard_pos + [1,0]
            
        # Chamar a função que atualiza a posição do lagarto(Para a parte visual)

    def update_lizard_pos(self, new_pos):
        self.lizard_pos = new_pos

    def get_lizard_pos(self):
        return self.lizard_pos

    def get_cricket_pos(self):
        return self.cricket_pos


    def posible_actions(self, cur_pos):
        """
        Definimos a ação da seguinte maneira:
        1 - Andar para baixo
        2 - Andar para cima
        3 - Andar para esquerda
        4 - Andar para direita

        Para verificar as possíveis ações, devemos então verificar o que tem nos objetos adjacentes ao agente.
        Assim:
        Se cur_pos + [0,1](Andar para cima) == árvore
        OU
        Se cur_pos - [0,1](Andar para baixo) == árvore
        OU
        se cur_pos - [1,0](Andar para esquerda) == árvore
        OU
        Se cur_pos + [1,0](Andar para direita) == árvore
        Então
        Remove ação
        """
        actions = np.array([0, 1, 2, 3]) # A priori, todas as ações são possiveis
        return actions

    def last_reward(self):
        if np.array_equal(self.lizard_pos, self.five_cricket_pos):
            self.sum_reward += 10
        elif np.array_equal(self.lizard_pos, self.bird_pos):
            self.sum_reward -= 10

    def get_reward(self):
        if np.array_equal(self.lizard_pos, self.cricket_pos):
            self.sum_reward += 1
            return 1
        elif np.array_equal(self.lizard_pos, self.five_cricket_pos):
            self.sum_reward += 10
            return 10
        elif np.array_equal(self.lizard_pos, self.bird_pos):
            self.sum_reward -= 10
            return - 10
        else:
            self.sum_reward -= 1
            return -1

    def terminate(self):
        if np.array_equal(self.lizard_pos, self.five_cricket_pos) or np.array_equal(self.lizard_pos, self.bird_pos) or (self.lizard_pos == self.trees).any():
            print("Sua recompensa total foi: "+str(self.sum_reward))
            return True
        else:
            return False

    def t(self):
        self.reset()
        GG = False
        while GG == False:
            self.render()
            print("actions: "+str(self.posible_actions(self.lizard_pos)))
            action = int(input("digite sua action: 0 down 1 up 2 left 3 right"))
            print('ação escolhida: '+str(action))
            new_pos = self.get_next_pos(action)
            self.update_lizard_pos(new_pos)
            GG = self.terminate()

    def get_sum_reward(self):
        return self.sum_reward

if __name__ == '__main__':
    maze = Maze()
    maze.t()
    maze.mainloop()
