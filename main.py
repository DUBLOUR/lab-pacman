import tkinter as tk
#import random
root = tk.Tk()

root.wm_title('Baka-baka-baka')
padding = [25, 81, 15, 60]
pacman_size = 20
cell_size = 20
field_size = [23, 22]

window_width = cell_size * field_size[0] + padding[0] + padding[2]
window_height = cell_size * field_size[1] + padding[1] + padding[3]

window_width, window_height = 464,624

pacman_direction = 'U'
pacman_next_direction = 'U'


def keyboard_input(event=None):
    convertor = dict({ 
        'w':'U', 'Up'   :'U', 
        'a':'L', 'Left' :'L',
        's':'D', 'Down' :'D', 
        'd':'R', 'Right':'R'
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
    ball = canvas.create_oval((0,0), (pacman_size, pacman_size), 
                fill="yellow", outline="yellow", tag="pacman")
    canvas.create_line((8,8), (8,24), tag="pacman")
    canvas.create_line((24,8), (24,24), tag="pacman")
    canvas.move("pacman", padding[0]-pacman_size//2, padding[1]-pacman_size//2)    

canvas = tk.Canvas(root, width=window_width, height=window_height)

canvas.focus_set()
canvas.bind('<Key>', keyboard_input)


def isAvaiableCoord(x, y):
    x -= padding[0]
    y -= padding[1]
    return \
        0 <= y <= field_size[1]*cell_size and \
        0 <= x <= field_size[0]*cell_size and \
        (x % cell_size == 0 or y % cell_size == 0)

def getPacCoord():
    c = list(map(int, canvas.coords(ball)))
    return c[0]+pacman_size//2, c[1]+pacman_size//2
    

def moveBall():

    #tryChangeDirection()
    #print(canvas.coords(ball))
    global pacman_direction
    x, y = getPacCoord()
    print(x,y)
    dir_to_vect = {'U':[0,-1], 'D':[0,1], 'L':[-1,0], 'R':[1,0]}
    vec = dir_to_vect[pacman_next_direction]

    if isAvaiableCoord(x+vec[0], y+vec[1]):
        pacman_direction = pacman_next_direction
    
    vec = dir_to_vect[pacman_direction]
    if isAvaiableCoord(x+vec[0], y+vec[1]):
        canvas.move("pacman", vec[0], vec[1]) 
    root.after(10, moveBall)
    

def show_grid():
    for y in range(window_height):
        for x in range(window_width):
            if isAvaiableCoord(x, y):
                canvas.create_line(x, y, x, y, width=1, fill="gray")
    


def add_background():
    def part(source: tk.PhotoImage, corner1_x, corner1_y, corner2_x, corner2_y) -> tk.PhotoImage:
        def tuple_rgb(arg):
            return '#{:02x}{:02x}{:02x}'.format(*arg)

        if corner1_x > corner2_x:
            corner1_x, corner2_x = corner2_x, corner1_x
        if corner1_y > corner2_y:
            corner1_y, corner2_y = corner2_y, corner1_y
        w = corner2_x - corner1_x
        h = corner2_y - corner1_y
        dest = tk.PhotoImage(width=w, height=h)
        for j in range(h):
            for i in range(w):
                dest.put(tuple_rgb(source.get(corner1_x + i, corner1_y + j)), to=(i, j))
        return dest

    global gim
    gim = part(tk.PhotoImage(file='resourses/bg.png'), 0, 0, 464, 624)
    canvas.create_image(0, 0, image=gim, anchor=tk.NW, tag='qwe')


canvas.pack()

add_background()
show_grid()

create_memes()
moveBall()


root.mainloop()
