from mapa.mapa_base import gerar_mapa
from mapa.celula import TipoCelula

### Informações do Mapa
TAMANHO = 7
ENTRADA = (0, 0)
JOIA = (6, 6)

### Coordenadas dos obstáculos
obstaculos_fixos = {
    TipoCelula.GUARDA: [(1, 1), (1, 2), (2, 3), (3, 5), (4, 6), (5, 1), (6, 2)],
    TipoCelula.CAMERA: [(1, 3), (2, 5), (3, 6), (4, 4), (5, 2), (6, 6), (0, 6)],
    TipoCelula.PORTA_TRANCADA: [(2, 0), (3, 1), (4, 2), (5, 3), (6, 0), (6, 1), (0, 4)],
    TipoCelula.ARMADILHA: [(0, 1), (2, 2), (3, 3), (4, 0), (5, 4), (1, 6), (3, 4)],
}

def gerar_mapa_7x7():
    return gerar_mapa(TAMANHO, ENTRADA, JOIA, obstaculos_fixos)
