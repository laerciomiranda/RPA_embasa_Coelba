from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from src.model.fatura import Fatura
from src.components.base import Base
from src.components.webdriver import WebDrive
from src.repository.sqlExecute import SQL
from src.services.bianaTech import BianatechService

class Embasa:
    
    def __init__(self):
        self.webDirve = any
        self.base = any
        self.sqlExecute = SQL("EMBASA")
        self.bianatech = BianatechService()
            
    def iniciar (self):
        listEmpresas = self.sqlExecute.select("Empresas", "Empresa = 'EMBASA' And Codigo = '03795071001600'")
        for item in listEmpresas:
            self.webDirve =  WebDrive()
            self.base = Base(self.webDirve.driver, "EMBASA")
            self.base.log.processo("EMBASA",f"🚦 Iniciando Login: {item[5]}")
            listclientes = self.sqlExecute.select("Clientes", f"EmpresasId = {item[1]} order by ClientesId desc")
            self.webDirve.acessar_site(f"{item[4]}")
            self.login(item[5], item[6])
            self.base.driver.get('https://atendimentovirtual.embasa.ba.gov.br/segunda-via')
            self.processo(listclientes, item[3])
            self.webDirve.fechar_navegador()
            self.base.log.processo("EMBASA",f"🚦 Finalizando Login: {item[5]}")
        
    def login(self, user, pwd):
        self.base.interacoes.preencher_campo(By.ID, "inputCpf", user)
        self.base.interacoes.preencher_campo(By.ID, "inputPassword", pwd)
        self.base.interacoes.clicar_elemento(By.XPATH, "//button[span[contains(text(), 'Entrar')]]")
        self.base.interacoes.esperar_elemento(By.XPATH, "//section[contains(@class, 'menu-servicos')]")
        
    def processo(self, listClientes, empresa):
        self.base.interacoes.executar_Js("document.body.style.zoom = '0.3'", None)
        self.base.interacoes.esperar_elemento(By.XPATH, "//*[@id='wizard']/div/h2")
        self.escolherCnpj()
        print(f"escolhendo empresa: {empresa.strip()}")
        for option in self.select.options:
            if option.get_attribute("value").strip() == empresa.strip():
                option.click()
                time.sleep(1)
                self.verificarAviso()
                break
        print("Empresa escolhida")
        time.sleep(3)
        print("Verificando se Empresa Existe!")
        if self.base.interacoes.elemento_existe(By.XPATH, ".//div[contains(text(), 'Não existe matrícula para este')]"):
            print("Não existe matrícula para este CPF")
            return
        
        self.base.interacoes.clicar_elemento(By.XPATH, "//section/div/ul/div/div[1]/li")
        self.base.interacoes.clicar_elemento(By.XPATH, "//button[contains(text(), 'Selecionar Matrícula')]")
        time.sleep(1)
        self.verificarAviso()
        elemento = self.base.interacoes.esperar_elemento(By.ID, "input-matricula")
        self.base.interacoes.executar_Js("arguments[0].scrollIntoView();", elemento)
        time.sleep(1)
        for list in listClientes:
            self.base.log.processo("Embasa",f"       -> Iniciando Matrícula : {list[3]}")
            self.base.interacoes.preencher_campo(By.XPATH, "//*[@id='input-matricula']", str(list[3]).strip())
            self.base.interacoes.clicar_elemento(By.CLASS_NAME, "btn-pesquisar-conta")
            while True:
                loading = self.base.interacoes.elemento_existe(By.XPATH, "//div[span[contains(text(), 'Loading.') ]]")
                if loading == False:
                    break
                
            if self.base.interacoes.elemento_existe(By.XPATH, "//div[contains(text(), 'A Matrícula informada não possui débitos.') ]", None):
                self.base.log.processo("Embasa",f"       {list[3]} -> 0 - 0 - 0,00 - 0,00 - A Matrícula informada não possui débitos.")
                self.base.log.processo("Embasa",f"       -> Finnalizando Matrícula : {list[3]}")
                continue
            
            time.sleep(2)
            self.base.interacoes.executar_Js_seletor("document.querySelectorAll('.card.matricula-endereco, .card.p-4.card-total').forEach(el => el.remove());")
            cards = self.base.interacoes.executar_Js_seletor("return document.querySelectorAll('.content .card');")
            for card in cards:
                status = self.base.interacoes.esperar_elemento_lista(By.XPATH, card,".//div[contains(@class, 'conta-a-vencer')]")
                if status.text == "Conta em Análise":
                    self.base.log.processo("Embasa",f"       {list[3]} -> 0 - 0 - 0,00 - 0,00 - Conta em Análise.")
                    self.base.log.processo("Embasa",f"       -> Finnalizando Matrícula : {list[3]}")
                    continue
                
                referencia      = self.base.interacoes.esperar_elemento_lista(By.XPATH, card, ".//div[text()='Referência:']/following-sibling::div")
                Venncimento     = self.base.interacoes.esperar_elemento_lista(By.XPATH, card, ".//div[text()='Vencimento:']/following-sibling::div")
                valor_servico   = self.base.interacoes.esperar_elemento_lista(By.XPATH, card,".//div[text()='Valor Serviço:']/following-sibling::div")
                total           = self.base.interacoes.esperar_elemento_lista(By.XPATH, card,".//div[contains(@class, 'font-weight-bold') and contains(text(), 'R$')]")
                comptenciaReal = self.base.funcoes.corrigir_mes(referencia.text, list[5])
                
                ultimoValSalvo = self.base.faturasRepository.select(f"Embasa-{list[3]}-{Venncimento.text}")
                if(ultimoValSalvo == total.text.replace("R$ ","")):
                    self.base.log.processo("Embasa",f"           {list[3]} - {referencia.text} - {Venncimento.text} - {valor_servico.text} - {total.text} - {status.text}")
                    continue
                
                if(ultimoValSalvo != total.text.replace("R$&nbsp;","")):
                    self.base.faturasRepository.update(f"Embasa-{list[3]}-{referencia.text}-{Venncimento.text}")
                
                botao_baixar = self.base.interacoes.esperar_elemento_lista(By.XPATH, card,".//button[contains(text(), 'BAIXAR 2ª VIA')]")
                self.base.interacoes.executar_Js("arguments[0].click();",botao_baixar )        
                
                time.sleep(1)
                if self.base.interacoes.elemento_existe(By.XPATH, "//*[@id='modalWarningTitle']"):
                    self.base.interacoes.clicar_elemento(By.XPATH, "//button[contains(text(), 'Sim')]")
                    
                time.sleep(1)
                while True:
                    print("true while")
                    loading = self.base.interacoes.elemento_existe(By.CLASS_NAME, "spinner-border")
                    if loading == False:
                        print("loading true")
                        time.sleep(2)
                        break
                
                move = self.base.moveFile.get_latest_file_1(f"{empresa}/{list[3]}", comptenciaReal, "Embasa")
                if move == False:
                    self.base.log.processo("Embasa",f"--> Erro ao mover o PDF da fatura: {empresa} - {list[3]}")
                    continue
                
                textoPdf = self.base.leitorPdf.lerPdf(move)
                dadosPdf = self.base.leitorPdf.ObterDadosEmbasa(textoPdf)
                img_base_64 = self.base.file.imagem_para_base64(move)
                
                dadosBiana = self.bianatech.consultar(img_base_64, "Mês/Ano|VALOR A PAGAR (R$)|Vencimento|Data Leitura Anterior|Data Leitura Atual|Próxima Leitura|Dias de Consumo|Data Emissão|Consumo (m³)|")
                fatura = Fatura( 
                        Empresa             = "Embasa", 
                        Cliente             = list[3],
                        Vencimento          = dadosBiana["Vencimento"] if dadosBiana["Vencimento"] != "não informado" else dadosPdf.Vencimento, 
                        MesRef              = dadosBiana["Mês/Ano"] if dadosBiana["Mês/Ano"] != "não informado" else dadosPdf.MesRef, 
                        MesEmis             = dadosBiana["Data Emissão"] if dadosBiana["Data Emissão"] != "não informado" else dadosPdf.MesEmis, 
                        Valor               = dadosBiana["VALOR A PAGAR (R$)"] if dadosBiana["VALOR A PAGAR (R$)"] != "não informado" else dadosPdf.Valor if dadosPdf.Valor is not None else total.text.replace("R$&nbsp;",""), 
                        Situacao            = self.base.funcoes.comparar_data(dadosBiana["Vencimento"]) if dadosBiana["Vencimento"] != "não informado" else self.base.funcoes.comparar_data(dadosPdf.Vencimento) if dadosPdf.Vencimento is not None else status.text,
                        LeituraAnter        = dadosPdf.LeituraAnt,
                        LeituraAtual        = dadosPdf.LeituraAtu,
                        LeituraProxi        = dadosPdf.leituraPro,
                        NumDias             = dadosBiana["Dias de Consumo"] if dadosBiana["Dias de Consumo"] != "não informado" else dadosPdf.NumDias,
                        TaxaColetaLixo      = dadosPdf.tcl,
                        ConservacaoHidrometro   = dadosPdf.hidrometro,
                        ConsumoAtivoNaPonta = dadosPdf.consumoNap,
                        ConsumoAtivoForaDaPonta = dadosPdf.ConsumoAfp,
                        ConsumoTUSDFPonta   = dadosPdf.ConsumoAnp,
                        ConsumoTUSDNPonta   = dadosPdf.ConsumoFop,
                        MetroCubicos        = dadosBiana["Consumo (m³)"] if dadosBiana["Consumo (m³)"] != "não informado" else dadosPdf.m3,
                        Cancelado           = False, 
                        Arquivo             = move, 
                        Base64File          = img_base_64
                )
                
                self.base.faturasRepository.Insert(fatura)
                self.base.log.processo("Embasa",f"       -> Finalizando Matrícula : {list[3]}")
                
            if len(cards) > 0:
                self.base.interacoes.clicar_elemento(By.XPATH, "//button[contains(text(), 'ANTERIOR')]")
                continue            
            
            if self.base.interacoes.elemento_existe(By.XPATH, "//div[contains(text(), 'Esse serviço só poderá ser solicitado')]", None):
                self.base.log.processo("Embasa", f"              A Matrícula: {list[3]} não está vinculada ao CNPJ: {empresa}")
                continue
            
            if self.base.interacoes.elemento_existe(By.XPATH, "//div[contains(text(), 'Matrícula inválida')]", None):
                self.base.log.processo("Embasa", f"              Matrícula inválida: {list[3]} - CNPJ: {empresa}")
                continue
                  
    def escolherCnpj(self):
        print("Clicar no botão")
        self.base.interacoes.clicar_elemento(By.CLASS_NAME, "btn-matricula")
        self.base.interacoes.executar_Js_seletor("document.querySelectorAll('.d-none').forEach(el => el.classList.remove('d-none'));")
        time.sleep(3)
        select_element = self.base.interacoes.esperar_elemento(By.ID, "comboCnpj")
        time.sleep(1)
        self.select = Select(select_element)
    
    def verificarAviso(self):
        time.sleep(2)
        if self.base.interacoes.elemento_existe(By.XPATH, "//p[contains(text(), 'trabalhando')]", None) or self.base.interacoes.elemento_existe(By.XPATH, "//p[contains(text(), 'O fornecimento de água')]", None):
            self.base.interacoes.clicar_elemento(By.XPATH, "//button[contains(text(), 'OK')]")
        