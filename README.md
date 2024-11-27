# Pouso do foguete

## Descrição Básica do Projeto
Este projeto é um jogo criado para simular, de forma simplificada, o pouso de um foguete em diversos ambientes. O objetivo
é dar ao usuário uma experiência prática dos efeitos de conceitos como: viscosidade, velocidade e aceleração.
O objetivo do jogo é pousar o foguete, a partir de uma posição X aleatória, na área indicada, tendo que gerenciar o
combustível e a trajetória do foguete.
Analisando esse problema, vemos que ele possúi diversas variáveis que podem impactar no resultado final, pois, na
física, todos esses fatores estão conectados, a massa do combustível afeta a massa total do foguete, que por sua vez impacta
na velocidade que será expressa, a qual impacta na força viscosa sentida pelo objeto, além de várias outras relações.

## Conceitos de Física e Modelo Matemático:
### Forças
#### Força Gravitacional
Como sabemos, nosso foguete, assim como os outros corpos nos planetas, sofre o efeito da força gravitacional, sendo atraído
em direção ao solo.
Tomando um referencial estático no solo e um sistema de cordenadas cartesiano, temos que tal força, em nosso objeto de estudo,
pode ser representada da seguinte maneira:
<p align="center">
    <img alt="Foguete" src="/images/foguete_gravidade.png">
</p>
Dessa forma, podemos descrever essa força da seguinte maneira em nosso sistema:

$$\begin{equation}
\vec{F}_g = - m \cdot g  \hat{j}
\end{equation}$$

#### Força Viscosa
Agora, outra força que precisamos analisar em nosso sistema é a força viscosa, a qual irá variar de intensidade dependendo da
atmosfera do planeta e da velocidade do nosso foguete, sendo ela representada assim em nosso sistema de coordenadas:
<p align="center">
    <img alt="Foguete" src="/images/foguete_viscosidade.png">
</p>
Dessa forma, podemos descrever essa força da seguinte maneira em nosso sistema:

$$\begin{equation}
\vec{F}_v = - b \cdot \vec{v}
\end{equation}$$

#### Força de propulsão do foguete
Fora da simulação, um foguete queima seu combustível, expelindo gases, para conseguir, por meio da 3º Lei de Newton, gerar uma
força de reação, que por sua vez propele o foguete na direção desejada.
Análogo à isso, nosso jogo usa um IMPULSO do combustível de $500000 \frac{kg.m}{s^2}$, que, ao jogador acionar o propulsor,
gera uma força de propulsiona o foguete.
Podemos modelor tal força dessa forma em nosso sistema:
<p align="center">
    <img alt="Foguete" src="/images/foguete_propu.png">
</p>
Podemos decompor essa força da seguinte forma:

$$\begin{equation}
\vec{F}_{propu x} = \text{IMPULSO} \cdot \sin{\theta} \hat{i}
\end{equation}$$

$$\begin{equation}
\vec{F}_{propu y} = \text{IMPULSO} \cdot \cos{\theta} \hat{j}
\end{equation}$$

Em que $\theta$ é o ângulo definido pelo jogador que o foguete foi rotacionado.

### Vetores Cinemâticos
Agora, para que possamos descrever o movimento do foguete em nosso sistema de cordenadas, precisamos escrever nossos vetores
cinemáticos nesse sistema, assim, nós temos:

$$\begin{equation}
\vec{r}(t) =  x(t)\hat{i} + y(t)\hat{j}
\end{equation}$$

$$\begin{equation}
\vec{v}(t) =  \dot{x} (t) \hat{i} + \dot{x} (t) \hat{j}
\end{equation}$$

$$\begin{equation}
\vec{a}(t) = \ddot{x} (t) \hat{i} + \ddot{y} (t) \hat{j}
\end{equation}$$

### EDOs
Aplicando a 2ª lei de Newton, conseguimos deduzir as seguintes EDOs do nosso sistema:

$$\begin{equation}
\ddot{x}(t) \cdot m \hat{i} = \vec{F}_{propu x} + \vec{F_v}_x
\end{equation}$$

$$\begin{equation}
\ddot{y}(t) \cdot m \hat{j} = \vec{F}_{propu y} + \vec{F_v}_y + \vec{F}_g
\end{equation}$$

