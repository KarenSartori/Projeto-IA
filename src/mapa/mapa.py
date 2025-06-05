from mapa.celula import Celula, TipoCelula

TAMANHO = 5

def gerar_mapa():
    # salva o mapa com base no tamanho fixo
    matriz = [[Celula(x, y) for y in range(TAMANHO)] for x in range(TAMANHO)]

    # Começo e objetivo
    matriz[0][0].adicionar_tipo(TipoCelula.ENTRADA)
    matriz[4][4].adicionar_tipo(TipoCelula.JOIA)

    # Obstáculos (coloquei pouco pra teste)
    obstaculos_fixos = {
        TipoCelula.GUARDA: [
            (0, 1), (0,2), (2, 2), (3, 3)
        ],
        TipoCelula.CAMERA: [
            (1, 1), (0,2), (2, 2), (3, 0)
        ],
        TipoCelula.PORTA_TRANCADA: [
            (0, 3), (2, 0), (4, 1)
        ],
        TipoCelula.ARMADILHA: [
            (1, 1), (3, 2), (4, 3)
        ],
    }

    for tipo, posicoes in obstaculos_fixos.items():
        for x, y in posicoes:
            celula = matriz[x][y]
            if TipoCelula.ENTRADA not in celula.tipos and TipoCelula.JOIA not in celula.tipos:
                celula.adicionar_tipo(tipo)

    return matriz

def exibir_mapa_console(matriz):
    TAMANHO = len(matriz)
    print(f"\nMapa ({TAMANHO}x{TAMANHO}):")
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

            conteudo = conteudo[:2].ljust(2)  # coloquei no max 2 por estado
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
