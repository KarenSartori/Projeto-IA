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

# def calcular_heuristica(celula, objetivo):
#     x = 3  # peso do risco
#     y = 2  # peso do atraso
#     z = 1  # peso da distância
#
#     risco = calcular_risco(celula)
#     atraso = calcular_atraso(celula)
#     distancia = distancia_euclidiana(celula.x, celula.y, objetivo.x, objetivo.y)
#
#     h = x * risco + y * atraso + z * distancia
#
#     print(f"Heurística de ({celula.x},{celula.y}): "
#           f"risco={risco}, atraso={atraso}, distância={round(distancia,1)} "
#           f"-> h(n) = {x}*{risco} + {y}*{atraso} + {z}*{round(distancia,1)} = {round(h, 1)}")
#
#     return round(h, 1)


def calcular_heuristica(celula, objetivo, log=False):
    x = 3
    y = 2  # peso do atraso
    z = 1  # peso da distância

    risco = calcular_risco(celula)
    atraso = calcular_atraso(celula)
    distancia = distancia_euclidiana(celula.x, celula.y, objetivo.x, objetivo.y)

    h = x * risco + y * atraso + z * distancia

    if log:
        print(f"Heurística de ({celula.x},{celula.y}): "
              f"risco={risco}, atraso={atraso}, distância={round(distancia,1)} "
              f"-> h(n) = {x}*{risco} + {y}*{atraso} + {z}*{round(distancia,1)} = {round(h, 1)}")

    return round(h, 1)
