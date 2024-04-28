import argparse
import tkinter as tk

parser = argparse.ArgumentParser()
parser.add_argument("--grid", "-g", type=str, choices=['4x4', '16x16',  '16x32', 
                                                       '32x32', '32x64', '64x64', 
                                                       '16x64', '16x96', '16x128', 
                                                       '5x5', '6x6', '10x10',  '100x100',
                                                       '128x128', '256x256'],
                    help="defind grid size. < 256x256")

grid_size = (16,16)
cells = {} # reference to cell instances
state = {} # track state of a cell

def make_cell(root, grid_row, grid_col):
    cell = tk.Canvas(master=root, width=16, height=16, background='gray75')
    cell.create_rectangle(0,0,16,16, fill='red') # init color
    # cell.bind( "<B1-Motion>", receive_interaction )
    cell.bind("<Button>",  lambda e: toggle_cell(grid_row, grid_col))
    cell.bind("c",  lambda e: check_cell(grid_row, grid_col))
    # cell.bind("<Return>",  lambda : toggle_cell(grid_row, grid_col))
    cell.grid(row=grid_row, column=grid_col, sticky=(tk.N, tk.W, tk.E, tk.S))
    cells[(grid_row, grid_col)] = cell # Set global reference
    state[(grid_row, grid_col)] = 0 # Mark dead initally
    return cell

def in_grid_range(row, col) -> bool:
    row_ok,  col_ok = False, False
    if row >= 0 and row < grid_size[0]:
        row_ok = True
    if col >= 0  and col < grid_size[1]:
        col_ok = True
    return row_ok and col_ok # True if both True

def  neighbors_of(grid_row, grid_col):
    """Returns the eight neighbors and the cell."""
    region = []
    region.append(state[(grid_row, grid_col)]) # self
    # out-of-bound grid check...
    if in_grid_range(grid_row-1, grid_col-1):
        region.append(state[(grid_row-1, grid_col-1)])
    if in_grid_range(grid_row-1, grid_col):
        region.append(state[(grid_row-1, grid_col)])
    if in_grid_range(grid_row, grid_col-1):
        region.append(state[(grid_row, grid_col-1)])
    if in_grid_range(grid_row+1, grid_col+1):
        region.append(state[(grid_row+1, grid_col+1)])
    if in_grid_range(grid_row+1, grid_col):
        region.append(state[(grid_row+1, grid_col)])
    if in_grid_range(grid_row, grid_col+1):
        region.append(state[(grid_row, grid_col+1)])
    if in_grid_range(grid_row+1, grid_col-1):
        region.append(state[(grid_row+1, grid_col-1)])
    if in_grid_range(grid_row-1, grid_col+1):
        region.append(state[(grid_row-1, grid_col+1)])
    return region

def apply_rules(grid_row, grid_col, debug=False):
    """The rules for Conway's game of life:
    1. living cell with fewer than two live neighbors die
    2. living cell with two to three live neighbors live
    3. living cell with more than three live neighbors die
    4. dead cell with three live neighbors or more become alive

    Initial value is null. When the ruleset is applied the region current state is calculated.
    The rule is applied for the current cell and then apply for the negihbors
    """
    the_region = neighbors_of(grid_row, grid_col)
    living_cells = sum(the_region[1:])
    if debug:
        print(f"{grid_row},{grid_col} state={the_region} live_neighbors={living_cells}")
    # global state
    # apply rule to current cell
    current_state = state[(grid_row, grid_col)]
    if living_cells < 2: # to die (rule 1)
        mark_dead(grid_row, grid_col)
    if living_cells in [2,3]: # stay alive (rule 2)
        mark_alive(grid_row, grid_col)
    if living_cells > 3 and current_state == 1: # to die (rule 3)
        mark_dead(grid_row, grid_col)
    if living_cells > 3 and current_state == 0: # become alive (rule 4)
        mark_alive(grid_row, grid_col)
    # need pause?

def clear_grid():
    for k in state.keys():
        mark_dead(k[0], k[1])

def mark_dead(grid_row, grid_col):
    cell = cells[(grid_row, grid_col)]
    state[(grid_row, grid_col)] = 0
    cell.create_rectangle(0,0,16,16, fill='black')

def mark_alive(grid_row, grid_col):
    cell = cells[(grid_row, grid_col)]
    state[(grid_row, grid_col)] = 1
    cell.create_rectangle(0,0,16,16, fill='blue')

def check_cell(grid_row, grid_col):
    print(f"Stat row={grid_row} col={grid_col}")
    the_region = neighbors_of(grid_row, grid_col)
    living_cells = sum(the_region[1:])
    print(f"{grid_row},{grid_col} state={the_region} live_neighbors={living_cells}")

def toggle_cell(grid_row, grid_col):
    print(f"Toggle row={grid_row} col={grid_col}")
    # update state 
    cell_state = state[(grid_row, grid_col)]
    cell = cells[(grid_row, grid_col)]
    if cell_state == 0:  # Dead -> Alive
        cell.create_rectangle(0,0,16,16, fill='blue')
        state[(grid_row, grid_col)] = 1
    if cell_state == 1:  # Alive -> Alive
        cell.create_rectangle(0,0,16,16, fill='black')
        state[(grid_row, grid_col)] = 0
    # and so on
    # apply_rules(grid_row, grid_col, debug=True) # appply after toggle ensures live count never below zero

def next_period():
    """compute state and next period of the game."""
    current_state = state
    print(current_state.values())
    for k in current_state.keys():
        # if state[k] == 1:
        apply_rules(k[0], k[1], debug=True)
    next_state = state
    print(next_state.values())

def main(args):
    if args.grid:
        print(f"Grid specify to: {args.grid}")
        p = args.grid.split('x')
        nrow, ncol = int(p[0]), int(p[1])
        global grid_size
        grid_size = (nrow, ncol) # set global
    else:
        print(f"Grid default: {grid_size}")
        nrow, ncol = grid_size
    window = tk.Tk()
    btn_frame = tk.Frame(master=window)
    btn_frame.pack()
    b1 = tk.Button(master=btn_frame, text="clear", command=clear_grid)
    b2 = tk.Button(master=btn_frame, text="next", command=next_period)
    b1.pack(side=tk.LEFT)
    b2.pack(side=tk.LEFT)
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