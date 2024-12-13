from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox, QLineEdit,
                             QPushButton, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class FormConfig:
    """Базовая конфигурация для форм"""
    font_family: str = "Arial"
    default_font_size: int = 10
    button_min_width: int = 120
    button_min_height: int = 40
    field_height: int = 25
    margin: int = 10


class FormManager:
    """Менеджер форм"""

    def __init__(self):
        self.config = FormConfig()
        self.widgets: Dict[str, Any] = {}

    def create_label(self,
                     parent: QWidget,
                     text: str,
                     geometry: Optional[QRect] = None,
                     font_size: int = None,
                     is_bold: bool = False) -> QLabel:
        """Создание метки с улучшенными параметрами"""
        label = QLabel(parent)
        if geometry:
            label.setGeometry(geometry)

        label.setText(text)
        label.setAlignment(Qt.AlignCenter)

        font = QFont(self.config.font_family,
                     font_size or self.config.default_font_size)
        font.setBold(is_bold)
        label.setFont(font)

        return label

    def create_input_field(self,
                           parent: QWidget,
                           is_combo: bool = False,
                           name: str = "",
                           geometry: Optional[QRect] = None,
                           placeholder: str = "") -> QWidget:
        """Создание поля ввода с дополнительными параметрами"""
        widget = QComboBox(parent) if is_combo else QLineEdit(parent)

        if geometry:
            widget.setGeometry(geometry)

        if name:
            widget.setObjectName(name)
            self.widgets[name] = widget

        if placeholder and isinstance(widget, QLineEdit):
            widget.setPlaceholderText(placeholder)

        return widget

    def create_button(self,
                      parent: QWidget,
                      text: str,
                      geometry: Optional[QRect] = None,
                      font_size: Optional[int] = None,
                      color: str = "#2196F3",
                      is_action_button: bool = False) -> QPushButton:
        """Создание кнопки с улучшенным дизайном"""
        button = QPushButton(text, parent)

        if geometry:
            button.setGeometry(geometry)

        # Настройка размера
        button.setMinimumSize(self.config.button_min_width,
                              self.config.button_min_height)

        # Настройка шрифта
        font = QFont(self.config.font_family,
                     font_size or self.config.default_font_size)
        font.setBold(is_action_button)
        button.setFont(font)

        # Настройка стиля
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
        """)

        return button


class LayoutManager:
    """Менеджер компоновки с улучшенными параметрами"""

    @staticmethod
    def create_horizontal_layout(parent: QWidget,
                                 margin: int = 0,
                                 spacing: int = 10) -> QHBoxLayout:
        """Создание горизонтального layout с настраиваемыми параметрами"""
        layout = QHBoxLayout(parent)
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(spacing)
        return layout

    @staticmethod
    def create_vertical_layout(parent: QWidget,
                               margin: int = 0,
                               spacing: int = 10) -> QVBoxLayout:
        """Создание вертикального layout с настраиваемыми параметрами"""
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(spacing)
        return layout