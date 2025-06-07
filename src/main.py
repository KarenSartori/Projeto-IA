from mapa.mapa5x5 import gerar_mapa_5x5
from mapa.mapa7x7 import gerar_mapa_7x7
from mapa.mapa8x8 import gerar_mapa_8x8
from mapa.mapa7x7_aleatorio import gerar_mapa_aleatorio
from mapa.mapa_base import exibir_mapa_console
from buscador.buscador import a_star

def escolher_mapa():
    print("Escolha o tipo de mapa:")
    print("1 - Mapa 5x5")
    print("2 - Mapa 7x7")
    print("3 - Mapa 8x8")
    print("4 - Mapa 7x7 aleatório")
    opcao = input("Digite o número da opção: ")

    if opcao == "1":
        return gerar_mapa_5x5()
    elif opcao == "2":
        return gerar_mapa_7x7()
    elif opcao == "3":
        return gerar_mapa_8x8()
    elif opcao == "4":
        return gerar_mapa_aleatorio()
    else:
        print("Opção inválida, usando mapa 5x5 por padrão.")
        return gerar_mapa_5x5()

if __name__ == "__main__":
    
    inicio, objetivo, mapa = escolher_mapa()
    exibir_mapa_console(mapa)
    caminho = a_star(inicio, objetivo, mapa)


