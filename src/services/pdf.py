import fitz
import re
from src.model.pdfModel import PdfModel

class LeitorPdf:
    def __init__(self):
        pass
    
    def lerPdf(self, caminho) -> str:
        with fitz.open(caminho) as pdf:
            texto = ""
            for pagina in pdf:
                texto += pagina.get_text()
        return texto
        
    def ObterDadosCoelba(self, texto) -> PdfModel:
        ref_match = re.search(r'REF[:\s]*MÊS/ANO\s*(?:\n\s*)*([\d/]{7})', texto, re.IGNORECASE)
        venc_match = re.search(r'VENCIMENTO\s*(?:\n\s*)*([\d/]{10})', texto, re.IGNORECASE)
        emissao_match = re.search(r'DATA DE EMISSÃO[:\s]*(?:\n\s*)*(\d{2}/\d{2}/\d{4})', texto, re.IGNORECASE)
        valor_match = re.search(r'TOTAL A PAGAR R\$\s*(?:\n\s*)*([\d\.,]+)', texto, re.IGNORECASE)

        leitura_anterior = re.search(r'LEITURA\s+ANTERIOR\s*(?:\n\s*)*(\d{2}/\d{2}/\d{4})', texto, re.IGNORECASE)
        leitura_atual = re.search(r'LEITURA\s+ATUAL\s*(?:\n\s*)*(\d{2}/\d{2}/\d{4})', texto, re.IGNORECASE)
        numero_dias = re.search(r'N[°º]?\s+DE\s+DIAS\s*(?:\n\s*)*(\d+)', texto, re.IGNORECASE)
        proxima_leitura = re.search(r'PR[ÓO]XIMA\s+LEITURA\s*(?:\n\s*)*(\d{2}/\d{2}/\d{4})', texto, re.IGNORECASE)

        # energia_inj = re.search(r'Energia injetada\s+NP\s+[\d,.]+kWh\s+e\s+FP\s+[\d,.]+k\s*Wh\s+no\s+mes', texto, re.IGNORECASE)
        energia_inj = re.search(r'Energia injetada no mes\s+([\d,.]+)kWh', texto, re.IGNORECASE)

        consumo_tusdNp = re.search(r'Consumo-TUSD\s+NPonta\s*\n\s*(kWh)\s*\n\s*([\d,.]+)', texto, re.IGNORECASE)
        consumo_tusdFp = re.search(r'Consumo-TUSD\s+F\.Ponta\s*\n\s*(kWh)\s*\n\s*([\d,.]+)', texto, re.IGNORECASE)
        consumo_ativo_na_ponta = re.search(r'Consumo Ativo Na Ponta\s*\n((?:.*\n){5})', texto, re.IGNORECASE)
        consumo_fora_ponta = re.search(r'Consumo Ativo Fora de Ponta\s*\n((?:.*\n){5})', texto, re.IGNORECASE)

        ref_mes_ano = ref_match.group(1) if ref_match else None
        vencimento = venc_match.group(1) if venc_match else None
        data_emissao = emissao_match.group(1) if emissao_match else None
        valor_total = valor_match.group(1) if valor_match else None
        data_leitura_anterior = leitura_anterior.group(1) if leitura_anterior else None
        data_leitura_atual = leitura_atual.group(1) if leitura_atual else None
        dias = int(numero_dias.group(1)) if numero_dias else None
        data_proxima_leitura = proxima_leitura.group(1) if proxima_leitura else None
        valor_energia = energia_inj.group(0) if energia_inj else None
        valor_consumo_tusdNp = f"{consumo_tusdNp.group(1)} {consumo_tusdNp.group(2)}" if consumo_tusdNp else None
        valor_consumo_tusdFp = f"{consumo_tusdFp.group(1)} {consumo_tusdFp.group(2)}" if consumo_tusdFp else None
        valor_consumo_ativo_ponta = ( consumo_ativo_na_ponta.group(1).strip().splitlines()[4].strip() if consumo_ativo_na_ponta else None )
        valor_consumo_fora_ponta = (consumo_fora_ponta.group(1).strip().splitlines()[4].strip() if consumo_fora_ponta else None )
        
        model = PdfModel(
                        MesRef=ref_mes_ano, 
                        Vencimento=vencimento, 
                        MesEmis=data_emissao, 
                        Valor=valor_total, 
                        LeituraAnt=data_leitura_anterior, 
                        LeituraAtu=data_leitura_atual, 
                        leituraPro=data_proxima_leitura, 
            NumDias=dias, 
            Energiainj=valor_energia, 
            consumoNap=valor_consumo_tusdNp, 
            ConsumoFop=valor_consumo_tusdFp, 
            ConsumoAnp=valor_consumo_ativo_ponta, 
            ConsumoAfp=valor_consumo_fora_ponta)
        
        return model
    
    def ObterDadosEmbasa(self, texto) -> PdfModel:
        valor_match = re.search(r'VALOR A PAGAR \(R\$\)\s*(?:\n\s*)*([\d.,]+)', texto, re.IGNORECASE)
        valor = valor_match.group(1) if valor_match else None
        
        titulos_match = re.search(r'Vencimento\s*M[êe]s/Ano\s*Emissão', texto, re.IGNORECASE)

        if titulos_match:
            valores_match = re.search(r'(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{4})', texto)
            if valores_match:
                vencimento = valores_match.group(1)
                emissao = valores_match.group(2)
                mes_ano = valores_match.group(3)
            else:
                vencimento = emissao = mes_ano = None
        else:
            vencimento = emissao = mes_ano = None
   
        data_leitura_anterior = re.search(r'Consumo\s*\(m³\)\s*(\d{2}/\d{2}/\d{4})', texto)
        data_leitura_atual = re.search(r'Cod\. Leitura\s*(\d{2}/\d{2}/\d{4})', texto)
        proxima_leitura = re.search(r'Dias de Consumo\s*\n\s*(\d{2}/\d{2}/\d{4})', texto)
        dias_consumo = re.search(r'Leitura Anterior\s*\n\s*(\d+)', texto)
        # Linha com os valores: A22HW0085520\n7722\n8090\n368
        leituras_match = re.search(r'Data Leitura Atual\s*[\w\d]+\s*(\d{4})\s*(\d{4})\s*\d+', texto)
        consumo_match = re.search(r'CONSUMO ÁGUA\s*(\d+)\s*M3', texto, re.IGNORECASE)
        
        
        valor_dataAnt = data_leitura_anterior.group(1) if data_leitura_anterior else None
        valor_dataAtu = data_leitura_atual.group(1) if data_leitura_atual else None
        valor_darapro = proxima_leitura.group(1) if proxima_leitura else None
        dias = dias_consumo.group(1) if dias_consumo else None
        leitAnt = leituras_match.group(1) if leituras_match else None
        leitAtu = leituras_match.group(2) if leituras_match else None
        valor_consumo = consumo_match.group(1) if consumo_match else None
        
        model = PdfModel(
            MesRef=mes_ano, Vencimento=vencimento, MesEmis=emissao, Valor=valor, 
            LeituraAnt=valor_dataAnt, LeituraAtu=valor_dataAtu, leituraPro=valor_darapro, 
            NumDias=dias, m3=valor_consumo, Energiainj="", consumoNap="", ConsumoFop="", ConsumoAnp=leitAnt, ConsumoAfp=leitAtu)
        
        return model
        
    def ObterDadosSaae(self, texto) -> PdfModel:
        datas = re.findall(r'\d{2}/\d{2}/\d{4}', texto)
        print(datas)
        anterior_data = datas[1] if len(datas) >= 3 else None
        atual_data = datas[2] if len(datas) >= 3 else None
        vencimento = datas[0] if len(datas) >= 3 else None

        # leitura_match = re.search(r'\b(\d{2,6})\s*\n\s*(\d{2,6})\s*\n\s*13/05/2025\s*\n\s*11/06/2025', texto)
        # anterior_leitura = leitura_match.group(1) if leitura_match else None
        # atual_leitura = leitura_match.group(2) if leitura_match else None

        # M³
        m3_match = re.search(r'(\d+)\s*M3', texto)
        m3 = m3_match.group(1) if m3_match else None

        # Dias
        # dias_match = re.search(r'\bDIAS\b\s*(?:\n\s*)*(\d+)', texto, re.IGNORECASE)
        # dias = dias_match.group(1) if dias_match else None
        dias = texto.splitlines()[45]

        # AGUA
        # agua_match = re.search(r'AGUA\s*\n\s*\d+\s*M3\s*\n\s*([\d,.]+)', texto, re.IGNORECASE)
        # agua = agua_match.group(1) if agua_match else None

        # ESGOTO
        # esgoto_match = re.search(r'ESGOTO\s*\n\s*\d+\s*M3\s*\n\s*([\d,.]+)', texto, re.IGNORECASE)
        # esgoto = esgoto_match.group(1) if esgoto_match else None

        # TCL
        # tcl_match = re.search(r'TCL-TAXA DE COLETA DE LIXO\s*(?:\n.*)?\n\s*([\d.,]+)', texto, re.IGNORECASE)
        # tcl = tcl_match.group(1) if tcl_match else None
        tcl = texto.splitlines()[63]
        
        # HIDRÔMETRO
        # hidro_match = re.search(r'CONSERVACAO DE HIDROMETRO\s*(?:\n.*)?\n\s*([\d.,]+)', texto, re.IGNORECASE)
        # hidrometro = hidro_match.group(1) if hidro_match else None
        hidrometro = texto.splitlines()[65]
        # FATURA
        # fatura_match = re.search(r'\b(\d{2}/\d{4})\b', texto)
        # fatura = fatura_match.group(1) if fatura_match else None
        fatura = texto.splitlines()[28]
        valor = texto.splitlines()[88]
        
        model = PdfModel(
            MesRef=fatura, Vencimento=vencimento, MesEmis="", Valor=valor, 
            LeituraAnt=anterior_data, LeituraAtu=atual_data, leituraPro="", 
            NumDias=dias, Energiainj="", consumoNap="", ConsumoFop="", ConsumoAnp="", ConsumoAfp="", tcl=tcl, hidrometro=hidrometro, m3=m3)
        
        return model     
    
