import serial
import serial.tools.list_ports
import my_crc16
import time


class OaiDDData:
    def __init__(self):
        self.adc_data = [0, 0, 0, 0]
        self.dac_data = 0
        self.names = ["Время, с",
                      "АЦП 1",
                      "АЦП 2",
                      "АЦП 3",
                      "АЦП 4",
                      "ЦАП 1",
                      ]
        self.data = []
        self.graph_data = None

    def create_table_data(self):
        self.data = ["%.3f" % time.clock(),
                     "%d" % self.adc_data[0],
                     "%d" % self.adc_data[1],
                     "%d" % self.adc_data[2],
                     "%d" % self.adc_data[3],
                     "%d" % self.dac_data,
                     ]
        # print("adc1 - 0x%04X" % self.adc_data[0], "adc2 - 0x%04X" % self.adc_data[1],)
        self.create_graph_data()
        return [[self.names[i], self.data[i]] for i in range(len(self.names))]

    def create_graph_data(self):
        if self.graph_data is None:
            self.graph_data = []
            for name in self.names[1:]:
                self.graph_data.append([name, [], []])
        else:
            for i in range(0, len(self.names)-1):
                self.graph_data[i][1].append(float(self.data[0]))
                self.graph_data[i][2].append(float(self.data[i+1]))
        while len(self.graph_data) > 10000:
            self.graph_data.pop(0)

    def reset_graph_data(self):
        self.graph_data = []
        for name in self.names:
            self.graph_data.append([name, [], []])

    def __str__(self):
        pass


class OaiDdSerial(serial.Serial):
    def __init__(self, **kw):
        serial.Serial.__init__(self)
        self.serial_numbers = []  # это лист возможных серийников!!! (не строка)
        self.baudrate = 115200
        self.timeout = 0.2
        self.self_id = 0x00
        self.dev_id = 0x00
        self.seq_num = 0
        self.port = "COM0"
        self.row_data = b""
        self.state = 0
        self.data = OaiDDData()
        for key in sorted(kw):
            if key == "serial_numbers":
                self.serial_numbers = kw.pop(key)
            elif key == "baudrate":
                self.baudrate = kw.pop(key)
            elif key == "timeout":
                self.baudrate = kw.pop(key)
            elif key == "port":
                self.baudrate = kw.pop(key)
            elif key == "self_id":
                self.self_id = kw.pop(key)
            elif key == "dev_id":
                self.dev_id = kw.pop(key)
            elif key == "data":
                self.data = kw.pop(key)
            else:
                pass
        self.error_string = "No error"

    def open_id(self):  # функция для установки связи с КПА
        com_list = serial.tools.list_ports.comports()
        for com in com_list:
            # print(com)
            for serial_number in self.serial_numbers:
                # print(com.serial_number, serial_number)
                if com.serial_number is not None:
                    if com.serial_number.find(serial_number) >= 0:
                        # print(com.device)
                        self.port = com.device
                        try:
                            self.open()
                        except serial.serialutil.SerialException as error:
                            self.error_string = str(error)
                    self.state = 1
                    self.error_string = "Переподключение успешно"
                    return True
        self.state = 0
        return False
        pass

    def serial_close(self):
        self.close()

    def request(self, req_type="test", data=[]):
        if req_type == "test":
            com = 0x00
            answer_leng = 8
        elif req_type == "get_adc":
            com = 0x01
            answer_leng = 16
        elif req_type == "set_dac":
            com = 0x02
            answer_leng = 10
        else:
            com = 0x00
            answer_leng = 8
            pass
        # сборка команды
        leng = len(data)
        com_data = [self.dev_id, self.self_id, self.seq_num, 0x00, com, leng]
        com_data.extend(data)
        crc16 = my_crc16.calc(com_data, len(com_data))
        com_data.extend([(crc16 >> 8) & 0xFF, (crc16 >> 0) & 0xFF])
        if self.is_open:
            try:
                self.write(bytes(com_data))
                self.row_data = b""
                self.row_data = self.read(size=answer_leng)
            except serial.serialutil.SerialException as error:
                self.error_string = str(error)
                self.close()
                self.state = 0
            self.parcing()
        else:
            self.state = 0
            self.open_id()

    def parcing(self):
        if len(self.row_data) > 5:
            if self.row_data[0] == self.self_id and self.row_data[1] == self.dev_id:
                if self.row_data[3] == 0x00 and self.row_data[4] == 0x00:  # тестовая команда
                    self.state = 0x01
                elif self.row_data[3] == 0x00 and self.row_data[4] == 0x01:  # команда на чтение данных из АЦП
                    if len(self.row_data) >= 5+8:
                        self.data.adc_data = [int.from_bytes(self.row_data[6+i*2:8+i*2], byteorder="big") for i in range(4)]
                        self.state = 0x01
                    else:
                        self.state = 0x00
                elif self.row_data[3] == 0x00 and self.row_data[4] == 0x02:  # команда на чтение данных из АЦП
                    if len(self.row_data) >= 5+2:
                        self.data.dac_data = int.from_bytes(self.row_data[6:8], byteorder="big")
                        self.state = 0x01
                    else:
                        self.state = 0x00
            else:
                self.state = 0x00
        else:
            self.state = 0x00
        pass
