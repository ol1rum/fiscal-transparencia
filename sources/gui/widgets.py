from PySide6.QtWidgets import QProgressBar, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit
from PySide6.QtGui import QColor, QPainter, QPaintEvent, QLinearGradient, QBrush, QFont, QPixmap
from PySide6.QtCore import QTimer, Qt, QRect, QPropertyAnimation, QEasingCurve

from ..core.comuns import ler_css, resources, sizeP, alinhar


class progressBarAnimated(QProgressBar):

    def __init__(
            self,
            bg_color = '#858585',
            bar_color = '#25ff00',
            width = 150,
            height = 20,
            radius = 10
        ):
        super().__init__()

        if radius > height / 2:
            raise ValueError('Radius must be lower or equal to the half of height')
        
        self.bg_color = QColor(bg_color)
        self.bar_color = QColor(bar_color)
        self._height = height
        self._width = width
        self.radius = radius

        self.setFixedSize(self._width, self._height)

    def setValueAnimated(self, value, speed: int = 10):
        if value > 100 or value < 0:
            raise ValueError('The value must be between 0 and 100')

        self.animateTimer = QTimer(self)
        self.to_value = value
        self.animateTimer.timeout.connect(self.__animateValue)
        self.animateTimer.start(speed)
    
    def __animateValue(self):
        to_value = self.to_value
        
        if self.value() < to_value:
            self.setValue(self.value() + 1)

        elif self.value() > to_value: 
            self.setValue(self.value() - 1)

        elif self.value() == to_value:
            self.animateTimer.stop()
        
    
    def paintEvent(self, arg__1: QPaintEvent) -> None:

        pen = QPainter(self)
        pen.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen.setPen(Qt.PenStyle.NoPen)

        rect = QRect(0, 0, self._width, self._height)
        radius = self.radius

        # DESENHANDO FUNDO DA BARRA DE PROGRESSO
        pen.setBrush(QColor(self.bg_color))
        pen.drawRoundedRect(0, 0, rect.width(), rect.height(), radius, radius)

        # DESENHANDO A BARRA DE PROGRESSO
        gradient = QLinearGradient(0, 0, int(rect.width() * (self.value() / 100)), rect.height())
        color_green = QColor(self.bar_color)
        gradient.setColorAt(0, color_green.darker(200))
        gradient.setColorAt(1, color_green)

        # DESENHANDO O TEXTO
        # pen.drawText()

        
        pen.setBrush(QBrush(gradient))
        pen.drawRoundedRect(0, 0, int(rect.width() * (self.value() / 100)), rect.height(), radius, radius)

        pen.end()


class text_progressbar(QWidget):

    def __init__(
            self,
            text: str = 'Carregando...',
            bg_color = '#858585',
            bar_color = '#25ff00',
            width = 150,
            height = 20,
            radius = 10,
            font: QFont | None = None
            ):
        super().__init__()

        # =================================================================================================
        # Progress bar
        # =================================================================================================
        self.layout_progress = QVBoxLayout()
        self.layout_progress.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ========================================
        # label dos passos
        # ========================================a
        self.text = QLabel(text)

        if font:
            self.text.setFont(font)

        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ========================================
        # Progress bar
        # ========================================
        self.progress_bar = progressBarAnimated(bg_color, bar_color, width, height, radius)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ========================================
        # Adicionando widgets ao layout
        # ========================================
        self.layout_progress.setSpacing(13)
        self.layout_progress.addWidget(self.text)
        self.layout_progress.addWidget(self.progress_bar)

        self.setLayout(self.layout_progress)


class collapsibleWidget(QWidget):

    def __init__(
            self,
            button_text: str = "texto",
            info: str = "texto",
            button_height: int = 35
    ):
        super().__init__()
        # =================================================================================================
        # Construindo botão personalizado
        # ========================================
        # Botão
        # ========================================
        self.botao = QPushButton()

        self.botao.setObjectName('recolhido')
        self.botao.setFixedHeight(button_height)
        self.botao.setCursor(Qt.CursorShape.PointingHandCursor)
        self.botao.setCheckable(True)

        self.botao.clicked.connect(self.toggle_details)
        # ========================================
        # texto
        # ========================================
        self.texto = QLabel(button_text)
        self.texto.setObjectName('collapse')

        fonte_button = QFont('Open Sans', 12)
        self.texto.setFont(fonte_button)
        # ========================================
        # imagem seta
        # ========================================
        self.pixmap_seta_cima = QPixmap(str(resources / "imgs" / 'seta_cima.png'))
        self.pixmap_seta_cima.setDevicePixelRatio(12)

        self.pixmap_seta_baixo = QPixmap(str(resources / "imgs" / 'seta_baixo.png'))
        self.pixmap_seta_baixo.setDevicePixelRatio(12)

        self.seta = QLabel()
        self.seta.setPixmap(self.pixmap_seta_baixo)


        # ========================================
        # Layout do botão
        # ========================================
        self.lay_button = QHBoxLayout()
        self.lay_button.addWidget(self.texto)
        self.lay_button.addStretch()
        self.lay_button.addWidget(self.seta)

        self.botao.setLayout(self.lay_button)        

        # =================================================================================================
        # Detalhe
        # =================================================================================================
        self.detalhe_label = QLabel(info)
        self.detalhe_label.setObjectName('detalhe')
        fonte_text = QFont('Open Sans', 10)

        self.detalhe_label.setWordWrap(True)
        self.detalhe_label.setContentsMargins(0, 0, 0, 0)
        self.detalhe_label.setSizePolicy(sizeP.Expanding, sizeP.Fixed)
        self.detalhe_label.setFont(fonte_text)
        self.detalhe_label.setVisible(False)
        self.detalhe_label.setMaximumHeight(0)

        # =================================================================================================
        # Main layout
        # =================================================================================================
        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(self.botao)
        self.layout_main.addWidget(self.detalhe_label, alignment=alinhar.AlignTop)
        self.layout_main.setSpacing(0)

        # ========================================
        # Ajustes finais
        # ========================================
        self.setLayout(self.layout_main)
        self.setStyleSheet(ler_css(str(resources / 'css' / 'collapsible.css')))

        # =================================================================================================
        # Montando animação de abbertura dos detalhes
        # ========================================
        # Animação
        # ========================================
        self.animation = QPropertyAnimation(self.detalhe_label, b"maximumHeight")

        self.animation.setDuration(400)
        self.animation.setStartValue(0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.animation.finished.connect(self._on_animation_finished)

    def toggle_details(self):
        self.animation.stop()
        checked = self.botao.isChecked()

        if checked:
            # EXPANDIR
            self.detalhe_label.setVisible(True)
            self.seta.setPixmap(self.pixmap_seta_cima)
            self.botao.setObjectName('aberto')
            
            self.animation.setStartValue(self.detalhe_label.height())
            self.animation.setEndValue(self.detalhe_label.sizeHint().height())

            self.botao.style().unpolish(self.botao)
            self.botao.style().polish(self.botao)
        else:
            # RECOLHER
            self.seta.setPixmap(self.pixmap_seta_baixo)
            self.animation.setStartValue(self.detalhe_label.height())
            self.animation.setEndValue(0)
        
        self.animation.start()

    def _on_animation_finished(self):
        if not self.botao.isChecked():
            self.detalhe_label.setVisible(False)
            self.botao.setObjectName('recolhido')
            self.botao.style().unpolish(self.botao)
            self.botao.style().polish(self.botao)


class InputField(QLineEdit):

    def __init__(self, placeholder_text: str = ''):
        super().__init__()
        self.setPlaceholderText(placeholder_text)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        
