from src.context.conexao import Conexao
from datetime import datetime

class Faturas:
    def __init__(self, empresa):
        conexao = Conexao(empresa)
        self.conn = conexao.conectar()
    
    def select(self, chave):
        try:
            if self.conn:
                cursor = self.conn.cursor()
                criado = datetime.now()
                sql = "SELECT Valor FROM Faturas where 1=1 and Cancelado = 0 and CONCAT(Empresa,'-',cliente,'-',MesRef,'-', Vencimento) = ? and MONTH(criado) = ?"
                valores = (chave, criado.month)
                cursor.execute(sql, valores)
                resultados = cursor.fetchall()
                if(len(resultados) > 0):
                    return resultados[0][0]
                return ""
        except Exception as e:
            return ""
        
    def Insert(self, fatura):
        try:
            if self.conn:
                cursor = self.conn.cursor()
                sql = """
                    INSERT INTO Faturas (
                        Chave, Empresa, Cliente, Vencimento, MesRef,
                        MesEmis, Valor, Situacao, LeituraAnter, LeituraAtual,
                        LeituraProxi, NumDias, EnergiaInjetada, ConsumoAtivoNaPonta,
                        ConsumoAtivoForaDaPonta, ConsumoTUSDNPonta, ConsumoTUSDFPonta,
                        TaxaColetaLixo, ConservacaoHidrometro, MetroCubicos,
                        Cancelado, Arquivo, Base64File, Criado
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                valores = (
                    fatura.Chave, fatura.Empresa, fatura.Cliente, fatura.Vencimento, fatura.MesRef,
                    fatura.MesEmis, fatura.Valor, fatura.Situacao, fatura.LeituraAnter, fatura.LeituraAtual,
                    fatura.LeituraProxi, fatura.NumDias, fatura.EnergiaInjetada, fatura.ConsumoAtivoNaPonta,
                    fatura.ConsumoAtivoForaDaPonta, fatura.ConsumoTUSDNPonta, fatura.ConsumoTUSDFPonta,
                    fatura.TaxaColetaLixo, fatura.ConservacaoHidrometro, fatura.MetroCubicos,
                    fatura.Cancelado, fatura.Arquivo, fatura.Base64File, fatura.Criado
                )

                cursor.execute(sql, valores)
                self.conn.commit()
                print("Fatura inserida com sucesso.")
        except Exception as e:
            print("Erro ao inserir fatura:", e)
            
    def update(self, chave):
        try:
            if self.conn:
                cursor = self.conn.cursor()
                criado = datetime.now()
                sql = "update Faturas set Cancelado = 1 where 1=1 and Cancelado = 0 and CONCAT(Empresa,'-',cliente,'-',MesRef,'-', Vencimento) = ? and MONTH(criado) = ?"
                valores = (chave, criado.month)
                cursor.execute(sql, valores)
                self.conn.commit()
                return True
        except Exception as e:
            print(f"erro update: {e}")
            return False