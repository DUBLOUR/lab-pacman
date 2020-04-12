import tkinter as tk
import random
root = tk.Tk()

root.wm_title('Baka-baka-baka')
window_width = 310
window_height = 400

pacman_direction = 'R'
pacman_next_direction = 'R'

pacman_size = 32

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


canvas = tk.Canvas(root, width=window_width, height=window_height, bg='black')

ball = canvas.create_oval((0,0), (pacman_size, pacman_size), 
            fill="yellow", outline="yellow", tag="pacman")
canvas.create_line((8,8), (8,24), tag="pacman")
canvas.create_line((24,8), (24,24), tag="pacman")

canvas.focus_set()
canvas.bind('<Key>', keyboard_input)
canvas.pack()

def moveBall():

    def isAvaiableCoord(x, y):
        return x >= 0 and \
            y >= 0 and \
            x < window_width-pacman_size and \
            y < window_height-pacman_size

    #tryChangeDirection()
    #print(canvas.coords(ball))
    global pacman_direction
    x, y = map(int, canvas.coords(ball)[0:2]) 
    print(x,y)
    dir_to_vect = {'U':[0,-1], 'D':[0,1], 'L':[-1,0], 'R':[1,0]}
    vec = dir_to_vect[pacman_next_direction]

    if isAvaiableCoord(x+vec[0], y+vec[1]):
        pacman_direction = pacman_next_direction
    
    vec = dir_to_vect[pacman_direction]
    if isAvaiableCoord(x+vec[0], y+vec[1]):
        canvas.move("pacman", vec[0], vec[1]) 
    root.after(10, moveBall)
    
    

moveBall()

root.mainloop()
