import serial
import serial.tools.list_ports


class OaiDdSerial(serial.Serial):
    def __init__(self, cnf={}, **kw):
        serial.Serial.__init__(self)
        self.serial_numbers = []  # это лист возможных серийников!!! (не строка)
        self.baudrate = 115200
        self.timeout = 0.1
        self.self_id = 0x00
        self.dev_id = 0x00
        self.seq_num = 0
        self.port = "COM0"
        self.row_data = b""
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
            else:
                pass

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
                        self.open()
                    return True
        return False
        pass

    def serial_close(self):
        self.close()

    def request(self, req_type="test", data=[]):

        if req_type == "test":
            data_to_bdd = [self.dev_id, self.self_id, self.seq_num, 0x00, 0x00, len[data], 0x00, 0x00]
        elif req_type == "test":
            data_to_bdd = [self.dev_id, self.self_id, self.seq_num, 0x00, 0x01, len[data], 0x00, 0x00]
        elif req_type == "test":
            data_to_bdd = [self.dev_id, self.self_id, self.seq_num, 0x00, 0x02, len[data], 0x00, 0x00]
        #
        else:
            data_to_bdd = "E0 B7 00 00 08 " + bdd_id[2:5] + " 0A 00 03 01 00 00 00 0E"
            pass
        com_var = str_to_list(data_to_bdd)
        if self.is_open is True:
            self.write(com_var)
            self.command_error[data_to_bdd[3:5]] += 1
            # print("{:.3f} write: 0x {}".format(time.clock(), data_to_bdd))
            return data_to_bdd
        else:
            # raise SystemError("COM-port error")
            pass

    def reading_thread_function(self):
        buf = bytearray(b"")
        work_data = b""
        status = ""
        while True:
            time.sleep(0.01)
            if self.is_open is True:
                try:
                    read_data = self.read(128)
                    self.read_data=read_data
                except (TypeError, serial.serialutil.SerialException, AttributeError):
                    read_data = b""
                if read_data:
                    read_data = buf + bytes(read_data)  # прибавляем к новому куску старый кусок
                    #print(bytes_array_to_str(read_data))
                    buf = bytearray(b"")
                    while read_data:
                        #print(bytes_array_to_str(read_data))
                        if read_data[0] == 0xEE:
                            if len(read_data) >= 2:  # находим начало пакета
                                if read_data[1] in [0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB7]:
                                    if len(read_data) >= 6:
                                        if read_data[5] == 0x0E:
                                            work_data = read_data[0:6]
                                            read_data = read_data[6:len(read_data)]
                                elif read_data[1] in [0xB5, 0xC5]:
                                    if len(read_data) >= 71:
                                        if read_data[70] == 0x0E:
                                            work_data = read_data[0:71]
                                            read_data = read_data[71:len(read_data)]
                                elif read_data[1] == 0xB6:
                                    if len(read_data) >= 14:
                                        if read_data[13] == 0x0E:
                                            work_data = read_data[0:14]
                                            read_data = read_data[14:len(read_data)]
                                elif read_data[1] == 0xB8:
                                    if len(read_data) >= 5:
                                        data_len = read_data[4]
                                        if len(read_data) >= (5 + data_len + 1):
                                            if read_data[5 + data_len] == 0x0E:
                                                #print(bytes_array_to_str(read_data))
                                                work_data = read_data[0:5 + data_len + 1]
                                                read_data = read_data[(5 + data_len + 1):len(read_data)]
                                    pass
                                if work_data:
                                    status = self.kpa_data.parsing(work_data)
                                    self.command_error[bytes_array_to_str(work_data)[6:8]] -= 1
                                    # print("{:.3f} read {}: {}".format(time.clock(), status, bytes_array_to_str(work_data)))
                                    work_data = b""
                                    # print(self.command_error)
                                else:
                                    buf = read_data
                                    read_data = bytearray(b"")
                            else:
                                buf = read_data
                                read_data = bytearray(b"")
                        else:
                            read_data.pop(0)
                        pass
            else:
                pass
            if self._close_event.is_set() is True:
                self._close_event.clear()
                return
        pass

    def form_bdd_data(self, bdd_id="0x02"):
        if bdd_id in "0x02":
            return ["{:.2E}".format(self.kpa_data.bdd1_pressure),
                    "{:.2f}".format(self.kpa_data.bdd1_temp),
                    "{:.2f}".format(self.kpa_data.kpa_volt),
                    "{:.2f}".format(self.kpa_data.bdd1_curr)]
        elif bdd_id in "0x03":
            return ["{:.2E}".format(self.kpa_data.bdd2_pressure),
                    "{:.2f}".format(self.kpa_data.bdd2_temp),
                    "{:.2f}".format(self.kpa_data.kpa_volt),
                    "{:.2f}".format(self.kpa_data.bdd2_curr)]