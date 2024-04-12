import os
import shutil
import sys
import zipfile

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt
from qtpy import QtCore


def filter_list(list_widget, text):
    text_lower = text.lower()
    for i in range(list_widget.count()):
        list_widget.item(i).setHidden(text_lower not in list_widget.item(i).text().lower())


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Окно
        self.setWindowTitle("E-Book Manager")
        self.move(475, 225)
        self.setFixedSize(1027, 475)
        self.setWindowIcon(QtGui.QIcon('bookshelf-icon.png'))

        self.custom_books_lib_widget = None

        # Списки
        self.comp_list = MyListWidget(self)
        self.stor_list = MyListWidget(self)

        self.comp_list.setGeometry(290, 140, 360, 325)
        self.stor_list.setGeometry(660, 140, 360, 325)

        self.populate_list(self.comp_list, "iofolder/comp_path.txt")
        self.populate_list(self.stor_list, "iofolder/stor_path.txt")

        self.comp_list.setDragEnabled(True)
        self.comp_list.setAcceptDrops(True)
        self.comp_list.setDropIndicatorShown(True)
        self.comp_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.comp_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.comp_list.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

        self.stor_list.setDragEnabled(True)
        self.stor_list.setAcceptDrops(True)
        self.stor_list.setDropIndicatorShown(True)
        self.stor_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.stor_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.stor_list.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

        # Поля ввода
        self.comp_TextField = QtWidgets.QLineEdit(self)
        self.stor_TextField = QtWidgets.QLineEdit(self)

        self.comp_search = QtWidgets.QLineEdit(self)
        self.stor_search = QtWidgets.QLineEdit(self)

        self.comp_TextField.setText(self.path_checker("iofolder/comp_path.txt"))
        self.stor_TextField.setText(self.path_checker("iofolder/stor_path.txt"))

        self.comp_TextField.setGeometry(10, 20, 800, 25)
        self.stor_TextField.setGeometry(10, 70, 800, 25)

        self.comp_search.setGeometry(290, 110, 360, 25)
        self.stor_search.setGeometry(660, 110, 360, 25)

        self.comp_search.textChanged.connect(lambda: filter_list(self.comp_list, self.comp_search.text()))
        self.stor_search.textChanged.connect(lambda: filter_list(self.stor_list, self.stor_search.text()))

        # Лейблы

        self.comp_label = QtWidgets.QLabel(self)
        self.stor_label = QtWidgets.QLabel(self)

        self.comp_label.move(10, 5)
        self.comp_label.setText("<b>Папка 1:</b>")
        self.comp_label.adjustSize()

        self.stor_label.move(10, 55)
        self.stor_label.setText("<b>Папка 2:</b>")
        self.stor_label.adjustSize()
        # Кнопки

        self.dial1 = QtWidgets.QPushButton(self)
        self.dial2 = QtWidgets.QPushButton(self)

        self.dial1.move(825, 18)
        self.dial1.setText("...")
        self.dial1.adjustSize()
        self.dial1.clicked.connect(lambda: self.get_dir(self.comp_TextField))

        self.dial2.move(825, 68)
        self.dial2.setText("...")
        self.dial2.adjustSize()
        self.dial2.clicked.connect(lambda: self.get_dir(self.stor_TextField))

        self.resort_btn = QtWidgets.QPushButton(self)

        self.resort_btn.setText("Перезапуск")
        self.resort_btn.setGeometry(10, 150, 250, 30)
        self.resort_btn.clicked.connect(self.restart)

        self.save_button = QtWidgets.QPushButton("Сохранить", self)
        self.save_button.setGeometry(10, 200, 250, 30)
        self.save_button.clicked.connect(self.save_changes)

        self.send_comp_dir = QtWidgets.QPushButton(self)
        self.send_stor_dir = QtWidgets.QPushButton(self)

        self.send_comp_dir.setText("Отправить")
        self.send_comp_dir.move(925, 18)
        self.send_comp_dir.adjustSize()
        self.send_comp_dir.clicked.connect(
            lambda: self.path_sender(self.comp_TextField.text(), "iofolder/comp_path.txt"))

        self.send_stor_dir.move(925, 68)
        self.send_stor_dir.setText("Отправить")
        self.send_stor_dir.adjustSize()
        self.send_stor_dir.clicked.connect(
            lambda: self.path_sender(self.stor_TextField.text(), "iofolder/stor_path.txt"))

        """Добавление кнопки вызова кастомного виджета"""
        self.custom_books_lib_btn = QtWidgets.QPushButton("Открыть каталог книг", self)
        self.custom_books_lib_btn.setGeometry(10, 250, 250, 30)
        self.custom_books_lib_btn.clicked.connect(self.open_custom_books_lib_widget)

    def open_custom_books_lib_widget(self):
        """Создание и отображение кастомного виджета"""
        if os.path.exists("BooksLib"):
            pass
        else:
            os.mkdir("BooksLib")
        self.custom_books_lib_widget = CustomBooksLibWidget(self)
        self.setDisabled(True)
        self.custom_books_lib_widget.show()

    def process_directory1(self, directory_path1, items1):
        """Обрабатываем папку file_path1"""
        for item in os.listdir(directory_path1):
            item_path = os.path.join(directory_path1, item)
            if item not in items1 and os.path.isfile(item_path):
                current_widget = self.sender().parentWidget().findChild(QtWidgets.QListWidget)
                destination = os.path.join(self.path_checker("iofolder/stor_path.txt"), item)
                shutil.move(item_path, destination)
                existing_item = current_widget.findItems(item, Qt.MatchExactly)
                if existing_item:
                    existing_item[0].setData(Qt.UserRole, destination)

    def process_directory2(self, directory_path2, items2):
        """Обрабатываем папку file_path2"""
        for item in os.listdir(directory_path2):
            item_path = os.path.join(directory_path2, item)
            if item not in items2 and os.path.isfile(item_path):
                current_widget = self.sender().parentWidget().findChild(QtWidgets.QListWidget)
                destination = os.path.join(self.path_checker("iofolder/comp_path.txt"), item)
                shutil.move(item_path, destination)
                existing_item = current_widget.findItems(item, Qt.MatchExactly)
                if existing_item:
                    existing_item[0].setData(Qt.UserRole, destination)

    def get_dir(self, text_field):
        """Открываем проводник и выбираем папку"""
        dir_list = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        text_field.setText(dir_list)

    def restart(self):
        """Перезаполняем списки"""

        self.comp_list.clear()
        self.stor_list.clear()
        self.populate_list(self.comp_list, "iofolder/comp_path.txt")
        self.populate_list(self.stor_list, "iofolder/stor_path.txt")

        """Обновление содержимого полей ввода"""

        self.comp_TextField.setText(self.path_checker("iofolder/comp_path.txt"))
        self.stor_TextField.setText(self.path_checker("iofolder/stor_path.txt"))

        """Очищение фильтров"""

        self.comp_search.clear()
        self.stor_search.clear()

    def save_changes(self):
        """Сохраняем изменения в файлах, но не в папках"""
        directory_path1, directory_path2 = self.get_directory_paths()
        items1 = [self.comp_list.item(i).text() for i in range(self.comp_list.count())]
        items2 = [self.stor_list.item(i).text() for i in range(self.stor_list.count())]
        if directory_path1 != directory_path2:
            self.process_directory1(directory_path1, items1)
            self.process_directory2(directory_path2, items2)
            self.restart()

    def path_checker(self, path):
        """Проверяем путь. В случае, если файл не найден, возвращаем C:\\Users"""
        with open(path, encoding="utf8") as f:
            first_line = f.readline().strip()
            if first_line:
                if os.path.exists(first_line):
                    return first_line

            return os.getenv("SystemDrive") + "\\"

    def path_sender(self, new_path, txt_path):
        """Записываем путь в файл"""
        with open(txt_path, "w", encoding="utf8") as f:
            f.write(new_path)

        self.restart()

    def populate_list(self, list_widget, file_path):
        """Заполняем список"""
        directory_path = self.path_checker(file_path)

        for filename in os.listdir(directory_path):
            item = QListWidgetItem(filename)
            item.setData(Qt.UserRole, os.path.join(directory_path, filename))  # Store full file path in UserRole data
            list_widget.addItem(item)

    def get_files_in_directory(self, directory_path):
        """Получаем список файлов в папке"""
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        return files

    def get_directory_paths(self):
        """Получаем пути к директориям"""
        path1 = self.path_checker("iofolder/comp_path.txt")
        path2 = self.path_checker("iofolder/stor_path.txt")
        return path1, path2


