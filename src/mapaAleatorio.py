import random
from celula import Celula, TipoCelula

TAMANHO = 7 
# poder escolher o tamanho?
# se puder escolher a qntd de obstáculos?

def gerar_mapa():
    matriz = [[Celula(x, y) for y in range(TAMANHO)] for x in range(TAMANHO)]

    posicoes_disponiveis = [(x, y) for x in range(TAMANHO) for y in range(TAMANHO)]
    random.shuffle(posicoes_disponiveis) # Embaralha as posições disponíveis

    # Posições aleatórias pra Entrada e Joia
    entrada_pos = posicoes_disponiveis.pop()
    joia_pos = posicoes_disponiveis.pop()

    matriz[entrada_pos[0]][entrada_pos[1]].adicionar_tipo(TipoCelula.ENTRADA)
    matriz[joia_pos[0]][joia_pos[1]].adicionar_tipo(TipoCelula.JOIA)

    tipos_obstaculo = [
        TipoCelula.GUARDA,
        TipoCelula.CAMERA,
        TipoCelula.PORTA_TRANCADA,
        TipoCelula.ARMADILHA
    ]

    contadores = {tipo: 0 for tipo in tipos_obstaculo} # Dict por compressão: mapeia para cada tipo o valor 0, sendo usado para contar quantos obstáculos daquele tipo já foram adicionados

    # Definindo a posição dos obstáculos (7 de cada), com até 2 obstáculos por célula
    for x, y in posicoes_disponiveis:
        celula = matriz[x][y]

        qntd_obstaculos_por_celula = random.randint(1, 2)
        tipos_disponiveis = []
        for tipo in tipos_obstaculo:
            if contadores[tipo] < 7:
                tipos_disponiveis.append(tipo)

        if len(tipos_disponiveis) == 0:
            break # Não existem mais tipos disponíveis
                
        if qntd_obstaculos_por_celula == 2 and len(tipos_disponiveis) >= 2: # Verifica se ainda tem ao menos 2 tipos disponíveis se for colocar 2 obstáculos por célula
            tipos_sorteados = random.sample(tipos_disponiveis, 2)
            for tipo in tipos_sorteados:
                celula.adicionar_tipo(tipo)
                contadores[tipo] += 1
        else:
            tipo = random.choice(tipos_disponiveis)
            celula.adicionar_tipo(tipo)
            contadores[tipo] += 1

    return matriz

def exibir_mapa_console(matriz):
    print("\nMapa (7x7):")
    separador = "+" + "+".join(["----"] * TAMANHO) + "+"
    for linha in matriz:
        linha_str = "|"
        for cel in linha:
            if isinstance(cel, str):
                conteudo = cel
            else:
                if TipoCelula.ENTRADA in cel.tipos:
                    conteudo = "E"
                elif TipoCelula.JOIA in cel.tipos:
                    conteudo = "J"
                elif not cel.tipos:
                    conteudo = "  "
                else:
                    conteudo = "".join(sorted(t.value for t in cel.tipos))

            conteudo = conteudo[:2].ljust(2)
            linha_str += f" {conteudo} |"
        print(separador)
        print(linha_str)
    print(separador)

def exibir_mapa_txt(mapa, caminho=None):
    TAMANHO = len(mapa)
    linhas = []
    linhas.append("+" + "----+" * TAMANHO)

    for x in range(TAMANHO):
        linha = "|"
        for y in range(TAMANHO):
            celula = mapa[x][y]

            if caminho and celula in caminho:
                marcador = "*"
            elif celula.tipos:
                marcador = "".join(t.value for t in celula.tipos)
            else:
                marcador = "."

            linha += f" {marcador:2} |"
        linhas.append(linha)
        linhas.append("+" + "----+" * TAMANHO)

    return "\n".join(linhas) + "\n"

mapa = gerar_mapa()
exibir_mapa_console(mapa)