# from mapa.mapa5x5 import gerar_mapa_5x5
# from mapa.mapa7x7 import gerar_mapa_7x7
# from mapa.mapa8x8 import gerar_mapa_8x8
# from mapa.mapa_aleatorio import gerar_mapa_aleatorio
# from mapa.mapa_base import exibir_mapa_console
# from arvoreBusca.arvore import exibir_arvore
# from buscador.buscador import a_star, a_star_inadmissivel

# def escolher_mapa():
#     print("Escolha o tipo de mapa:")
#     print("1 - Mapa 5x5")
#     print("2 - Mapa 7x7")
#     print("3 - Mapa 8x8")
#     print("4 - Mapa Aleatório")
#     opcao = input("Digite o número da opção: ")

#     if opcao == "1":
#         return gerar_mapa_5x5()
#     elif opcao == "2":
#         return gerar_mapa_7x7()
#     elif opcao == "3":
#         return gerar_mapa_8x8()
#     elif opcao == "4":
#         print("Escolha o tamanho:")
#         print("1 - 5x5")
#         print("2 - 7x7")
#         print("3 - 8x8")
#         opcao_tam = input("Digite o número da opção: ")
#         if opcao_tam == "1":
#             return gerar_mapa_aleatorio(5)
#         if opcao_tam == "2":
#             return gerar_mapa_aleatorio(7)
#         if opcao_tam == "2":
#             return gerar_mapa_aleatorio(8)
#         else:
#             print("Opção inválida, usando mapa 7x7 por padrão.")
#             return gerar_mapa_aleatorio(7)
#     else:
#         print("Opção inválida, usando mapa 5x5 por padrão.")
#         return gerar_mapa_5x5()

# if __name__ == "__main__":
    
#     inicio, objetivo, mapa = escolher_mapa()
#     exibir_mapa_console(mapa)
#     caminho, arvore = a_star(inicio, objetivo, mapa)
#     # caminho, arvore = a_star_inadmissivel(inicio, objetivo, mapa)
#     exibir_arvore(arvore)

from interface.tela_inicial import iniciar_interface

if __name__ == "__main__":
    iniciar_interface()


