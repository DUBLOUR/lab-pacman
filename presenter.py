from model import Model
from view import View



class Presenter:
    def __init__(self, levels):
        self.__levels = levels
        self.__now_level = 0

        self.__model = Model()
        self.__view = View(self.__model)
    

    def start_game(self):
        self.__run_level(self.__levels[0])


    def __show(self):
        self.__view.show()


    def __set_binds(self):
        self.__view.canvas.bind('<Key>', self.__keyboard_input)


    def __exit(self):
        exit()


    def __run_level(self, level):
        self.__model.init_level(level)
        self.__view.load_level_textures()
        self.__view.draw_background()
        self.__view.create_enemies()
        self.__set_binds()
        #view.show_grid()
        self.__main_loop()
        self.__show()


    def __show_manual(self):
        print("      WASD or Arrows - move Pacman")
        print("     `h' or `?' - show this manual")
        print("         `q' - quit from game")
        print("        `p' - turn on/off pause")


    def __keyboard_input(self, event=None):   
        convertor = dict({
            "w":"U",  "W":"U",  "Up": "U",
            "a":"L",  "A":"L",  "Left": "L",
            "s":"D",  "S":"D",  "Down": "D",
            "d":"R",  "D":"R",  "Right": "R"
        })

        key = str(event.keysym)
        #print(key)
        if key == "q" or key == "Q":
            self.__exit()

        if key == "h" or key == "H" or key == "question":
            self.__show_manual()

        if key == "p" or key == "P":
            self.pause()

        if key in convertor:
            self.__model.pacman.next_direction = convertor[key]


    def pause(self):
        self.__model.pause = not self.__model.pause


    def __handle_pacman_cell(self):
        x, y = self.__model.pacman.get_center()
        if  not self.__model.is_cell_center(x, y):
            return

        x = (x - self.__model.padding[0]) // self.__model.cell_size
        y = (y - self.__model.padding[1]) // self.__model.cell_size
        if  not(0 <= x < self.__model.field_size[0]) or \
            not(0 <= y < self.__model.field_size[1]):
            return


        tp = self.__model.map_field[y][x]
        hasChange = False
        if tp == '.':
            self.__model.eat_point(y, x)
            hasChange = True

        if tp == 'B':
            self.__model.eat_bonus(y, x)
            hasChange = True

        if hasChange:
            self.__view.draw_cell(y, x)


    def __move_pacman(self, x, y):
        p = self.__model.pacman
        p.x += x; 
        p.y += y
        self.__view.move_object("pacman", x, y)


    def __move_ball(self):
        pacman = self.__model.pacman
        x, y = pacman.get_center()

        dir_to_vect = {
            "U": [0, -2], 
            "D": [0, 2], 
            "L": [-2, 0], 
            "R": [2, 0]
        }
        dx, dy = dir_to_vect[pacman.next_direction]

        if self.__model.is_avaiable_coord(x + dx, y + dy):
            pacman.direction = pacman.next_direction
            
        dx, dy = dir_to_vect[pacman.direction]

        world_width = self.__model.world_width
        is_teleport = False

        if x + dx <= -pacman.size:
            # teleport Left -> Right
            is_teleport = True
            self.__move_pacman(world_width, 0)
        elif x + dx >= world_width - pacman.size + 1:
            # teleport Right -> Left
            is_teleport = True
            self.__move_pacman(-world_width, 0)
        elif self.__model.is_avaiable_coord(x + dx, y + dy):
            # Standart moving
            self.__move_pacman(dx, dy)
        
        if self.__model.level_finishes and is_teleport:
            self.__goto_next_level()


    def __goto_next_level(self):
        if self.__now_level == len(self.__levels)-1:
            self.__model.game_over(1)
            return
        
        scores = self.__model.score_point
        lives = self.__model.pacman.lives

        old_root = self.__view.root
        self.__model = Model()
        old_root.destroy()
        self.__view = View(self.__model)
        

        self.__model.score_point = scores
        self.__model.pacman.lives = lives
        
        self.__now_level += 1
        level = self.__levels[self.__now_level]
        self.__run_level(level)
    

    def __kill_pacman(self):
        self.__model.kill_pacman()


    def __kill_ghost(self, ghost):
        ghost.status = "fly";


    def __check_ghosts_collision(self):
        def handle_collision(g):
            if g.status == "fly":
                return;

            #print("IS COLLISTION WITH", g.id, "!!!")
            if pac.state == "prey":
                self.__kill_pacman()
            elif pac.state == "hunter":
                self.__kill_ghost(g)


        pac = self.__model.pacman
        px, py = pac.get_center()
        
        for g in self.__model.ghosts:
            gx, gy = g.get_center()
            max_dist_square = (pac.size + g.size) ** 2 // 4
            dist_square = (px-gx)**2 + (py-gy)**2
            if dist_square < max_dist_square:
                handle_collision(g);
                

    def __move_ghosts(self):
        for g in self.__model.ghosts:
            if g.at_home() and g.status == "fly":
                g.stop_fly()
                
            dx, dy = self.__model.ghost_moving(g, speed=2)
            g.x += dx
            g.y += dy
            tag = "ghost" + str(g.id)
            self.__view.move_object(tag, dx, dy)


    def __update_statuses(self):
        self.__model.update_statuses()
        for g in self.__model.ghosts:
            self.__view.set_ghost_color(g)


    def __main_loop(self):
        if not self.__model.pause:
            self.__model.frame_time += 1
            self.__model.tick_score()
            self.__handle_pacman_cell()
            self.__update_statuses()
            self.__check_ghosts_collision()
            self.__move_ghosts()
            self.__move_ball()
            self.__view.update_info()

            
        animation_delay = int(1000 / self.__model.fps)
        self.__view.root.after(animation_delay, self.__main_loop)



