import random
import json
import time


def get_dist(px, py, gx, gy):
    dx = px - gx
    dy = py - gy
    return (dx**2 + dy**2) ** 0.5

def ceil(x):
    return int(x + 1 - 1e-6)


class Enemy:
    def __init__(self, model):
        self._model = model
        self.size = 0
        self.x = 0
        self.y = 0

        self.direction = None
        self.next_direction = None
        

    
    def get_center(self):
        return self.x+self.size//2, self.y+self.size//2

    
    def get_start_xy(self):
        cx,cy = self.init_cell
        x = cx * self._model.cell_size + self._model.padding[0] - self.size // 2
        y = cy * self._model.cell_size + self._model.padding[1] - self.size // 2
        return x,y



class PacmanModel(Enemy):
    def __init__(self, model):
        super(PacmanModel, self).__init__(model)
        self.size = 22
        self.direction = 'U'
        self.next_direction = 'U'
        self.state = "prey"
        
        self.init_cell = [0,0]
        self.x = 0
        self.y = 0
                


class GhostModel(Enemy):
    def __init__(self, model, id, cell_x, cell_y, status):
        super(GhostModel, self).__init__(model)
        self.id = id
        self.size = 20
        self.init_cell = [cell_x, cell_y]
        self.status = status

        self.speed = random.uniform(0.3, 2)
        self.color_status = {
            "hunter": "red",
            "prey": "lightgreen",
            "fly": "blue"
        }


    def at_home(self):
        x, y = self.x, self.y
        hx, hy = self.get_start_xy()
        return get_dist(x, y, hx, hy) < 1e-6


    def stop_fly(self):
        self.status = "prey"
        self.x = int(self.x + 0.001)
        self.y = int(self.y + 0.001)


    def get_possible_steps(self):
        x, y = self.get_center()
        #print('\n', self.__dict__, x, y)
        if not self._model.is_cell_center(x, y):
            return self.direction
        
        #print(x, y, '\t', pacman.direction, pacman.next_direction)

        dir_to_vect = {
            "U": [0, -1], 
            "D": [0, 1], 
            "L": [-1, 0], 
            "R": [1, 0]
        }

        possibles = []
        for key, [dx, dy] in dir_to_vect.items():
            if self._model.is_avaiable_coord(x + dx, y + dy):
                possibles.append(key)

        #print(self.__dict__, possibles)
        return possibles






