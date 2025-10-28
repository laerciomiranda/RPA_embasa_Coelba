from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class Interacoes:
    def __init__(self, driver):
        self.driver = driver

    def esperar_elemento(self, by, valor, timeout=1000):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, valor))
            )
        except:
            return False

    def esperar_elemento_lista(self, by, element, valor, timeout=1000):
        return WebDriverWait(element, timeout).until(
            EC.visibility_of_element_located((by, valor))
        )

    def clicar_elemento(self, by, valor):
        elemento = self.esperar_elemento(by, valor)
        elemento.click()

    def preencher_campo(self, by, valor, texto):
        campo = self.esperar_elemento(by, valor)
        campo.click()
        campo.clear()
        campo.send_keys(texto)
        
    def listar_itens_ul(self, by, valor, ul_elemento):
        return ul_elemento.find_elements(by, valor)
    
    def esperar_elementos(self, by, valor):
        return self.driver.find_elements(by, valor)
        
    def clicar_item_lista(sell, li_element, by, valor, timeout=1000):
        elemento = WebDriverWait(li_element, timeout).until(
            EC.visibility_of_element_located((by, valor))
        )
        elemento.click()
        
    def mudar_de_pagina(self, url):
        self.driver.get(url)
    
    def proximaPagina(self, elemento, by, valor, timeout=2):
        try:
            element = WebDriverWait(elemento, timeout).until(
                EC.visibility_of_element_located((by, valor))
            )
            aria_disabled = element.get_attribute("aria-disabled")
            if aria_disabled:
                return False
            self.driver.execute_script("arguments[0].click();", element)
            
        except Exception as e:
            return False
    
    def pegar_texto_div(self, elemento, by, valor, timeout=1000):
        element = WebDriverWait(elemento, timeout).until(
            EC.visibility_of_element_located((by, valor))
        )
        return element.text
    
    def voltar_Pagina(self):
        self.driver.execute_script("window.history.go(-1);")
    
    def executar_Js(self, cod, elemento):
        self.driver.execute_script(cod, elemento)
    
    def elemento_existe(self, by, valor, elemento = None):
        if elemento is None:
            return len(self.driver.find_elements(by, valor)) > 0
        return len(elemento.find_elements(by, valor)) > 0
    
    def frase_existe(self, by, texto):
        return len(self.driver.find_elements(by, texto)) > 0
    
    def printHtml(self, elemento):
        print(elemento.get_attribute("outerHTML"))
    
    def executar_Js_seletor(self, cod):
        return self.driver.execute_script(cod)

    def esperar_loading_sumir(self, by, valor, timeout=1000):
        try:
            print("⏳ Aguardando loading desaparecer...")
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by, valor))
            )
            print("✅ Loading finalizado.")
        except Exception as e:
            print("⚠️ Timeout ao esperar loading desaparecer:", e)
