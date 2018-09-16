# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QTableWidgetItem
import data_graph

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class MainWindow(QMainWindow, data_graph.Ui_Form):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.type = "slave"  # необходимо для проерки на вид вызова окна - главное/дочернее
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        # data
        self.data = None
        self.pause = 0
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.graphicsViews.setLayout(layout)
        #
        self.restartButton.clicked.connect(self.plot)
        self.pauseButton.toggled.connect(self.pause_set_clr)

    def pause_set_clr(self, checked):
        if checked:
            self.pause = 1
        else:
            self.pause = 0

    def plot(self, data=None):
        if self.pause == 0:

            self.data = data
            name = []
            data_x = []
            data_y = []
            if self.data:
                for graph in self.data:
                    name.append(graph[0])
                    data_x.append(graph[1])
                    data_y.append(graph[2])
            else:
                name = ["Test"]
                data_x = [[0, 1, 2, 3]]
                data_y = [[0, 1, 4, 9]]
            time = data_x[0]
            # отрисуем график
            # instead of ax.hold(False)
            self.figure.clear()
            # create an axis
            axes = self.figure.add_subplot(111)
            # plot data
            [axes.plot(data_x[i], data_y[i], line_type_from_index(i), label=name[i]) for i in range(len(name))]
            axes.set_title("Данные с АЦП")
            axes.set_ylabel("АЦП, кв")
            axes.set_xlabel("Время, с")
            axes.grid()
            # refresh canvas
            self.canvas.draw()
            # заполним таблицу
            self.tableWidget.setRowCount(len(self.data) + 1)
            time_name_item = QTableWidgetItem("Время")
            self.tableWidget.setItem(0, 1, time_name_item)
            time_item = QTableWidgetItem("NA")  # "{:.3g}".format(data_x[0][-1]))
            self.tableWidget.setItem(0, 2, time_item)
            for row in range(len(self.data)):
                for column in range(1, 3):
                    if column == 1:
                        table_item = QTableWidgetItem(name[row])
                    elif column == 2:
                        try:
                            table_item = QTableWidgetItem("{:.3g}".format(data_y[row][-1]))
                        except IndexError:
                            table_item = QTableWidgetItem("NA")
                    else:
                        table_item = QTableWidgetItem("NA")
                    self.tableWidget.setItem(row, column, table_item)
        else:
            pass

    # Переопределение метода closeEvent, для перехвата события закрытия окна
    def closeEvent(self, event):
        if self.type == "master":
            event.ignore()
        else:
            self.hide()


def line_type_from_index(n):
    color_line = ["b", "r", "g", "c", "m", "y", "k"]
    style_line = ["-", "--", "-.", ":"]
    try:
        color = color_line[n % len(color_line)]
        style = style_line[n // len(color_line)]
        # print(n % len(color_line), n // len(color_line))
        return style + color
    except Exception:
        return "-r"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.type = "master"
    main.show()
    sys.exit(app.exec_())