class Model:
    def __init__(self):
        self.padding = [12, 12+20, -12, 80]
        self.cell_size = 24
        self.field_size = [22, 22]   
        self.score_point = 0
        self.count_diamonds = 0
        self.bonus_lasting = 0
        self.frame_time = 0
        
        self.level_id = 0
        self.level_finishes = False

        self.ghosts = []
        self.pacman = PacmanModel(self)


    def get_enemy_start_xy(self, enemy):
        cx,cy = enemy.init_cell
        x = cx * self.cell_size + self.padding[0] - enemy.size // 2
        y = cy * self.cell_size + self.padding[1] - enemy.size // 2
        return x,y

    
    def set_pacman_init(self, x, y):
        p = self.pacman
        p.init_cell = [x,y]
        p.x, p.y = self.pacman.get_start_xy()
        

    def add_ghost(self, x, y):
        id = len(self.ghosts)
        g = GhostModel(self, id, x, y, "hunter")
        g.init_cell = [x,y]
        g.x, g.y = g.get_start_xy()
        self.ghosts.append(g)


    def ghost_moving(self, g, speed):
        def fly_moving():
            need_x, need_y = g.get_start_xy()
            dx = need_x - g.x
            dy = need_y - g.y
            #dist = get_dist(g.x, g.y, need_x, need_y)
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist <= 1:
                return dx, dy

            dx *= speed / dist
            dy *= speed / dist
            return dx, dy
            

        def cell_walking(motivations):
            if random.random() > speed/ceil(speed):
                return 0,0

            need_x, need_y = self.pacman.get_center()

            avaiable_steps = g.get_possible_steps()
            ant_dir = {
                "U": "D",
                "D": "U",
                "L": "R",
                "R": "L",
                None: None
            }[g.direction]

            vct = {
                "U": [0, -1], 
                "D": [0, 1], 
                "L": [-1, 0], 
                "R": [1, 0]
            }

            weights = [1] * len(avaiable_steps)
            if g.direction in avaiable_steps:
                ind = avaiable_steps.index(g.direction) 
                weights[ind] *= motivations["go_forward"]

            if ant_dir in avaiable_steps:
                ind = avaiable_steps.index(ant_dir) 
                weights[ind] *= motivations["turn_around"]
            
            for i in range(len(avaiable_steps)):
                x = g.x + vct[avaiable_steps[i]][0]
                y = g.y + vct[avaiable_steps[i]][1]
                p = self.pacman
                now_dist = get_dist(g.x, g.y, p.x, p.y)
                new_dist = get_dist(x, y, p.x, p.y)
                if new_dist < now_dist: # closer to pacman
                    weights[i] *= motivations["to_pac"]
                    if new_dist < 4*self.cell_size:
                        weights[i] *= motivations["to_close_pac"]

            g.direction = random.choices(avaiable_steps, weights)[0]

            dx, dy = vct[g.direction]
            dx *= ceil(speed)
            dy *= ceil(speed)
            return dx, dy


        def hunt_moving():
            motivations = {
                "go_forward": 2,
                "turn_around": 1/8,
                "to_pac": 2,
                "to_close_pac": 3
            }
            return cell_walking(motivations)


        def avoid_moving():
            motivations = {
                "go_forward": 2,
                "turn_around": 1/8,
                "to_pac": 1/2,
                "to_close_pac": 0
            }
            return cell_walking(motivations)


        func_transpose = {
            "fly": fly_moving,
            "prey": avoid_moving,
            "hunter": hunt_moving
        }[g.status]

        
        dx, dy = func_transpose()

            # left <-> right teleport
        world_width = 24 * self.cell_size
        x = g.x + dx 
        if x <= -self.pacman.size:
            dx = world_width
        elif x >= world_width - self.pacman.size + 1:
            dx = -world_width

        return dx, dy




    def is_cell_center(self, x, y):
        x -= self.padding[0]
        y -= self.padding[1]
        return (x % self.cell_size == 0 and y % self.cell_size == 0)


    def is_avaiable_coord(self, x, y):
        padding = self.padding
        cell_size = self.cell_size
        map_field = self.map_field

        x -= padding[0]
        y -= padding[1]
        if x % cell_size != 0 and y % cell_size != 0:
            return False

        y += cell_size // 2
        x += cell_size // 2
        if map_field[y // cell_size][x // cell_size] == '#':
            return False
        if map_field[(y - cell_size // 2 - 0) // cell_size][x // cell_size] == '#':
            return False
        if map_field[(y + cell_size // 2 - 1) // cell_size][x // cell_size] == '#':
            return False
        if map_field[y // cell_size][(x - cell_size // 2 - 0) // cell_size] == '#':
            return False
        if map_field[y // cell_size][(x + cell_size // 2 - 1) // cell_size] == '#':
            return False
        return True


    def init_level(self, number):
        def read_level_data():
            path = f"resourses/level{str(number)}.dat"
            map_data = []

            with open(path) as f:
                field = f.readlines()
                field[-1] += "\n"

                for y in range(self.field_size[1]):
                    line = []
                    for x in range(self.field_size[0]+1):
                        line.append(field[y][x])
                    line.append(line[-1])
                    line.append(line[-2])
                    map_data.append(line[:])
                map_data.append(map_data[-1])
                map_data.append(map_data[-1])

            print(map_data)
            return map_data


        def read_level_colors():
            path = f"resourses/level{str(number)}_colors.json"
            with open(path) as f:
                colors = json.load(f)
            return colors


        def parse_map():
            for x in range(self.field_size[0] + 1):
                for y in range(self.field_size[1]):
                    tp = self.map_field[y][x]
                    if tp == '.':
                        self.count_diamonds += 1
                    if tp == 'G':
                        self.add_ghost(x,y)
                    if tp == 'P':
                        self.set_pacman_init(x,y)


        self.level_id = number
        self.map_field = read_level_data()
        self.map_colors = read_level_colors()
        parse_map()
        

    def update_statuses(self):
        if self.frame_time > self.bonus_lasting:
            self.pacman.status = "prey"
            for g in self.ghosts:
                if g.status != "fly":
                    g.status = "hunter"
            return

        self.pacman.status = "hunter"
        for g in self.ghosts:
            if g.status != "fly":
                g.status = "prey"

        
    def eat_point(self, y, x):
        self.map_field[y][x] = ' '
        self.score_point += 100
        self.count_diamonds -= 1
        if not self.count_diamonds:
            self.level_finishes = True
        print(self.score_point)
    

    def eat_bonus(self, y, x):
        self.map_field[y][x] = ' '
        self.score_point += 1000
        bonus_duration = 1000
        self.bonus_lasting = self.frame_time + bonus_duration

    