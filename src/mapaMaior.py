from celula import Celula, TipoCelula

TAMANHO = 10


def gerar_mapa():
    matriz = [[Celula(x, y) for y in range(TAMANHO)] for x in range(TAMANHO)]

    # Entrada e objetivo
    matriz[0][0].adicionar_tipo(TipoCelula.ENTRADA)
    matriz[9][9].adicionar_tipo(TipoCelula.JOIA)

    # Obstáculos fixos com 20 posições cada
    obstaculos_fixos = {
        TipoCelula.GUARDA: [
            (1, 1), (1, 2), (2, 3), (3, 5), (4, 7),
            (5, 9), (6, 2), (7, 4), (8, 6), (1, 8),
            (2, 1), (2, 5), (3, 7), (4, 9), (6, 4),
            (5, 1), (6, 3), (7, 6), (8, 7), (5, 5)
        ],
        TipoCelula.CAMERA: [
            (1, 3), (2, 5), (3, 7), (4, 9), (6, 6),
            (5, 2), (7, 3), (8, 5), (9, 1), (0, 6),
            (1, 4), (2, 6), (3, 8), (4, 4), (5, 6),
            (6, 7), (7, 8), (8, 2), (9, 3), (1, 6)
        ],
        TipoCelula.PORTA_TRANCADA: [
            (0, 5), (1, 7), (2, 9), (6, 0), (7, 2),
            (3, 1), (4, 2), (5, 3), (6, 5), (7, 7),
            (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
            (6, 1), (7, 1), (8, 1), (9, 1), (8, 3)
        ],
        TipoCelula.ARMADILHA: [
            (3, 3), (4, 4), (5, 5), (7, 7), (8, 8),
            (0, 1), (1, 1), (2, 2), (3, 3), (4, 4),
            (5, 5), (6, 6), (7, 7), (8, 8), (9, 9),
            (0, 8), (1, 9), (2, 8), (3, 9), (5, 8)
        ],
    }

    for tipo, posicoes in obstaculos_fixos.items():
        for x, y in posicoes:
            celula = matriz[x][y]
            if TipoCelula.ENTRADA not in celula.tipos and TipoCelula.JOIA not in celula.tipos:
                celula.adicionar_tipo(tipo)

    return matriz


def exibir_mapa_console(matriz):
    print("\nMapa (10x10):")
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
