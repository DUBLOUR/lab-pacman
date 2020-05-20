import tkinter as tk
from tkinter.font import Font


class ShadowLabel:
    def __init__(self, view, text, x, y, anchor="nw", size=12, color="#DDDDDD"):
        self.__view = view
        self.text = text
        self.x = x
        self.y = y
        self.color = [color, "black"]
        self.anchor = anchor
        self.size = size
        
        self.last_l = None
        self.last_r = None
        self.last_c = None
        
        self.__create_text("Consolas", size)


    def __create_text(self, font_family, size):
        font = Font(family=font_family, size=size, weight="bold")
        c = self.__view.canvas
        x,y = self.x, self.y
        justify = "left"
        self.id1 = c.create_text((x,y),
                                 text=self.text,
                                 fill=self.color[1],
                                 font=font,
                                 justify=justify,
                                 anchor=self.anchor)
        
        font = Font(family=font_family, size=size, weight="normal")
        self.id2 = c.create_text((x,y),
                                 text=self.text,
                                 fill=self.color[0],
                                 font=font,
                                 justify=justify,
                                 anchor=self.anchor)


    def update(self, left="", right="", color=None):
        if self.last_l == left and self.last_r == right and \
                                   self.last_c == color:
            return

        self.last_l = left
        self.last_r = right
        self.last_c = color
        
        text = str(left) + self.text + str(right)
        c = self.__view.canvas
        c.itemconfig(self.id1, text=text)
        c.itemconfig(self.id2, text=text)
        if color and self.color[0] != color:
            self.color[0] = color
            c.itemconfig(self.id2, fill=color)
            


