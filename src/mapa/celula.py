from enum import Enum

### Enum que define os tipos possíveis de células no mapa..
class TipoCelula(str, Enum):
    VAZIO = " "                     # Espaço vazio no mapa
    ENTRADA = "E"                   # Ponto de entrada do jogador
    JOIA = "J"                      # Objetivo do jogo, a joia
    GUARDA = "G"                    # Guarda (Obstáculo)
    CAMERA = "C"                    # Câmera (Obstáculo)
    PORTA_TRANCADA = "P"            # Porta (Obstáculo)
    ARMADILHA = "A"                 # Armadilha (Obstáculo)

### Classe que representa cada célula individual do mapa (matriz/grid)
class Celula:
    def __init__(self, x, y, tipos=None):
        self.x = x
        self.y = y
        self.tipos = set(tipos) if tipos else set() # Conjunto de tipos que essa célula possui

    ### Método para comparar se duas células são na mesma posição (mesmo x e y)
    def __eq__(self, other):
        return isinstance(other, Celula) and self.x == other.x and self.y == other.y

    ### Garante que a célula pode ser usada como chave em dicionários e em estruturas
    def __hash__(self):
        return hash((self.x, self.y))

    ### Necessário para estruturas que exigem orgenação, como heapq (Fila de prioridade)
    ### Esse método ordena as células com base na posição (x, y)
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    ### Adiciona um tipo à célula 
    def adicionar_tipo(self, tipo):
        self.tipos.add(tipo)

    ### Remove um tipo da célula
    def remover_tipo(self, tipo):
        self.tipos.discard(tipo)

    ### Verifica se a célula possui um determinado tipo
    # def tem_tipo(self, tipo):
    #     return tipo in self.tipos

