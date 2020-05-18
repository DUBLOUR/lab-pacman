from model import Model
from view import View

class Presenter:
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
            self._model.pacman_next_direction = convertor[key]


    def getPacCoord(self):
        c = list(map(int, self._view.canvas.coords(self._view.ball)))
        return (c[0] + c[2]) // 2, (c[1] + c[3]) // 2


    def open_next_level(self):
        pass


    def cellHandling(self, x, y):
        x = (x - self._model.padding[0]) // self._model.cell_size
        y = (y - self._model.padding[1]) // self._model.cell_size
        if  not(0 <= x < self._model.field_size[0]) or \
            not(0 <= y < self._model.field_size[1]):
            return

        tp = self._model.map_field[y][x]
        print("IS CELL", x, y, tp)
        hasChange = False
        if tp == '.':
            self._model.map_field[y][x] = ' '
            self._model.score_point += 100
            self._model.count_diamonds -= 1
            if self._model.count_diamonds == 0:
                self.open_next_level()
            print(self._model.score_point)
            hasChange = True

        if hasChange:
            self._view.drawCell(y, x)



    def moveBall(self):

        pacman_direction = self._model.pacman_direction
        pacman_next_direction = self._model.pacman_next_direction

        x, y = self.getPacCoord()
        print(x, y, '\t', pacman_direction, pacman_next_direction)
        if self._model.isCellCenter(x, y):
             self.cellHandling(x, y)
        # checkGhostCollision()

        dir_to_vect = {'U': [0, -1], 'D': [0, 1], 'L': [-1, 0], 'R': [1, 0]}
        vec = dir_to_vect[pacman_next_direction]

        if self._model.isAvaiableCoord(x + vec[0], y + vec[1]):
            pacman_direction = pacman_next_direction
            self._model.pacman_direction = pacman_direction

        vec = dir_to_vect[pacman_direction]

        if x + vec[0] == -self._model.pacman_size:
            self._view.canvas.move("pacman", 24 * self._model.cell_size, 0)
        elif x + vec[0] == 24 * self._model.cell_size - self._model.pacman_size + 1:
            self._view.canvas.move("pacman", -24 * self._model.cell_size, 0)
        elif self._model.isAvaiableCoord(x + vec[0], y + vec[1]):
            self._view.canvas.move("pacman", vec[0], vec[1])
        self._view._root.after(10, self.moveBall)




