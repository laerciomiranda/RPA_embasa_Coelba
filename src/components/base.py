from src.components.interacoes import Interacoes
from src.services.files import File
from src.services.movefile import Movefile
from src.services.log import Log
from src.services.funcoes import Funcoes
from src.repository.faturas import Faturas
from src.repository.sqlExecute import SQL
from src.services.pdf import LeitorPdf

class Base:
    def __init__(self, driver, empresa):
        self.driver = driver
        self.interacoes = Interacoes(driver)
        self.file = File()
        self.moveFile = Movefile()
        self.log = Log()
        self.funcoes = Funcoes()
        self.faturasRepository = Faturas(empresa)
        self.leitorPdf = LeitorPdf()
        
        
        # CONT-01958-X7D7Y9 e CONT-01955-W9Y3Q7