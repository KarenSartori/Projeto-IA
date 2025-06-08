import heapq
import os
from heuristica.heuristica import calcular_heuristica, decompor_heuristica
from mapa.mapa_base import exibir_mapa_txt, exibir_mapa_console
from mapa.celula import TipoCelula

### Função para registrar logs tanto no terminal quanto em um arquivo .txt
def log(msg="", end="\n"):
    print(msg, end=end) # Imprime no terminal
    with open("Resultado_busca.txt", "a", encoding="utf-8") as f:
        f.write(str(msg) + end) # Escreve no arquivo de log

### Calcula o custo real de uma célula baseado nos tipos que ela possui
def custo_real(celula):
    custo = 0
    # Soma o custo associado a cada tipo especial da célula
    for tipo in celula.tipos:
        if tipo == TipoCelula.GUARDA:
            custo += 5
        elif tipo == TipoCelula.CAMERA:
            custo += 3
        elif tipo == TipoCelula.PORTA_TRANCADA:
            custo += 2
        elif tipo == TipoCelula.ARMADILHA:
            custo += 4
    # Garante custo mínimo de 1 para células comuns (default)
    return max(custo, 1)

### Retorna a lista de células vizinhas (acima, abaixo, esquerda, direita)
def get_vizinhos(celula, mapa):
    vizinhos = []
    # Movimentos possíveis nas 4 direções
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in direcoes:
        nx, ny = celula.x + dx, celula.y + dy
        # Verifica se a posição está dentro dos limites do mapa
        if 0 <= nx < len(mapa) and 0 <= ny < len(mapa[0]):
            vizinhos.append(mapa[nx][ny])
    return vizinhos

### Reconstrói o caminho da célula inicial até a célula final 
def reconstruir_caminho(caminho, atual):
    caminho_final = []

    # Enquanto houver predecessor, vai acumulando no caminho
    while atual in caminho:
        caminho_final.append(atual)
        atual = caminho[atual]
    caminho_final.append(atual)     # Adiciona o primeiro nó (início)
    caminho_final.reverse()         # Inverte para ficar do início ao fim
    return caminho_final


