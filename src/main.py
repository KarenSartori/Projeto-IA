# from mapaAleatorio import gerar_mapa, exibir_mapa_console
#from mapaPequeno import gerar_mapa, exibir_mapa_console
from mapaMedio import gerar_mapa, exibir_mapa_console
from buscador import a_star
from arvore import exibir_arvore


if __name__ == "__main__":
    #Gerar mapa aleatorio
    # inicio, objetivo, mapa = gerar_mapa()
    
    #Gerar mapa médio
    mapa = gerar_mapa()
    inicio = mapa[0][0]
    objetivo = mapa[6][6]

    exibir_mapa_console(mapa) 

    caminho, arvore = a_star(inicio, objetivo, mapa)

    exibir_arvore(arvore)
