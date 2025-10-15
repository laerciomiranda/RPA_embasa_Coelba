import json
import os
from datetime import datetime
import base64
 
class File:
    def __init__(self):
        self.caminho = ".\\files\\"
    
    def criar_pasta(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        
    def criar_json(self, pasta, nome_arquivo, conteudo):
        path = self.caminho + pasta
        self.criar_pasta(path)
        hoje = datetime.today()
        data_formatada = hoje.strftime("%d%m%Y")
        caminho_completo = os.path.join(path, f"{nome_arquivo}_{data_formatada}.json")
        with open(caminho_completo, "a", encoding="utf-8") as file:
            json.dump(conteudo.__dict__, file, indent=4, ensure_ascii=False)
     
    def gerar_arquivo(self, pasta, file, conteudo):
        path = self.caminho + pasta
        self.criar_pasta(path)
        hoje = datetime.today()
        data_formatada = hoje.strftime("%d%m%Y")
        caminho_completo = os.path.join(path, f"{file}_{data_formatada}.txt")
        
        with open(caminho_completo, "a", encoding="utf-8") as log_file:
            log_file.write(f"{conteudo}\n")
            
    def cliente_baixado(self, pasta, file, conteudo):
        path = self.caminho + pasta
        self.criar_pasta(path)
        hoje = datetime.today()
        data_formatada = hoje.strftime("%d%m%Y")
        caminho_completo = os.path.join(path, f"{file}_{data_formatada}.txt")
        if os.path.exists(caminho_completo) == False:
            open(caminho_completo, "w").close()

        with open(f"{caminho_completo}", "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                print("aqui")
                if conteudo in linha.strip():
                    return True
        return False
        
    def imagem_para_base64(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, "rb") as imagem:
                imagem_base64 = base64.b64encode(imagem.read()).decode('utf-8')
                return imagem_base64
        except Exception as e:
            print("Erro ao converter imagem:", e)
            return None