### ALGORITMO A* PRINCIPAL PARA ENCONTRAR O CAMINHO DO INÍCIO AO OBJETIVO
def a_star(inicio, objetivo, mapa):
    # Limpa o arquvio de log no início da execução
    with open("resultado_busca.txt", "w", encoding="utf-8") as f:
        f.write("INÍCIO DA BUSCA A*\n\n")
        f.write("Mapa inicial:\n")
        f.write(exibir_mapa_txt(mapa))
        f.write("\n")

    open_list = []       # Fila de prioridade para nós a serem explorados
    ordem_abertura = []  # Para registrar a ordem do s nós abertos
    contador = 0         # Contador para desempate no heapq (quando f(n) igual)

    # Adiciona o nó inicial na lista de abertos com f(n) = 0 
    heapq.heappush(open_list, (0, contador, inicio))
    ordem_abertura.append((inicio, 0, calcular_heuristica(inicio, objetivo)))

    closed_list = []     # Lista de nós já explorados
    closed_set = set()   # Conjunto para acesso rápido e 

    g = {inicio: 0}      # Custo do caminho desde o início até cada nó
    f = {}               # Custo estimado total (g(n) + h(n))
    caminho = {}         # Armazenar os antecessores dos nós

    while open_list:
        os.system('cls' if os.name == 'nt' else 'clear') # Limpa o console

        # Pega o nó com menor f(n) na lista dos nós abertos
        _, _, atual = heapq.heappop(open_list)

        # Ignora se já foi visitado
        if atual in closed_set:
            continue

        # Logs sobre o nó atual visitado
        log(f"\nVisitando: ({atual.x}, {atual.y})")
        log(f"  - tipos: {', '.join(t.value for t in atual.tipos)}")

        g_atual = g.get(atual, 0)                       # Custo real até o nó atual
        h_val = calcular_heuristica(atual, objetivo)    # Custo heurístico até o objetivo
        f_val = g_atual + h_val                         # Custo estimado total

        # Verifica se é o estado inicial
        if TipoCelula.ENTRADA in atual.tipos:
            log("Estado Inicial")
        else:
            # Exibe g(n), h(n) e f(n) para o nó atual
            log(f"  - g(n): {g_atual:.1f}")
            log(f"  - h(n): {h_val:.1f}")
            log(f"  - f(n): {f_val:.1f}")

        # Depois de visitado, adiciona o nó atual na lista dos visitados
        closed_list.append(atual)
        closed_set.add(atual)

        # Cria uma visualização do mapa para exibir o progresso
        mapa_visual = [["".join(t.value for t in cel.tipos) if cel.tipos else "." for cel in linha] for linha in mapa]
        
        # Marca as células já visitadas com 'X' e a célula atual com 'S'
        for celula in closed_list:
            mapa_visual[celula.x][celula.y] = "X"
        mapa_visual[atual.x][atual.y] = "S"
        exibir_mapa_console(mapa_visual) # Imprime no terminal

        # Se chegou no objetivo, reconstrói o caminho e finaliza
        if atual == objetivo:
            caminho_final = reconstruir_caminho(caminho, atual)

            log("\nCaminho ótimo encontrado:\n")
            # Imprime o caminho com posições e tipos
            for i, cel in enumerate(caminho_final):
                tipos = ', '.join(t.value for t in cel.tipos)
                log(f"{i + 1:>2}. ({cel.x},{cel.y})  Tipos: {tipos}")

            custo_total = g[objetivo]
            log(f"\nCusto total da solução (g(n) do estado final): {custo_total}")
            
            heuristica_inicio_fim = calcular_heuristica(inicio, objetivo, log=True)
            log(f"Heurística: ({inicio.x},{inicio.y}) até o objetivo ({objetivo.x},{objetivo.y}): {heuristica_inicio_fim}")
            
            log("\nMapa final da solução com *:")
            log(exibir_mapa_txt(mapa, caminho_final)) # Mostra o mapa com o caminho marcado
            return caminho_final

        # Obtém os vizinhos do nó atual para expandir
        vizinhos = get_vizinhos(atual, mapa)
        heuristicas = []

        # Calcula a heurísticas para os vizinhos (mostra só no log)
        for viz in vizinhos:
            if viz in closed_set:
                continue
            h = calcular_heuristica(viz, objetivo)
            heuristicas.append((viz.x, viz.y, h))

        # Log dos vizinhos adjacentes com as suas heurísticas
        log("\nADJACENTES DO ESTADO ATUAL:")
        for x, y, h in sorted(heuristicas, key=lambda x: x[2]):
            log(f"  ({x}, {y}) -> h(n) = {round(h, 2)}")

        # Para cada vizinho, atualiza os valores g(n), f(n) e o caminho se for melhor
        for vizinho in vizinhos:
            if vizinho in closed_set:
                continue

            h_atual = calcular_heuristica(vizinho, objetivo, log=True)
            g_novo = g[atual] + h_atual + 1     # Custo acumulado até o vizinho
            f_novo = g_novo + h_atual           

            contador += 1
            heapq.heappush(open_list, (f_novo, contador, vizinho))      # Adiciona na lista de abertos para explorar depois
            ordem_abertura.append((vizinho, g_novo, h_atual))           # Registra a ordem para o log

            # Atualiza o melhor caminho e o custo caso encontrado um caminho mais barato
            if vizinho not in g or g_novo < g[vizinho]:
                caminho[vizinho] = atual
                g[vizinho] = g_novo
                f[vizinho] = f_novo

        # Log da lista de abertos com nós ainda para explorar 
        log("\nLISTA DE OPEN (na ordem de inserção):")
        for cel, g_val, h_val in ordem_abertura:
            if cel not in closed_set:
                log(f"  ({cel.x}, {cel.y}) -> f(n) = {g_val:.1f} + {h_val:.1f} = {(g_val + h_val):.1f}")

        # Log da lista de fechados com os nós já visitados
        log("LISTA DE CLOSED: " + str([f"({n.x}, {n.y})" for n in closed_list]))
        log("-" * 40)

        # Pausa para acompanhar cada passo
        input("Pressione Enter para continuar...")

    return None 



