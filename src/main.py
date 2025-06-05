# from mapa.mapaAleatorio import gerar_mapa, exibir_mapa_console
# from buscador.buscador import a_star


# if __name__ == "__main__":

#     inicio, objetivo, mapa = gerar_mapa()
    
#     exibir_mapa_console(mapa) #apaga?

#     caminho = a_star(inicio, objetivo, mapa)

from interface.tela_inicial import iniciar_interface

if __name__ == "__main__":
    iniciar_interface()

