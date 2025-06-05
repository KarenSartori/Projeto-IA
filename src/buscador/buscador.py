import heapq
import os
from heuristica.heuristica import calcular_heuristica
from mapa.mapaMedio import exibir_mapa_txt
from mapa.celula import TipoCelula
from mapa.mapaMedio import exibir_mapa_console

# coloquei um arq .txt pra ver se ta certo os calculos
def log(msg="", end="\n"):
    print(msg, end=end)
    with open("resultado_busca.txt", "a", encoding="utf-8") as f:
        f.write(str(msg) + end)

# o custo final do caminho é 1 ou o custo da celular
def custo_real(celula):
    custo = 0
    for tipo in celula.tipos:
        if tipo == TipoCelula.GUARDA:
            custo += 5
        elif tipo == TipoCelula.CAMERA:
            custo += 3
        elif tipo == TipoCelula.PORTA_TRANCADA:
            custo += 2
        elif tipo == TipoCelula.ARMADILHA:
            custo += 4
    return max(custo, 1)

def get_vizinhos(celula, mapa):
    vizinhos = []
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in direcoes:
        nx, ny = celula.x + dx, celula.y + dy
        if 0 <= nx < len(mapa) and 0 <= ny < len(mapa[0]):
            vizinhos.append(mapa[nx][ny])
    return vizinhos

def reconstruir_caminho(caminho, atual):
    caminho_final = []
    while atual in caminho:
        caminho_final.append(atual)
        atual = caminho[atual]
    caminho_final.append(atual)
    caminho_final.reverse()
    return caminho_final

def a_star(inicio, objetivo, mapa):
    # mapa no arquivo .txt
    with open("resultado_busca.txt", "w", encoding="utf-8") as f:
        f.write("INÍCIO DA BUSCA A*\n\n")
        f.write("Mapa inicial:\n")
        f.write(exibir_mapa_txt(mapa))
        f.write("\n")

    ordem_abertura = []
    open_list = []
    # heapq organiza os nós com menor valor no topo
    contador = 0
    heapq.heappush(open_list, (0, contador, inicio))
    ordem_abertura.append(inicio)

    closed_list = []
    closed_set = set()

    # g = {inicio: 0}
    # g = {inicio: calcular_heuristica(inicio, objetivo) + 1}
    # f = {inicio: calcular_heuristica(inicio, objetivo)}
    g = {inicio: 0}
    f = {inicio: 0}

    # caminho funciona como dicioanrio pra guardar os estados e os anteriores dele
    # fica tipo { (1,0): (0,0) }
    caminho = {}

    while open_list:
        os.system('cls' if os.name == 'nt' else 'clear')
        # pega o nó de menor valor
        _, _, atual = heapq.heappop(open_list)

        log(f"\nVisitando: ({atual.x}, {atual.y})")
        log(f"  - tipos: {', '.join(t.value for t in atual.tipos)}")

        if TipoCelula.ENTRADA in atual.tipos:
            log("Estado Inicial")
        else:
            log(f"  - g(n): {g[atual]:.1f}")
            h_val = calcular_heuristica(atual, objetivo)
            log(f"  - h(n): {h_val}")
            log(f"  - f(n): {round(g[atual] + h_val, 1)}")

        # add na lista de closed
        closed_list.append(atual)  # visualização
        closed_set.add(atual)  # lógica de controle

        mapa_visual = [["".join(t.value for t in cel.tipos) if cel.tipos else "." for cel in linha] for linha in mapa]
        for celula in closed_list:
            mapa_visual[celula.x][celula.y] = "X"
        mapa_visual[atual.x][atual.y] = "S"
        exibir_mapa_console(mapa_visual)

        # pega os adjacentes do estado
        vizinhos = get_vizinhos(atual, mapa)
        heuristicas = []
        for viz in vizinhos:
            if viz in closed_list:
                continue
            h = calcular_heuristica(viz, objetivo)
            heuristicas.append((viz.x, viz.y, h))

        log("\nADJACENTES DO ESTADO ATUAL:")
        for x, y, h in sorted(heuristicas, key=lambda x: x[2]):
            log(f"  ({x}, {y}) -> h(n) = {round(h, 2)}")

        for vizinho in vizinhos:
            if vizinho in closed_set:
                continue

            # g_novo = g[atual] + custo_real(vizinho)
            # o g é o custo de um estado ao outro
            # g_novo = g[atual] + 1

            # h = calcular_heuristica(vizinho, objetivo, log=True)
            # g_novo = h + 1
            # f_novo = g_novo + h

            h_atual = calcular_heuristica(vizinho, objetivo, log=True)
            g_novo = g[atual] + h_atual + 1
            f_novo = g_novo + h_atual

            if vizinho not in g or f_novo < f.get(vizinho, float('inf')):
                caminho[vizinho] = atual
                g[vizinho] = g_novo
                f[vizinho] = f_novo
                contador += 1
                heapq.heappush(open_list, (f_novo, contador, vizinho))
                ordem_abertura.append(vizinho)

        log("\nLISTA DE OPEN (na ordem de inserção):")
        for cel in ordem_abertura:
            if cel not in closed_set:
                g_val = g.get(cel, '?')
                h_val = calcular_heuristica(cel, objetivo)
                # log(f"  ({cel.x}, {cel.y}) -> f(n) = {g_val} + {round(h_val, 2)} = {round(g_val + h_val, 2)}")
                log(f"  ({cel.x}, {cel.y}) -> f(n) = {g_val:.1f} + {h_val:.1f} = {(g_val + h_val):.1f}")

        log("LISTA DE CLOSED: " + str([f"({n.x}, {n.y})" for n in closed_list]))
        log("-" * 40)
        input("Pressione Enter para continuar...")

        if atual == objetivo:
            caminho_final = reconstruir_caminho(caminho, atual)
            log("\nCaminho ótimo encontrado:\n")
            for i, cel in enumerate(caminho_final):
                tipos = ', '.join(t.value for t in cel.tipos)
                log(f"{i + 1:>2}. ({cel.x},{cel.y})  Tipos: {tipos}")

            # Soma dos g(n) de cada célula do caminho
            custo_total = sum(g[cel] for cel in caminho_final)
            log(f"\nCusto total da solução (soma dos g(n)): {custo_total}")

            # Heurística do início direto até o objetivo
            heuristica_inicio_fim = calcular_heuristica(inicio, objetivo, log=True)
            log(f"Heurística: ({inicio.x},{inicio.y}) até o objetivo ({objetivo.x},{objetivo.y}): {heuristica_inicio_fim}")

            # Exibe e salva o mapa final com caminho
            log("\nMapa final da solução com *:")
            log(exibir_mapa_txt(mapa, caminho_final))

            return caminho_final
    return None