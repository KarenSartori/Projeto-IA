import customtkinter as ctk
from interface.imagens_celulas import carregar_imagens

class TelaResultado:
    def __init__(self, mapa_original, mapa_com_caminho, caminho_final, texto_caminho_final, texto_custo_total, texto_heuristica):
        self.app = ctk.CTk()
        self.app.title("Resultado da Busca A*")
        self.app.after(100, lambda: self.app.state("zoomed"))
        self.app.resizable(False, False)

        self.grid_size = len(mapa_original)  # Define o tamanho da grade (matriz) baseada no mapa original
        self.grid_widgets_esquerda = []  # Guarda os widgets (labels) do grid à esquerda (mapa original)
        self.grid_widgets_direita = []   # Guarda os widgets do grid à direita (mapa com caminho)
        self.imagens = carregar_imagens()  # Carrega as imagens das células (agente, obstáculo, caminho, etc.)

        # Guarda as informações do caminho final e textos que serão exibidos na interface
        self.caminho_final = caminho_final
        self.texto_caminho = texto_caminho_final
        self.texto_custo = texto_custo_total
        self.texto_heuristica = texto_heuristica

        self.criar_interface()

        self.atualizar_grid(self.grid_widgets_esquerda, mapa_original)
        self.atualizar_grid(self.grid_widgets_direita, mapa_com_caminho, mapa_com_caminho=True)

        self.app.mainloop()

    def criar_interface(self):
        # Cria o container principal da janela, fundo escuro
        container_principal = ctk.CTkFrame(self.app, fg_color="#1f1f1f")
        container_principal.pack(fill="both", expand=True, padx=20, pady=20)

        # Container superior que terá os dois grids lado a lado
        container_superior = ctk.CTkFrame(container_principal, fg_color="#1f1f1f")
        container_superior.pack(side="top", fill="both", expand=True)

        # Frame à esquerda: exibirá o mapa original
        frame_esquerda = ctk.CTkFrame(container_superior, fg_color="#2b2b2b", corner_radius=15)
        frame_esquerda.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Frame à direita: exibirá o mapa com o caminho traçado
        frame_direita = ctk.CTkFrame(container_superior, fg_color="#2b2b2b", corner_radius=15)
        frame_direita.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Labels título acima dos grids, com ícones e fonte estilizada
        ctk.CTkLabel(frame_esquerda, text="🔍 MAPA INICIAL", font=("Segoe UI", 20, "bold"), text_color="#ffffff").pack(pady=10)
        ctk.CTkLabel(frame_direita, text="🌟 CAMINHO FINAL", font=("Segoe UI", 20, "bold"), text_color="#ffffff").pack(pady=10)

        # Frame que terá a grade (matriz) do mapa original
        self.grid_esquerda = ctk.CTkFrame(frame_esquerda, fg_color="#2b2b2b")
        self.grid_esquerda.pack(expand=True)

        # Frame que terá a grade do mapa com caminho final
        self.grid_direita = ctk.CTkFrame(frame_direita, fg_color="#2b2b2b")
        self.grid_direita.pack(expand=True)

        # Para cada linha do grid, cria uma lista de labels (um para cada célula),
        # tanto para o lado esquerdo quanto para o direito e armazena nas listas correspondentes
        for i in range(self.grid_size):
            linha_e = []
            linha_d = []
            for j in range(self.grid_size):
                label_e = ctk.CTkLabel(self.grid_esquerda, text="", width=67, height=67, fg_color="#e0e0e0", corner_radius=10)
                label_e.grid(row=i, column=j, padx=2, pady=2)
                linha_e.append(label_e)

                label_d = ctk.CTkLabel(self.grid_direita, text="", width=67, height=67, fg_color="#e0e0e0", corner_radius=10)
                label_d.grid(row=i, column=j, padx=2, pady=2)
                linha_d.append(label_d)

            self.grid_widgets_esquerda.append(linha_e)
            self.grid_widgets_direita.append(linha_d)

        # Barra inferior para exibir informações do caminho e botão para finalizar
        barra_inferior = ctk.CTkFrame(container_principal, fg_color="#292929")
        barra_inferior.pack(side="bottom", fill="x", padx=10, pady=10)

        # Label que exibe texto informativo sobre o caminho encontrado (ou não)
        info_texto = self.gerar_texto_info()
        self.label_info = ctk.CTkLabel(
            barra_inferior, 
            text=info_texto, 
            text_color="#ffffff", 
            anchor="w", 
            font=("Segoe UI", 14),
            wraplength=1000, # Quebra texto para não sair da tela
            justify="left"
        )
        self.label_info.pack(side="left", padx=15, pady=10, expand=True)

        # Botão para fechar a janela e finalizar visualização
        botao_finalizar = ctk.CTkButton(
            barra_inferior, 
            text="🆗 Finalizar",
            font=("Segoe UI", 16, "bold"),
            fg_color="#4CAF25",
            width=120,
            height=50,
            corner_radius=10, 
            command=self.app.destroy
        )
        botao_finalizar.pack(side="right", padx=20, pady=10)
    
    def gerar_texto_info(self):
        if not self.caminho_final:
            return "Nenhum caminho foi encontrado..."
        
        # Retorna o texto formatado com informações do caminho, custo e heurística
        # que foram recebidos na inicialização 
        return f"{self.texto_caminho}\n{self.texto_custo} | {self.texto_heuristica}"



    def atualizar_grid(self, grid_widgets, mapa, mapa_com_caminho=False):
        # Atualiza a grade de labels com as imagens correspondentes às células do mapa
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                celula = mapa[i][j]

                # Obtém os tipos da célula, que podem ser enum ou string
                tipos_brutos = celula.tipos

                # Converte os tipos para string, acessando o atributo .value se for enum
                tipos = set(
                    t.value if hasattr(t, 'value') else t
                    for t in tipos_brutos
                )

                # Se o grid for o mapa com caminho, mostra a imagem especial para células do caminho
                if mapa_com_caminho and "CAMINHO" in tipos:
                    imagem = self.imagens["caminho"]
                else:
                    tipos_frozen = frozenset(tipos)
                    imagem = self.imagens.get(tipos_frozen, self.imagens[frozenset()])

                # Atualiza o label da célula com a imagem selecionada e limpa o texto
                grid_widgets[i][j].configure(image=imagem, text="")
                grid_widgets[i][j].image = imagem


