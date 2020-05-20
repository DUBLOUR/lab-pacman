import random

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

        self.direction = None
        self.next_direction = None

    
    def get_center(self):
        return self.x+self.size//2, self.y+self.size//2

    
    def get_start_xy(self):
        cx,cy = self.init_cell
        x = cx * self._model.cell_size + self._model.padding[0] - self.size // 2
        y = cy * self._model.cell_size + self._model.padding[1] - self.size // 2
        return x,y


    def dist(self, other):
        x1, y1 = self.get_center()
        x2, y2 = other.get_center()
        d = ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
        return d


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
        
        self.lives = 3
                


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
        if not self._model.is_cell_center(x, y):
            return self.direction
        
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

        return possibles
