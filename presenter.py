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

        if key in convertor:
            self._model.pacman.next_direction = convertor[key]



    def open_next_level(self):
        pass


    def cell_handling(self, x, y):
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

        if hasChange:
            self._view.draw_cell(y, x)


    def move_pacman(self, x, y):
        p = self._model.pacman
        p.x += x; p.y += y
        self._view.canvas.move("pacman", x, y)


    def move_ball(self):

        pacman = self._model.pacman
        
        x, y = pacman.get_center()
        #print(x, y, '\t', pacman.direction, pacman.next_direction)
        if self._model.is_cell_center(x, y):
             self.cell_handling(x, y)
        # checkGhostCollision()

        dir_to_vect = {
            'U': [0, -1], 
            'D': [0, 1], 
            'L': [-1, 0], 
            'R': [1, 0]
        }
        vec = dir_to_vect[pacman.next_direction]

        if self._model.is_avaiable_coord(x + vec[0], y + vec[1]):
            pacman.direction = pacman.next_direction
            
        vec = dir_to_vect[pacman.direction]

        if x + vec[0] == -pacman.size:
            self.move_pacman(24 * self._model.cell_size, 0)
        elif x + vec[0] == 24 * self._model.cell_size - pacman.size + 1:
            self.move_pacman(-24 * self._model.cell_size, 0)
        elif self._model.is_avaiable_coord(x + vec[0], y + vec[1]):
            self.move_pacman(vec[0], vec[1])
        


    def main_loop(self):
        if self._model.level_finishes:
            print("YAHO")
            self.exit()

        self.move_ball()
        
        animation_delay = int(1000 / self.fps)
        self._view._root.after(animation_delay, self.main_loop)



