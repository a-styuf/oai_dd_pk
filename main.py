import tkinter as tk
import graph_window as gw


def read_adc():
    pass


def get_dac():
    pass


def graph_window():
    gr_w.deiconify()
    pass


def close_root():
    root.destroy()
    pass


# саздание основного окна для tkinter
root = tk.Tk()
root.title("Overpressure #3")
root.geometry('825x360')
root.resizable(False, False)
root.config(bg="grey95")
root.protocol("WM_DELETE_WINDOW", close_root)

# окно с графиками
gr_w = gw.GraphWindow(root, mode=1)

# ### #
save_button = tk.Button(root, text='Сохранить', command=save_cfg, bg="gray80")
save_button .place(relx=1, x=-105, rely=1, y=-25, height=20, width=100)

# ### #
graph_button = tk.Button(root, text='Графики', command=graph_window, bg="gray80")
graph_button .place(relx=1, x=-210, rely=1, y=-25, height=20, width=100)
