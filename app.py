from PySide6.QtWidgets import QApplication
from sources.gui.main import FiscalTransparenciaApp
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = FiscalTransparenciaApp()
    window.showMaximized()

    sys.exit(app.exec())
    