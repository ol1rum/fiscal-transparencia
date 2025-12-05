from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import Qt
from pathlib import Path

# =================================================================================================
# Variaveis comuns
# =================================================================================================
dir_principal = Path(__file__).parent.parent.parent.absolute()
resources = dir_principal / 'resources'

alinhar = Qt.AlignmentFlag
sizeP = QSizePolicy.Policy

# =================================================================================================
# Funções comuns
# =================================================================================================
def ler_css(file: str):
    with open(file, 'r') as f:
        return f.read()


cores_paginas = ler_css(str(resources / 'css' / 'paginas.qss'))    

if __name__ == '__main__':
    print("Raiz:", dir_principal)
    print("Resources:", resources)
    # print(cores_paginas)