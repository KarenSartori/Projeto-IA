import os
from PIL import Image, ImageTk

CAMINHO_IMAGENS = "interface/imagens/"
TAMANHO_IMAGEM = (45, 45)

# Mapeia combinações de tipos para nomes de imagem
TIPOS_PARA_NOME = {
    frozenset(): "vazio",
    frozenset({"S"}): "agente",
    frozenset({"J"}): "joia",
    frozenset({"G"}): "guarda",
    frozenset({"C"}): "camera",
    frozenset({"P"}): "porta",
    frozenset({"A"}): "armadilha",
    frozenset({"G", "A"}): "guarda_armadilha",
    frozenset({"G", "C"}): "guarda_camera",
    frozenset({"G", "P"}): "guarda_porta",
    frozenset({"C", "A"}): "camera_armadilha",
    frozenset({"C", "P"}): "camera_porta",
    frozenset({"P", "A"}): "porta_armadilha",
}

def carregar_imagens():
    imagens = {}
    for tipos, nome_arquivo in TIPOS_PARA_NOME.items():
        # Pega o path da imagem
        caminho = os.path.join(CAMINHO_IMAGENS, f"{nome_arquivo}.png")
        imagem_pil = Image.open(caminho).resize(TAMANHO_IMAGEM)
        imagens[tipos] = ImageTk.PhotoImage(imagem_pil)
    return imagens

def obter_imagem_para_celula(celula, imagens):
    tipos = frozenset(t.value for t in celula.tipos)
    return imagens.get(tipos, imagens[frozenset()])  # padrão: vazio
