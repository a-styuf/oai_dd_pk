import sys
from PyQt5 import QtWidgets, QtCore
import oai_dd_pc_ui
import data_graph_main
import com_port


class MainWindow(QtWidgets.QMainWindow, oai_dd_pc_ui.Ui_Form):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        # создание и подключение графиков
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.cycle_body)
        # работа с COM-портом и данными с платы
        self.oai_dd = com_port.OaiDdSerial(dev_id=0x01, self_id=0x00)
        # создание второго окна с графиками
        self.GraphWindow = data_graph_main.MainWindow()
        #
        self.GetADCButton.clicked.connect(self.get_adc)
        self.SetDACButton.clicked.connect(self.set_dac)
        self.COMOpenButton.clicked.connect(self.com_open)
        self.CycleButton.toggled.connect(self.cycle_body)

    def cycle_start_stop(self, checked):
        if checked:
            if self.timer.isActive():
                pass
            else:
                self.timer.start(1000)
        else:
            self.timer.stop()
        pass

    def cycle_body(self):
        self.get_adc()
        self.fill_data_table()
        print(self.timer.remainingTime())
        self.state_check()
        pass

    def get_adc(self):
        self.oai_dd.request(req_type="get_adc")
        self.fill_data_table()
        self.state_check()
        pass

    def set_dac(self):
        data = int(self.DACEntry.text())
        self.oai_dd.request(req_type="set_dac", data=[(data >> 8) & 0xFF, (data >> 0) & 0xFF])
        self.fill_data_table()
        self.state_check()
        pass

    def fill_data_table(self):
        data = self.oai_dd.data.create_table_data()
        for row in range(len(data)):
            for column in range(len(data[row])):
                table_item = QtWidgets.QTableWidgetItem(data[row][column])
                self.tableWidget.setItem(row, column, table_item)
        pass

    def com_open(self):
        print(self.SerialNumEntry.text())
        self.oai_dd.serial_numbers = [self.SerialNumEntry.text()]
        if self.oai_dd.open_id():
            self.StateMessage.setText("Подключение успешно")
            self.COMOpenButton.setStyleSheet('QPushButton {background-color: seagreen;}')
        else:
            self.StateMessage.setText("Подключение не успешно")
            self.COMOpenButton.setStyleSheet('QPushButton {background-color: salmon}')

    def state_check(self):
        if self.oai_dd.state:
            self.COMOpenButton.setStyleSheet('QPushButton {background-color: seagreen}')
        else:
            self.COMOpenButton.setStyleSheet('QPushButton {background-color: salmon}')
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
