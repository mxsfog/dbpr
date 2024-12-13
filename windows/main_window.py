from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QTableWidget,
                             QVBoxLayout, QHBoxLayout, QFrame, QLabel,
                             QTableWidgetItem, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPalette


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система управления базой данных")
        self.setMinimumSize(1000, 600)
        self.setup_ui()

    def setup_ui(self):
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной вертикальный layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        header = QLabel("Управление данными")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Фрейм для кнопок управления
        button_frame = QFrame()
        button_frame.setFrameShape(QFrame.StyledPanel)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(10)

        # Создаем кнопки
        buttons = {
            'select': ('Поиск', '#4CAF50'),
            'insert': ('Добавить', '#2196F3'),
            'update': ('Изменить', '#FF9800'),
            'delete': ('Удалить', '#f44336')
        }

        for name, (text, color) in buttons.items():
            button = QPushButton(text)
            button.setMinimumSize(120, 40)
            button.setFont(QFont("Arial", 10))
            button.setProperty("class", name)
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
            button_layout.addWidget(button)
            setattr(self, f'btn_{name}', button)

        main_layout.addWidget(button_frame)

        # Создаем таблицу
        self.table = QTableWidget()
        self.setup_table()
        main_layout.addWidget(self.table)

        # Нижний статус бар с информацией
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Всего записей: 0")
        status_layout.addWidget(self.status_label)

        # Кнопка обновления
        refresh_button = QPushButton("Обновить")
        refresh_button.setMaximumWidth(100)
        status_layout.addWidget(refresh_button)

        main_layout.addLayout(status_layout)

    def setup_table(self):
        # Настройка таблицы
        headers = ['Фамилия', 'Имя', 'Отчество', 'Улица',
                   'Дом', 'Корпус', 'Квартира', 'Телефон']

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Настройка внешнего вида таблицы
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        # Растягиваем столбцы
        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, header.Stretch)

        # Настройка заголовков
        header.setFont(QFont("Arial", 10, QFont.Bold))
        header.setFixedHeight(40)

        # Настройка строк
        self.table.verticalHeader().setVisible(False)
        self.table.setRowHeight(0, 35)

    def add_row_to_table(self, data):
        """Добавление строки в таблицу"""
        row = self.table.rowCount()
        self.table.insertRow(row)

        for col, value in enumerate(data):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, col, item)

    def clear_table(self):
        """Очистка таблицы"""
        self.table.setRowCount(0)

    def update_status(self, count):
        """Обновление статуса"""
        self.status_label.setText(f"Всего записей: {count}")