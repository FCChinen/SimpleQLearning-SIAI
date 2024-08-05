Autor: Felipe Churuyuki Chinen

    O jogo

O código implementado é baseado no "jogo" do lagarto[1]. O objetivo do lagarto é chegar o mais rápido possível no quadrado que contém 5 lagartos e assim o jogo se finaliza como vitória. Outra maneira do jogo ser finalizado, é quando o lagarto encontra o pássaro, no entanto, esse estado é considerado derrota. O ambiente pode ser descrito por uma matriz 3x3:

6 7 8 3 4 5 0 1 2

0 -> posição inicial do lagarto 1 -> quadrado vazio 2 -> 5 grilos 3 -> quadrado vazio 4 -> pássaro 5 -> quadrado vazio 6 -> 1 grilo 7 -> quadrado vazio 8 -> quadrado vazio

Foi escolhido arbitráriamente, que o jogo irá dizer quais são as ações possíveis para o lagarto. Além disso, nas posições fora da matriz, não é possivel que o lagarto consiga andar. No geral, o lagarto em 4 possíveis ações: Para cima, para baixo, para a direita e para a esquerda(Ou seja, movimentos na diagonal não são possíveis). Note que o jogo também não dará ações que não são fisicamente possíveis(EX:. Na posição inicial, o jogo não deixa o lagarto se movimentar para baixo ou para esquerda).

Recompensas do jogo: A cada ação tomada pelo lagarto, há recompensas, sendo elas: Quadrado vazio = -1 Pássaro = -10 1 grilo = +1 5 grilos = +10

    Q-Learning O algoritmo implementado para decidir os melhores movimentos para o lagarto é o q-learning. A principal estrutura desse algoritmo é a Q-Table, no qual é uma tabela que contém informações de quais são os melhores movimentos que o lagarto irá tomar. Cada linha dessa tabela indica a o quadrado(posição) no qual o lagarto pode andar e cada coluna indica quais são as possíveis ações e cada posição da matrix(posição, coluna) indica uma pontuação para cada ação. Assim, para escolher o melhor movimento, basta comparar os valores de cada coluna da posição que se encontra e escolher a ação que tem o maior valor. Mas como o algoritmo popula essa tabela?

2.1 Equação Toda a vez que o lagarto faz uma ação, ele atualiza o valor da matriz utilizando a seguinte equação: Q(s, a) = (1- alpha) * Q(s, a) + alpha * (R + lambda * max(q(s', a')))

s é o estado(posição, quadrado) no qual o lagarto se encontra a é o ação que foi tomada (Ou seja, supondo que o lagarto foi para direita, o estado seria 0 e a ação tomada seria "direita") Q indica apenas que estamos utilizando/atualizando os valores da Q-Table alpha é um valor arbitrário, no qual indica a taxa de aprendizado. R é a recompensa depois que o agente(O lagarto, no nosso caso) toma a ação a. lambda é a taxa/fator de desconto max é a função que retorna o maior valor dentre os possíveis s' e a' indicam a melhor próxima ação

Descrita a formula, algumas considerações: Por que utilizar q(s', a')? Pense que você está numa trajetória de carro e quer otimizar o tempo para chegar no seu destino. Traçar uma linha reta até o seu destino parece a melhor escolha. Mas supondo que você está seguindo essa trajetória e no meio do caminho se encontra um rio, para atravessá-lo você deve encontrar uma ponte. Assim, por mais que naquele ponto você foi o mais eficiente possível, não é possível continuar a trajetória e você deverá encontrar um outro caminho para atravessar o rio. Análogamente, de maneira simplória, o nosso agente irá pegar algumas vezes esse caminho, só que uma interação antes, ele irá verificar que esse caminho é ruim e irá explorar outros caminhos, para achar o caminho ótimo.

O que é esse lambda?[2] O fator de desconto, que basicamente é um truque matemático para que o valor para cada célula da matriz converja. EX: Se uma PG Infinita não tiver q < 1, então ela irá crescer infinitamente e assim, o valor sempre irá crescer(ou decrescer) e não iria atingir um ponto ótimo(ou a vizinhança de um ponto ótimo).

O que é esse alpha? Alpha é o fator de aprendizado, para melhor entendimento, podemos modificar a equação para:

Q(s,a) = (1-alpha) * Q(s,a) + alpha * Novo Valor

Note, que se o valor de alpha for 1, ele não irá considerar nada do valor antigo(Q(s,a)) e irá somente manter o novo valor calculado. Se o valor for 0, o valor antigo será sempre mantido, e essa equação não faria sentido.

Dessa maneira, o nosso algoritmo utiliza um mecanismo para que o lagarto possa aprender ou utilizar a q-table para tomar sua decisão(Explorar)

    Aprendizado ou Exploração O sentido de exploração nesse contexto é de utilizar os conhecimentos adquiridos para tomar a melhor decisão, enquanto aprendizado é de simplesmente tomar uma decisão aleatória e verificar o que acontece nesse estado. No início, o agente deverá aprender, pois não há nenhum conhecimento sobre o ambiente(Q-Table está com valores zerados) e depois que há certo conhecimento, poderá utilizar os conhecimentos para pegar o melhor caminho. Então, para tomar a decisão de quando aprender e quando explorar, foi utilizado um fator chamado epsilon greedy(egreedy). Então basicamente, utiliza-se um número aleatório e compara com esse fator, caso esse número seja maior que o egreedy ele então irá explorar, senão aprender. O valor de egreedy é inicializado com 1(Sempre aprendendo) e a cada iteração(Cada final de jogo) esse valor é atualizado multiplicando por um fator de decaimento. Assim, o valor de egreedy decai conforme o agente vai aprendendo e tentando explorar cada vez mais.

[1] https://deeplizard.com/learn/video/qhRNvCVVJaA [2] https://stats.stackexchange.com/questions/221402/understanding-the-role-of-the-discount-factor-in-reinforcement-learning
