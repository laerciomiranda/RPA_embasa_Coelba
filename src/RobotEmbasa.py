from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from src.components.interacoes import Interacoes
from src.model.fatura import Fatura
from src.services.files import File
from src.services.movefile import Movefile
from src.services.log import Log
from src.repository.faturas import Faturas
from src.services.funcoes import Funcoes

class RPAEmbasa:

    def __init__(self, driver):
        self.driver = driver
        self.interacoes = Interacoes(driver)
        self.file = File()
        self.moveFile = Movefile()
        self.log = Log()
        self.funcoes = Funcoes()
        self.faturasRepository = Faturas("Embasa")
        self.select = ""
    
    def acessar(self, user, pwd):       
        self.interacoes.preencher_campo(By.ID, "inputCpf", user)
        self.interacoes.preencher_campo(By.ID, "inputPassword", pwd)
        self.interacoes.clicar_elemento(By.XPATH, "//button[span[contains(text(), 'Entrar')]]")
        self.interacoes.esperar_elemento(By.XPATH, "//section[contains(@class, 'menu-servicos')]")
      
    def escolherCnpj(self):
        self.interacoes.clicar_elemento(By.CLASS_NAME, "btn-matricula")
        self.interacoes.executar_Js_seletor("document.querySelectorAll('.d-none').forEach(el => el.classList.remove('d-none'));")
        time.sleep(3)
        select_element = self.interacoes.esperar_elemento(By.ID,"comboCnpj")
        time.sleep(1)
        self.select = Select(select_element)
        
    def iniciar(self):
        self.interacoes.executar_Js("document.body.style.zoom = '0.3'", None)
        self.escolherCnpj()
        for index in range(1, len(self.select.options)):  
            option = self.select.options[index]
            cnpj = option.get_attribute('value').strip()
            self.log.processo("Embasa",f"    -> Iniciando CNPJ: {cnpj}")
            matriculas = self.file.obter_matriculas_por_cnpj(option.get_attribute('value'))
            if(len(matriculas) == 0):
                self.log.processo("Embasa",f"       -> Não há matrículas para este CNPJ")
                self.log.processo("Embasa",f"    -> Finalizando CNPJ: {cnpj}")
                continue
            
            option.click()
            self.verificarAviso()
            
            time.sleep(2)
            self.interacoes.clicar_elemento(By.XPATH, "//section/div/ul/div/div[1]/li")
            self.interacoes.clicar_elemento(By.XPATH, "//button[contains(text(), 'Selecionar Matrícula')]")
            
            self.verificarAviso()
            
            elemento = self.interacoes.esperar_elemento(By.ID, "input-matricula")
            self.interacoes.executar_Js("arguments[0].scrollIntoView();", elemento)
            time.sleep(1)
            for iten in matriculas:
                self.log.processo("Embasa",f"       -> Iniciando Matrícula : {iten}")
                while True:
                    self.interacoes.preencher_campo(By.XPATH, "//*[@id='input-matricula']", iten)
                    self.interacoes.clicar_elemento(By.CLASS_NAME, "btn-pesquisar-conta")
                    while True:
                        loading = self.interacoes.elemento_existe(By.XPATH, "//div[span[contains(text(), 'Loading.') ]]")
                        if loading == False:
                            break
                    
                    if self.interacoes.elemento_existe(By.XPATH, "//div[contains(text(), 'A Matrícula informada não possui débitos.') ]", None):
                        self.log.processo("Embasa",f"       {iten} -> 0 - 0 - 0,00 - 0,00 - A Matrícula informada não possui débitos.")
                        self.log.processo("Embasa",f"       -> Finnalizando Matrícula : {iten}")
                        break
                
                    time.sleep(2)
                    self.interacoes.executar_Js_seletor("document.querySelectorAll('.card.matricula-endereco, .card.p-4.card-total').forEach(el => el.remove());")
                    cards = self.interacoes.executar_Js_seletor("return document.querySelectorAll('.content .card');")
                    for card in cards:
                        status           = self.interacoes.esperar_elemento_lista(By.XPATH, card,".//div[contains(@class, 'conta-a-vencer')]")
                        if status.text == "Conta em Análise":
                            self.log.processo("Embasa",f"       {iten} -> 0 - 0 - 0,00 - 0,00 - Conta em Análise.")
                            self.log.processo("Embasa",f"       -> Finnalizando Matrícula : {iten}")
                            continue
                        
                        referencia      = self.interacoes.esperar_elemento_lista(By.XPATH, card, ".//div[text()='Referência:']/following-sibling::div")
                        Venncimento     = self.interacoes.esperar_elemento_lista(By.XPATH, card, ".//div[text()='Vencimento:']/following-sibling::div")
                        valor_servico   = self.interacoes.esperar_elemento_lista(By.XPATH, card,".//div[text()='Valor Serviço:']/following-sibling::div")
                        total           = self.interacoes.esperar_elemento_lista(By.XPATH, card,".//div[contains(@class, 'font-weight-bold') and contains(text(), 'R$')]")
                        
                        ultimoValSalvo = self.faturasRepository.select(f"Embasa-{iten}-{referencia.text}-{Venncimento.text}")
                        if(ultimoValSalvo == total.text.replace("R$&nbsp;","")):
                            self.log.processo("Embasa",f"           {iten} - {referencia.text} - {Venncimento.text} - {valor_servico.text} - {total.text} - {status.text}")
                            continue
                        
                        if(ultimoValSalvo != total.text.replace("R$&nbsp;","")):
                            self.faturasRepository.update(f"Embasa-{iten}-{referencia.text}-{Venncimento.text}")
                        
                        botao_baixar = self.interacoes.esperar_elemento_lista(By.XPATH, card,".//button[contains(text(), 'BAIXAR 2ª VIA')]")
                        self.interacoes.executar_Js("arguments[0].click();",botao_baixar )
                        
                        if self.interacoes.elemento_existe(By.XPATH, "//*[@id='modalWarningTitle']"):
                            self.interacoes.clicar_elemento(By.XPATH, "//button[contains(text(), 'Sim')]")
                        
                        while True:
                            loading = self.interacoes.elemento_existe(By.CLASS_NAME, "spinner-border")
                            if loading == False:
                                time.sleep(2)
                                break
                            
                        newfile = self.moveFile.get_latest_file(cnpj, self.funcoes.corrigir_mes(f"01/{referencia.text}"), "Embasa")
                        self.log.processo("Embasa",f"           {iten} - {referencia.text} - {Venncimento.text} - {valor_servico.text} - {total.text} - {status.text}")
                        fatura = Fatura(cliente=iten, empresa="Embasa", vencimento=Venncimento.text, CompetenciaSistema = referencia.text, CompetenciaReal=self.funcoes.corrigir_mes(f"01/{referencia.text}"), valor= total.text.replace("R$&nbsp;",""), situacao=status.text, cancelado=False, arquivo=newfile, base64file=self.file.imagem_para_base64(newfile))
                        self.faturasRepository.Insert(fatura)
                        self.log.processo("Embasa",f"       -> Finnalizando Matrícula : {iten}")
                    
                    if len(cards) > 0:
                        self.interacoes.clicar_elemento(By.XPATH, "//button[contains(text(), 'ANTERIOR')]")
                        break
                    
                    if self.interacoes.elemento_existe(By.XPATH, "//div[contains(text(), 'Esse serviço só poderá ser solicitado')]", None):
                        self.log.processo("Embasa", f"              A Matrícula: {iten} não está vinculada ao CNPJ: {cnpj}")
                        break
                    
                    if self.interacoes.elemento_existe(By.XPATH, "//div[contains(text(), 'Matrícula inválida')]", None):
                        self.log.processo("Embasa", f"              Matrícula inválida: {iten} - CNPJ: {cnpj}")
                        break
                
            self.log.processo("Embasa",f"    -> Finalizando CNPJ: {cnpj}")
            self.escolherCnpj()
        
    def verificarAviso(self):
        time.sleep(2)
        if self.interacoes.elemento_existe(By.XPATH, "//p[contains(text(), 'trabalhando')]", None) or self.interacoes.elemento_existe(By.XPATH, "//p[contains(text(), 'O fornecimento de água')]", None):
            self.interacoes.clicar_elemento(By.XPATH, "//button[contains(text(), 'OK')]")
            
            
            