### VERSÃO ITERATIVA DO A* PARA O USO NA INTERFACE GRÁFICA
# Adicionei essa "versão 2.0" do método acima para não apagar o método
# e poder usar esse aqui na interface gráfica
def a_star_iterativo(inicio, objetivo, mapa):
    open_list = []
    closed_list = []
    closed_set = set()
    g = {inicio: 0}
    f = {}
    caminho = {}
    contador = 0

    heapq.heappush(open_list, (0, contador, inicio))

    while True:
        if not open_list:
            yield {"estado_final": True, "caminho_final": None}  # Caminho não encontrado
            return

        _, _, atual = heapq.heappop(open_list)

        if atual in closed_set:
            continue

        closed_list.append(atual)
        closed_set.add(atual)

        if atual == objetivo:

            caminho_final = reconstruir_caminho(caminho, atual)

            # Calcula todas as coisas para mandar
            texto_caminho = "CAMINHO ÓTIMO ENCONTRADO: "
            texto_caminho += " → ".join(f"({cel.x}, {cel.y})" for cel in caminho_final)
            
            texto_custo = f"CUSTO TOTAL: {g[objetivo]}"
            texto_heuristica = f"HEURÍSTICA ATÉ O OBJETIVO: {calcular_heuristica(inicio, objetivo)}"
            
            yield {
                "mapa": mapa,
                "atual": atual,
                "fechados": closed_list.copy(),
                "abertos": [item[2] for item in open_list if item[2] not in closed_set],
                "estado_final": True,
                "caminho_final": caminho_final,
                "f_dict": f,
                "adjacentes": [],
                "caminho_encontrado_texto": texto_caminho,
                "custo_total_texto": texto_custo,
                "heuristica_texto": texto_heuristica 
            }
            return

        adjacentes = []
        heuristicas_adjacentes = []
        for vizinho in get_vizinhos(atual, mapa):
            if vizinho in closed_set:
                continue

            h = calcular_heuristica(vizinho, objetivo)
            g_novo = g[atual] + h + 1
            f_novo = g_novo + h

            contador += 1
            heapq.heappush(open_list, (f_novo, contador, vizinho))

            risco, atraso, distancia = decompor_heuristica(vizinho, objetivo)

            if vizinho not in g or g_novo < g[vizinho]:
                caminho[vizinho] = atual
                g[vizinho] = g_novo
                f[vizinho] = f_novo

            # Dados completos da heurística

            # Colocando os pesos aqui para imprimir e também caso precise mudar depois
            peso_risco = 3
            peso_atraso = 2
            peso_dist = 1

            adjacentes.append((vizinho.x, vizinho.y, h))
            heuristicas_adjacentes.append(f"Heurística de ({vizinho.x}, {vizinho.y}) →"
                              + f" Risco: {risco}"
                              + f", Atraso: {atraso}"
                              + f", Distância: {distancia:.1f}:\n"
                              + f"H(n) = ({peso_risco} * {risco}) + "
                              + f"({peso_atraso} * {atraso}) + "
                              + f"({peso_dist} * {distancia:.1f})"
                              + f" = {round(h, 1)}")
                    

        yield {
            "mapa": mapa,
            "atual": atual,
            "fechados": closed_list.copy(),
            "abertos": [item[2] for item in open_list if item[2] not in closed_set],
            "estado_final": False,
            "caminho_final": None,
            "f_dict": f,
            "adjacentes": adjacentes,
            "heuristicas_adjacentes": heuristicas_adjacentes 
        }
