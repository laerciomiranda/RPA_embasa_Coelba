from src.services.files import File
from datetime import datetime

class Log:
    def __init__(self):
        self.file = File()
        
    def iniciar(self, fileName, empresa):
        self.file.gerar_arquivo(f"Log", fileName, f"----Iniciando Empresa: {empresa} - {datetime.today()} -----")
        self.file.gerar_arquivo(f"Log", fileName, "-------------------------------------------------------------------") 
    
    def finalizar(self, fileName, empresa):
        self.file.gerar_arquivo(f"Log", fileName, "-------------------------------------------------------------------") 
        self.file.gerar_arquivo(f"Log", fileName, f"----Finalizado Empresa: {empresa} - {datetime.today()} ----------")
    
    def erro(self, fileName, erro):
        self.file.gerar_arquivo(f"Log", fileName, "-------------------------------------------------------------------") 
        self.file.gerar_arquivo(f"Log", fileName, f"----Erro: {erro}")
    
    def processo(self, fileName, msg):
        self.file.gerar_arquivo(f"Log", fileName, f"    {msg}")