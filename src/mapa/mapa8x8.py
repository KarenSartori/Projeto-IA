from mapa.mapa_base import gerar_mapa
from mapa.celula import TipoCelula

### Informações do Mapa
TAMANHO = 8
ENTRADA = (0, 0)
JOIA = (7, 7)

### Coordenadas dos obstáculos
obstaculos_fixos = {
    TipoCelula.GUARDA: [(1, 1), (1, 2), (2, 3), (3, 5), (5, 1), (6, 4), (5, 5)],
    TipoCelula.CAMERA: [(1, 3), (2, 5), (3, 6), (4, 4), (7, 3), (0, 6), (6, 2)],
    TipoCelula.PORTA_TRANCADA: [(0, 5), (1, 7), (3, 1), (4, 2), (6, 1), (7, 2), (2, 0)],
    TipoCelula.ARMADILHA: [(0, 1), (2, 2), (3, 3), (0, 7), (1, 6), (2, 7), (6, 6)],
}

def gerar_mapa_8x8():
    return gerar_mapa(TAMANHO, ENTRADA, JOIA, obstaculos_fixos)
