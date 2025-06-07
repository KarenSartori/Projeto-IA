#from mapaAleatorio import gerar_mapa, exibir_mapa_console
from mapaMedio import gerar_mapa, exibir_mapa_console
from buscador import a_star
from grafo import exibir_arvore_restricao


if __name__ == "__main__":
    #gerar mapa aleatorio
    #inicio, objetivo, mapa = gerar_mapa()
    
    #gerar mapa medio
    mapa = gerar_mapa()
    inicio = mapa[0][0]
    objetivo = mapa[6][6]

    exibir_mapa_console(mapa) #apaga?

    caminho, arvore = a_star(inicio, objetivo, mapa)
    
    
    exibir_arvore_restricao(arvore, objetivo)