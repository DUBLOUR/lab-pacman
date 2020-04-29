import tkinter as tk
#import random
root = tk.Tk()

root.wm_title('Baka-baka-baka')
padding = [12, 81, -12, 20]
pacman_size = 24
cell_size = 24
field_size = [22, 22]

window_width = cell_size * (field_size[0] + 1) + padding[0] + padding[2]
window_height = cell_size * field_size[1] + padding[1] + padding[3]

#window_width, window_height = 464,624

pacman_direction = 'U'
pacman_next_direction = 'U'
score_point = 0
count_diamonds = 0

gim = []
last_cell_object = [[None for j in range(field_size[0]+2)] for i in range(field_size[1]+2)] 

def keyboard_input(event=None):
    convertor = dict({
        'w': 'U', 'Up': 'U',
        'a': 'L', 'Left': 'L',
        's': 'D', 'Down': 'D',
        'd': 'R', 'Right': 'R'
    })

    key = str(event.keysym)
    print(key)
    if key == 'q':
        exit()

    if key in convertor:
        global pacman_next_direction
        pacman_next_direction = convertor[key]


def create_memes():
    global canvas, ball
    ball = canvas.create_oval((0, 0), (pacman_size, pacman_size),
                              fill="yellow", outline="black", tag="pacman")
    #canvas.create_line((8,8), (8,24), tag="pacman")
    #canvas.create_line((24,8), (24,24), tag="pacman")

    global gim
    path = f'resourses/textures/small_golden_helmet.png'
    gim.append(tk.PhotoImage(file=path))
    #canvas.create_image(0, 0, image=gim[-1], anchor=tk.NW, tag="pacman")

    pac_x = 11 * cell_size + padding[0] - pacman_size // 2
    pac_y = 16 * cell_size + padding[1] - pacman_size // 2
    canvas.move("pacman", pac_x, pac_y)


canvas = tk.Canvas(root, width=window_width, height=window_height)

canvas.focus_set()
canvas.bind('<Key>', keyboard_input)


def isAvaiableCoord(x, y):
    x -= padding[0]
    y -= padding[1]
    if not(x % cell_size == 0 or y % cell_size == 0):
        return False

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
    return True


def getPacCoord():
    c = list(map(int, canvas.coords(ball)))
    return (c[0] + c[2]) // 2, (c[1] + c[3]) // 2


def isCellCenter(x, y):
    x -= padding[0]
    y -= padding[1]
    return (x % cell_size == 0 and y % cell_size == 0)


def open_next_level():
    print("YOU WIN!");


def cellHandling(x, y):
    x = (x - padding[0]) // cell_size
    y = (y - padding[1]) // cell_size
    if  not(0 <= x < field_size[0]) or \
        not(0 <= y < field_size[1]):
        return

    global map_field
    tp = map_field[y][x]
    print("IS CELL", x, y, map_field[y][x])
    hasChange = False
    if tp == '.':
        map_field[y][x] = ' '
        global score_point
        score_point += 100
        global count_diamonds
        count_diamonds -= 1
        if count_diamonds == 0:
            open_next_level()
        print(score_point)
        hasChange = True

    if hasChange:
        drawCell(y, x)


def drawCell(y, x):
    tp = map_field[y][x][0]
    color = {
        '#': 'red',
        '.': 'black',
        'P': 'yellow',
        ' ': 'blue',
        'B': 'orange',
        'G': 'white',
        '_': 'green',
        '|': 'magenta'
    }[tp]

    texture = {
        '#': 'bricks',
        '.': 'diamond_ore',
        ' ': 'stone',
        'P': 'stone',
        '_': 'oak_planks',
        '|': 'stone',
        'G': 'cobblestone',
        'B': 'mossy_cobblestone'
    }.get(tp, None)

    xc = x * cell_size + padding[0] - cell_size // 2
    yc = y * cell_size + padding[1] - cell_size // 2

    global last_cell_object
    canvas_object = last_cell_object[y][x]
    if canvas_object != None:
        canvas.delete(canvas_object)

    if texture is not None:
        canvas_object = put_cell_img(texture, xc, yc)
    else:
        canvas_object = canvas.create_rectangle(
            xc, yc, xc + cell_size, yc + cell_size, fill=color)
    
    canvas.tag_lower(canvas_object)
    last_cell_object[y][x] = canvas_object
    print(canvas_object)



def moveBall():

    # tryChangeDirection()
    # print(canvas.coords(ball))
    global pacman_direction
    x, y = getPacCoord()
    #print(x, y)
    if isCellCenter(x, y):
        cellHandling(x, y)

    dir_to_vect = {'U': [0, -1], 'D': [0, 1], 'L': [-1, 0], 'R': [1, 0]}
    vec = dir_to_vect[pacman_next_direction]

    if isAvaiableCoord(x + vec[0], y + vec[1]):
        pacman_direction = pacman_next_direction

    vec = dir_to_vect[pacman_direction]

    if x + vec[0] == -pacman_size:
        canvas.move("pacman", 24 * cell_size, 0)
    elif x + vec[0] == 24 * cell_size - pacman_size + 1:
        canvas.move("pacman", -24 * cell_size, 0)
    elif isAvaiableCoord(x + vec[0], y + vec[1]):
        canvas.move("pacman", vec[0], vec[1])
    root.after(10, moveBall)


def show_grid():
    return
    for y in range(window_height):
        for x in range(window_width):
            if isAvaiableCoord(x, y):
                canvas.create_line(x, y, x, y, width=1, fill="gray")


def add_background():
    global gim
    gim = tk.PhotoImage(file='resourses/bg.png')
    canvas.create_image(0, 0, image=gim, anchor=tk.NW, tag='qwe')


canvas.pack()

# add_background()




def put_cell_img(name, x, y):
    global gim
    path = f'resourses/textures/small_{name}.png'
    gim.append(tk.PhotoImage(file=path))
    return canvas.create_image(x, y, image=gim[-1], anchor=tk.NW)


def paint_background():
    def get_level_data(number):
        map_data = []
        path = f"resourses/level{str(number)}.dat"
        # with open(path) as f:
        #     map_data = f.readlines()
        #     for i in range(len(map_data) - 1):
        #         map_data[i] = map_data[i][:]
        #     map_data[-1] += "\n"
        #     map_data.append(map_data[-1])

        with open(path) as f:
            field = f.readlines()
            field[-1] += "\n"

            for y in range(field_size[1]):
                line = []
                for x in range(field_size[0]+1):
                    line.append(field[y][x])
                line.append(line[-1])
                #line.append(line[-2])
                map_data.append(line[:])
            map_data.append(map_data[-1])

        print(map_data)
        return map_data

    global map_field
    global count_diamonds
    map_field = get_level_data(2)

    for x in range(field_size[0] + 1):
        for y in range(field_size[1]):
            drawCell(y, x)
            if map_field[y][x] == '.':
                count_diamonds += 1




# paint_background()
paint_background()
# exit()
show_grid()

create_memes()
moveBall()


root.mainloop()
