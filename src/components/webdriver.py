from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.services.log import Log
from datetime import datetime

class WebDrive:
    
    def __init__(self):
        self.log = Log()
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")  # Remove detecção de bot
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        prefs = {
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "profile.default_content_settings.popups": 0,
            "safebrowsing.enabled": True,
            "profile.default_content_setting_values.automatic_downloads": 1
        }

        options.add_experimental_option("prefs", prefs)
        
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")  # MUITO IMPORTANTE pro layout carregar certo
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36")

        # options.add_argument("--headless=new")  # Usa o novo modo headless (mais compatível)
        options.headless = False
        # service = Service("./config/chromedriver.exe")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    
    def acessar_site(self, url):
        self.driver.get(url)
    
    def fechar_navegador(self):
        self.driver.quit()
