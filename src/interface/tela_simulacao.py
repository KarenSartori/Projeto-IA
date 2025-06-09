import customtkinter as ctk
from tkinter import messagebox
from copy import deepcopy
from interface.imagens_celulas import carregar_imagens
from mapa.celula import TipoCelula
from mapa.mapa5x5 import gerar_mapa_5x5
from mapa.mapa7x7 import gerar_mapa_7x7
from mapa.mapa8x8 import gerar_mapa_8x8
from mapa.mapa_aleatorio import gerar_mapa_aleatorio
from buscador.buscador import a_star_iterativo

class Simulacao:
    def __init__(self, tipo_mapa, tamanho_personalizado=None):
        self.tipo_mapa = tipo_mapa
        self.tamanho_personalizado = tamanho_personalizado

        self.app = ctk.CTk()
        self.app.title(f"Simulação A* - Mapa{tipo_mapa.capitalize()}")
        self.app.after(100, lambda: self.app.state("zoomed")) # Garante que a tela em zoom após carregar
        # self.app.resizable(False, False)

        self.grid_size = self.definir_tamanho_mapa(tipo_mapa)  # Define o tamanho do mapa (grid) com base no tipo
        self.grid_widgets = [] # Guarda os widgets que representam as células na interface
        self.imagens = carregar_imagens() # Carrega as imagens correspondentes a cada tipo de célula
        
        self.criar_interface() # Cria a interface visual da simulação
        
        # Gera o mapa inicial e posições do agente e objetivo conforme o tipo selecionado
        self.inicio, self.objetivo, self.mapa = self.gerar_mapa_inicial()
        
        # Salva uma cópia do mapa original para uso posterior (exibição final, comparação, etc.)
        self.mapa_original = deepcopy(self.mapa)

        # Cria um iterador para o algoritmo A* para execução passo a passo
        self.iterator_a_star = a_star_iterativo(self.inicio, self.objetivo, self.mapa)

        # Atualiza a interface para mostrar o mapa inicial e o agente na posição inicial
        self.atualizar_grid_com_mapa(self.mapa, self.inicio)

        self.estado_botao = "iniciar" # Estado inicial do botão "Continuar"
        self.atualizar_botao() # Método para atualizar o botão automaticamente

        self.app.mainloop() 


    # Define o tamanho da grade do mapa com base no tipo selecionado ou tamanho personalizado
    def definir_tamanho_mapa(self, tipo):
        if tipo == "aleatorio" and self.tamanho_personalizado is not None:
            return self.tamanho_personalizado # Retorna tamanho personalizado caso mapa seja aleatório

        # Dicionário com tamanho fixo para os mapas predefinidos
        return {
            "pequeno": 5,
            "medio": 7,
            "grande": 8,
        }.get(tipo, 7) # Deixei 7 como default
    

    # Gera o mapa inicial e posições do agente e objetivo conforme o tipo de mapa
    def gerar_mapa_inicial(self):
        if self.tipo_mapa == "aleatorio":
            return gerar_mapa_aleatorio(tamanho=self.grid_size)
        elif self.tipo_mapa == "pequeno":
            return gerar_mapa_5x5()
        elif self.tipo_mapa == "medio":
            return gerar_mapa_7x7()
        elif self.tipo_mapa == "grande":
            return gerar_mapa_8x8()
        else:
            messagebox.showerror("Erro", "Tipo de mapa desconhecido")
            self.app.destroy()


    # Cria a interface gráfica com todos os frames, labels, botões e áreas de texto
    def criar_interface(self):

        # Container principal
        container = ctk.CTkFrame(self.app, fg_color="#1f1f1f")
        container.pack(fill="both", expand=True, padx=20, pady=20)


        # === Parte Direita ===
        # Área para mostrar listas de abertos, fechados e adjacentes 
        frame_direita = ctk.CTkFrame(container, fg_color="#2b2b2b", corner_radius=15)
        frame_direita.pack(side="right", fill="y", padx=10, pady=10)

        # Container vertical para empilhar as listas e os adjacentes
        listas_container = ctk.CTkFrame(frame_direita, fg_color="#2b2b2b")
        listas_container.pack(padx=10, pady=10, fill="y", expand=True)

        # Subcontainer com listas de abertos e fechados lado a lado
        listas_superiores = ctk.CTkFrame(listas_container, fg_color="#2b2b2b")
        listas_superiores.pack()

        # === Lista de Abertos ===
        frame_abertos = ctk.CTkFrame(listas_superiores, fg_color="#2b2b2b")
        frame_abertos.pack(side="left", padx=10)
        ctk.CTkLabel(
            frame_abertos, 
            text="🔓 LISTA DE ABERTOS:", 
            font=("Segoe UI", 18, "bold"),
            text_color="#ffffff"
        ).pack(pady=5)
        self.lista_abertos = ctk.CTkTextbox(
            frame_abertos,
            width=220,
            height=500,
            font=("Segoe UI", 16),
            text_color="#ffffff",
            fg_color="#3a3a3a"
        )        
        self.lista_abertos.pack()


        # === Lista de Fechados ===
        frame_fechados = ctk.CTkFrame(listas_superiores, fg_color="#2b2b2b")
        frame_fechados.pack(side="left", padx=10)
        ctk.CTkLabel(
            frame_fechados,
            text="🔒 LISTA DE FECHADOS",
            font=("Segoe UI", 18, "bold"),
            text_color="#ffffff"
        ).pack(pady=5)
        self.lista_fechados = ctk.CTkTextbox(
            frame_fechados,
            width=220,
            height=500,
            font=("Segoe UI", 16),
            text_color="#ffffff",
            fg_color="#3a3a3a"
        )
        self.lista_fechados.pack()


        # === LIsta de Adjacentes === (Horizontal abaixo dos dois lá de cima)
        frame_adjacentes = ctk.CTkFrame(listas_container, fg_color="#2b2b2b")
        frame_adjacentes.pack(pady=(20, 0)) # Espaço em cima
        ctk.CTkLabel(
            frame_adjacentes,
            text="📍 NÓS ABERTOS ADJACENTES DO ESTADO ATUAL:",
            font=("Segoe UI", 18, "bold"),
            text_color="#ffffff"
        ).pack(pady=5)

        self.lista_adjacentes = ctk.CTkTextbox(
            frame_adjacentes,
            width=470,
            height=150,
            font=("Segoe UI", 14),
            text_color="#ffffff",
            fg_color="#3a3a3a"
        )
        self.lista_adjacentes.pack()



        # === Parte Esquerda ===
        # Área que exibe o mapa e botões
        frame_esquerda = ctk.CTkFrame(container, fg_color="#2b2b2b", corner_radius=15)
        frame_esquerda.pack(side="left", fill="both", expand=True, padx=5, pady=10)

        # === Botão Voltar ===
        self.botao_voltar = ctk.CTkButton(
            frame_esquerda,
            text="←",
            width=30,
            height=40,
            font=("Segoe UI", 20, "bold"),
            fg_color="#3a3a3a",
            hover_color="#555555",
            corner_radius=50,
            command=self.voltar_tela_inicial
        )
        self.botao_voltar.place(x=20, y=20)

        # Subframe centralizado dentro do frame esquerdo
        sub_frame = ctk.CTkFrame(frame_esquerda, fg_color="#2b2b2b")
        sub_frame.pack(expand=True) # Centraliza

        # Grid / Mapa
        self.grid = ctk.CTkFrame(sub_frame, fg_color="#2b2b2b")
        self.grid.pack()

        # Cria uma matriz de labels que representam cada célula do mapa visualmente
        for i in range(self.grid_size):
            linha = []
            for j in range(self.grid_size):
                label = ctk.CTkLabel( 
                    self.grid, 
                    text="", 
                    width=80, 
                    height=80, 
                    fg_color="#e0e0e0", 
                    corner_radius=10
                )
                label.grid(row=i, column=j, padx=2, pady=2)
                linha.append(label)
            self.grid_widgets.append(linha)

        # Botão "Continuar" -> Avançar a simulação
        self.btn_continuar = ctk.CTkButton(
            sub_frame, 
            font=("Segoe UI", 16, "bold"),
            width=160,
            height=48,
            corner_radius=12,
            command=self.continuar
            )
        self.btn_continuar.pack(pady=20)

    
    # Fecha a janela atual e abre a tela inicial
    def voltar_tela_inicial(self):
        self.app.destroy() # Fecha a janela atual
        # Abre a tela inicial
        from interface.tela_inicial import iniciar_interface
        iniciar_interface()


    # Executa a próxima iteração do algoritmo A* e atualiza a interface
    def continuar(self):     
        # Se o estado atual é para mostrar o resultado, aí muda de tela
        # Só pra não ter que fazer outro botão
        if self.estado_botao == "mostrar_resultado":
            self.app.destroy()
            from interface.tela_resultado import TelaResultado
            TelaResultado(
                mapa_original=self.mapa_original, 
                mapa_com_caminho=self.mapa_com_caminho,
                caminho_final=self.caminho_final,
                texto_caminho_final=self.texto_caminho_final,
                texto_custo_total=self.texto_custo_total,
                texto_heuristica=self.texto_heuristica
            )
            return
        
        try:
            # Avança uma etapa do algoritmo A*
            resultado = next(self.iterator_a_star)

            if self.estado_botao == "iniciar":
                self.estado_botao = "continuar"
                self.atualizar_botao()

            # Caso tenha chegado ao estado final (objetivo alcançado ou falha)
            if resultado.get("estado_final"):
                if resultado.get("caminho_final"):

                    # Mostra o caminho encontrado
                    caminho = resultado["caminho_final"]
                    mapa_com_caminho = deepcopy(self.mapa_original)

                    for celula in caminho:
                        mapa_com_caminho[celula.x][celula.y].tipos.add("CAMINHO")
                    
                    self.caminho_final = caminho
                    self.mapa_com_caminho = mapa_com_caminho

                    # Atualiza a grade para mostrar o agente e nós fechados
                    self.atualizar_grid_com_mapa(self.mapa, agente=resultado.get("atual"), fechados=resultado.get("fechados", []))
                    self.atualizar_listas(resultado) # Atualiza a lista com o nó objetivo

                    # Salva textos informativos para exibir no resultado final
                    self.texto_caminho_final = resultado.get("caminho_encontrado_texto")
                    self.texto_custo_total = resultado.get("custo_total_texto")
                    self.texto_heuristica = resultado.get("heuristica_texto")

                    messagebox.showinfo("Busca Finalizada", "O agente encontrou o objetivo!")

                else:
                    self.caminho_final = []
                    messagebox.showinfo("Busca Finalizada", "Não foi possível encontrar um caminho.")

                # Muda o estado do botão para "Finalizado"
                self.estado_botao = "finalizar"
                self.atualizar_botao()
                return

            else:
                # Se ainda está rodando, atualiza o mapa e listas conforme o estado atual
                self.atualizar_grid_com_mapa(self.mapa, agente=resultado.get("atual"), fechados=resultado.get("fechados", []))
                self.atualizar_listas(resultado)

        except StopIteration:
            # Caso o iterador termine sem retorno final, mostra mensagem e finaliza
            messagebox.showinfo("Busca Concluída", "A busca foi encerrada.")
            self.estado_botao = "finalizar"
            self.atualizar_botao()

    # Atualiza visualmente a grade do mapa, mostrando agente, nós fechados e tipos de células com imagens
    def atualizar_grid_com_mapa(self, matriz, agente=None, fechados=None):
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                celula = matriz[i][j]

                # Se é a posição do agente secreto, mostra a imagem correspondente
                if agente and (i, j) == (agente.x, agente.y):
                    imagem = self.imagens.get(frozenset({"S"}))

                # Se está na lista de fechados, marca como visitado 
                elif fechados and any(n.x == i and n.y == j for n in fechados):
                    imagem = self.imagens.get(frozenset({"X"}))

                else:
                    tipos = frozenset(t.value if isinstance(t, TipoCelula) else t for t in celula.tipos)
                    imagem = self.imagens.get(tipos, self.imagens[frozenset()])

                widget = self.grid_widgets[i][j]
                widget.configure(image=imagem, text="")
                widget.image = imagem

    # Atualiza o texto do botão "Continuar" conforme o estado da simulação
    def atualizar_botao(self):
        if self.estado_botao == "iniciar":
            self.btn_continuar.configure(
                text="▶ INICIAR",
                fg_color="#2196F3",  # azul
                hover_color="#1e88e5"
            )
        elif self.estado_botao == "continuar":
            self.btn_continuar.configure(
                text="⏩ CONTINUAR",
                fg_color="#4CAF50",  # verde
                hover_color="#43a047"
            )
        elif self.estado_botao == "finalizar":
            self.btn_continuar.configure(
                text="📊 VER RESULTADO",
                fg_color="#FFC107",  # amarelo
                hover_color="#FFB300",
            )
            self.estado_botao = "mostrar_resultado"


    # Atualiza as listas de abertos, fechados e adjacentes na interface
    def atualizar_listas(self, resultado):
        abertos = resultado.get("abertos", []) # Lista de tuplas (Nó, F(n))
        fechados = resultado.get("fechados", [])
        # f_dict = resultado.get("f_dict", {})  # Pega o f(n) dos resultados
        adjacentes = resultado.get("adjacentes", [])
        heuristicas_texto = "\n".join(resultado.get("heuristicas_adjacentes", []))

        # Formata os textos
        texto_abertos = "\n".join(f"({n.x}, {n.y})  |  F(n) = {f:.1f}" for n , f in abertos)
        texto_fechados = "\n".join(f"({n.x}, {n.y})" for n in fechados)
        texto_adjacentes = "\n".join(f"({x}, {y}) --→ h(n) = {h:.1f}" for x, y, h in sorted(adjacentes, key=lambda x: x[2]))

        # Atualiza os campos na interface
        self.lista_abertos.delete("1.0", "end")
        self.lista_abertos.insert("1.0", texto_abertos)

        self.lista_fechados.delete("1.0", "end")
        self.lista_fechados.insert("1.0", texto_fechados)

        self.lista_adjacentes.delete("1.0", "end")
        self.lista_adjacentes.insert("1.0", texto_adjacentes)
        self.lista_adjacentes.insert("end", "\n\n" + heuristicas_texto)

