from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from src.model.fatura import Fatura
from src.components.base import Base
from src.components.webdriver import WebDrive
from src.repository.sqlExecute import SQL
from src.services.bianaTech import BianatechService

class Saae:
    def __init__(self):
        self.webDirve = any
        self.base = any
        self.sqlExecute = SQL("SAAE")
        self.indexMultFatura = 0
        self.CountMultFatura = 1
        self.bianatech = BianatechService()
        
    def iniciar (self):
        listEmpresas = self.sqlExecute.select("Empresas", "Empresa = 'SAAE'")
        for item in listEmpresas:
            listclientes = self.sqlExecute.select("Clientes", f"EmpresasId = {item[1]}")
            for cliente in listclientes:
                self.CountMultFatura = 1
                self.webDirve =  WebDrive()
                self.base = Base(self.webDirve.driver, "SAAE")
                self.base.log.processo("SAAE",f"🚦 Iniciando Login: {cliente[3]}")
                self.webDirve.acessar_site(f"{item[4]}")
                repetirCliente = self.processo(cliente, item[3])
                self.webDirve.fechar_navegador()
                while True:
                    if repetirCliente == False:
                        break
                    
                    self.webDirve =  WebDrive()
                    self.base = Base(self.webDirve.driver, "SAAE")
                    self.base.log.processo("SAAE",f"🚦      Baixando outra fatura: {cliente[3]}")
                    self.webDirve.acessar_site(f"{item[4]}")
                    repetirCliente = self.processo(cliente, item[3])
                    self.webDirve.fechar_navegador()
                self.base.log.processo("SAAE",f"🚦 Finalizando Login: {cliente[3]}")
            
    def processo(self, cliente, empresa):
        self.base.interacoes.clicar_elemento(By.CLASS_NAME, "btn-ok")
        self.base.interacoes.clicar_elemento(By.XPATH, "//div[@class='tatodesk-widget-reply' and contains(text(), 'Faturas')]")
        self.base.interacoes.clicar_elemento(By.XPATH, "//div[@class='tatodesk-widget-reply' and contains(text(), 'Conta detalhada')]")
        self.base.interacoes.clicar_elemento(By.XPATH, "//*[contains(text(), 'Digite sua Matrícula')]")
        self.base.interacoes.preencher_campo(By.CLASS_NAME, "new-message", str(cliente[3]))
        self.base.interacoes.clicar_elemento(By.CLASS_NAME, "send-button-icon")
        repetirCliente = False
        qtdFaturas = 1
        search = "Encontrei uma conta"
        while True:
            print("aqui")
            dados = self.base.interacoes.esperar_elemento(By.XPATH, f"//*[contains(text(), '{search}')]", 20)
            if dados != False:
                print("aqui 1")
                if qtdFaturas == 1:
                    print("aqui 2")
                    repetirCliente = self.umaConta(cliente, empresa)
                    break
                else:
                    print("aqui 3")
                    repetirCliente = self.DuasContaMais(cliente, empresa)
                    break
            qtdFaturas +=1
            search = f"Encontrei {qtdFaturas} contas"
        return repetirCliente
    
    def umaConta(self, cliente, empresa):
        print("aqui 4")
        dados = self.base.interacoes.esperar_elemento(By.XPATH, "//*[contains(text(), 'Encontrei uma conta para sua matrícula:')]")
        print("aqui 5")
        valores = self.base.funcoes.extract_date_and_value(dados.text)
        print("aqui 6")
        competenciaReal = valores[0]
        valor = valores[1]
        print("aqui 7")
        vencimento = self.base.funcoes.vencimentoSaae(competenciaReal)
        situacao = self.base.funcoes.comparar_data(vencimento)
        print("aqui 8")
        ultimoValSalvo = self.base.faturasRepository.select(f"SAAE-{cliente[3]}-{competenciaReal}-{vencimento}")
        if(ultimoValSalvo == valor.replace("R$&nbsp;","")):
            self.base.log.processo("SAAE",f" Já baixada:           {cliente} - {competenciaReal} - {vencimento} - {valor} - {situacao}")   
        else:
            self.BaixarFatura(cliente, empresa, competenciaReal, vencimento, situacao, valor)
        
        return False    
            
    def DuasContaMais(self, cliente, empresa):
        self.base.interacoes.clicar_elemento(By.XPATH, "//div[@class='tatodesk-widget-reply' and contains(text(), 'Escolher uma conta')]")
        list_faturas = self.base.interacoes.esperar_elemento(By.CLASS_NAME, 'replies')
        
        lista_divs = self.base.interacoes.listar_itens_ul(By.CLASS_NAME, "tatodesk-widget-reply",list_faturas)
        lista_divs_count = len(lista_divs)
        for resposta in lista_divs:
            dados = lista_divs[self.indexMultFatura].text.split(" - ")
            competenciaReal = dados[0]
            valor = dados[1]
            vencimento = self.base.funcoes.vencimentoSaae(competenciaReal)
            situacao = self.base.funcoes.comparar_data(vencimento)
            
            ultimoValSalvo = self.base.faturasRepository.select(f"SAAE-{cliente[3]}-{competenciaReal}-{vencimento}")
            if(ultimoValSalvo == valor.replace("R$&nbsp;","")):
                self.base.log.processo("SAAE",f" Já baixada:           {cliente} - {competenciaReal} - {vencimento} - {valor} - {situacao}")   
            else:
                self.base.interacoes.clicar_elemento(By.XPATH, f"//div[@class='tatodesk-widget-reply' and contains(text(), '{lista_divs[self.indexMultFatura].text}')]")
                self.BaixarFatura(cliente, empresa, competenciaReal, vencimento, situacao, valor)
            break
        
        if lista_divs_count > 1 and self.CountMultFatura < lista_divs_count:
            self.indexMultFatura += 1
            self.CountMultFatura += 1
            return True
        return False
        
    def BaixarFatura(self, cliente, empresa, competenciaReal, vencimento, situacao, valor):
        self.base.interacoes.clicar_elemento(By.XPATH, "//div[@class='tatodesk-widget-reply' and contains(text(), 'Baixar PDF')]")
        self.base.interacoes.clicar_elemento(By.XPATH, "//a[@class='file-link' and .//span[contains(text(), 'Baixar Arquivo')]]")
        time.sleep(3)
        while True:
            move = self.base.moveFile.get_latest_file_1(f"{empresa}/{cliente[3]}", competenciaReal, "SAAE")
            if move != None:
                break
        
        time.sleep(2)
        competenciaCorrigida = self.base.funcoes.corrigir_mes(competenciaReal, cliente[5])
        textoPdf = self.base.leitorPdf.lerPdf(move)
        dadosPdf = self.base.leitorPdf.ObterDadosSaae(textoPdf)
        img_base_64 = self.base.file.imagem_para_base64(move)
        dadosBiana = self.bianatech.consultar(img_base_64, "Mês/Ano|VALOR A PAGAR (R$)|Vencimento|Data Leitura Anterior|Data Leitura Atual|Próxima Leitura|DIAS|Data Emissão|(M³)|Esgoto|TCL-TAXA DE COLETA DE LIXO|CONSERVACAO DE HIDROMETRO")
        print(dadosBiana)
        fatura = Fatura( 
                        Empresa             = "SAAE", 
                        Cliente             = cliente[3],
                        Vencimento          = dadosBiana["Vencimento"] if dadosBiana["Vencimento"] != "não informado" else dadosPdf.Vencimento, 
                        MesRef              = dadosBiana["Mês/Ano"] if dadosBiana["Mês/Ano"] != "não informado" else dadosPdf.MesRef, 
                        MesEmis             = dadosBiana["Data Emissão"] if dadosBiana["Data Emissão"] != "não informado" else dadosPdf.MesEmis, 
                        Valor               = dadosBiana["VALOR A PAGAR (R$)"] if dadosBiana["VALOR A PAGAR (R$)"] != "não informado" else dadosPdf.Valor if dadosPdf.Valor is not None else valor.replace("R$&nbsp;",""), 
                        Situacao            = self.base.funcoes.comparar_data(dadosBiana["Vencimento"]) if dadosBiana["Vencimento"] != "não informado" else self.base.funcoes.comparar_data(dadosPdf.Vencimento) if dadosPdf.Vencimento is not None else status.text,
                        LeituraAnter        = dadosPdf.LeituraAnt,
                        LeituraAtual        = dadosPdf.LeituraAtu,
                        LeituraProxi        = dadosPdf.leituraPro,
                        NumDias             = dadosBiana["Dias de Consumo"] if dadosBiana["Dias de Consumo"] != "não informado" else dadosPdf.NumDias,
                        TaxaColetaLixo      = dadosBiana["TCL-TAXA DE COLETA DE LIXO"] if dadosBiana["TCL-TAXA DE COLETA DE LIXO"] != "não informado" else dadosPdf.tcl,
                        ConservacaoHidrometro   = dadosBiana["CONSERVACAO DE HIDROMETRO"] if dadosBiana["CONSERVACAO DE HIDROMETRO"] != "não informado" else dadosPdf.hidrometro,
                        MetroCubicos        = dadosBiana["Consumo (m³)"] if dadosBiana["Consumo (m³)"] != "não informado" else dadosPdf.m3,
                        Cancelado           = False, 
                        Arquivo             = move, 
                        Base64File          = img_base_64
                )
        
        self.base.faturasRepository.Insert(fatura)
        print("Salvo com sucesso!")