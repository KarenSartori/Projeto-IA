import customtkinter as ctk
from tkinter import messagebox
from interface.imagens_celulas import carregar_imagens
from mapa.celula import TipoCelula
from mapa.mapa5x5 import gerar_mapa_5x5
from mapa.mapa7x7 import gerar_mapa_7x7
from mapa.mapa8x8 import gerar_mapa_8x8
from mapa.mapa7x7_aleatorio import gerar_mapa_aleatorio
from buscador.buscador import a_star_iterativo

class Simulacao:
    def __init__(self, tipo_mapa):
        self.tipo_mapa = tipo_mapa
        self.app = ctk.CTk()
        self.app.title(f"Simulação A* - Mapa{tipo_mapa.capitalize()}")
        self.app.after(100, lambda: self.app.state("zoomed")) # Garante que a tela em zoom após carregar
        self.app.resizable(False, False)

        self.grid_size = self.definir_tamanho_mapa(tipo_mapa)
        self.grid_widgets = []
        self.imagens = carregar_imagens() # Carrega todas as imagens

        self.criar_interface() # Chama para criar o visual
        
        # Cria o mapa de acrodo com o tipo selecionado 
        self.inicio, self.objetivo, self.mapa = self.gerar_mapa_inicial()
        # Inicia o iterator A*
        self.iterator_a_star = a_star_iterativo(self.inicio, self.objetivo, self.mapa)

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
        frame_fechados = ctk.CTkFrame(listas_container, fg_color="#2b2b2b")
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



        # === Parte Esquerda ===
        frame_esquerda = ctk.CTkFrame(container, fg_color="#2b2b2b", corner_radius=15)
        frame_esquerda.pack(side="left", fill="both", expand=True, padx=5, pady=10)

        # Subframe centralizado dentro do frame esquerdo
        sub_frame = ctk.CTkFrame(frame_esquerda, fg_color="#2b2b2b")
        sub_frame.pack(expand=True) # Centraliza essa droga

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
                    width=80, 
                    height=80, 
                    fg_color="#e0e0e0", 
                    corner_radius=10
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
        try:
            resultado = next(self.iterator_a_star)

            if resultado.get("estado_final"):
                if resultado.get("caminho_final"):
                    # Mostra o caminho encontrado
                    for celula in resultado["caminho_final"]:
                        celula.tipos.add("CAMINHO")
                    self.atualizar_grid_com_mapa(self.mapa, agente=resultado.get("atual"))
                    messagebox.showinfo("Busca Finalizada", "O agente encontrou o objetivo!")
                else:
                    messagebox.showinfo("Busca Finalizada", "Não foi possível encontrar um caminho.")

            else:
                self.atualizar_grid_com_mapa(self.mapa, agente=resultado.get("atual"))
                self.atualizar_listas(resultado)

        except StopIteration:
            messagebox.showinfo("Busca Concluída", "A busca foi encerrada.")


    def atualizar_grid_com_mapa(self, matriz, agente=None):
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                celula = matriz[i][j]

                # Se é a posição do agente secreto, mostra a imagem correspondente
                if agente and (i, j) == (agente.x, agente.y):
                    imagem = self.imagens.get(frozenset({"S"}))
                else:
                    tipos = frozenset(t.value if isinstance(t, TipoCelula) else t for t in celula.tipos)
                    imagem = self.imagens.get(tipos, self.imagens[frozenset()])

                widget = self.grid_widgets[i][j]
                widget.configure(image=imagem, text="") # Deixa o texto null e adiciona a Imagem
                widget.image = imagem


    def atualizar_listas(self, resultado):
        abertos = resultado.get("abertos", [])
        fechados = resultado.get("fechados", [])
        f_dict = resultado.get("f_dict", {})  # Pega o f(n) dos resultados

        # Formata texto para mostrar os abertos e os fechados
        texto_abertos = "\n".join(
            f"({n.x}, {n.y}) |  F(n) = {f_dict[n]:.1f}" for n in abertos if n in f_dict
        )
        texto_fechados = "\n".join(f"({n.x}, {n.y})" for n in fechados)

        self.lista_abertos.delete("1.0", "end")
        self.lista_abertos.insert("1.0", texto_abertos)

        self.lista_fechados.delete("1.0", "end")
        self.lista_fechados.insert("1.0", texto_fechados)
