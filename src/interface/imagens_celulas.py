import os
from PIL import Image
import customtkinter as ctk
from mapa.celula import TipoCelula

CAMINHO_IMAGENS = "interface/imagens/"
TAMANHO_IMAGEM = (60, 60)

# Mapeia combinações de tipos para nomes de imagem
TIPOS_PARA_NOME = {
    frozenset(): "vazio",
    frozenset({"S"}): "agente",
    frozenset({TipoCelula.JOIA.value}): "joia",
    frozenset({TipoCelula.GUARDA.value}): "guarda",
    frozenset({TipoCelula.CAMERA.value}): "camera",
    frozenset({TipoCelula.PORTA_TRANCADA.value}): "porta",
    frozenset({TipoCelula.ARMADILHA.value}): "armadilha",
    frozenset({"X"}) : "visitado",

    # Não sei se tem a possibilidade de vir trocado, mas coloquei por precaução
    frozenset({TipoCelula.GUARDA.value, TipoCelula.ARMADILHA.value}): "guarda_armadilha",
    frozenset({TipoCelula.ARMADILHA.value, TipoCelula.GUARDA.value}): "guarda_armadilha",

    frozenset({TipoCelula.GUARDA.value, TipoCelula.CAMERA.value}): "guarda_camera",
    frozenset({TipoCelula.CAMERA.value, TipoCelula.GUARDA.value}): "guarda_camera",
    
    frozenset({TipoCelula.GUARDA.value, TipoCelula.PORTA_TRANCADA.value}): "guarda_porta",
    frozenset({TipoCelula.PORTA_TRANCADA.value, TipoCelula.GUARDA.value}): "guarda_porta",
    
    frozenset({TipoCelula.CAMERA.value, TipoCelula.ARMADILHA.value}): "camera_armadilha",
    frozenset({TipoCelula.ARMADILHA.value, TipoCelula.CAMERA.value}): "camera_armadilha",
    
    frozenset({TipoCelula.CAMERA.value, TipoCelula.PORTA_TRANCADA.value}): "camera_porta",
    frozenset({TipoCelula.PORTA_TRANCADA.value, TipoCelula.CAMERA.value}): "camera_porta",
    
    frozenset({TipoCelula.PORTA_TRANCADA.value, TipoCelula.ARMADILHA.value}): "porta_armadilha",
    frozenset({TipoCelula.ARMADILHA.value, TipoCelula.PORTA_TRANCADA.value}): "porta_armadilha",

}

def carregar_imagens():
    imagens = {}
    for tipos, nome_arquivo in TIPOS_PARA_NOME.items():
        # Pega o path da imagem
        caminho = os.path.join(CAMINHO_IMAGENS, f"{nome_arquivo}.png")
        imagem_pil = Image.open(caminho).resize(TAMANHO_IMAGEM)
        imagens[tipos] = ctk.CTkImage(dark_image=imagem_pil, size=TAMANHO_IMAGEM)
    return imagens
