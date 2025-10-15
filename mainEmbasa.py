from src.RobotEmbasa import RPAEmbasa
from components.webdriver import Base
from src.services.files import File
from src.services.log import Log
from src.repository.faturas import Faturas

if __name__ == "__main__":
    log = Log()
    file = File()
    fat = Faturas("Embasa")
    try:
        auth = file.login_senha_embasa()
        log.iniciar("Embasa","Embasa 🏬")
        base = Base()
        base.acessar_site(auth["LinkLogin"])
        bot = RPAEmbasa(base.driver)
        bot.acessar(auth["Login"], auth["Senha"])
        base.acessar_site(auth["LinkVia"])
        bot.driver = base.driver
        bot.iniciar()
        base.fechar_navegador()
        log.finalizar("Embasa","Embasa 🏬")
        
    except Exception as e:
        log.erro("Embasa",e)