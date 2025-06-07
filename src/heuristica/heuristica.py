from math import sqrt
from mapa.celula import TipoCelula

### Função que calcula o risco total associado a uma célula,
### considerando a presença de guardas e câmeras
def calcular_risco(celula):
    total_risco = 0

    if TipoCelula.GUARDA in celula.tipos:
        total_risco += 5
    if TipoCelula.CAMERA in celula.tipos:
        total_risco += 3
    
    return total_risco

### Função que calcula o atraso total associado a uma célula,
### considerando portas trancadas e armadilhas
def calcular_atraso(celula):
    total_atraso = 0

    if TipoCelula.PORTA_TRANCADA in celula.tipos:
        total_atraso += 2
    if TipoCelula.ARMADILHA in celula.tipos:
        total_atraso += 4

    return total_atraso

### Função para calcular a distância euclidiana entre dois pontos (x1,y1) e (x2,y2)
### Essa distância é a "linha reta" entre os pontos, usada como parte da heurística
def distancia_euclidiana(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


### Função principal para calcular a heurística de uma célula com base em 3 fatores:
### Risco, Atraso e Distância até o objetivo
### Cada fator recebe um peso diferente para equilibrar sua importância no cálculo
### O parâmetro 'log' permite imprimir os detalhes do cálculo
def calcular_heuristica(celula, objetivo, log=False):
    x = 3  # Peso do risco (ex: guardas e câmeras)
    y = 2  # Peso do atraso (ex: portas trancadas e armadilhas)
    z = 1  # Peso da distância euclidiana até o objetivo

    risco = calcular_risco(celula)
    atraso = calcular_atraso(celula)
    distancia = distancia_euclidiana(celula.x, celula.y, objetivo.x, objetivo.y)

    # Combina os fatores ponderados para obter o valor final da heurística
    h = x * risco + y * atraso + z * distancia

    # Se 'log' for TRUE, imprime detalhes do cálculo para facilitar o entendimento
    if log:
        print(f"Heurística de ({celula.x},{celula.y}): "
              f"risco={risco}, atraso={atraso}, distância={round(distancia,1)} "
              f"-> h(n) = {x}*{risco} + {y}*{atraso} + {z}*{round(distancia,1)} = {round(h, 1)}")

    return round(h, 1)
