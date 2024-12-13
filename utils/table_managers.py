from PyQt5 import QtWidgets
from typing import List, Any
from utils.enums import TableColumns


class TableManager:
    """Менеджер для работы с таблицами"""

    def __init__(self, table_widget: QtWidgets.QTableWidget):
        self.table = table_widget
        self.setup_table()

    def setup_table(self) -> None:
        """Настройка таблицы"""
        self.table.setColumnCount(len(TableColumns))
        self.table.setRowCount(0)
        self.setup_headers()

    def setup_headers(self) -> None:
        """Настройка заголовков таблицы"""
        for column in TableColumns:
            item = QtWidgets.QTableWidgetItem(column.title)
            self.table.setHorizontalHeaderItem(column.index, item)

    def update_data(self, data: List[Any]) -> None:
        """Обновление данных в таблице"""
        self.table.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.table.insertRow(row_index)
            for col_index, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.table.setItem(row_index, col_index, item)

    def get_selected_row_data(self) -> List[str]:
        """Получение данных выбранной строки"""
        row = self.table.currentRow()
        if row >= 0:
            return [
                self.table.item(row, col).text()
                for col in range(self.table.columnCount())
            ]
        return []

    def clear_table(self) -> None:
        """Очистка таблицы"""
        self.table.setRowCount(0)