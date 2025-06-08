import heapq
import os
from heuristica import calcular_heuristica
from mapaPequeno import exibir_mapa_txt, exibir_mapa_console
from celula import TipoCelula

#Comentar esse import quando for usar heuristica admissivel
from heuristica import calcular_heuristica_inadmissivel 

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

# Função com heurística admissível
def a_star(inicio, objetivo, mapa):
    with open("resultado_busca.txt", "w", encoding="utf-8") as f:
        f.write("INÍCIO DA BUSCA A*\n\n")
        f.write("Mapa inicial:\n")
        f.write(exibir_mapa_txt(mapa))
        f.write("\n")

    open_list = []
    ordem_abertura = []
    contador = 0
    heapq.heappush(open_list, (0, contador, inicio))
    ordem_abertura.append((inicio, 0, calcular_heuristica(inicio, objetivo)))

    closed_list = []
    closed_set = set()

    g = {inicio: 0}
    f = {}
    caminho = {}
    
    arvore_busca = []
    arvore_busca.append({
        'x': inicio.x,
        'y': inicio.y,
        'pai': None,
        'g': 0,
        'h': calcular_heuristica(inicio, objetivo),
        'f': calcular_heuristica(inicio, objetivo)
    })

    while open_list:
        os.system('cls' if os.name == 'nt' else 'clear')
        _, _, atual = heapq.heappop(open_list)

        if atual in closed_set:
            continue

        log(f"\nVisitando: ({atual.x}, {atual.y})")
        log(f"  - tipos: {', '.join(t.value for t in atual.tipos)}")

        g_atual = g.get(atual, 0)
        h_val = calcular_heuristica(atual, objetivo)
        f_val = g_atual + h_val

        if TipoCelula.ENTRADA in atual.tipos:
            log("Estado Inicial")
        else:
            log(f"  - g(n): {g_atual:.1f}")
            log(f"  - h(n): {h_val:.1f}")
            log(f"  - f(n): {f_val:.1f}")
            
        closed_list.append(atual)
        closed_set.add(atual)

        mapa_visual = [["".join(t.value for t in cel.tipos) if cel.tipos else "." for cel in linha] for linha in mapa]
        for celula in closed_list:
            mapa_visual[celula.x][celula.y] = "X"
        mapa_visual[atual.x][atual.y] = "S"
        exibir_mapa_console(mapa_visual)

        if atual == objetivo:
            input("Objetivo alcançado! Pressione Enter para exibir o caminho ótimo...")

            caminho_final = reconstruir_caminho(caminho, atual)
            log("\nCaminho ótimo encontrado:\n")
            for i, cel in enumerate(caminho_final):
                tipos = ', '.join(t.value for t in cel.tipos)
                log(f"{i + 1:>2}. ({cel.x},{cel.y})  Tipos: {tipos}")

            custo_total = g[objetivo]
            log(f"\nCusto total da solução (g(n) do estado final): {custo_total}")
            heuristica_inicio_fim = calcular_heuristica(inicio, objetivo, log=True)
            log(f"Heurística: ({inicio.x},{inicio.y}) até o objetivo ({objetivo.x},{objetivo.y}): {heuristica_inicio_fim}")
            log("\nMapa final da solução com *:")
            log(exibir_mapa_txt(mapa, caminho_final))
            return caminho_final, arvore_busca

        vizinhos = get_vizinhos(atual, mapa)

        heuristicas = []
        for viz in vizinhos:
            if viz in closed_set:
                continue
            #admissivel
            h = calcular_heuristica(viz, objetivo)
            heuristicas.append((viz.x, viz.y, h))
                    
        
        log("\nADJACENTES DO ESTADO ATUAL:")
        adjacentes_ordenados = sorted(heuristicas, key=lambda x: x[2])
        for x, y, h in adjacentes_ordenados:
            log(f"  ({x}, {y}) -> h(n) = {round(h, 2)}")

        # Imprimir a heuristica
        for x, y, _ in adjacentes_ordenados:
            celula = mapa[x][y]
            calcular_heuristica(celula, objetivo, log=True) 

        for vizinho in vizinhos:
            if vizinho in closed_set:
                continue
           
            h_atual = calcular_heuristica(vizinho, objetivo)
            g_novo = g[atual] + h_atual + 1
            f_novo = g_novo + h_atual

            contador += 1
            heapq.heappush(open_list, (f_novo, contador, vizinho))
            ordem_abertura.append((vizinho, g_novo, h_atual))
            
            arvore_busca.append({
                'x': vizinho.x,
                'y': vizinho.y,
                'pai': (atual.x, atual.y),
                'g': g_novo,
                'h': h_atual,
                'f': f_novo
            })

            if vizinho not in g or g_novo < g[vizinho]:
                caminho[vizinho] = atual
                g[vizinho] = g_novo
                f[vizinho] = f_novo

        log("\nLISTA DE OPEN (na ordem de inserção):")
        for cel, g_val, h_val in ordem_abertura:
            if cel not in closed_set:
                log(f"  ({cel.x}, {cel.y}) -> f(n) = {g_val:.1f} + {h_val:.1f} = {(g_val + h_val):.1f}")

        log("LISTA DE CLOSED: " + str([f"({n.x}, {n.y})" for n in closed_list]))
        log("-" * 40)
        input("Pressione Enter para continuar...")

    return None, arvore_busca

