from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

from time import sleep
import sys

try:
    if sys.platform == "win32":
        from win32console import GetConsoleWindow
        from win32gui import ShowWindow
except ImportError:
    pass




class pesquisar_pagamentos():
     
    def __init__(self, inscricao: str):
        self.delay = 0.2
        self.inscricao = inscricao


    def Abrir_navegador(self):
        # =================================================================================================
        # COnfigurações iniciais
        # =================================================================================================

        # ========================================
        # Esconder Terminal
        # ========================================
        if sys.platform == "win32":
            try:
                if 'GetConsoleWindow' in globals() and 'ShowWindow' in globals():
                    hwnd = GetConsoleWindow()
                    ShowWindow(hwnd, 0)
            except Exception as e:
                print(f"Aviso: Não foi possível ocultar o console: {e}")
        
        # ========================================
        # Esconder janela do navegador
        # ========================================
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        # ========================================
        # Abrindo navegador
        # ========================================
        self.driver = webdriver.Edge(
            service=Service(
                executable_path=EdgeChromiumDriverManager(
                    url='https://msedgedriver.microsoft.com/',
                    latest_release_url='https://msedgedriver.microsoft.com/LATEST_RELEASE'
                ).install()),
            options=options
        )

    def carregar_pagina(self):
        self.driver.get("http://www.transparencia.feiradesantana.ba.gov.br/index.php?view=despesa")

    def pesquisar_cnpj(self):
        # =============== Verificação e formatação do numero de inscrição ===============
        numeros = self.inscricao.replace('.','').replace('-','').replace('/','')
        inscricao_formatada = ''

        # -------- CPF ---------
        if len(numeros) == 11:
            inscricao_formatada = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
    
        # -------- CNPJ ---------
        elif len(numeros) == 14:
            inscricao_formatada = f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:]}"

        cnpj_input = self.driver.find_element(By.ID, "cpfcnpj")
        cnpj_input.send_keys(inscricao_formatada)

        pesquisar = self.driver.find_element(By.XPATH, '//*[@id="formrel"]/div[2]/div/button')
        pesquisar.click()
        sleep(0.5)

    def abrir_detalhes(self):
        textos_detalhes = []
        resultados = self.driver.find_elements(By.CLASS_NAME, "accordion-toggle")
        num_results = len(resultados) - 1

        try:
            for n in range(num_results):
                det_txt = ''
                self.driver.find_element(By.XPATH, f'//*[@id="editable-sample"]/tbody/tr[{1+3*n}]/td[5]/button').click()
                sleep(self.delay)
                while not det_txt:
                    
                    det_txt = self.driver.find_element(By.XPATH, f'//*[@id="collapse{n}"]/div/table/tbody/tr[2]/td').text
                    data = self.driver.find_element(By.XPATH, f'//*[@id="editable-sample"]/tbody/tr[{1+3*n}]/td[1]').text
                    valor = self.driver.find_element(By.XPATH, f'//*[@id="editable-sample"]/tbody/tr[{1+3*n}]/td[4]').text

                    if 'tomba' in det_txt.lower():
                        pass
                    textos_detalhes.append({'data':data, 'valor':valor, 'detalhe':det_txt})

        except (NoSuchElementException, ElementClickInterceptedException) as erro:
            print('falha', erro.__class__, '\nRecarregando...')
            self.recarregar()
            
            
        # ========================================
        # configurando ID da pagina de despesas
        # ========================================
        id = 0
        for item in textos_detalhes:
            item: dict

            id += float(item['valor'][3:].replace('.','').replace(',','.'))

        self.driver.quit()  # saindo do webdriver

        return textos_detalhes, id
    
    def recarregar(self):
        self.driver.refresh()
        self.delay += 0.1
        sleep(1)

        WebDriverWait(self.driver, 20).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

        self.pesquisar_cnpj()
        self.abrir_detalhes()
    

if __name__ == '__main__':
    pesq = pesquisar_pagamentos('00000000000')
    pesq.Abrir_navegador()
    pesq.carregar_pagina()
    pesq.pesquisar_cnpj()
    pesq.abrir_detalhes()
