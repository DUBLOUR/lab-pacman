from model import Model
from view import View

class Presenter:
    def __init__(self, levels):
        self._levels = levels
        self._now_level = 0

        self._model = Model()
        self._view = View(self._model)
    

    def start_game(self):
        self._run_level(self._levels[0])


    def _show(self):
        self._view.show()


    def _set_binds(self):
        self._view.canvas.bind('<Key>', self._keyboard_input)


    def _exit(self):
        exit()


    def _run_level(self, level):
        self._model.init_level(level)
        self._view.load_textures()
        self._view.draw_background()
        self._view.create_enemies()
        self._set_binds()
        #view.show_grid()
        self._main_loop()
        self._show()




    def _show_manual(self):
        print("      WASD or Arrows - move Pacman")
        print("     `h' or `?' - show this manual")
        print("         `q' - quit from game")


    def _keyboard_input(self, event=None):   
        convertor = dict({
            'w': 'U',  'W': 'U',  'Up': 'U',
            'a': 'L',  'A': 'L',  'Left': 'L',
            's': 'D',  'S': 'D',  'Down': 'D',
            'd': 'R',  'D': 'R',  'Right': 'R'
        })

        key = str(event.keysym)
        #print(key)
        if key == 'q' or key == 'Q':
            self._exit()

        if key == 'question' or key == 'h':
            self._show_manual()

        if key == 'p' or key == 'P':
            self.pause()


        if key in convertor:
            self._model.pacman.next_direction = convertor[key]


    def pause(self):
        self._model.pause = not self._model.pause


    def _handle_pacman_cell(self):
        x, y = self._model.pacman.get_center()
        if  not self._model.is_cell_center(x, y):
            return

        x = (x - self._model.padding[0]) // self._model.cell_size
        y = (y - self._model.padding[1]) // self._model.cell_size
        if  not(0 <= x < self._model.field_size[0]) or \
            not(0 <= y < self._model.field_size[1]):
            return


        tp = self._model.map_field[y][x]
        hasChange = False
        if tp == '.':
            self._model.eat_point(y, x)
            hasChange = True

        if tp == 'B':
            self._model.eat_bonus(y, x)
            hasChange = True

        if hasChange:
            self._view.draw_cell(y, x)


    def _move_pacman(self, x, y):
        p = self._model.pacman
        p.x += x; 
        p.y += y
        self._view.move_object("pacman", x, y)


    def _move_ball(self):
        pacman = self._model.pacman
        x, y = pacman.get_center()

        dir_to_vect = {
            "U": [0, -2], 
            "D": [0, 2], 
            "L": [-2, 0], 
            "R": [2, 0]
        }
        dx, dy = dir_to_vect[pacman.next_direction]

        if self._model.is_avaiable_coord(x + dx, y + dy):
            pacman.direction = pacman.next_direction
            
        dx, dy = dir_to_vect[pacman.direction]

        world_width = 24 * self._model.cell_size
        is_teleport = False
        if x + dx <= -pacman.size:
            # teleport Left -> Right
            is_teleport = True
            self._move_pacman(world_width, 0)
        elif x + dx >= world_width - pacman.size + 1:
            # teleport Right -> Left
            is_teleport = True
            self._move_pacman(-world_width, 0)
        elif self._model.is_avaiable_coord(x + dx, y + dy):
            # Standart moving
            self._move_pacman(dx, dy)
        
        if self._model.level_finishes and is_teleport:
            self._goto_next_level()


    def _goto_next_level(self):
        if self._now_level == len(self._levels)-1:
            self._model.game_over(1)
            return
        
        scores = self._model.score_point
        lives = self._model.pacman.lives

        old_root = self._view._root
        self._model = Model()
        old_root.destroy()
        self._view = View(self._model)
        

        self._model.score_point = scores
        self._model.pacman.lives = lives
        
        self._now_level += 1
        level = self._levels[self._now_level]
        self._run_level(level)
    

    def _kill_pacman(self):
        self._model.kill_pacman()


    def _kill_ghost(self, ghost):
        ghost.status = "fly";


    def _check_ghosts_collision(self):
        def handle_collision(g):
            if g.status == "fly":
                return;

            #print("IS COLLISTION WITH", g.id, "!!!")
            if pac.state == "prey":
                self._kill_pacman()
            elif pac.state == "hunter":
                self._kill_ghost(g)


        pac = self._model.pacman
        px, py = pac.get_center()
        
        for g in self._model.ghosts:
            gx, gy = g.get_center()
            max_dist_square = (pac.size + g.size) ** 2 // 4
            dist_square = (px-gx)**2 + (py-gy)**2
            if dist_square < max_dist_square:
                handle_collision(g);
                


    def _move_ghosts(self):
        for g in self._model.ghosts:
            if g.at_home() and g.status == "fly":
                g.stop_fly()
                
            dx, dy = self._model.ghost_moving(g, speed=1)
            g.x += dx
            g.y += dy
            tag = "ghost" + str(g.id)
            self._view.move_object(tag, dx, dy)


    def _update_statuses(self):
        self._model.update_statuses()
        for g in self._model.ghosts:
            color = {
                "hunter": "red",
                "prey": "lightgreen",
                "fly": "blue"
            }[g.status]
            self._view.set_ghost_color(g)



    def _main_loop(self):
        if not self._model.pause:
            self._model.frame_time += 1
            if not self._model.frame_time % 5:
                self._model.score_point += 1
            self._handle_pacman_cell()
            self._update_statuses()
            self._check_ghosts_collision()
            self._move_ghosts()
            self._move_ball()
            self._view.update_info()

            
        animation_delay = int(1000 / self._model.fps)
        self._view._root.after(animation_delay, self._main_loop)



