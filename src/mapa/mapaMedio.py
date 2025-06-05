from mapa.celula import Celula, TipoCelula

TAMANHO = 7

def gerar_mapa():
    matriz = [[Celula(x, y) for y in range(TAMANHO)] for x in range(TAMANHO)]

    # Entrada e objetivo
    matriz[0][0].adicionar_tipo(TipoCelula.ENTRADA)
    matriz[6][6].adicionar_tipo(TipoCelula.JOIA)

    # Obstáculos (7 de cada)
    obstaculos_fixos = {
        TipoCelula.GUARDA: [
            (1, 1), (1, 2), (2, 3), (3, 5), (4, 6),
            (5, 1), (6, 2)
        ],
        TipoCelula.CAMERA: [
            (1, 3), (2, 5), (3, 6), (4, 4), (5, 2),
            (6, 6), (0, 6)
        ],
        TipoCelula.PORTA_TRANCADA: [
            (2, 0), (3, 1), (4, 2), (5, 3), (6, 0),
            (6, 1), (0, 4)
        ],
        TipoCelula.ARMADILHA: [
            (0, 1), (2, 2), (3, 3), (4, 0), (5, 4),
            (1, 6), (3, 4)
        ],
    }

    for tipo, posicoes in obstaculos_fixos.items():
        for x, y in posicoes:
            celula = matriz[x][y]
            if TipoCelula.ENTRADA not in celula.tipos and TipoCelula.JOIA not in celula.tipos:
                celula.adicionar_tipo(tipo)

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