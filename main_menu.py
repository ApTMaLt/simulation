import random
import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QSlider, QApplication, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets


class QHSeperationLine(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setLineWidth(5)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        return


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('test1.ui', self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.scroll_area)
        self.pushButton_2.clicked.connect(self.close_window)
        self.pushButton_2.setEnabled(False)
        self.closes = False

    def close_window(self):
        self.closes = True
        self.close()

    def get_lists(self):
        list_of_sizes = []
        list_of_density = []
        for i in self.gg:
            list_of_sizes.append(i.value())
        for j in self.gg2:
            list_of_density.append(j.value())
        return list_of_sizes, list_of_density

    def scroll_area(self):
        self.pushButton_2.setEnabled(True)
        w_container = QWidget()
        w_container.setFixedWidth(300)
        v_layout_container = QVBoxLayout()
        v_layout_container.setSpacing(30)
        self.gg = []
        self.gg2 = []
        self.kolvo = self.spinBox.value()
        for x in range(self.kolvo):
            self.seperator_horizontal = QHSeperationLine()
            self.size = QSlider(Qt.Horizontal)
            self.size.setMinimum(20)
            self.size.setMaximum(50)
            self.size.setValue(random.randint(20, 50))
            self.density = QSlider(Qt.Horizontal)
            self.density.setMinimum(1)
            self.density.setMaximum(10)
            self.density.setValue(random.randint(1, 10))
            self.label = QLabel(self)
            self.label.setText(f'Шар № {x + 1}')
            self.label.setFont(QFont('Arial', 10))
            self.label2 = QLabel(self)
            self.label2.setText('Размер:')
            self.label2.setFont(QFont('Arial', 10))
            self.label3 = QLabel(self)
            self.label3.setText('Плотность:')
            self.label3.setFont(QFont('Arial', 10))
            v_layout_container.addWidget(self.label)
            v_layout_container.addWidget(self.label2)
            v_layout_container.addWidget(self.size)
            v_layout_container.addWidget(self.label3)
            v_layout_container.addWidget(self.density)
            v_layout_container.addWidget(self.seperator_horizontal)
            self.gg.append(self.size)
            self.gg2.append(self.density)
        w_container.setLayout(v_layout_container)
        self.scrollArea.setWidget(w_container)
        v_layout_preview = QVBoxLayout()
        self.setLayout(v_layout_preview)
        v_layout_preview.addWidget(self.scrollArea)


def main_menu():
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    app.exec_()
    if ex.closes:
        return ex.kolvo, ex.get_lists(), ex.horizontalSlider_2.value(), ex.horizontalSlider.value()
