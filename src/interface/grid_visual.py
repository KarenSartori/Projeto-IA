import customtkinter as ctk
from PIL import Image
import os

class GridVisual:
    def __init__(self, parent_frame, tamanho):
        self.frame = parent_frame
        self.tamanho = tamanho
        self.celulas = []
        self.imagens = self.carregar_imagens()

        self.construir_grid()

    def carregar_imagens(self):
        """Carrega todas as imagens da pasta /interface/imagens e cria um dicionário."""
        imagem_dir = "interface/imagens"
        imagens = {}
        for nome_arquivo in os.listdir(imagem_dir):
            if nome_arquivo.endswith(".png"):
                chave = nome_arquivo.replace(".png", "")  # exemplo: guarda_camera
                caminho = os.path.join(imagem_dir, nome_arquivo)
                imagens[chave] = ctk.CTkImage(Image.open(caminho), size=(45, 45))
        return imagens

    def construir_grid(self):
        """Cria o grid inicial com células vazias."""
        for i in range(self.tamanho):
            linha = []
            for j in range(self.tamanho):
                label = ctk.CTkLabel(self.frame, text="", image=self.imagens["vazio"])
                label.grid(row=i, column=j, padx=1, pady=1)
                linha.append(label)
            self.celulas.append(linha)

    def atualizar_celula(self, i, j, tipo):
        """Atualiza uma única célula com base no tipo (string: ex 'guarda_camera')."""
        tipo_formatado = tipo.lower()
        if tipo_formatado in self.imagens:
            self.celulas[i][j].configure(image=self.imagens[tipo_formatado])
        else:
            self.celulas[i][j].configure(image=self.imagens.get("vazio"))

    def atualizar_mapa(self, matriz):
        """
        Espera uma matriz de strings (ex: [["vazio", "guarda_camera", ...], [...]]),
        e atualiza todo o grid.
        """
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                self.atualizar_celula(i, j, matriz[i][j])
