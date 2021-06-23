"""
Criando um ambiente para achar o mínimo de funções:
A função escolhida foi Ackley function

f(x,y) = -20 * exp (-0.2*sqrt(0.5(x**2+ y**2))) - exp(0.5(cos2pix+cos2piy)) + e + 20

global optimum = [0, 0]

Para esse ambiente, o agente poderá andar pelo ambiente no quadrado
[1,1]
[-1,1]
[-1,-1]
[1,-1]

e a sua posição inicial será 0.5,0.5

Ações =
1 - +0.1 ,0
2 - -0.1, 0
3 - 0, +0,1
4 - 0, -0.1 
Tomando o plano xy, então:
ação 1 anda para direita
ação 2 anda para esquerda
ação 3 anda para cima
ação 4 anda para baixo
"""
import numpy as np

class Funcao:
    def __init__(self, p0x = -1.6, p0y = -1.6, tamanho_passo = 0.2, limite_x = 2.0, limite_y = 2.0):
        self.p0x = p0x # Posição inicial x do a gente
        self.px = p0x # Posição inicial x do agente
        self.p0y = p0y
        self.py = p0y # Posição inicial y do agente
        self.tamanho_passo = tamanho_passo # Tamanho do passo que o algoritmo poderá dar
        if (limite_x > 5):
            limite_x = 5
        self.limite_x = limite_x # Limite do domínio em x
        if (limite_y > 5):
            limite_y = 5
        self.limite_y = limite_y # Limite do domínio em y
        self.lastcurz = self.z(self.px,self.py) # Essa variável é utilizada para calcular a recompensa
        self.curz = self.z(self.px,self.py) # Variável que retorna o valor Z da função

    def reset(self):
        self.px = self.p0x # Posição inicial x do agente
        self.py = self.p0y # Posição inicial y do agente
        self.lastcurz = self.z(self.px,self.py) # Essa variável é utilizada para calcular a recompensa
        self.curz = self.z(self.px,self.py) # Variável que retorna o valor Z da função

    def update_z(self):
        # Atualiza o valor da função Z
        # Ela modifica os valores de curz e lastcurz para o calculo da recompensa
        self.lastcurz = self.curz
        self.curz = self.z(self.px, self.py)

    def get_reward(self):
        """
        Calcula a recompensa em cada estado.
        """
        if self.curz == 0: # Achou o máximo global
            return 10.0
        elif (self.px > self.limite_x) or (self.px < (-1)*self.limite_x): # Saiu do limite no eixo x
            return -10.0
        elif (self.py > self.limite_y) or (self.py < (-1)*self.limite_y): # Saiu do limite no eixo y
            return -10.0
        else:
            # Caso se aproxima do mínimo global, aumenta
            # Senão diminui.
            #return self.curz - self.lastcurz 
            return self.lastcurz - self.curz

    def terminate(self):
        """
        Essa função verifica o fim de jogo
        Basicamente, quando ele sai do domínio da função
        ou quando ele acha o máximo global
        """
        if (self.px > self.limite_x) or (self.px < (-1)*self.limite_x):
            return True
        elif (self.py > self.limite_y) or (self.py < (-1)*self.limite_y):
            return True
        elif (self.curz == 0): # CUIDADO!! Lembrar que a conversão de dec to bin.
            return True
        else:
            return False

    def get_next_pos(self, action):
        """
        Essa função retorna a próxima posição
        """
        if action == 0:
            return self.px + self.tamanho_passo, self.py
        elif action == 1:
            return self.px - self.tamanho_passo, self.py
        elif action == 2:
            return self.px, self.py + self.tamanho_passo
        else:
            return self.px, self.py - self.tamanho_passo
            

    def update_pos(self, x, y):
        """
        A função movimenta o agente
        e retorna a posição
        """
        self.px = x
        self.py = y


    def z(self, x, y):
        # Calculo do valor da função de Akley
        primeiro_termo = np.exp(-0.2 * np.sqrt(0.5*(np.float_power(x, 2) + np.float_power(y, 2))))
        segundo_termo = np.exp(0.5 * (np.cos(2*np.pi*x)+np.cos(2*np.pi*y)))
        var = -20 * primeiro_termo - segundo_termo + np.exp(1) + 20
        return var

    def ret_pos(self):
        print("x:",self.px)
        print("y:",self.py)


    def pos_to_num(self, x, y):
        """
        Essa função mapeia uma tupla (x,y) dentro do domínio para um valor z
        Como os passos são de 0.2, entre -2 e 2, então irei mapear os 2 primeiros
        digitos para o valor em y e os 2 maiores digitos para o valor de x
        ou seja [-1.8, -1.8]
        se transformara em
        1-1
        Para o processamento dentro do dicionário
        """
        new_y = round((y+self.limite_x)/self.tamanho_passo)
        new_x = round((x+self.limite_y)/self.tamanho_passo)
        str_x = str(new_x)
        str_y = str(new_y)
        array_value  = str_x +'-'+ str_y
        return array_value

"""
Essa main foi criada para verificar se o programa está funcionando de maneira correta
"""
if __name__ == "__main__":
    f = Funcao()
    print(f.pos_to_num(f.px,f.py))
    while (f.check_end() == False):
        f.ret_pos()
        action = int(input("Digite uma ação de 1 a 4: "))
        new_x, new_y = f.get_next_pos(action)
        f.update_pos(new_x, new_y)
        print(f.pos_to_num(f.px,f.py))
        f.update_z()
        print("A recompensa foi: "+str(f.recompensa()))
    print("GG: tentou ir pra pos",f.px,f.py)
