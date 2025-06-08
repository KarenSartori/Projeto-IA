from PIL import Image  
import customtkinter as ctk
from interface.tela_simulacao import Simulacao

def iniciar_interface():
    # Define a aparência e o tema da interface
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    
    # Criação da janela principal
    app = ctk.CTk()
    app.geometry("900x600")
    app.title("Agente Secreto com Inteligência Artificial")
    app.resizable(False, False)

    # Centralizar a Janela
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = int( (screen_width / 2) - (900 / 2) )
    y = int( (screen_height / 2) - (600 / 2) )
    app.geometry(f"900x600+{x}+{y}")

    # Frame principal
    frame = ctk.CTkFrame(app, fg_color="#000000")
    frame.pack(fill="both", expand=True)

    # Imagem de fundo
    pil_image = Image.open("interface/imagens/capa.png")
    img = ctk.CTkImage(light_image=pil_image, size=(900, 420))
    label_img = ctk.CTkLabel(frame, image=img, text="")
    label_img.pack(pady=10)

    # Botões pra seleção de mapa
    frame_botoes = ctk.CTkFrame(
        frame, 
        fg_color="#1e1e1e",
        corner_radius=15,
        border_width=2,
        border_color="#000000"
        )
    frame_botoes.pack(pady=10, padx=10)

    # Função para abrir a tela de simulação, ocultando a tela inicial
    def abrir_simulacao(tipo):
        app.destroy()
        Simulacao(tipo)


    # Lista dos botões dos mapas
    botoes = [
        ("Mapa Pequeno (5x5)", "pequeno"),
        ("Mapa Médio (7x7)", "medio"),
        ("Mapa Grande (8x8)", "grande"),
        ("Mapa Aleatório (7x7)", "aleatorio")
    ]

    # Criando e exibindo os botões de forma estilizada
    for texto, tipo in botoes:
        btn = ctk.CTkButton(
            frame_botoes, 
            text=texto, 
            command=lambda t=tipo: abrir_simulacao(t), # o próprio python tá com errinho aqui...
            width=180,
            height=55,
            font=("Segoe UI", 16, "bold"),
            text_color="#ffffff",
            fg_color="#2ecc71",
            hover_color="#27ae60",
            corner_radius=12
            )
        btn.pack(side="left", padx=10, pady=5)

    app.mainloop()
