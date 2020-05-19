from model import Model
from view import View

class Presenter:
    fps = 100
    def __init__(self, model, view):
        self._init_model(model)
        self._init_view(view)


    def _init_model(self, model):
        self._model = model


    def _init_view(self, view):
        self._view = view


    def show(self):
        self._view.show()


    def set_binds(self):
        self._view.canvas.bind('<Key>', self.keyboard_input)


    def exit(self):
        exit()


    def start_game(self):
        self._model.init_level(2)
        self._view.load_textures()
        self._view.draw_background()
        self._view.create_enemies()
        self.set_binds()
        #view.show_grid()
        self.main_loop()
        self.show()


    def show_manual(self):
        print("      WASD or Arrows - move Pacman")
        print("     `h' or `?' - show this manual")
        print("         `q' - quit from game")


    def keyboard_input(self, event=None):
        convertor = dict({
            'w': 'U', 'Up': 'U',
            'a': 'L', 'Left': 'L',
            's': 'D', 'Down': 'D',
            'd': 'R', 'Right': 'R'
        })

        key = str(event.keysym)
        print(key)
        if key == 'q':
            self.exit()

        if key == 'question' or key == 'h':
            self.show_manual()

        if key in convertor:
            self._model.pacman.next_direction = convertor[key]



    def open_next_level(self):
        pass


    def handle_pacman_cell(self):
        x, y = self._model.pacman.get_center()
        if  not self._model.is_cell_center(x, y):
            return

        x = (x - self._model.padding[0]) // self._model.cell_size
        y = (y - self._model.padding[1]) // self._model.cell_size
        if  not(0 <= x < self._model.field_size[0]) or \
            not(0 <= y < self._model.field_size[1]):
            return


        tp = self._model.map_field[y][x]
        #print("IS CELL", x, y, tp)
        hasChange = False
        if tp == '.':
            self._model.eat_point(y, x)
            hasChange = True

        if tp == 'B':
            self._model.eat_bonus(y, x)
            hasChange = True

        if hasChange:
            self._view.draw_cell(y, x)


    def move_pacman(self, x, y):
        p = self._model.pacman
        p.x += x; 
        p.y += y
        self._view.move_object("pacman", x, y)


    def move_ball(self):
        pacman = self._model.pacman
        x, y = pacman.get_center()
        #print(x, y, '\t', pacman.direction, pacman.next_direction)

        dir_to_vect = {
            "U": [0, -1], 
            "D": [0, 1], 
            "L": [-1, 0], 
            "R": [1, 0]
        }
        dx, dy = dir_to_vect[pacman.next_direction]

        if self._model.is_avaiable_coord(x + dx, y + dy):
            pacman.direction = pacman.next_direction
            
        dx, dy = dir_to_vect[pacman.direction]

        world_width = 24 * self._model.cell_size
        if x + dx == -pacman.size:
            # teleport Left -> Right
            self.move_pacman(world_width, 0)
        elif x + dx == world_width - pacman.size + 1:
            # teleport Right -> Left
            self.move_pacman(-world_width, 0)
        elif self._model.is_avaiable_coord(x + dx, y + dy):
            # Standart moving
            self.move_pacman(dx, dy)
        

    

    def kill_pacman(self):
        print("You are dead...")


    def kill_ghost(self, ghost):
        ghost.status = "fly";
        


    def check_ghosts_collision(self):
        def handle_collision(g):
            if g.status == "fly":
                return;

            #print("IS COLLISTION WITH", g.id, "!!!")
            if pac.state == "prey":
                self.kill_pacman()
            elif pac.state == "hunter":
                self.kill_ghost(g)


        pac = self._model.pacman
        px, py = pac.get_center()
        
        for g in self._model.ghosts:
            gx, gy = g.get_center()
            max_dist_square = (pac.size + g.size) ** 2 // 4
            dist_square = (px-gx)**2 + (py-gy)**2
            if dist_square < max_dist_square:
                handle_collision(g);
                

    def end_game(self):
        print("YAHO")
        self.exit()


    def move_ghosts(self):
        for g in self._model.ghosts:
            if g.at_home() and g.status == "fly":
                g.stop_fly()
                
            dx, dy = self._model.ghost_moving(g, speed=1)
            g.x += dx
            g.y += dy
            tag = "ghost" + str(g.id)
            self._view.move_object(tag, dx, dy)


    def update_statuses(self):
        self._model.update_statuses()
        for g in self._model.ghosts:
            color = {
                "hunter": "red",
                "prey": "lightgreen",
                "fly": "blue"
            }[g.status]
            self._view.set_ghost_color(g)



    def main_loop(self):
        if self._model.level_finishes:
            self.end_game()

        self._model.frame_time += 1
        self.handle_pacman_cell()
        self.update_statuses()
        self.check_ghosts_collision()
        self.move_ghosts()
        self.move_ball()

        
        animation_delay = int(1000 / self.fps)
        self._view._root.after(animation_delay, self.main_loop)



