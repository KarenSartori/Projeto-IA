from mapa.mapa_base import gerar_mapa
from mapa.celula import TipoCelula

### Informações do Mapa
TAMANHO = 5
ENTRADA = (0, 0)
JOIA = (4, 4)

### Coordenadas dos obstáculos
obstaculos_fixos = {
    TipoCelula.GUARDA: [(0, 1), (0, 2), (2, 2), (3, 3)],
    TipoCelula.CAMERA: [(1, 1), (0, 2), (2, 2), (3, 0)],
    TipoCelula.PORTA_TRANCADA: [(0, 3), (2, 0), (4, 1)],
    TipoCelula.ARMADILHA: [(1, 1), (3, 2), (4, 3)],
}

def gerar_mapa_5x5():
    return gerar_mapa(TAMANHO, ENTRADA, JOIA, obstaculos_fixos)