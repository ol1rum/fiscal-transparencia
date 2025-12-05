from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon

from .inicio import Inicio
from ..core.comuns import resources, cores_paginas


class FiscalTransparenciaApp(QMainWindow):

    def __init__(self):
        super().__init__()
    
        # ========================================
        # Configurações iniciais
        # ========================================
        self.setWindowTitle("Fiscal de Transparência")
        self.setStyleSheet(cores_paginas)
        self.setMinimumSize(650, 400)

        self.icone = QIcon(str(resources / "imgs" / "favicon.ico"))
        self.setWindowIcon(self.icone)
        
        self.buildUI()

    def buildUI(self):
        self.inicio = Inicio()
        self.setCentralWidget(self.inicio)
    