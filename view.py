import tkinter as tk

class View:
    
    def __init__(self, model):
        self.model = model
        self.pacman_size = 22
        self.cell_size = 24
        self.ghost_size = 20
        self.field_size = [22, 22]
        self.gim = []
        self.padding = self.model.padding
        self.last_cell_object = [[None for j in range(self.model.field_size[0]+2)] for i in range(self.model.field_size[1]+2)] 

        self.window_width = self.cell_size * (self.field_size[0] + 1) + self.model.padding[0] + self.model.padding[2]
        self.window_height = self.cell_size * self.field_size[1] + self.model.padding[1] + self.model.padding[3]

        self._init_window()
        self._init_canvas()
        


    def _init_window(self):
        self._root = tk.Tk()
        self._root.title('Baka-baka-baka')
        self._root.resizable(width=False, height=False)


        self._padding = [12, 81, -12, 20]
        self.window_width = self.cell_size * (self.field_size[0] + 1) + \
                             self.padding[0] + self.padding[2]
        self.window_height = self.cell_size * self.field_size[1] + \
                              self.padding[1] + self.padding[3]


    def _init_canvas(self):
        self.canvas = tk.Canvas(self._root, 
                                width=self.window_width, 
                                height=self.window_height)
        self.canvas.focus_set()
        self.canvas.pack()


    def show(self):
        self._root.mainloop()


    def put_cell_img(self, name, x, y):
        path = f'resourses/textures/small_{name}.png'
        self.gim.append(tk.PhotoImage(file=path))
        return self.canvas.create_image(x, y, image=self.gim[-1], anchor=tk.NW)



    def drawCell(self, y, x):
        model = self.model
        tp = model.map_field[y][x][0]
        color = {
            '#': 'red',
            '.': 'black',
            'P': 'yellow',
            ' ': 'blue',
            'B': 'orange',
            'G': 'white',
            '_': 'green',
            '|': 'magenta'
        }[tp]

        texture = {
            '#': 'bricks',
            '.': 'diamond_ore',
            ' ': 'stone',
            'P': 'stone',
            '_': 'oak_planks',
            '|': 'stone',
            'G': 'cobblestone',
            'B': 'mossy_cobblestone'
        }.get(tp, None)

        xc = x * model.cell_size + model.padding[0] - model.cell_size // 2
        yc = y * model.cell_size + model.padding[1] - model.cell_size // 2

        
        canvas_object = self.last_cell_object[y][x]
        if canvas_object != None:
            self.canvas.delete(canvas_object)

        if texture is not None:
            canvas_object = self.put_cell_img(texture, xc, yc)
        else:
            canvas_object = self.canvas.create_rectangle(
                xc, yc, xc + cell_size, yc + cell_size, fill=color)
        
        self.canvas.tag_lower(canvas_object)
        self.last_cell_object[y][x] = canvas_object
        print(canvas_object)


    
    def paint_background(self):
        field_size = self.model.field_size
        
        for x in range(field_size[0] + 1):
            for y in range(field_size[1]):
                self.drawCell(y, x)



    def show_grid(self):
        for y in range(self.window_height):
            for x in range(self.window_width):
                if self.model.isAvaiableCoord(x, y):
                    self.canvas.create_line(x, y, x, y, width=1, fill="gray")

    
    def create_memes(self):
        canvas = self.canvas
        self.ball = canvas.create_oval((0, 0), (self.pacman_size, self.pacman_size),
                                  fill="yellow", outline="black", tag="pacman")
        
    
        pac_x = self.model.pac_init_cell[0] * self.cell_size + self.model.padding[0] - self.pacman_size // 2
        pac_y = self.model.pac_init_cell[1] * self.cell_size + self.model.padding[1] - self.pacman_size // 2
        canvas.move("pacman", pac_x, pac_y)

        for i in range(self.model.ghost_count):
            id = "ghost" + str(i)
            enemy = canvas.create_oval((0, 0), (self.ghost_size, self.ghost_size),
                                  fill="red", outline="black", tag=id)
        
            x = self.model.ghosts_init_cell[i][0] * self.cell_size + self.model.padding[0] - self.ghost_size // 2
            y = self.model.ghosts_init_cell[i][1] * self.cell_size + self.model.padding[1] - self.ghost_size // 2
            canvas.move(id, x, y)
