import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow
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
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.data = None
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.graphicsViews.setLayout(layout)
        #
        self.restartButton.clicked.connect(self.plot)

    def plot(self):
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
        # instead of ax.hold(False)
        self.figure.clear()
        # create an axis
        axes = self.figure.add_subplot(111)
        # plot data
        [axes.plot(data_x[i], data_y[i], line_type_from_index(i)) for i in range(len(name))]
        axes.set_title("Данные с АЦП")
        # refresh canvas
        self.canvas.draw()


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
    main.show()

    sys.exit(app.exec_())
