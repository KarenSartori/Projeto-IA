from mapa.celula import Celula, TipoCelula

### Método para gerar o mapa fixo com obstáculos e célula de entrada/objetivo
def gerar_mapa(tamanho, entrada, joia, obstaculos_fixos):
    # Cria uma matriz de acordo com o tamanho preenchida com objetos da classe Celula
    matriz = [[Celula(x, y) for y in range(tamanho)] for x in range(tamanho)]

    # Define a posição inicial do jogador (Entrada) e o objetivo (Joia)
    matriz[entrada[0]][entrada[1]].adicionar_tipo(TipoCelula.ENTRADA)
    matriz[joia[0]][joia[1]].adicionar_tipo(TipoCelula.JOIA)


    # Adiciona os tipos de obstáculos nas células correspondentes,
    # evitando sobrescrever a ENTRADA e a JOIA
    for tipo, posicoes in obstaculos_fixos.items():
        for x, y in posicoes:
            celula = matriz[x][y]
            if TipoCelula.ENTRADA not in celula.tipos and TipoCelula.JOIA not in celula.tipos:
                celula.adicionar_tipo(tipo)

    # Pega as células de início e objetivo (entrada e joia)
    inicio = matriz[entrada[0]][entrada[1]]
    objetivo = matriz[joia[0]][joia[1]]

    return inicio, objetivo, matriz


### Exibe o mapa no terminal de forma visual com bordas e símbolos
def exibir_mapa_console(matriz):
    tamanho = len(matriz)
    print(f"\nMapa ({tamanho}x{tamanho}):")

    # Cria a linha separadora para o visual do mapa
    separador = "+" + "+".join(["----"] * tamanho) + "+"

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
                    # Junta os tipos de célula em string (ex: "GA" para Guarda + Armadilha)
                    conteudo = "".join(sorted(t.value for t in cel.tipos))

            # Garante que a célula tenha no máximo 2 obstáculos
            conteudo = conteudo[:2].ljust(2)  
            linha_str += f" {conteudo} |"

        print(separador)
        print(linha_str)
    print(separador)


### Gera uma string formatada do mapa com a marcação do caminho 
def exibir_mapa_txt(matriz, caminho=None):
    tamanho = len(matriz)
    linhas = []
    linhas.append("+" + "----+" * tamanho)

    for x in range(tamanho):
        linha = "|"
        for y in range(tamanho):
            celula = matriz[x][y]

            # Marca com '*' se a célula estiver no caminho passado
            if caminho and celula in caminho:
                marcador = "*"
            elif celula.tipos:
                # Junta os tipos presentes na célula
                marcador = "".join(t.value for t in celula.tipos)
            else:
                marcador = "."

            linha += f" {marcador:2} |"

        linhas.append(linha)
        linhas.append("+" + "----+" * tamanho)

    return "\n".join(linhas) + "\n"
