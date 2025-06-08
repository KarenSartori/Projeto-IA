import customtkinter as ctk
from interface.imagens_celulas import carregar_imagens

class TelaResultado:
    def __init__(self, mapa_original, mapa_com_caminho):
        self.app = ctk.CTk()
        self.app.title("Resultado da Busca A*")
        self.app.after(100, lambda: self.app.state("zoomed"))
        self.app.resizable(False, False)

        self.grid_size = len(mapa_original)
        self.grid_widgets_esquerda = []
        self.grid_widgets_direita = []
        self.imagens = carregar_imagens()

        self.criar_interface()

        self.atualizar_grid(self.grid_widgets_esquerda, mapa_original)
        self.atualizar_grid(self.grid_widgets_direita, mapa_com_caminho, mapa_com_caminho=True)


        self.app.mainloop()

    def criar_interface(self):
        container_principal = ctk.CTkFrame(self.app, fg_color="#1f1f1f")
        container_principal.pack(fill="both", expand=True, padx=20, pady=20)

        frame_esquerda = ctk.CTkFrame(container_principal, fg_color="#2b2b2b", corner_radius=15)
        frame_esquerda.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_direita = ctk.CTkFrame(container_principal, fg_color="#2b2b2b", corner_radius=15)
        frame_direita.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame_esquerda, text="🔍 MAPA INICIAL", font=("Segoe UI", 20, "bold"), text_color="#ffffff").pack(pady=10)
        ctk.CTkLabel(frame_direita, text="🌟 CAMINHO FINAL", font=("Segoe UI", 20, "bold"), text_color="#ffffff").pack(pady=10)

        self.grid_esquerda = ctk.CTkFrame(frame_esquerda, fg_color="#2b2b2b")
        self.grid_esquerda.pack(expand=True)

        self.grid_direita = ctk.CTkFrame(frame_direita, fg_color="#2b2b2b")
        self.grid_direita.pack(expand=True)

        for i in range(self.grid_size):
            linha_e = []
            linha_d = []
            for j in range(self.grid_size):
                label_e = ctk.CTkLabel(self.grid_esquerda, text="", width=80, height=80, fg_color="#e0e0e0", corner_radius=10)
                label_e.grid(row=i, column=j, padx=2, pady=2)
                linha_e.append(label_e)

                label_d = ctk.CTkLabel(self.grid_direita, text="", width=80, height=80, fg_color="#e0e0e0", corner_radius=10)
                label_d.grid(row=i, column=j, padx=2, pady=2)
                linha_d.append(label_d)

            self.grid_widgets_esquerda.append(linha_e)
            self.grid_widgets_direita.append(linha_d)

    def atualizar_grid(self, grid_widgets, mapa, mapa_com_caminho=False):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                celula = mapa[i][j]

                # Obtém os tipos da célula
                tipos_brutos = celula.tipos

                # Converte os tipos para valores string
                tipos = set(
                    t.value if hasattr(t, 'value') else t
                    for t in tipos_brutos
                )

                # Se for o mapa com caminho e a célula tiver '*', mostra o caminho
                if mapa_com_caminho and "*" in tipos:
                    imagem = self.imagens["caminho"]
                else:
                    tipos_frozen = frozenset(tipos)
                    imagem = self.imagens.get(tipos_frozen, self.imagens[frozenset()])

                grid_widgets[i][j].configure(image=imagem, text="")
                grid_widgets[i][j].image = imagem


