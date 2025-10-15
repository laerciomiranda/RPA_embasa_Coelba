from src.services.log import Log
import pyodbc

class Conexao:
    
    def __init__(self, empresa):
        self.log = Log()
        self.empresa = empresa
    
    def conectar(self):
        try:
            conexao = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=SSD201-113;'
                'DATABASE=DB_RPA_EC;'
                'UID=usr_integra_rpa;'
                'PWD=(cgbK[=LC.Md'
            )
            return conexao
        except Exception as e:
            self.log.erro(self.empresa, f"Erro na conexão: {e}")
            return None
