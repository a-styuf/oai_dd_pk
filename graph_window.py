import data_visualisation
import tkinter as tk


class GraphWindow(tk.Toplevel):
    def __init__(self, root, **kw):
        self.title_text = "Визуализация данных"
        self.mode = 0
        for key in sorted(kw):
            if key == "title":
                self.title_text = kw.pop(key)
            elif key == "mode":
                self.mode = kw.pop(key)
            else:
                pass
        tk.Toplevel.__init__(self, root, kw)

        self.title(self.title_text)
        self.geometry('1050x600')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: self.withdraw())
        self.deiconify()

        self.graph_frame = data_visualisation.DVFrame(self, mode=self.mode)
        self.graph_frame.place(x=10, y=10, relheight=1, height=-20, relwidth=1, width=-20)

        self.after(500, self.lower)

    def place_data(self, data):
        if data:
            self.graph_frame.data_manager(data)
        pass
