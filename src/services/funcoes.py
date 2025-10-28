from datetime import datetime, timedelta, date
from selenium.webdriver.common.by import By
import re

class Funcoes:
    
    def corrigir_mes(self, data, competencia="MANTER"):
        meses = {
            "JANEIRO": 1, "FEVEREIRO": 2, "MARÇO": 3, "ABRIL": 4,
            "MAIO": 5, "JUNHO": 6, "JULHO": 7, "AGOSTO": 8,
            "SETEMBRO": 9, "OUTUBRO": 10, "NOVEMBRO": 11, "DEZEMBRO": 12
        }

        if len(data.split("/")) > 2:
            data = self.formatar_data(data)
        
        if len(data.split("/")[0]) == 2:
            data = self.formatar_data(f"01/{data}")
            
        if "/" in data:
            mes_nome, ano = data.split("/")
            mes_num = meses[mes_nome.upper()]
            ano = int(ano)
            
            if competencia == "POSTERIOR":
                mes_num += 1
                if mes_num > 12:
                    mes_num = 1
                    ano += 1
            elif competencia == "ANTERIOR":
                mes_num -= 1
                if mes_num < 1:
                    mes_num = 12
                    ano -= 1
            
            return f"{str(mes_num).zfill(2)}/{ano}"
    
        return ""

    def formatar_data(self, data_str):
        meses = {
            1: "JANEIRO",
            2: "FEVEREIRO",
            3: "MARÇO",
            4: "ABRIL",
            5: "MAIO",
            6: "JUNHO",
            7: "JULHO",
            8: "AGOSTO",
            9: "SETEMBRO",
            10: "OUTUBRO",
            11: "NOVEMBRO",
            12: "DEZEMBRO"
        }
        
        data = datetime.strptime(data_str, "%d/%m/%Y")
        nome_mes = meses[data.month]
        return f"{nome_mes}/{data.year}"

    def extract_date_and_value(self, div_text: str) -> list:
        pattern = r'(\d{2}/\d{4}), (R\$ \d+\.\d{2})'
        match = re.search(pattern, div_text)
        if match:
            date_part = match.group(1)
            value_part = match.group(2)
            return [date_part, value_part]
        else:
            return []
        
    def vencimentoSaae(self, valor):
        if "/" in valor:
            data = valor.split("/")
            mes = int(data[0])
            mes = mes + 1
            
            return f"15/{mes}/{data[1]}"
        return ""
    
    def comparar_data(self, data_str):
        try:
            data_informada = datetime.strptime(data_str, "%d/%m/%Y").date()
        except ValueError:
            return "Formato inválido. Use dd/m/yyyy"

        hoje = date.today()

        if data_informada < hoje:
            return "vencida"
        elif data_informada > hoje:
            return "A Vencer"
        else:
            return "A Vencer"
        
    def de_para_by(self, value):
        if value == "By.CLASS_NAME":
            return By.CLASS_NAME
        if value == "By.ID":
            return By.ID
        if value == "By.XPATH":
            return By.XPATH
        if value == "By.TAG_NAME":
            return By.TAG_NAME
        
        return value