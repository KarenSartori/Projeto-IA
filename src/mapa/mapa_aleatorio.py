import random
from mapa.celula import Celula, TipoCelula
from mapa.mapa_base import exibir_mapa_console, exibir_mapa_txt


### Nesse método, o usuário pode escolher o tamanho da matriz aleatória 
# Daria para escolher também o número máximo de obstáculos, mas decidimos colocar 7 mesmo

def gerar_mapa_aleatorio(tamanho, max_obstaculos_por_tipo = 7):
    matriz = [[Celula(x, y) for y in range(tamanho)] for x in range(tamanho)]

    posicoes_disponiveis = [(x, y) for x in range(tamanho) for y in range(tamanho)]
    random.shuffle(posicoes_disponiveis) # Embaralha as posições disponíveis

    # Coloca duas posições aleatórias para marcar a Entrada (agente) e o Objetivo (joia)
    entrada_pos = posicoes_disponiveis.pop()
    objetivo_pos = posicoes_disponiveis.pop()

    # Marca a célula de entrada e a célula de objetivo no mapa
    matriz[entrada_pos[0]][entrada_pos[1]].adicionar_tipo(TipoCelula.ENTRADA)
    matriz[objetivo_pos[0]][objetivo_pos[1]].adicionar_tipo(TipoCelula.JOIA)

    # Pega apenas os tipos possíveis de obstáculos a serem adicionados
    tipos_obstaculo = [
        TipoCelula.GUARDA,
        TipoCelula.CAMERA,
        TipoCelula.PORTA_TRANCADA,
        TipoCelula.ARMADILHA
    ]

    # Inicialia contadores para cada tipo de obstáculo, para controlar o limite máximo
    contadores = {tipo: 0 for tipo in tipos_obstaculo} 
    
    # Percorre as posições restantes para adicionar q quantidade de obstácuos 
    # de acordo com a quantidade máxima definida. 
    # Cada célula pode ter até 2 obstáculos diferentes
    for x, y in posicoes_disponiveis:
        celula = matriz[x][y]

        # Define aleatoriamente se a célula terá 1 ou 2 obstáculos
        qntd_obstaculos_por_celula = random.randint(1, 2)

        # Lista os tipos de obstáculos que ainda podem ser adicionados (não atingiram o limite)
        tipos_disponiveis = []
        for tipo in tipos_obstaculo:
            if contadores[tipo] < max_obstaculos_por_tipo:
                tipos_disponiveis.append(tipo)

        # Se não tem mais tipos disponíveis para adicionar, interrompe
        if not tipos_disponiveis:
            break 

        # Se for pra adicionar 2 obstáculos e houver pelo menos 2 tipos disponíveis
        if qntd_obstaculos_por_celula == 2 and len(tipos_disponiveis) >= 2: 
            # Sorteira 2 tipos DIFERENTES para adicionar na célula
            tipos_sorteados = random.sample(tipos_disponiveis, 2)
            for tipo in tipos_sorteados:
                celula.adicionar_tipo(tipo)
                contadores[tipo] += 1
        else:
            # Caso contrário, adiciona apenas 1 tipo aleatório disponível
            tipo = random.choice(tipos_disponiveis)
            celula.adicionar_tipo(tipo)
            contadores[tipo] += 1
    
    inicio = matriz[entrada_pos[0]][entrada_pos[1]]
    objetivo = matriz[objetivo_pos[0]][objetivo_pos[1]]

    return inicio, objetivo, matriz

