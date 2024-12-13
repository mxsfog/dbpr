from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class BaseWindowConfig:
    """Базовая конфигурация окна"""
    title: str = "Window"
    width: int = 400
    height: int = 300
    font_size: int = 10
    button_height: int = 25
    margin: int = 10

@dataclass
class MainWindowConfig(BaseWindowConfig):
    """Конфигурация главного окна"""
    title: str = "Управление базой данных"
    width: int = 927
    height: int = 378
    table_margin: int = 40

@dataclass
class InsertDialogConfig(BaseWindowConfig):
    """Конфигурация окна добавления"""
    title: str = "Добавление записи"
    width: int = 438
    height: int = 381
    field_height: int = 25

@dataclass
class UpdateDialogConfig(BaseWindowConfig):
    """Конфигурация окна обновления"""
    title: str = "Обновление записи"
    width: int = 518
    height: int = 428
    field_height: int = 25

@dataclass
class ReferenceDialogConfig(BaseWindowConfig):
    """Конфигурация окна справочника"""
    title: str = "Справочник"
    width: int = 333
    height: int = 142