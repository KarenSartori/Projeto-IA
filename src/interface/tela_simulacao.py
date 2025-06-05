import customtkinter as ctk
from tkinter import messagebox

class Simulacao:
    def __init__(self, tipo_mapa):
        self.tipo_mapa = tipo_mapa
        self.app = ctk.CTk()
        self.app.title(f"Simulação A* - Mapa{tipo_mapa.capitalize()}")
        self.app.geometry("1000x600")
        self.app.resizable(False, False)
        self.centralizar_janela()

        self.grid_size = self.definir_tamanho_mapa(tipo_mapa)
        self.grid_widgets = []

        self.criar_interface() # Chama para criar o visual
        self.app.mainloop() # Inicia a interface

    def centralizar_janela(self):
        self.app.update_idletasks()
        x = (self.app.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.app.winfo_screenheight() // 2) - (600 // 2)
        self.app.geometry(f"{1000}x{600}+{x}+{y}")        

    def definir_tamanho_mapa(self, tipo):
        return {
            "pequeno": 5,
            "medio": 7,
            "grande": 8,
            "aleatorio": 7  
        }.get(tipo, 7)

    def criar_interface(self):
        container = ctk.CTkFrame(self.app, fg_color="#333333")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        # Parte esquerda que tem o grid e botão
        esquerda = ctk.CTkFrame(container, fg_color="#333333")
        esquerda.pack(side="right", padx=40, pady=10)

        self.grid = ctk.CTkFrame(esquerda, fg_color="#333333")
        self.grid.pack()

        for i in range(self.grid_size):
            linha = []
            for j in range(self.grid_size):
                cell = ctk.CTkLabel(self.grid, text="", width=45, height=45, fg_color="white", corner_radius=4)
                cell.grid(row=i, column=j, padx=1, pady=1)
                linha.append(cell)
            self.grid_widgets.append(linha)

        self.btn_continuar = ctk.CTkButton(
            esquerda, 
            text="CONTINUAR", 
            fg_color="#4CAF50", 
            hover_color="#45A049",
            width=130,
            height=45,
            font=("Arial", 16, "bold"),
            command=self.continuar
            )
        self.btn_continuar.pack(pady=15)

        # Parte direita: listas
        direita = ctk.CTkFrame(container, fg_color="#333333")
        direita.pack(side="right", padx=30, pady=10)

        # Container que tem as duas listas
        listas_container = ctk.CTkFrame(direita, fg_color="#333333")
        listas_container.pack()

        frame_abertos = ctk.CTkFrame(listas_container, fg_color="#333333")
        frame_abertos.pack(side="left", padx=5)
        ctk.CTkLabel(frame_abertos, text="LISTA DE ABERTOS:", font=("Arial", 14, "bold")).pack()
        self.lista_abertos = ctk.CTkTextbox(frame_abertos, width=220, height=500, font=("Arial", 14))
        self.lista_abertos.pack()

        frame_fechados = ctk.CTkFrame(listas_container, fg_color="#333333")
        frame_fechados.pack(side="left", padx=5)
        ctk.CTkLabel(frame_fechados, text="LISTA DE FECHADOS:", font=("Arial", 14, "bold")).pack()
        self.lista_fechados = ctk.CTkTextbox(frame_fechados, width=220, height=500, font=("Arial", 14))
        self.lista_fechados.pack()

    def continuar(self):
        messagebox.showinfo("Ação", "Executar próxima iteração do A*")
      