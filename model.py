import random

class Model:
    def __init__(self):
        self.padding = [12, 81, -12, 20]
        self.pacman_size = 22
        self.cell_size = 24
        self.field_size = [22, 22]   
        self.pacman_direction = 'U'
        self.pacman_next_direction = 'U'
        self.score_point = 0
        self.count_diamonds = 0
        self.ghost_size = 20
        self.ghost_count = 0
        self.ghosts_init_cell = []
        self.pac_init_cell = [0,0]
        self.pacman_state = "prey"
        self.ghost_status = []
        


    def isAvaiableCoord(self, x, y):
        padding = self.padding
        cell_size = self.cell_size
        map_field = self.map_field

        x -= padding[0]
        y -= padding[1]
        if not(x % cell_size == 0 or y % cell_size == 0):
            return False

        try:
            y = y + cell_size // 2
            x = x + cell_size // 2
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
        except BaseException as e:
            print(x, y, cell_size, len(map_field), len(map_field[0]))
            print(e.__rept__)
            exit()
        return True


    def init_level(self, number):
        def get_level_data(number):
            map_data = []
            path = f"resourses/level{str(number)}.dat"

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

        self.map_field = get_level_data(number)

        for x in range(self.field_size[0] + 1):
            for y in range(self.field_size[1]):
                tp = self.map_field[y][x]
                if tp == '.':
                    self.count_diamonds += 1
                if tp == 'G':
                    self.ghosts_init_cell.append([x,y])
                if tp == 'P':
                    self.pac_init_cell = [x,y]
        
        self.ghost_count = len(self.ghosts_init_cell);
        self.ghost_status = ["normal"] * self.ghost_count 


    def isCellCenter(self, x, y):
        x -= self.padding[0]
        y -= self.padding[1]
        return (x % self.cell_size == 0 and y % self.cell_size == 0)
