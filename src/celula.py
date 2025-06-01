from enum import Enum

# cada celula é representada por um objeto da classe celula (x, y e tipo)
class TipoCelula(str, Enum):
    VAZIO = " "
    ENTRADA = "E"
    JOIA = "J"
    GUARDA = "G"
    CAMERA = "C"
    PORTA_TRANCADA = "P"
    ARMADILHA = "A"

class Celula:
    def __init__(self, x, y, tipos=None):
        self.x = x
        self.y = y
        self.tipos = set(tipos) if tipos else set()

    # compara a posicao
    def __eq__(self, other):
        return isinstance(other, Celula) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    # para usar o heapq
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def adicionar_tipo(self, tipo):
        self.tipos.add(tipo)

    def remover_tipo(self, tipo):
        self.tipos.discard(tipo)

    # retorna true se for o tipo
    # def tem_tipo(self, tipo):
    #     return tipo in self.tipos

