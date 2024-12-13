import sys
from PyQt5.QtWidgets import QApplication
from windows.main_window import MainWindow
from database_config import DatabaseConfig, init_database


def main():
    try:
        # Инициализация базы данных
        db_config = DatabaseConfig()
        init_database(db_config)

        # Запуск приложения
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())

    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()