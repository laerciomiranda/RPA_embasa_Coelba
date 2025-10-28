from selenium.webdriver.common.by import By
import time
from src.model.fatura import Fatura
from src.components.base import Base
from src.components.webdriver import WebDrive
from src.repository.sqlExecute import SQL
from src.services.bianaTech import BianatechService

class Coelba:
    def __init__(self):
        self.webDirve = any
        self.base = any
        self.sqlExecute = SQL("COELBA")
        self.bianatech = BianatechService()

    def iniciar (self):
        listEmpresas = self.sqlExecute.select("Empresas", "Empresa = 'COELBA'")
        for item in listEmpresas:
            self.webDirve =  WebDrive()
            self.base = Base(self.webDirve.driver, "Coelba")
            
            self.base.log.processo("Coelba",f"🚦 Iniciando Login: {item[5]}")
            listclientes = self.sqlExecute.select("Clientes", f"EmpresasId = {item[1]}")
            self.webDirve.acessar_site(item[4])
            
            self.login(item[5], item[6])
            self.processo(listclientes, item[3])
            self.base.log.processo("Coelba",f"🏁 Fim Login: {item[5]}")
            self.webDirve.fechar_navegador()
            
    def login(self, user, pwd):
        self.base.interacoes.esperar_loading_sumir(By.TAG_NAME, "app-spinner")
        self.base.interacoes.clicar_elemento(By.CLASS_NAME, "mat-flat-button")
        self.base.interacoes.preencher_campo(By.ID, "userId", user)
        self.base.interacoes.preencher_campo(By.ID, "password", pwd)
        self.base.interacoes.clicar_elemento(By.CLASS_NAME, "btn-neoprimary")

    def processo(self, clientes, empresa):
        time.sleep(2)
        self.base.interacoes.esperar_loading_sumir(By.TAG_NAME, "app-spinner")
        self.base.interacoes.clicar_elemento(By.XPATH, "//mat-card[contains(text(), 'Bahia')]")
        self.base.interacoes.esperar_loading_sumir(By.TAG_NAME, "app-spinner")

        for cliente in clientes:
            self.base.interacoes.preencher_campo(By.CLASS_NAME, "pesquisar", cliente[3])
            self.base.interacoes.clicar_elemento(By.CLASS_NAME, "filter")
            self.base.log.processo("Coelba",f"--> Iniciando Cliente: {cliente[3]}")
            time.sleep(2)
            self.base.interacoes.esperar_loading_sumir(By.TAG_NAME, "app-spinner")
            self.base.interacoes.clicar_elemento(By.XPATH, "//*[@id='meus-imoveis']/div/section[2]/ul/li[1]/app-uc-list-item/div/mat-icon")
            time.sleep(2)
            self.base.interacoes.esperar_loading_sumir(By.TAG_NAME, "app-spinner")
            
            # faturas_page = self.base.interacoes.esperar_elemento(By.XPATH, "//span[contains(text(), 'Faturas e 2ª via de faturas')]")
            # self.base.interacoes.executar_Js("arguments[0].click();",faturas_page)
            # time.sleep(2)
            # self.base.interacoes.esperar_loading_sumir(By.TAG_NAME, "app-spinner")

            if(self.ExisteFatura(cliente[3]) == False):
                continue

            valor       = self.base.interacoes.esperar_elemento(By.ID, "valor").text
            vencimento  = self.base.interacoes.esperar_elemento(By.XPATH, "//span[text()='Vencimento:']/following-sibling::span").text
            situacao    = self.base.interacoes.esperar_elemento(By.XPATH, "//span[text()='Situação:']/following-sibling::span").text
            # competencia = self.base.interacoes.esperar_elemento(By.XPATH, "//span[text()='Vencimento:']/following-sibling::span").text
            
            # while True:
            #     if self.base.interacoes.elemento_existe(By.CLASS_NAME, "mensagem-box"):
            #         break
            #     if self.base.interacoes.elemento_existe(By.XPATH, "//span[1]/div/div[2]/div/div[1]/span[2]"):
            #         competencia = self.base.interacoes.esperar_elemento(By.XPATH, "//span[text()='REFERÊNCIA']/following-sibling::span").text
            #         break
            
            ultimoValSalvo = self.base.faturasRepository.select(f"Coelba-{cliente[3]}-{vencimento}")
            if(ultimoValSalvo == valor.replace("R$&nbsp;","")):
                self.base.log.processo("Coelba",f" Já baixada:           {cliente} - {vencimento.text} - {valor.text} - {situacao.text}")
                self.base.log.processo("Coelba",f"--> Finalizado Cliente: {cliente}")
                self.base.interacoes.voltar_Pagina()
                continue
            
            comptenciaReal = self.base.funcoes.corrigir_mes(vencimento, cliente[5])
            while True:
                maisOpcoes = self.base.interacoes.esperar_elemento(By.XPATH, "//button[span[contains(text(), 'MAIS OPÇÕES')]]")
                self.base.interacoes.executar_Js("arguments[0].click();",maisOpcoes)

                opcoes_fatura = self.base.interacoes.esperar_elemento(By.XPATH, "//button[contains(text(), 'Opções de fatura')]")
                self.base.interacoes.executar_Js("arguments[0].click();",opcoes_fatura)
                    
                download  = self.base.interacoes.esperar_elemento(By.XPATH, "//button[contains(text(), 'Download')]")
                self.base.interacoes.executar_Js("arguments[0].click();",download )
                
                self.base.interacoes.clicar_elemento(By.XPATH, "//span[contains(text(), 'Não Estou Com Fatura Em Mãos')]")
                self.base.interacoes.clicar_elemento(By.XPATH, "//button[div[contains(text(), 'BAIXAR')]]")

                indisponivel = False
                while True:
                    if self.base.interacoes.elemento_existe(By.XPATH, "//h4[contains(text(), 'Fatura indisponível')]"):
                        self.base.interacoes.clicar_elemento(By.XPATH, "//button[contains(text(), 'FECHAR')]")
                        self.base.log.processo("Coelba",f"--> Fatura indisponível no canal digital: {cliente[3]}")
                        indisponivel = True
                        break
                    
                    if self.base.interacoes.elemento_existe(By.XPATH, "//h4[contains(text(), 'Download realizado com sucesso')]"):
                        self.base.interacoes.clicar_elemento(By.XPATH, "//button[contains(text(), 'OK')]")
                        break
                    
                if indisponivel:
                    break
                
                time.sleep(2)
                move = self.base.moveFile.get_latest_file_1(f"{empresa}/{cliente[3]}", comptenciaReal)
                if move != False:
                    break
            
            if indisponivel:
                self.base.log.processo("Coelba",f"--> Finalizado Cliente: {cliente[3]}")
                self.base.interacoes.voltar_Pagina()
                self.base.interacoes.clicar_elemento(By.XPATH, "//span[contains(text(), 'Minhas Unidades')]")
                continue 
            
            textoPdf = self.base.leitorPdf.lerPdf(move)
            dadosPdf = self.base.leitorPdf.ObterDadosCoelba(textoPdf)
            img_base_64 = self.base.file.imagem_para_base64(move)
            dadosBiana = self.bianatech.consultar(img_base_64, "REF:MÊS/ANO|TOTAL A PAGAR R$|VENCIMENTO|LEITURA ANTERIOR|LEITURA ATUAL|PRÓXIMA LEITURA|N° DE DIAS|DATA DE EMISSÃO:|Energia injetada no mes| CAMPOVAZIO")
            fatura = Fatura( 
                        Empresa             = "Coelba", 
                        Cliente             = cliente[3],
                        Vencimento          = dadosBiana["VENCIMENTO"] if dadosBiana["VENCIMENTO"] != "não informado" else dadosPdf.Vencimento, 
                        MesRef              = dadosBiana["REF:MÊS/ANO"] if dadosBiana["REF:MÊS/ANO"] != "não informado" else dadosPdf.MesRef, 
                        MesEmis             = dadosBiana["DATA DE EMISSÃO:"] if dadosBiana["DATA DE EMISSÃO:"] != "não informado" else dadosPdf.MesEmis, 
                        Valor               = dadosBiana["TOTAL A PAGAR R$"] if dadosBiana["TOTAL A PAGAR R$"] != "não informado" else dadosPdf.Valor if dadosPdf.Valor is not None else valor.replace("R$&nbsp;",""), 
                        Situacao            = self.base.funcoes.comparar_data(dadosBiana["VENCIMENTO"]) if dadosBiana["VENCIMENTO"] != "não informado" else self.base.funcoes.comparar_data(dadosPdf.Vencimento) if dadosPdf.Vencimento is not None else situacao, 
                        LeituraAnter        = dadosPdf.LeituraAnt,
                        LeituraAtual        = dadosPdf.LeituraAtu,
                        LeituraProxi        = dadosPdf.leituraPro,
                        NumDias             = dadosBiana["N° DE DIAS"] if dadosBiana["N° DE DIAS"] != "não informado" else dadosPdf.NumDias,
                        EnergiaInjetada     = dadosBiana["Energia injetada no mes"] if dadosBiana["Energia injetada no mes"] != "não informado" else dadosPdf.Energiainj,
                        ConsumoAtivoNaPonta = dadosPdf.consumoNap,
                        ConsumoAtivoForaDaPonta = dadosPdf.ConsumoAfp,
                        ConsumoTUSDFPonta   = dadosPdf.ConsumoAnp,
                        ConsumoTUSDNPonta   = dadosPdf.ConsumoFop,
                        Cancelado           = False, 
                        Arquivo             = move, 
                        Base64File          = img_base_64
                )
            
            self.base.faturasRepository.Insert(fatura)
            self.base.log.processo("Coelba",f"--> Finalizado Cliente: {cliente[3]}")
            
            self.base.interacoes.voltar_Pagina()
            self.base.interacoes.esperar_loading_sumir(By.TAG_NAME, "app-spinner")
            
            # self.base.interacoes.esperar_loading_sumir(By.TAG_NAME, "app-spinner")
            # self.base.interacoes.clicar_elemento(By.XPATH, "//span[contains(text(), 'Minhas Unidades')]") 
            # time.sleep(2)
            # self.base.interacoes.esperar_loading_sumir(By.TAG_NAME, "app-spinner")
            
    def ExisteFatura(self, cliente):
        if self.base.interacoes.elemento_existe(By.ID, "sem-fatura"):
            self.base.log.processo("Coelba",f"S/F:           {cliente} - Não existem ainda faturas emitidas para esta unidade consumidora")
            self.base.interacoes.clicar_elemento(By.XPATH, "//span[contains(text(), 'Minhas Unidades')]")
            return False
        if self.base.interacoes.frase_existe(By.XPATH, "//p[contains(text(), 'O valor desta fatura será inserido em uma próxima fatura')]"):
            self.base.log.processo("Coelba",f"S/F:           {cliente} - O valor desta fatura será inserido em uma próxima fatura")
            self.base.interacoes.clicar_elemento(By.XPATH, "//span[contains(text(), 'Minhas Unidades')]")
            return False
        return True