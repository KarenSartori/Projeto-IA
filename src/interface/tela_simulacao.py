import customtkinter as ctk
from tkinter import messagebox
from interface.imagens_celulas import carregar_imagens
from mapa.mapa5x5 import gerar_mapa_5x5
from mapa.mapa7x7 import gerar_mapa_7x7
from mapa.mapa8x8 import gerar_mapa_8x8
from mapa.mapa7x7_aleatorio import gerar_mapa_aleatorio
from buscador.buscador import a_star

class Simulacao:
    def __init__(self, tipo_mapa):
        self.tipo_mapa = tipo_mapa
        self.app = ctk.CTk()
        self.app.title(f"Simulação A* - Mapa{tipo_mapa.capitalize()}")
        self.app.geometry("1000x600")
        # self.app.resizable(False, False) # Mudar para colocar a tela inteira e aumantar o tamanho da matriz porque está meio pequena
        self.centralizar_janela()

        self.grid_size = self.definir_tamanho_mapa(tipo_mapa)
        self.grid_widgets = []
        self.imagens = carregar_imagens() # Carrega todas as imagens

        self.criar_interface() # Chama para criar o visual
        
        # Cria o mapa de acrodo com o tipo selecionado 
        self.inicio, self.objetivo, self.mapa = self.gerar_mapa_inicial()
        self.atualizar_grid_com_mapa(self.mapa, self.inicio)

        self.app.mainloop() 





    # Define o tamanho do grid com base no tipo de mapa selecionado
    def definir_tamanho_mapa(self, tipo):
        return {
            "pequeno": 5,
            "medio": 7,
            "grande": 8,
            "aleatorio": 7  
        }.get(tipo, 7) # Deixei 7 como default
    
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






    # Centraliza a janela principal na tela do usuário
    def centralizar_janela(self):
        self.app.update_idletasks()
        x = (self.app.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.app.winfo_screenheight() // 2) - (600 // 2)
        self.app.geometry(f"{1000}x{600}+{x}+{y}")        


    # Constrói todos os componentes visuais da interface
    def criar_interface(self):

        # Container principal
        container = ctk.CTkFrame(self.app, fg_color="#1f1f1f")
        container.pack(fill="both", expand=True, padx=20, pady=20)



        # === Parte Direita ===
        frame_direita = ctk.CTkFrame(container, fg_color="#2b2b2b", corner_radius=15)
        frame_direita.pack(side="right", fill="y", padx=10, pady=10)

        # Container que tem as duas listas
        listas_container = ctk.CTkFrame(frame_direita, fg_color="#2b2b2b")
        listas_container.pack(padx=10)


        # === Lista de Abertos ===
        frame_abertos = ctk.CTkFrame(listas_container, fg_color="#2b2b2b")
        frame_abertos.pack(side="left", padx=10)
        ctk.CTkLabel(
            frame_abertos, 
            text="🔓 LISTA DE ABERTOS:", 
            font=("Segoe UI", 15, "bold"),
            text_color="#ffffff"
        ).pack(pady=5)
        self.lista_abertos = ctk.CTkTextbox(
            frame_abertos,
            width=220,
            height=500,
            font=("Segoe UI", 14),
            text_color="#ffffff",
            fg_color="#3a3a3a"
        )        
        self.lista_abertos.pack()


        # === Lista de Fechados ===
        frame_fechados = ctk.CTkFrame(listas_container, fg_color="#2b2b2b")
        frame_fechados.pack(side="left", padx=10)
        ctk.CTkLabel(
            frame_fechados,
            text="🔒 LISTA DE FECHADOS",
            font=("Segoe UI", 15, "bold"),
            text_color="#ffffff"
        ).pack(pady=5)
        self.lista_fechados = ctk.CTkTextbox(
            frame_fechados,
            width=220,
            height=500,
            font=("Segoe UI", 14),
            text_color="#ffffff",
            fg_color="#3a3a3a"
        )
        self.lista_fechados.pack()



        # === Parte Esquerda ===
        frame_esquerda = ctk.CTkFrame(container, fg_color="#2b2b2b", corner_radius=15)
        frame_esquerda.pack(side="left", fill="both", expand=True, padx=5, pady=10)

        # Subframe centralizado dentro do frame esquerdo
        sub_frame = ctk.CTkFrame(frame_esquerda, fg_color="#2b2b2b")
        sub_frame.place(relx=0.5, rely=0.45, anchor="center") # Centraliza essa droga

        # Grid / Mapa
        self.grid = ctk.CTkFrame(sub_frame, fg_color="#2b2b2b")
        self.grid.pack()

        # Essa parte do código que vê as células 
        for i in range(self.grid_size):
            linha = []
            for j in range(self.grid_size):
                label = ctk.CTkLabel( 
                    self.grid, 
                    text="", 
                    width=45, 
                    height=45, 
                    fg_color="#e0e0e0", 
                    corner_radius=6
                )
                label.grid(row=i, column=j, padx=2, pady=2)
                linha.append(label)
            self.grid_widgets.append(linha)

        # Botão "Continuar"
        self.btn_continuar = ctk.CTkButton(
            sub_frame, 
            text="▶ CONTINUAR", 
            fg_color="#4CAF50", 
            hover_color="#43a047",
            text_color="#ffffff",
            font=("Segoe UI", 16, "bold"),
            width=160,
            height=48,
            corner_radius=12,
            command=self.continuar
            )
        self.btn_continuar.pack(pady=20)

        

    def continuar(self):
        ''' Executar a próxima iteração da simulação '''
        messagebox.showinfo("Ação", "Executar próxima iteração do A*")


    def atualizar_grid_com_mapa(self, matriz, agente=None):
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                celula = matriz[i][j]

                # Se é a posição do agente secreto, mostra a imagem correspondente
                if agente and (i, j) == (agente.x, agente.y):
                    imagem = self.imagens.get(frozenset({"S"}))
                else:
                    tipos = frozenset(t.value for t in celula.tipos)
                    imagem = self.imagens.get(tipos, self.imagens[frozenset()])

                widget = self.grid_widgets[i][j]
                widget.configure(image=imagem, text="") # Deixa o texto null e adiciona a Imagem
                widget.image = imagem