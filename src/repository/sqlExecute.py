from src.context.conexao import Conexao

class SQL:
    def __init__(self, empresa):
        conexao = Conexao(empresa)
        self.conn = conexao.conectar()
    
    def select(self, table, filter = "1=1"):
        try:
            if self.conn:
                cursor = self.conn.cursor()
                sql = f"SELECT * FROM {table} where 1=1 and {filter}"
                cursor.execute(sql)
                resultados = cursor.fetchall()
                if(len(resultados) > 0):
                    return resultados
                return ""
        except Exception as e:
            return ""
      