Substituindo, temos:

$$\begin{equation}
\ddot{x}(t) \cdot m \hat{i} = \text{IMPULSO} \cdot \sin{\theta} \hat{i} - b \cdot v_x(t) \hat{i}
\end{equation}$$

$$\begin{equation}
\ddot{y}(t) \cdot m \hat{j} = \text{IMPULSO} \cdot \cos{\theta} \hat{j} - b \cdot v_y(t) \hat{j} - m \cdot g
\end{equation}$$

Vamos resolver a primeira (eixo x):

$$\begin{equation}
\ddot{x}(t) \cdot m = \text{IMPULSO} \cdot \sin{\theta} - b \cdot v_x(t)
\end{equation}$$

$$\begin{equation}
\ddot{x}(t) \cdot m + b \cdot \dot{x}(t) \cdot \sin{\theta} = \text{IMPULSO} \cdot \sin{\theta},
\end{equation}$$

$$\begin{equation}
\text{Assumindo: } k_1 = \frac{m}{b.\sin{\theta}} \text{, } k_2 = -\frac{\text{IMPULSO} \cdot \sin{\theta}}{m},
\end{equation}$$

$$\begin{equation}
\ddot{x}(t) + \frac{1}{k_1} \cdot \dot{x}(t) + k_2 = 0
\end{equation}$$

Agora, vamos resolver a segunda (eixo y):

$$\begin{equation}
\ddot{y}(t) \cdot m = \text{IMPULSO} \cdot \cos{\theta} - b \cdot v_y(t) - m \cdot g
\end{equation}$$

$$\begin{equation}
\ddot{y}(t) \cdot m + b \cdot \dot{y}(t) \cdot \cos{\theta} = \text{IMPULSO} \cdot \cos{\theta} - m \cdot g,
\end{equation}$$

$$\begin{equation}
\text{Assumindo: } k'_1 = \frac{m}{b.\cos{\theta}} \text{, } k'_2 = -\frac{\text{IMPULSO} \cdot \cos{\theta}}{m} - g,
\end{equation}$$

$$\begin{equation}
\ddot{y}(t) + \frac{1}{k'_1} \cdot \dot{y}(t) +  k'_2 = 0
\end{equation}$$

Vamos determinar a equação que resolve as EDO's:

Primeiramente podemos reescrever a equação da seguinte forma:

$$\begin{equation}
\dot{v_x}(t) + \frac{1}{k_1} \cdot {v_x}(t) + k_2 = 0
\end{equation}$$

Agora, utilizando uma mudança de variável dependente $$v_z$$ para $$u = k_1^{-1}v_x + k_2$$. Vamos calcular $$\dot{v_x}$$ em relação a $$u$$. 

$$\begin{equation}
\dot{v_x} = u \cdot k_1 - g 
\end{equation}$$

$$\begin{equation}
\dot{v_x} = \dot{u} \cdot k_1 
\end{equation}$$

Substituindo esse resultado na equação:

$$\begin{equation}
\dot{u}k_1 + u = 0 
\end{equation}$$

Agora podemos resolver a EDO

$$\begin{equation}
\frac{du}{dt} + \frac{1}{k_1}u = 0 
\end{equation}$$

$$\begin{equation}
\frac{du}{u} = -\frac{1}{k_1}dt 
\end{equation}$$

Integrando os dois lados

$$\begin{equation}
\ln{u} = -\frac{t}{k_1} + C' 
\end{equation}$$

$$\begin{equation}
u(t) = Ce^{-\frac{t}{k_1}} \text{, note que, } C = e^{C'} 
\end{equation}$$

Determinamos a equação de $v_z(t)$ como:

$$\begin{equation}
v_z(t) = -k_2k_1(1-e^{-t/k_1})
\end{equation}$$

Integrando ambos os lados da equação, conseguimos a equação da trajetória  $$z(t)$$

$$\begin{equation}
z(t) = -k_2k_1(C + t + k_1e^{-t/k_1})
\end{equation}$$

Também é possível perceber que a equação do movimento no eixo y pode ser resolvido com a mesma equação.



## Como Usar


## Referências:
