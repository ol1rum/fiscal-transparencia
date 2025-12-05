from PySide6.QtCore import QThread, Signal

from .pesquisa import pesquisar_pagamentos
from time import sleep


class ThreadPesquisa(QThread):
    proximo = Signal(str, int)
    concluido = Signal(list, int)

    def __init__(self, inscricao: str):
        super().__init__()
        self.inscricao = inscricao
        
    def run(self):
        sleep(1)
        pesq = pesquisar_pagamentos(self.inscricao)

        self.proximo.emit('Abrindo navegador...', 25)
        pesq.Abrir_navegador()

        self.proximo.emit('Carregando página...', 50)
        pesq.carregar_pagina()

        self.proximo.emit('Pesquisando CNPJ...', 75)
        pesq.pesquisar_cnpj()

        self.proximo.emit('Coletando Dados...', 90)
        pagamentos, ID = pesq.abrir_detalhes()
        self.proximo.emit('Concluído!', 100)

        sleep(1.5)
        self.concluido.emit(pagamentos, ID)
        