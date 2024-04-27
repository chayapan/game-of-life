import argparse
import tkinter as tk

parser = argparse.ArgumentParser()
parser.add_argument("--grid", "-g", type=str, choices=['4x4', '16x16',  '16x32', 
                                                       '32x32', '32x64', '64x64', 
                                                       '16x64', '16x96', '16x128', 
                                                       '128x128', '256x256'],
                    help="defind grid size. < 256x256")

default_grid_size = (16,16)
cells = {} # reference to cell instances
state = {} # track state of a cell

def receive_interaction(event):
   # Co-ordinates.
    x1, y1, x2, y2 = ( event.x - 3 ),( event.y - 3 ), ( event.x + 3 ),( event.y + 3 ) 
    print(x1,y1,x2,y2)

def make_cell(root, grid_row, grid_col):
    cell = tk.Canvas(master=root, width=16, height=16, background='gray75')
    cell.create_rectangle(0,0,16,16, fill='red') # init color
    # cell.bind( "<B1-Motion>", receive_interaction )
    cell.bind("<Button>",  lambda e: toggle_cell(grid_row, grid_col))
    # cell.bind("<Return>",  lambda : toggle_cell(grid_row, grid_col))
    cell.grid(row=grid_row, column=grid_col, sticky=(tk.N, tk.W, tk.E, tk.S))
    cells[(grid_row, grid_col)] = cell # Set global reference
    state[(grid_row, grid_col)] = 0 # Mark dead initally
    return cell

def  neighbors_of(grid_row, grid_col):
    """Returns the eight neighbors and the cell."""
    region = []
    region.append(state[(grid_row, grid_col)]) # self
    region.append(state[(grid_row-1, grid_col-1)])
    region.append(state[(grid_row-1, grid_col)])
    region.append(state[(grid_row, grid_col-1)])
    region.append(state[(grid_row+1, grid_col+1)])
    region.append(state[(grid_row+1, grid_col)])
    region.append(state[(grid_row, grid_col+1)])
    region.append(state[(grid_row+1, grid_col-1)])
    region.append(state[(grid_row-1, grid_col+1)])
    return region

def apply_rules(grid_row, grid_col):
    """The Conway's game of life rules:
    1. living cell with fewer than two live neighbors die
    2. living cell with two to three live neighbors live
    3. living cell with more than three live neighbors die
    4. dead cell with three live neighbors become alive
    ."""
    the_region = neighbors_of(grid_row, grid_col)
    print(the_region)


def toggle_cell(grid_row, grid_col):
    print(f"Toggle row={grid_row} col={grid_col}")
    # get state 
    cell_state = state[(grid_row, grid_col)]
    cell = cells[(grid_row, grid_col)]
    # cell.destroy() 
    apply_rules(grid_row, grid_col)
    if cell_state == 0:  # Dead -> Alive
        cell.create_rectangle(0,0,16,16, fill='green')
        state[(grid_row, grid_col)] = 1
    if cell_state == 1:  # Alive -> Alive
        cell.create_rectangle(0,0,16,16, fill='black')
        state[(grid_row, grid_col)] = 0
    # and so on

def main(args):
    if args.grid:
        print(f"Grid specify to: {args.grid}")
        p = args.grid.split('x')
        nrow, ncol = int(p[0]), int(p[1])
    else:
        print(f"Grid : {default_grid_size}")
        nrow, ncol = default_grid_size
    window = tk.Tk()
    frame1 = tk.Frame(master=window, width=100, height=100, bg="red")
    frame1.pack()
    for i in range(nrow):
        for j in range(ncol):
            b = make_cell(frame1, grid_row=i, grid_col=j)
    my_platform = window.tk.call('tk', 'windowingsystem')
    print(my_platform)
    # Menu
    window.option_add('*tearOff', tk.FALSE)
    menubar = tk.Menu(window)
    window['menu'] = menubar
    menu_file = tk.Menu(menubar)
    menu_edit = tk.Menu(menubar)
    menubar.add_cascade(menu=menu_file, label='File')
    menubar.add_cascade(menu=menu_edit, label='Edit')
    window.mainloop()

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)