import tkinter as tk

class View:
    
    def __init__(self):
        self._pacman_size = 22
        self._cell_size = 24
        self._ghost_size = 20
        self._field_size = [22, 22]
        self._gim = []

        self._init_window()
        print("abc")


    def _init_window(self):
        self._root = tk.Tk()
        self._root.title('Baka-baka-baka')
        self._root.resizable(width=False, height=False)


        self._padding = [12, 81, -12, 20]
        self._window_width = self._cell_size * (self._field_size[0] + 1) + self._padding[0] + self._padding[2]
        self._window_height = self._cell_size * self._field_size[1] + self._padding[1] + self._padding[3]





