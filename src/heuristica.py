from math import sqrt
from celula import TipoCelula

def calcular_risco(celula):
    total_risco = 0
    if TipoCelula.GUARDA in celula.tipos:
        total_risco += 5
    if TipoCelula.CAMERA in celula.tipos:
        total_risco += 3
    return total_risco

def calcular_atraso(celula):
    total_atraso = 0
    if TipoCelula.PORTA_TRANCADA in celula.tipos:
        total_atraso += 2
    if TipoCelula.ARMADILHA in celula.tipos:
        total_atraso += 4
    return total_atraso

def distancia_euclidiana(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def custo_real_da_celula(celula):
    risco = calcular_risco(celula)
    atraso = calcular_atraso(celula)
    return round(1 + 3 * risco + 2 * atraso, 1)

#Heurística admissível
def calcular_heuristica(celula, objetivo, log=False):
    x = 3  #Peso do risco 
    y = 2  #Peso do atraso
    z = 1  #Peso da distância

    risco = calcular_risco(celula)
    atraso = calcular_atraso(celula)
    distancia = distancia_euclidiana(celula.x, celula.y, objetivo.x, objetivo.y)

    h = x * risco + y * atraso + z * distancia

    if log:
        print(f"Heurística de ({celula.x},{celula.y}): "
              f"risco={risco}, atraso={atraso}, distância={round(distancia,1)} "
              f"-> h(n) = {x}*{risco} + {y}*{atraso} + {z}*{round(distancia,1)} = {round(h, 1)}")

    return round(h, 1)

#Heuristica inadmissível 
def calcular_heuristica_inadmissivel(celula, objetivo, log= False):
    x = 30
    y = 20
    z = 10
    
    risco = calcular_risco(celula)
    atraso = calcular_atraso(celula)
    distancia = distancia_euclidiana(celula.x, celula.y, objetivo.x, objetivo.y)

    h = x * risco + y * atraso + z * distancia

    if log:
        print(f"[INADMISSÍVEL] Heurística de ({celula.x},{celula.y}): "
              f"risco={risco}, atraso={atraso}, distância={round(distancia,1)} "
              f"-> h(n) = 1000 - ({x}*{risco} + {y}*{atraso} + {z}*{round(distancia,1)}) = {round(1000-h, 1)}")

    return round(1000-h, 1)

