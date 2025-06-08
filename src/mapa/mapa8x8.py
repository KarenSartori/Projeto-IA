from mapa.mapa_base import gerar_mapa
from mapa.celula import TipoCelula

### Informações do Mapa
TAMANHO = 8
ENTRADA = (0, 0)
JOIA = (7, 7)

### Coordenadas dos obstáculos
obstaculos_fixos = {
        TipoCelula.GUARDA: [
            (3, 0), (2, 6), (0, 4), (5, 3), (1, 1), (6, 2), (4, 5)
        ],
        TipoCelula.CAMERA: [
            (4, 0), (2, 1), (0, 6), (1, 3), (6, 0), (3, 4), (5, 5)
        ],
        TipoCelula.PORTA_TRANCADA: [
            (1, 2), (3, 1), (2, 5), (6, 1), (0, 3), (4, 6), (5, 0)
        ],
        TipoCelula.ARMADILHA: [
            (3, 6), (6, 3), (0, 0), (2, 0), (1, 5), (4, 2), (5, 6)
        ],
    }

def gerar_mapa_8x8():
    return gerar_mapa(TAMANHO, ENTRADA, JOIA, obstaculos_fixos)
