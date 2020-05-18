import tkinter as tk

class View:
    
    def __init__(self, model):
        self.model = model
        
        self.image = {}
        self.padding = self.model.padding
        self.last_cell_object = [[None for j in range(model.field_size[0]+2)] 
                                       for i in range(model.field_size[1]+2)] 

        self._init_window()
        self._init_canvas()
        

    def _init_window(self):
        window_title = 'Baka-baka-baka'
        self._root = tk.Tk()
        self._root.title(window_title)
        self._root.resizable(width=False, height=False)



    def _init_canvas(self):
        m = self.model
        self.window_width = m.cell_size * (m.field_size[0] + 1) + \
                            m.padding[0] + m.padding[2]
        self.window_height = m.cell_size * m.field_size[1] + \
                             m.padding[1] + m.padding[3]

        self.canvas = tk.Canvas(self._root, 
                                width=self.window_width, 
                                height=self.window_height)
        self.canvas.focus_set()
        self.canvas.pack()


    def show(self):
        self._root.mainloop()


    def load_textures(self):
        textures = self.model.map_colors.values()
        unical = set()
        for c,t in textures:
            if t:
                unical.add(t)
        
        for t in unical:
            img = f'resourses/textures/small_{t}.png'
            self.image[t] = tk.PhotoImage(file=img)
        



    def get_cell_image(self, y, x):
        cell = self.model.map_field[y][x][0]
        convertor = self.model.map_colors
        color, texture = convertor.get(cell, [None,None])
        return color, texture


    def draw_cell(self, y, x):
        model = self.model
        xc = x * model.cell_size + model.padding[0] - model.cell_size // 2
        yc = y * model.cell_size + model.padding[1] - model.cell_size // 2

        canvas_object = self.last_cell_object[y][x]
        if canvas_object != None:
            self.canvas.delete(canvas_object)

        color, texture = self.get_cell_image(y, x)
        if texture is not None:
            canvas_object = self.canvas.create_image(
                                                xc, 
                                                yc, 
                                                image=self.image[texture], 
                                                anchor=tk.NW)
        else:
            canvas_object = self.canvas.create_rectangle(
                                                xc, 
                                                yc, 
                                                xc + self.model.cell_size, 
                                                yc + self.model.cell_size, 
                                                fill=color)
        
        self.canvas.tag_lower(canvas_object)
        self.last_cell_object[y][x] = canvas_object
        print(canvas_object)

    
    def draw_background(self):
        field_size = self.model.field_size
        
        for x in range(field_size[0] + 1):
            for y in range(field_size[1]):
                self.draw_cell(y, x)



    def show_grid(self):
        for y in range(self.window_height):
            for x in range(self.window_width):
                if self.model.isAvaiableCoord(x, y):
                    self.canvas.create_line(x, y, x, y, width=1, fill="gray")

    
    def create_enemies(self):
        canvas = self.canvas
        
        def create_pacman(p):
            self.ball = canvas.create_oval( (p.x, p.y), 
                                            (p.x+p.size, p.y+p.size),
                                            fill="yellow", 
                                            outline="black", 
                                            tag="pacman")
        

        def create_ghost(g):
            canvas.create_oval( (g.x, g.y), 
                                (g.x+g.size, g.y+g.size),
                                fill="red", 
                                outline="black", 
                                tag=g.id)


        create_pacman(self.model.pacman)
        for g in self.model.ghosts:
            create_ghost(g)
            
