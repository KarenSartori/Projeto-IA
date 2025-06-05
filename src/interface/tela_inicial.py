# interface/tela_inicial.py
from PIL import Image  
import customtkinter as ctk
from interface.tela_simulacao import Simulacao

def iniciar_interface():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    
    app = ctk.CTk()
    app.geometry("900x600")
    app.title("Agente Secreto com Inteligência Artificial")
    app.resizable(False, False)

    # Centralizar a Janela
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = int( (screen_width / 2) - (750 / 2) )
    y = int( (screen_height / 2) - (650 / 2) )
    app.geometry(f"900x600+{x}+{y}")

    # Frame principal
    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(fill="both", expand=True)

    # Imagem de fundo
    pil_image = Image.open("interface/imagens/capa.png")
    img = ctk.CTkImage(light_image=pil_image, size=(900, 420))
    label_img = ctk.CTkLabel(frame, image=img, text="")
    label_img.pack(pady=10)

    # Botões pra seleção de mapa
    frame_botoes = ctk.CTkFrame(frame, fg_color=frame.cget("fg_color"))
    frame_botoes.pack(pady=10)

    def abrir_simulacao(tipo):
        app.withdraw()
        Simulacao(tipo)
        app.deiconify()

    botoes = [
        ("Mapa Pequeno (5x5)", "pequeno"),
        ("Mapa Médio (7x7)", "medio"),
        ("Mapa Grande (8x8)", "grande"),
        ("Mapa Aleatório (7x7)", "aleatorio")
    ]

    

    for texto, tipo in botoes:
        btn = ctk.CTkButton(
            frame_botoes, 
            text=texto, 
            command=lambda t=tipo: abrir_simulacao(t), # o próprio python tá com errinho aqui...
            width=180,
            height=55,
            font=("Arial", 18)
            )
        btn.pack(side="left", padx=15)

    app.mainloop()
