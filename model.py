import random
import json


def get_dist(px, py, gx, gy):
    dx = px - gx
    dy = py - gy
    return (dx**2 + dy**2) ** 0.5


class Enemy:
    def __init__(self, model):
        self._model = model
        self.size = 0
        self.x = 0
        self.y = 0

    
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
        self.state = "hunter"

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
        self.color = "red"


    def at_home(self):
        x = round(self.x, 3)
        y = round(self.y, 3)
        hx, hy = self.get_start_xy()
        hx = round(hx, 3)
        hy = round(hy, 3)
        
        return (x, y) == (hx, hy)


    def stop_fly(self):
        self.status = "normal"



class Model:
    def __init__(self):
        self.padding = [12, 12+20, -12, 80]
        self.cell_size = 24
        self.field_size = [22, 22]   
        self.score_point = 0
        self.count_diamonds = 0
        
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
        g = GhostModel(self, id, x, y, "normal")
        g.init_cell = [x,y]
        g.x, g.y = g.get_start_xy()
        self.ghosts.append(g)


    def ghost_moving(self, g, speed):
        speed *= g.speed
        def fly_moving():
            need_x, need_y = g.get_start_xy()
            dx = need_x - g.x
            dy = need_y - g.y
            #dist = get_dist(g.x, g.y, need_x, need_y)
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist <= speed:
                return dx, dy

            return dx/dist, dy/dist
            

        def hunt_moving():
            need_x, need_y = self.pacman.get_center()
            dx = need_x - g.x
            dy = need_y - g.y
            #dist = get_dist(g.x, g.y, need_x, need_y)
            dist = (dx ** 2 + dy ** 2) ** 0.5

            return dx/dist, dy/dist


        def avoid_moving():
            home = g.get_start_xy()
            hunter = self.pacman.get_center()

            dx = (home[0] - g.x)**0.5 - (hunter[0] - g.x)**0.7
            dy = (home[1] - g.y)**0.5 - (hunter[1] - g.y)**0.7
            return dx, dy


        func_transpose = {
            "fly": fly_moving,
            "avoid": avoid_moving,
            "normal": hunt_moving
        }[g.status]

        dx, dy = func_transpose()
        return dx * speed, dy * speed




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
        

        
    def eat_point(self, y, x):
        self.map_field[y][x] = ' '
        self.score_point += 100
        self.count_diamonds -= 1
        if not self.count_diamonds:
            self.level_finishes = True
        print(self.score_point)
    

    