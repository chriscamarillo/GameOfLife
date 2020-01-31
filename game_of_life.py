from tkinter import *
from random import randint

# initial cell creation for a given grid
def create_cells():
    cell_w, cell_h = CANVAS_W // GRID_R, CANVAS_H // GRID_C

    global cells
    cells = [[window.create_rectangle(x, y, x + cell_w, y + cell_w, fill='white')
             for y in range(0, CANVAS_W, cell_w)]
             for x in range(0, CANVAS_H, cell_h)]

# cell status checks
def is_alive(cell_pos):
    x, y = cell_pos
    return window.itemconfig(cells[x][y])['fill'][4] == 'black'

def inbounds(cell_pos):
    x, y = cell_pos
    return 0 <= x < GRID_C and 0 <= y < GRID_R

def neighbors(pos):
    x, y = pos
    neighbors = [(x + dx, y + dy) for dx in [0, 1, -1] for dy in [0, 1, -1] if
                 not (dx == 0 and dy == 0)]
    
    neighbors = filter(inbounds, neighbors)
    neighbors = filter(is_alive, neighbors)
    return list(neighbors)

# callbacks
def playpause_callback():
    play_pause.config(text='Pause' if play_pause['text'] == 'Play' else 'Play')
    global running
    running = not running
    
def randomize_callback():
    for row in range(GRID_R):
        for col in range(GRID_C):
            window.itemconfig(cells[row][col], fill='black' if randint(0,5) == 0 else 'white')

def cell_callback(event):
    # find clicked cell
    cell_x = event.x * GRID_R // CANVAS_W
    cell_y = event.y * GRID_C // CANVAS_H
    cell_pos = (cell_x, cell_y)

    # toggle cell status
    cell = cells[cell_x][cell_y]
    fill = window.itemconfig(cell)['fill'][4]
    window.itemconfig(cell, fill='white' if fill == 'black' else 'black')

    # print count of nearby living cells
    print(len(neighbors(cell_pos)))
    pass

# game logic
def setup():
    global window
    global play_pause, randomize_button
    global running
    global ticks_per_sec

    window = Canvas(root, width=CANVAS_W, height=CANVAS_H)
    window.grid(row=0, columnspan=3)
    window.bind('<ButtonPress>', cell_callback)
    
    play_pause = Button(root, text='Play', command=playpause_callback)
    play_pause.grid(row=1, column=0)

    randomize_button = Button(root, text='Random', command=randomize_callback)
    randomize_button.grid(row=1, column=1)
    
    ticks_per_sec = Scale(root, from_=1, to=60, orient=HORIZONTAL)
    ticks_per_sec.grid(row=1, column=2, columnspan=2)

    reset()

def reset():
    try:
        for row in range(GRID_R):
            for col in range(GRID_C):
                window.itemconfig(cells[row][col], fill='white')
    except NameError:
        window.delete(ALL)
        create_cells()

    running = False

def tick():
    if running:
        # main Game of Life code
        new_sheet = []
        
        for row in range(GRID_R):
            sheet_row = []
            for col in range(GRID_C):
                # population rules
                cell_pos = (row, col)
                neighbor_count = len(neighbors(cell_pos))
                if (is_alive(cell_pos) and neighbor_count == 2) or neighbor_count == 3:
                    sheet_row.append(1)
                else:
                    sheet_row.append(0)
            new_sheet.append(sheet_row)

        # parse new sheet
        for row in range(GRID_R):
            for col in range(GRID_C):
                cell = cells[row][col]
                alive = new_sheet[row][col]
                window.itemconfig(cell, fill='black' if alive else 'white')
    
    root.after(int(1000 / ticks_per_sec.get()), tick)

if __name__ == '__main__':
    global GRID_R, GRID_C
    global CANVAS_W, CANVAS_H
    global running
    global root

    GRID_R, GRID_C = 20, 20
    CANVAS_W, CANVAS_H = 500, 500
    running = False
    
    root = Tk()
    root.title('Conway\'s Game of Life')
    setup()
    tick()

    
    
