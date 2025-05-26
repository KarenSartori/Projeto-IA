from mapa import gerar_mapa, exibir_mapa_console
from buscador import a_star

if __name__ == "__main__":
    mapa = gerar_mapa()
    exibir_mapa_console(mapa)

    inicio = mapa[0][0]
    objetivo = mapa[4][4]

    caminho = a_star(inicio, objetivo, mapa)