class View:
    __window_title = 'Baka-baka'
    __icon_path = 'resourses/icon.png'
    __textures_path = "resourses/textures/"
    
    def __init__(self, model):
        self.__model = model
        
        self.__image = {}
        self.__last_ghost_color = dict()
        self.last_cell_object = [[None for j in range(model.field_size[0]+2)] 
                                       for i in range(model.field_size[1]+2)] 

        self.__init_window()
        self.__init_canvas()
        self.__init_texts()


    def __init_texts(self):
        bottom_field = self.__model.cell_size * (self.__model.field_size[1]-4)
        
        self.__info = dict()
        self.__info["level"] = ShadowLabel(self, 
                                text="", 
                                x=self.window_width // 2, 
                                y=5,
                                anchor="n")

        self.__info["score"] = ShadowLabel(self, 
                                text="Score: ", 
                                x=3, 
                                y=bottom_field,
                                anchor="nw")
        
        self.__info["lives"] = ShadowLabel(self, 
                                text="Lives: ", 
                                x=self.window_width-3, 
                                y=bottom_field,
                                anchor="ne",
                                size=12)                 

        self.__info["bonus_timer"] = ShadowLabel(self, 
                                text="", 
                                x=self.window_width // 2, 
                                y=bottom_field+25,
                                anchor="n",
                                size=18)

        
        self.__info["keyboard"] = ShadowLabel(self, 
                                text="WASD/Arrows for move\n" + 
                                     "Q for quit, P for pause", 
                                x=4, 
                                y=self.window_height-5,
                                anchor="sw",
                                size=12)

        self.__info["copyright"] = ShadowLabel(self, 
                                text="© Nikitenko Maxik 2020", 
                                x=self.window_width - 3, 
                                y=self.window_height, 
                                anchor="se",
                                size=10)

        
        self.__info["loose"] = ShadowLabel(self, 
                                text="", 
                                x=self.window_width // 2, 
                                y=bottom_field+20,
                                anchor="n",
                                size=18)


        self.__info["win"] = ShadowLabel(self, 
                                text="", 
                                x=self.window_width // 2, 
                                y=bottom_field+20,
                                anchor="n",
                                size=18,
                                color="lightgreen")


        self.__info["get_level"] = ShadowLabel(self, 
                                text="", 
                                x=self.window_width // 2, 
                                y=bottom_field+20,
                                anchor="n",
                                size=18,
                                color="lightgreen")


    def update_info(self):
        m = self.__model
        self.__info["score"].update(right=m.score_point)
        self.__info["level"].update(left=m.level_name)
        self.__info["lives"].update(right=m.pacman.lives)
 
        if m.is_lose:
            text = "You lost to foolish red balls…"
            self.__info["loose"].update(left=text)

        if m.is_win:
            text = "YOU WIN! CONGRATULATIONS!"
            self.__info["win"].update(left=text)

        if m.level_finishes and not m.is_win:
            text = "NICE! LEAVE FROM MAP!"
            self.__info["get_level"].update(left=text)
        else:
            self.__info["get_level"].update()


        b_time = (m.bonus_lasting - m.frame_time) / m.fps
        if b_time > 0 and not (m.is_lose or m.is_win or m.level_finishes):
            urgent_time = 2.5 
            if b_time > urgent_time:
                color = "yellow"
            else:
                color = "red"

            text = "HUNTER MODE: {:.2f}".format(b_time)
            self.__info["bonus_timer"].update(right=text, color=color)
        else:
            self.__info["bonus_timer"].update()


    def __init_window(self):        
        self.root = tk.Tk()
        self.root.title(self.__window_title)
        self.root.resizable(width=False, height=False)
        
        self.__icon = tk.PhotoImage(file=self.__icon_path)
        self.root.iconphoto(False, self.__icon)


    def __init_canvas(self):
        m = self.__model
        self.window_width = m.cell_size * (m.field_size[0] + 1) + \
                            m.padding[0] + m.padding[2]
        self.window_height = m.cell_size * m.field_size[1] + \
                             m.padding[1] + m.padding[3]

        self.canvas = tk.Canvas(self.root, 
                                width=self.window_width, 
                                height=self.window_height,
                                highlightthickness=0,
                                background="black")
        self.canvas.focus_set()
        self.canvas.pack()


    def show(self):
        self.root.mainloop()


    def move_object(self, tag, dx, dy):
        self.canvas.move(tag, dx, dy)


    def load_level_textures(self):
        textures = self.__model.map_colors.values()
        unical = set()
        for c,t in textures:
            if t:
                unical.add(t)
        
        for t in unical:
            img = self.__textures_path + f'small_{t}.png'
            self.__image[t] = tk.PhotoImage(file=img)
        

    def __get_cell_image(self, y, x):
        cell = self.__model.map_field[y][x][0]
        convertor = self.__model.map_colors
        color, texture = convertor.get(cell, [None,None])
        return color, texture


    def draw_cell(self, y, x):
        model = self.__model
        xc = x * model.cell_size + model.padding[0] - model.cell_size // 2
        yc = y * model.cell_size + model.padding[1] - model.cell_size // 2

        canvas_object = self.last_cell_object[y][x]
        if canvas_object != None:
            self.canvas.delete(canvas_object)

        color, texture = self.__get_cell_image(y, x)
        if texture is not None:
            canvas_object = self.canvas.create_image(
                                                xc, 
                                                yc, 
                                                image=self.__image[texture], 
                                                anchor=tk.NW)
        else:
            canvas_object = self.canvas.create_rectangle(
                                                xc, 
                                                yc, 
                                                xc + self.__model.cell_size, 
                                                yc + self.__model.cell_size, 
                                                fill=color)
        
        self.canvas.tag_lower(canvas_object)
        self.last_cell_object[y][x] = canvas_object
        # print(canvas_object)

    
    def draw_background(self):
        field_size = self.__model.field_size
        
        for x in range(field_size[0] + 1):
            for y in range(field_size[1]):
                self.draw_cell(y, x)


    def show_grid(self):
        for y in range(self.window_height):
            for x in range(self.window_width):
                if self.__model.is_avaiable_coord(x, y):
                    self.canvas.create_line(x, y, x, y, width=1, fill="gray")


    def set_ghost_color(self, g, color=None):
        if not color:
            color = g.color_status[g.status]
        if self.__last_ghost_color.get(g.id, None) == color:
            return

        self.__last_ghost_color[g.id] = color
        tag = "ghost" + str(g.id)
        self.canvas.itemconfig(tag, fill=color)

    
    def create_enemies(self):
        def create_pacman(p):
            self.ball = self.canvas.create_oval( 
                                (p.x, p.y), 
                                (p.x+p.size, p.y+p.size),
                                fill="yellow", 
                                outline="black", 
                                width=1.35,
                                tag="pacman")


        def create_ghost(g):
            tag = "ghost" + str(g.id)
            color = g.color_status[g.status]
            self.canvas.create_oval( 
                                (g.x, g.y), 
                                (g.x+g.size, g.y+g.size),
                                fill=color, 
                                outline="black", 
                                tag=tag)


        create_pacman(self.__model.pacman)
        for g in self.__model.ghosts:
            create_ghost(g)
            