#Função com heurística inadmissível
# def a_star(inicio, objetivo, mapa):
#     with open("resultado_busca.txt", "w", encoding="utf-8") as f:
#         f.write("INÍCIO DA BUSCA A*\n\n")
#         f.write("Mapa inicial:\n")
#         f.write(exibir_mapa_txt(mapa))
#         f.write("\n")

#     open_list = []
#     ordem_abertura = []
#     contador = 0
#     heapq.heappush(open_list, (0, contador, inicio))
#     ordem_abertura.append((inicio, 0, calcular_heuristica_inadmissivel(inicio, objetivo)))

#     closed_list = []
#     closed_set = set()

#     g = {inicio: 0}
#     f = {}
#     caminho = {}

#     # Inicia a árvore de restrição
#     arvore_busca = []
#     arvore_busca.append({
#         'x': inicio.x,
#         'y': inicio.y,
#         'pai': None,
#         'g': 0,
#         'h': calcular_heuristica_inadmissivel(inicio, objetivo),
#         'f': calcular_heuristica_inadmissivel(inicio, objetivo)
#     })
    

#     while open_list:
#         os.system('cls' if os.name == 'nt' else 'clear')
#         _, _, atual = heapq.heappop(open_list)

#         if atual in closed_set:
#             continue

#         log(f"\nVisitando: ({atual.x}, {atual.y})")
#         log(f"  - tipos: {', '.join(t.value for t in atual.tipos)}")

#         g_atual = g.get(atual, 0)
#         h_val = calcular_heuristica_inadmissivel(atual, objetivo)
#         f_val = g_atual + h_val

#         if TipoCelula.ENTRADA in atual.tipos:
#             log("Estado Inicial")
#         else:
#             log(f"  - g(n): {g_atual:.1f}")
#             log(f"  - h(n): {h_val:.1f}")
#             log(f"  - f(n): {f_val:.1f}")
            
#         closed_list.append(atual)
#         closed_set.add(atual)

#         mapa_visual = [["".join(t.value for t in cel.tipos) if cel.tipos else "." for cel in linha] for linha in mapa]
#         for celula in closed_list:
#             mapa_visual[celula.x][celula.y] = "X"
#         mapa_visual[atual.x][atual.y] = "S"
#         exibir_mapa_console(mapa_visual)
        
#         if atual == objetivo:
#             input("Objetivo alcançado! Pressione Enter para exibir o caminho encontrado...")

#             caminho_final = reconstruir_caminho(caminho, atual)
#             log("\nCaminho encontrado:\n")
#             for i, cel in enumerate(caminho_final):
#                 tipos = ', '.join(t.value for t in cel.tipos)
#                 log(f"{i + 1:>2}. ({cel.x},{cel.y})  Tipos: {tipos}")

#             custo_total = g[objetivo]
#             log(f"\nCusto total da solução (g(n) do estado final): {custo_total}")
#             heuristica_inicio_fim = calcular_heuristica_inadmissivel(inicio, objetivo, log=True)
#             log(f"Heurística: ({inicio.x},{inicio.y}) até o objetivo ({objetivo.x},{objetivo.y}): {heuristica_inicio_fim}")
#             log("\nMapa final da solução com *:")
#             log(exibir_mapa_txt(mapa, caminho_final))
#             return caminho_final, arvore_busca        

#         vizinhos = get_vizinhos(atual, mapa)

#         heuristicas = []
#         for viz in vizinhos:
#             if viz in closed_set:
#                 continue
#             h = calcular_heuristica_inadmissivel(viz, objetivo)
#             heuristicas.append((viz.x, viz.y, h))
                    
        
#         log("\nADJACENTES DO ESTADO ATUAL:")
#         adjacentes_ordenados = sorted(heuristicas, key=lambda x: x[2])
#         for x, y, h in adjacentes_ordenados:
#             log(f"  ({x}, {y}) -> h(n) = {round(h, 2)}")

#         # Imprimir a heuristica
#         for x, y, _ in adjacentes_ordenados:
#             celula = mapa[x][y]
#             calcular_heuristica_inadmissivel(celula, objetivo, log=True) 

#         for vizinho in vizinhos:
#             if vizinho in closed_set:
#                 continue

#             heuristica_admissivel = calcular_heuristica(vizinho,objetivo) #g(n) é a heurística admissível + 1
            
#             h_atual = calcular_heuristica_inadmissivel(vizinho, objetivo)
#             g_novo = g[atual] + heuristica_admissivel + 1
#             f_novo = g_novo + h_atual
            
#             contador += 1
#             heapq.heappush(open_list, (f_novo, contador, vizinho))
#             ordem_abertura.append((vizinho, g_novo, h_atual))
            
#             arvore_busca.append({
#                 'x': vizinho.x,
#                 'y': vizinho.y,
#                 'pai': (atual.x, atual.y),
#                 'g': g_novo,
#                 'h': h_atual,
#                 'f': f_novo
#             })

#             if vizinho not in g or g_novo < g[vizinho]:
#                 caminho[vizinho] = atual
#                 g[vizinho] = g_novo
#                 f[vizinho] = f_novo

#         log("\nLISTA DE OPEN (na ordem de inserção):")
#         for cel, g_val, h_val in ordem_abertura:
#             if cel not in closed_set:
#                 log(f"  ({cel.x}, {cel.y}) -> f(n) = {g_val:.1f} + {h_val:.1f} = {(g_val + h_val):.1f}")

#         log("LISTA DE CLOSED: " + str([f"({n.x}, {n.y})" for n in closed_list]))
#         log("-" * 40)
#         input("Pressione Enter para continuar...")

#     return None, arvore_busca


