import heapq
import os
from heuristica import calcular_heuristica
from mapa import exibir_mapa_txt
from celula import TipoCelula
from mapa import exibir_mapa_console

# coloquei um arq .txt pra ver se ta certo os calculos
def log(msg="", end="\n"):
    print(msg, end=end)
    with open("resultado_busca.txt", "a", encoding="utf-8") as f:
        f.write(str(msg) + end)

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

    open_list = []
    # heapq organiza os nós com menor valor no topo
    heapq.heappush(open_list, (0, inicio))
    closed_list = []

    g = {inicio: 0}
    f = {inicio: calcular_heuristica(inicio, objetivo)}
    caminho = {}

    while open_list:
        os.system('cls' if os.name == 'nt' else 'clear')
        _, atual = heapq.heappop(open_list)

        log(f"\nVisitando: ({atual.x}, {atual.y})")
        log(f"  - tipos: {', '.join(t.value for t in atual.tipos)}")
        log(f"  - g(n): {g[atual]}")
        h_val = calcular_heuristica(atual, objetivo)
        log(f"  - h(n): {h_val}")
        log(f"  - f(n): {round(g[atual] + h_val, 1)}")
        # add na lista de closed
        closed_list.append(atual)

        mapa_visual = [["".join(t.value for t in cel.tipos) if cel.tipos else "." for cel in linha] for linha in mapa]
        for celula in closed_list:
            mapa_visual[celula.x][celula.y] = "X"
        mapa_visual[atual.x][atual.y] = "S"
        exibir_mapa_console(mapa_visual)

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
            if vizinho in closed_list:
                continue

            # g_novo = g[atual] + custo_real(vizinho)
            g_novo = g[atual] + 1
            h = calcular_heuristica(vizinho, objetivo)
            f_novo = g_novo + h

            if vizinho not in g or f_novo < f.get(vizinho, float('inf')):
                caminho[vizinho] = atual
                g[vizinho] = g_novo
                f[vizinho] = f_novo
                heapq.heappush(open_list, (f_novo, vizinho))

        log("\nLISTA DE OPEN (com f(n) = g(n) + h(n)):")
        for f_score, n in sorted(open_list, key=lambda x: x[0]):
            g_val = g.get(n, '?')
            h_val = calcular_heuristica(n, objetivo)
            log(f"  ({n.x}, {n.y}) -> f(n) = {g_val} + {round(h_val, 2)} = {round(g_val + h_val, 2)}")

        log("LISTA DE CLOSED: " + str([f"({n.x}, {n.y})" for n in closed_list]))
        log("-" * 40)
        input("Pressione Enter para continuar...")

        if atual == objetivo:
            caminho_final = reconstruir_caminho(caminho, atual)
            log("\nCaminho ótimo encontrado:\n")
            for i, cel in enumerate(caminho_final):
                tipos = ', '.join(t.value for t in cel.tipos)
                log(f"{i + 1:>2}. ({cel.x},{cel.y})  Tipos: {tipos}")

            custo_total = g[objetivo]
            log(f"\nCusto total da solução: {custo_total}")

            # exibe e salva o mapa final com caminho
            log("\nMapa final da solução com *:")
            log(exibir_mapa_txt(mapa, caminho_final))

            return caminho_final
    return None
