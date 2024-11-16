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
### Força Gravitacional
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

### Força Viscosa
Agora, outra força que precisamos analisar em nosso sistema é a força viscosa, a qual irá variar de intensidade dependendo da
atmosfera do planeta e da velocidade do nosso foguete, sendo ela representada assim em nosso sistema de coordenadas:
<p align="center">
    <img alt="Foguete" src="/images/foguete_viscosidade.png">
</p>
Dessa forma, podemos descrever essa força da seguinte maneira em nosso sistema:
$$\begin{equation}
\vec{F}_v = - b \cdot \vec{v}
\end{equation}$$


## Implementação




## Como Usar




## Referências: 
