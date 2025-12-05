# 🏛️ Fiscal de Transparência (Web Scraper Desktop)

> Ferramenta de automação desktop desenvolvida em Python e PySide6 para auditoria e monitoramento de pagamentos públicos no portal da transparência.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Selenium](https://img.shields.io/badge/Selenium-Headless-green)
![PySide6](https://img.shields.io/badge/GUI-PySide6-red)

## 🎯 Objetivo
Facilitar o acesso e a fiscalização de contas públicas. O software automatiza a navegação no **Portal da Transparência de Feira de Santana/BA**, extraindo detalhes de pagamentos que normalmente exigiriam dezenas de cliques manuais e permitindo a filtragem rápida dos dados.

## ✨ Funcionalidades

* **🔍 Busca Dinâmica:** Permite consultar pagamentos de qualquer fornecedor informando apenas o **CPF** ou **CNPJ**. O sistema valida e formata os dados automaticamente antes da consulta.
* **📂 Extração Detalhada:** O robô navega em segundo plano (Headless), expande as linhas da tabela do portal e captura detalhes ocultos (como a descrição completa do empenho).
* **filtro Inteligente:** Possui um sistema de busca local que filtra os resultados baixados por palavras-chave em tempo real, facilitando encontrar pagamentos específicos (ex: "Limpeza", "Manutenção").
* **Resiliência:** Sistema de reconexão automática que detecta instabilidades no site da prefeitura e tenta retomar a coleta sem perder os dados.

## 🧠 Destaques Técnicos

* **Navegação Headless:** O navegador (Edge) roda em modo oculto, sem interferir no uso do computador.
* **Stealth Mode (Windows):** Utilização da API `win32console` para ocultar o terminal do Python, proporcionando uma experiência de aplicativo nativo.
* **Arquitetura Assíncrona:** A interface gráfica (GUI) não trava durante o scraping, pois o processo de busca roda em uma *Thread* separada, comunicando-se via *Signals*.

## 🛠️ Stack Tecnológica

* **Linguagem:** Python 3.x
* **Interface:** PySide6 (Qt for Python).
* **Automação Web:** Selenium WebDriver (com *WebDriverWait* para carregamento dinâmico).
* **Gerenciamento de Driver:** `webdriver-manager` (instala o driver do Edge automaticamente).
* **Integração OS:** `pywin32` (para manipulação de janelas no Windows).

## ⚙️ Instalação e Uso

### Pré-requisitos
* Python 3 instalado.
* Navegador Microsoft Edge instalado (o script utiliza o motor Chromium do Edge).

### Passo a Passo

1.  Clone o repositório:
    
        git clone https://github.com/ol1rum/fiscal-transparencia
        cd fiscal-transparencia

2.  Crie um ambiente virtual e instale as dependências:

        python -m venv venv
        .\venv\Scripts\activate
        pip install -r requirements.txt

3.  Execute a aplicação:

        python app.py

### Como Usar
1.  Insira o **CPF** ou **CNPJ** da empresa/pessoa que deseja fiscalizar.
2.  Clique em **Pesquisar** e aguarde a barra de progresso.
3.  Após a conclusão, use o campo "Filtrar" para encontrar termos específicos nos detalhes dos pagamentos.

---
*Desenvolvido por Murilo*
