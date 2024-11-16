# Pouso do foquete

## Descrição Básica do Projeto
Este projeto é um jogo criado para simular, de forma simplificada, o pouso de um foquete em diversos ambientes. O objetivo
é dar ao usuário uma experiência prática dos efeitos de conceitos como: viscosidade, velocidade e aceleração.
O objetivo do jogo é pousar o foquete, a partir de uma posição X aleatória, na área indicada, tendo que gerenciar o
combustível e a trajetória do foquete.
Analisando esse problema, vemos que ele possúi diversas variáveis que podem impactar no resultado final, pois, na
física, todos esses fatores estão conectados, a massa do combustível afeta a massa total do foguete, que por sua vez impacta
na velocidade que será expressa, a qual impacta na força viscosa sentida pelo objeto, além de várias outras relações.

## Conceitos de Física e Modelo Matemático:
### Forças
#### Força Gravitacional
Como sabemos, nosso foquete, assim como os outros corpos nos planetas, sofre o efeito da força gravitacional, sendo atraído
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
\text{Assumindo: } k_1 = \frac{b.\sin{\theta}}{m} \text{, } k_2 = \frac{\text{IMPULSO} \cdot \sin{\theta}}{m},
\end{equation}$$

$$\begin{equation}
\ddot{x}(t) + k_1 \cdot \dot{x}(t) = k_2
\end{equation}$$

Agora, vamos resolver a segunda (eixo y):

$$\begin{equation}
\ddot{y}(t) \cdot m = \text{IMPULSO} \cdot \cos{\theta} - b \cdot v_y(t) - m \cdot g
\end{equation}$$

$$\begin{equation}
\ddot{y}(t) \cdot m + b \cdot \dot{y}(t) \cdot \cos{\theta} = \text{IMPULSO} \cdot \cos{\theta} - m \cdot g,
\end{equation}$$

$$\begin{equation}
\text{Assumindo: } k'_1 = \frac{b.\cos{\theta}}{m} \text{, } k'_2 = \frac{\text{IMPULSO} \cdot \cos{\theta}}{m} - g,
\end{equation}$$

$$\begin{equation}
\ddot{y}(t) + k'_1 \cdot \dot{y}(t) = k'_2
\end{equation}$$


## Como Usar


## Referências:
