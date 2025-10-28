import sys
from src.Apps.modules.Coelba import Coelba
from src.Apps.modules.Embasa import Embasa
from src.Apps.Saae.Robot import Saae
from src.services.log import Log
from src.services.pdf import LeitorPdf
if __name__ == "__main__":
    # parametro = sys.argv[1] if len(sys.argv) > 1 else None
    parametro = "Embasa"
    log = Log()
    coelba = Coelba()
    embasa = Embasa()
    saae = Saae()
    pdf = LeitorPdf()
    try:
        print("Iniciando do sistema ...")
        embasa.iniciar()
        # embasa.iniciar()
        #saae.iniciar()
         
    except Exception as e:
        if "ERR_CONNECTION_RESET" in str(e):
            print("Conexão resetada! Enviando e-mail...")
        log.processo(parametro,f"erro: {e}")
 