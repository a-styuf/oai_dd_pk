import serial
import serial.tools.list_ports
import my_crc16


class OaiDDData:
    def __init__(self):
        self.adc_data = [0, 0, 0, 0]
        self.dac_data = 0

    def create_table_data(self):
        name = ["АЦП 1",
                "АЦП 2",
                "АЦП 3",
                "АЦП 4",
                "ЦАП 1",
                ]
        data = ["%d" % self.adc_data[0],
                "%d" % self.adc_data[1],
                "%d" % self.adc_data[2],
                "%d" % self.adc_data[3],
                "%d" % self.dac_data,
                ]
        return [[name[i], data[i]] for i in range(len(name))]


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

    def open_id(self):  # функция для установки связи с КПА
        com_list = serial.tools.list_ports.comports()
        for com in com_list:
            print(com)
            for serial_number in self.serial_numbers:
                print(com.serial_number, serial_number)
                if com.serial_number is not None:
                    if com.serial_number.find(serial_number) >= 0:
                        # print(com.device)
                        self.port = com.device
                        self.open()
                    self.state = 0x01
                    return True
        self.state = 0x00
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
            self.write(bytes(com_data))
            self.row_data = b""
            try:
                self.row_data = self.read(size=answer_leng)
            except serial.serialutil.SerialException:
                pass
            self.parcing()
        else:
            self.state = 0

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