class MyListWidget(QtWidgets.QListWidget):
    def __init__(self, main_window):
        super(MyListWidget, self).__init__(main_window)
        self.rename_widget = None
        self.main_window = main_window

        # Создание контекстного меню
        self.contextMenu = QtWidgets.QMenu(self)

        self.deleteAction = QtWidgets.QAction("Удалить", self)
        self.contextMenu.addAction(self.deleteAction)

        self.renameAction = QtWidgets.QAction("Переименовать", self)
        self.contextMenu.addAction(self.renameAction)

        # Подключение сигнала к действию удаления
        self.deleteAction.triggered.connect(self.delete_selected_item)
        self.renameAction.triggered.connect(self.rename_selected_item)

    def contextMenuEvent(self, event):
        # Отображение контекстного меню при нажатии ПКМ

        self.contextMenu.exec_(event.globalPos())

    def delete_selected_item(self):
        """Удаление выбранного элемента"""
        item = self.currentItem()

        if item.text() is not None:
            reply = QMessageBox.question(self, 'Файл будет удалён',
                                     f'Вы не сможете восстановить {item.text()}\nХотите продолжить?',
                                     QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:

                file_path = item.data(Qt.UserRole)

                if os.path.exists(file_path):
                    os.remove(file_path)

                self.takeItem(self.row(item))

    def rename_selected_item(self):
        # Переименование выбранного элемента
        item = self.currentItem()
        new_path = ""

        new_name, ok = QtWidgets.QInputDialog.getText(self, f"Переименовывание {item}", "Введите новое имя файла:")

        if ok:

            old_path = item.data(Qt.UserRole)

            try:
                new_path = old_path[:-len(item.text())] + new_name + "." + item.text().rsplit(".", 1)[-1]

            except Exception:
                new_path = old_path[:-len(item.text())] + new_name

            os.rename(old_path, new_path)
            self.main_window.restart()


class CustomBooksLibWidget(QtWidgets.QWidget):
    def __init__(self, main_window):
        super(CustomBooksLibWidget, self).__init__()
        self.main_window = main_window
        self.initUI()
        self.setWindowIcon(QtGui.QIcon('bookshelf-icon.png'))
        # Окно
        self.setWindowTitle("BooksLib Manager")
        self.setFixedSize(525, 330)
        self.move(710, 330)

        # Список
        self.assembly_list = QtWidgets.QListWidget(self)
        self.assembly_list.setGeometry(220, 55, 300, 268)

        self.populate_assembly_list()

        # Лейблы

        self.add_label = QtWidgets.QLabel(self)
        self.add_label.setText("Добавление новой папки:")
        self.add_label.setGeometry(5, 5, 400, 25)

        # Поле ввода
        self.add_field = QtWidgets.QLineEdit(self)
        self.assembly_search = QtWidgets.QLineEdit(self)

        self.add_field.setGeometry(5, 25, 200, 25)
        self.assembly_search.setGeometry(220, 25, 300, 25)

        self.assembly_search.textChanged.connect(lambda: filter_list(self.assembly_list, self.assembly_search.text()))

        # Кнопки
        self.choose_button = QtWidgets.QPushButton("Выбрать", self)
        self.choose_button.setGeometry(5, 55, 200, 50)
        self.choose_button.clicked.connect(self.choose_item_to_manipulate)

        self.add_button = QtWidgets.QPushButton("Добавить", self)
        self.add_button.setGeometry(5, 110, 200, 50)
        self.add_button.clicked.connect(self.add_item)

        self.delete_button = QtWidgets.QPushButton("Удалить", self)
        self.delete_button.setGeometry(5, 165, 200, 50)
        self.delete_button.clicked.connect(self.delete_item)

        self.archive_button = QtWidgets.QPushButton("Архивировать", self)
        self.archive_button.setGeometry(5, 220, 200, 50)
        self.archive_button.clicked.connect(self.archive_directory)

        self.unpack_button = QtWidgets.QPushButton("Разархивировать", self)
        self.unpack_button.setGeometry(5, 275, 200, 50)
        self.unpack_button.clicked.connect(self.unpack_zip_file)

    def save_widget_changes(self):
        """Выводим изменения"""
        self.assembly_list.clear()
        self.populate_assembly_list()

    def unpack_zip_file(self):
        """Разархивируем zip-архив"""
        selected_item = self.assembly_list.currentItem()
        if zipfile.is_zipfile("BooksLib/" + selected_item.text()):
            directory_path = "BooksLib/" + selected_item.text()[0:-5]  # Удаляем расширение и эмодзи
            zip_name = directory_path + "📚.zip"
            with zipfile.ZipFile(zip_name, 'r') as zip_file:
                zip_file.extractall(directory_path)

            zip_file.close()  # Закрываем zip-архив
            os.remove(zip_name)  # Удаляем zip-архив

            self.save_widget_changes()

    def archive_directory(self):
        """Архивируем папку"""
        directory_path = "BooksLib/" + self.assembly_list.currentItem().text()
        if os.path.isdir(directory_path)\
                and directory_path != self.main_window.path_checker("iofolder/stor_path.txt"):
            zip_name = directory_path + "📚.zip"
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(directory_path):
                    for file in files:
                        file_path = os.path.join(root, file)  # Получаем путь к файлу
                        zip_file.write(file_path, os.path.relpath(file_path, directory_path))  # Записываем файл в архив

            zip_file.close()  # Закрываем zip-архив
            shutil.rmtree(directory_path)  # Удаляем исходную директорию после архивации

            self.save_widget_changes()

    def add_item(self):
        """Создаём новую папку"""
        if self.add_field.text() != "":
            new_path = os.path.join("BooksLib", self.add_field.text())
            os.mkdir(new_path)
            self.save_widget_changes()
        self.add_field.setText("")

    def choose_item_to_manipulate(self):
        """Выбираем папку"""
        selected_item = self.assembly_list.currentItem()

        if os.path.isdir("BooksLib/" + selected_item.text()):
            widget_directory_path = "BooksLib/" + selected_item.text()
            self.widget_path_sender(widget_directory_path)

            self.main_window.setEnabled(True)
            self.main_window.restart()
            self.hide()

    def initUI(self):
        self.setWindowTitle('Custom Close Button Example')
        self.setGeometry(400, 250, 1000, 500)

    def closeEvent(self, event):
        self.main_window.setEnabled(True)
        self.main_window.restart()
        self.hide()
        event.accept()

    def delete_item(self):
        """Удаляем папку"""
        selected_item = self.assembly_list.currentItem()
        if selected_item is not None:
            shutil.rmtree("BooksLib/" + selected_item.text())
            self.save_widget_changes()

    def widget_path_sender(self, new_path):
        """Записываем путь в файл"""
        with open("iofolder/stor_path.txt", "w", encoding="utf8") as f:
            f.write(new_path)

    def get_dirs_in_directory(self):
        """Получаем список директорий в BooksLib"""
        dirs = [f for f in os.listdir("BooksLib") if
                os.path.isdir(os.path.join("BooksLib", f))
                or
                zipfile.is_zipfile(os.path.join("BooksLib", f))]

        return dirs

    def populate_assembly_list(self):
        dirs_in_directory = self.get_dirs_in_directory()
        self.assembly_list.addItems(dirs_in_directory)
