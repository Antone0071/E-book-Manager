import os
import shutil
import sys

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from qtpy import QtCore


class CustomBooksLibWidget(QtWidgets.QWidget):
    def __init__(self, main_window):
        super(CustomBooksLibWidget, self).__init__()
        self.main_window = main_window
        self.initUI()
        # Окно
        self.setWindowTitle("BooksLib Manager")
        self.move(400, 250)
        self.setFixedSize(1000, 500)

        # Список
        self.assembly_list = QtWidgets.QListWidget(self)
        self.assembly_list.setGeometry(425, 55, 450, 405)

        self.populate_assembly_list()

        # Лейблы

        self.add_label = QtWidgets.QLabel(self)
        self.add_label.setText("Добавление новой папки:")
        self.add_label.setGeometry(5, 5, 400, 25)

        # Поле ввода
        self.add_field = QtWidgets.QLineEdit(self)
        self.add_field.setGeometry(5, 25, 800, 25)

        # Кнопки
        self.delete_button = QtWidgets.QPushButton("Удалить", self)
        self.delete_button.setGeometry(5, 250, 200, 50)
        self.delete_button.clicked.connect(self.delete_item)

        self.add_button = QtWidgets.QPushButton("Добавить", self)
        self.add_button.setGeometry(5, 325, 200, 50)
        self.add_button.clicked.connect(self.add_item)

        self.choose_button = QtWidgets.QPushButton("Выбрать", self)
        self.choose_button.setGeometry(5, 400, 200, 50)
        self.choose_button.clicked.connect(self.choose_item_to_manipulate)

    def save_widget_changes(self):
        """Выводим изменения"""
        self.assembly_list.clear()
        self.populate_assembly_list()

    def add_item(self):
        """Создаём новую папку"""
        if self.add_field.text() != "":
            new_path = os.path.join("BooksLib", self.add_field.text())
            os.mkdir(new_path)
            self.save_widget_changes()

    def choose_item_to_manipulate(self):
        """Выбираем папку"""
        if self.assembly_list.selectedItems():
            selected_item = self.assembly_list.currentItem()
            widget_directory_path = "BooksLib/" + selected_item.text()
            self.widget_path_sender(widget_directory_path)

            """self.main_window.setEnabled(True)"""
            self.main_window.restart()
            self.hide()

    def initUI(self):
        self.setWindowTitle('Custom Close Button Example')
        self.setGeometry(400, 250, 1000, 500)

    def closeEvent(self, event):
        """self.main_window.setEnabled(True)"""
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
        dirs = [f for f in os.listdir("BooksLib") if os.path.isdir(os.path.join("BooksLib", f))]
        return dirs

    def populate_assembly_list(self):
        dirs_in_directory = self.get_dirs_in_directory()
        self.assembly_list.addItems(dirs_in_directory)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Окно
        self.setWindowTitle("E-Book Manager")
        self.move(275, 150)
        self.setFixedSize(1400, 700)

        self.custom_books_lib_widget = None

        # Списки
        self.list1 = QtWidgets.QListWidget(self)
        self.list2 = QtWidgets.QListWidget(self)

        self.list1.setGeometry(350, 155, 400, 530)
        self.list2.setGeometry(750, 155, 400, 530)

        self.populate_list(self.list1, "iofolder/comp_path.txt")
        self.populate_list(self.list2, "iofolder/stor_path.txt")

        self.list1.setDragEnabled(True)
        self.list1.setAcceptDrops(True)
        self.list1.setDropIndicatorShown(True)
        self.list1.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.list1.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list1.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

        self.list2.setDragEnabled(True)
        self.list2.setAcceptDrops(True)
        self.list2.setDropIndicatorShown(True)
        self.list2.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.list2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list2.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

        # Поля ввода
        self.comp_TextField = QtWidgets.QLineEdit(self)
        self.stor_TextField = QtWidgets.QLineEdit(self)

        self.comp_TextField.setText(self.path_checker("iofolder/comp_path.txt"))
        self.stor_TextField.setText(self.path_checker("iofolder/stor_path.txt"))

        self.comp_TextField.setGeometry(10, 30, 1000, 25)
        self.stor_TextField.setGeometry(10, 90, 1000, 25)

        # Лейблы

        self.comp_label = QtWidgets.QLabel(self)
        self.stor_label = QtWidgets.QLabel(self)

        self.comp_label.move(10, 10)
        self.comp_label.setText("<b>Папка 1:</b>")
        self.comp_label.adjustSize()

        self.stor_label.move(10, 70)
        self.stor_label.setText("<b>Папка 2:</b>")
        self.stor_label.adjustSize()
        # Кнопки

        self.dial1 = QtWidgets.QPushButton(self)
        self.dial2 = QtWidgets.QPushButton(self)

        self.dial1.move(1025, 28)
        self.dial1.setText("...")
        self.dial1.adjustSize()
        self.dial1.clicked.connect(lambda: self.get_dir(self.comp_TextField))

        self.dial2.move(1025, 88)
        self.dial2.setText("...")
        self.dial2.adjustSize()
        self.dial2.clicked.connect(lambda: self.get_dir(self.stor_TextField))

        self.resort_btn = QtWidgets.QPushButton(self)

        self.resort_btn.setText("Перезапуск")
        self.resort_btn.adjustSize()
        self.resort_btn.move(1250, 250)
        self.resort_btn.clicked.connect(self.restart)

        self.save_button = QtWidgets.QPushButton("Сохранить", self)
        self.save_button.move(1250, 300)
        self.save_button.adjustSize()
        self.save_button.clicked.connect(self.save_changes)

        self.send_comp_dir = QtWidgets.QPushButton(self)
        self.send_stor_dir = QtWidgets.QPushButton(self)

        self.send_comp_dir.move(1125, 28)
        self.send_comp_dir.setText("Отправить")
        self.send_comp_dir.adjustSize()
        self.send_comp_dir.clicked.connect(
            lambda: self.path_sender(self.comp_TextField.text(), "iofolder/comp_path.txt"))

        self.send_stor_dir.move(1125, 88)
        self.send_stor_dir.setText("Отправить")
        self.send_stor_dir.adjustSize()
        self.send_stor_dir.clicked.connect(
            lambda: self.path_sender(self.stor_TextField.text(), "iofolder/stor_path.txt"))

        """Добавление кнопки вызова кастомного виджета"""
        self.custom_books_lib_btn = QtWidgets.QPushButton("Открыть каталог книг", self)
        self.custom_books_lib_btn.move(1250, 350)
        self.custom_books_lib_btn.adjustSize()
        self.custom_books_lib_btn.clicked.connect(self.open_custom_books_lib_widget)

    def open_custom_books_lib_widget(self):
        """Создание и отображение кастомного виджета"""
        self.custom_books_lib_widget = CustomBooksLibWidget(self)

        self.setDisabled(True)
        self.custom_books_lib_widget.show()

    def process_directory1(self, directory_path, items1):
        """Обрабатываем папку file_path1"""
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if item not in items1 and os.path.isfile(item_path):
                destination = os.path.join(self.path_checker("iofolder/stor_path.txt"), item)
                shutil.move(item_path, destination)

    def process_directory2(self, directory_path, items2):
        """Обрабатываем папку file_path2"""
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if item not in items2 and os.path.isfile(item_path):
                destination = os.path.join(self.path_checker("iofolder/comp_path.txt"), item)
                shutil.move(item_path, destination)

    def get_dir(self, text_field):
        """Открываем проводник и выбираем папку"""
        dir_list = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        text_field.setText(dir_list)

    def restart(self):
        """Перезапуск программы"""
        QtCore.QCoreApplication.quit()
        QtCore.QProcess.startDetached(sys.executable, sys.argv)

    def save_changes(self):
        """Сохраняем изменения в файлах, но не в папках"""
        directory_path1, directory_path2 = self.get_directory_paths()
        items1 = [self.list1.item(i).text() for i in range(self.list1.count())]
        items2 = [self.list2.item(i).text() for i in range(self.list2.count())]
        if directory_path1 != directory_path2:
            self.process_directory1(directory_path1, items1)
            self.process_directory2(directory_path2, items2)
            self.list1.clear()
            self.list2.clear()
            self.populate_list(self.list1, "iofolder/comp_path.txt")
            self.populate_list(self.list2, "iofolder/stor_path.txt")

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

    def populate_list(self, list_widget, file_path):
        """Заполняем список"""
        directory_path = self.path_checker(file_path)
        files_in_directory = self.get_files_in_directory(directory_path)
        list_widget.addItems(files_in_directory)

    def get_files_in_directory(self, directory_path):
        """Получаем список файлов в папке"""
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        return files

    def get_directory_paths(self):
        """Получаем пути к директориям"""
        path1 = self.path_checker("iofolder/comp_path.txt")
        path2 = self.path_checker("iofolder/stor_path.txt")
        return path1, path2

    def start_drag(self, event):
        """Начало перетаскивания"""
        item = self.list2.currentItem()
        if item:
            pixmap = QtGui.QPixmap(item.size())
            item.render(pixmap)

            mime_data = QtCore.QMimeData()
            mime_data.setData("application/x-qabstractitemmodeldatalist", item.data(QtCore.Qt.UserRole))

            drag = QtGui.QDrag(self.list2)
            drag.setMimeData(mime_data)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos() - item.rect().topLeft())

            if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
                self.list2.takeItem(self.list2.row(item))
                self.list1.addItem(item.text())

    def dragEnterEvent(self, event):
        """Принимаем перетаскивание"""
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Приём перетаскивания"""
        data = event.mimeData().data('application/x-qabstractitemmodeldatalist')
        stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)

        if self.list1.rect().contains(event.pos()):
            target_list = self.list1

        else:
            target_list = self.list2

        while not stream.atEnd():
            row, column, parent = QtCore.QModelIndex(), QtCore.QModelIndex(), QtCore.QModelIndex()
            stream >> row >> column >> parent
            item = target_list.model().data(row, QtCore.Qt.DisplayRole)
            target_list.addItem(item)

        event.accept()
