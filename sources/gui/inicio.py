from PySide6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QFrame, QScrollArea, QSizePolicy, QWidget,
                               QHBoxLayout, QLineEdit, QStackedWidget)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, QTimer

from .widgets import text_progressbar, collapsibleWidget
from ..core.thread_pesquisa import ThreadPesquisa

from ..core.comuns import alinhar, resources

import sys

alinhar = Qt.AlignmentFlag
cursor = Qt.CursorShape
aspect = Qt.AspectRatioMode


class Inicio(QWidget):

    def __init__(self):
        super().__init__()
        self.buildUI()

    def buildUI(self):
        widget_inicio = self.inicio()

        layout_inicio = QHBoxLayout()
        layout_inicio.addWidget(widget_inicio)

        self.setLayout(layout_inicio)


    def inicio(self) -> QWidget:
        # =============== Logo ===============
        # -------- pixmap ---------
        self.logo_pixmap = QPixmap(str(resources / "imgs" / "logo.png"))
        self.logo_pixmap.setDevicePixelRatio(2.5)

        # -------- label ---------
        logo_label = QLabel()
        logo_label.setAlignment(alinhar.AlignLeft)
        logo_label.setPixmap(self.logo_pixmap)

        # =============== CAMPO DOS INPUTS ===============
        # -------- Inscrição ---------
        self.input_inscricao = QLineEdit()
        self.input_inscricao.setPlaceholderText("CPF ou CNPJ")
        self.input_inscricao.returnPressed.connect(self.pesquisar)

        # -------- Filtro ---------
        self.input_filtro = QLineEdit()
        self.input_filtro.setPlaceholderText("Filtrar")
        self.input_filtro.returnPressed.connect(self.filtrar)

        # -------- Layout ---------
        widget_inputs = QWidget()
        widget_inputs.setContentsMargins(0, 0, 0, 0)

        layout_inputs = QHBoxLayout()
        layout_inputs.addWidget(self.input_inscricao, stretch=1)
        layout_inputs.addWidget(self.input_filtro, stretch=2)
        widget_inputs.setLayout(layout_inputs)

        # =============== SEÇÃO DE PESQUISA ===============
        # -------- Resultados ---------
        self.resultados = QScrollArea()
        self.resultados.setWidgetResizable(True)
        self.resultados.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # -------- Carregando ---------
        info_fonte = QFont('Open Sans', 13)        
        self.barra = text_progressbar(width=550, height=30, radius=8, bar_color='#1D75CC', font=info_fonte)

        self.carregando = QWidget()
        layout_carregando = QVBoxLayout()
        layout_carregando.addWidget(self.barra)
        self.carregando.setLayout(layout_carregando)

        # -------- Juntando ---------
        self.campo_pesquisa = QStackedWidget()
        self.campo_pesquisa.addWidget(self.carregando)
        self.campo_pesquisa.addWidget(self.resultados)

        self.campo_pesquisa.setCurrentIndex(0)
        self.carregando.hide()

        # =============== LAYOUT DO INICIO ===============
        inicio_widget = QWidget()
        inicio_widget.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addWidget(logo_label)
        layout.addSpacing(20)
        layout.addWidget(widget_inputs)
        layout.addSpacing(20)
        layout.addWidget(self.campo_pesquisa)
        # layout.addStretch()   

        inicio_widget.setLayout(layout)
        return inicio_widget

    def pesquisar(self):
        # =============== VERIFICAÇÃO DE INSCRIÇÃO ===============
        numero_incricao = self.input_inscricao.text().replace('.','').replace('-','').replace('/','')
        if numero_incricao.isnumeric() and len(numero_incricao) in [11, 14]:
            pass
        else:
            self.inscricaoInvalida()
            return

        self.input_inscricao.setDisabled(True)
        self.input_filtro.setDisabled(True)

        self.carregando.show()
        # 1. Reseta a barra de progresso para o estado inicial
        self.barra.text.setText("Iniciando pesquisa...")
        self.barra.progress_bar.setValue(0)
        
        # 2. Mostra a tela de carregamento
        self.campo_pesquisa.setCurrentIndex(0)

        # 3. Inicia a nova pesquisa
        self.pesquisa = ThreadPesquisa(self.input_inscricao.text())
        self.pesquisa.proximo.connect(self.atualizarProgresso)
        self.pesquisa.concluido.connect(self.concluirPesquisa)

        self.pesquisa.start()

    def atualizarProgresso(self, texto, progresso):
        self.barra.text.setText(texto)
        self.barra.progress_bar.setValueAnimated(progresso)

    def concluirPesquisa(self, lista_pagamentos: list):
        self.lista_pagamentos = lista_pagamentos
        
        self.campo_pesquisa.setCurrentIndex(1)
        self.input_inscricao.setEnabled(True)
        self.input_filtro.setEnabled(True)

        self.criarLista(lista_pagamentos)

    def criarLista(self, lista_pagamentos: list):
        self.layout_dados = QVBoxLayout()
        self.layout_dados.setAlignment(alinhar.AlignTop | alinhar.AlignHCenter)

        for item in lista_pagamentos:            
            widget = collapsibleWidget(f"Data: {item['data']} | Valor: {item['valor']}", item['detalhe'], 35)
            widget.setMaximumWidth(800)
            self.layout_dados.addWidget(widget)

        self.layout_dados_center = QHBoxLayout()
        self.layout_dados_center.addLayout(self.layout_dados)
        container_resultados = QWidget()
        container_resultados.setLayout(self.layout_dados_center)
        self.resultados.setWidget(container_resultados)

    def filtrar(self):
        palavra_chave = self.input_filtro.text().lower()
        lista_filtrada = [item for item in self.lista_pagamentos if palavra_chave in item['detalhe'].lower()]
        
        self.criarLista(lista_filtrada)

    def inscricaoInvalida(self):
        self.input_inscricao.setStyleSheet("border: 1px solid red;")
        self.input_inscricao.setPlaceholderText("Inscrição inválida")

        voltar_placeholder = QTimer(self)
        voltar_placeholder.setSingleShot(True)
        voltar_placeholder.setInterval(2000)
        voltar_placeholder.timeout.connect(self.voltarPlaceholder)
        voltar_placeholder.start()

    def voltarPlaceholder(self):
        self.input_inscricao.setStyleSheet("border: 2px solid #ccc;")
        self.input_inscricao.setPlaceholderText("CPF ou CNPJ")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main_window = Inicio()
    main_window.show()

    app.exec()
