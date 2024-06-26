"""
V3 - this version uses a strategy to update whole display at once. 
The program enumerate the grid's cell and apply the logic that update global data structure.

before update
calculate live status of each cell
update state
render

Make a Cell instance. Each instance track current, previous, next state internally.?
Don't. This add overhead. The linear state dict is already good.
Use state and state_next is efficient.

The fix is to have the rendering logic seperate from the clear action and the next action.
"""

import argparse
import tkinter as tk

SUPPORT_GRID_SIZES = ['4x4', '16x16',  '16x32', '32x32', '32x64', '64x64', '16x64', '16x96', '16x128', '128x128', '256x256']
grid_size = (16,16)
cells = {} # reference to cell instances
state = {} # track state of a cell
state_next = {} # the state in next period 

parser = argparse.ArgumentParser()
parser.add_argument("--grid", "-g", type=str, choices=SUPPORT_GRID_SIZES,
                    help="define grid size. < 256x256")

def receive_interaction(event):
   # Co-ordinates.
    x1, y1, x2, y2 = ( event.x - 3 ),( event.y - 3 ), ( event.x + 3 ),( event.y + 3 ) 
    print(x1,y1,x2,y2)

def make_cell(root, grid_row, grid_col):
    cell = tk.Canvas(master=root, width=16, height=16, background='gray75')
    cell.create_rectangle(0,0,16,16, fill='red') # init color
    cell.bind("<Button>",  lambda e: toggle_cell(grid_row, grid_col))
    # cell.bind( "<B1-Motion>", receive_interaction )
    # cell.bind("<Return>",  lambda : toggle_cell(grid_row, grid_col))
    cell.grid(row=grid_row, column=grid_col, sticky=(tk.N, tk.W, tk.E, tk.S))
    cells[(grid_row, grid_col)] = cell # Set global reference
    state[(grid_row, grid_col)] = 0 # Mark dead initally
    state_next[(grid_row, grid_col)] = 0 
    return cell

def in_grid_range(row, col) -> bool:
    row_ok,  col_ok = False, False
    if row >= 0 and row < grid_size[0]:
        row_ok = True
    if col >= 0  and col < grid_size[1]:
        col_ok = True
    return row_ok and col_ok # True if both True

def update_display():
    # update each cell all at once. single loop.
    for k in cells.keys():        
        cell = cells[k]
        s0 = state[k] # if need to compare to previous state if there is change.
        s1 = state_next[k]
        if s1 == 1:
            cell.create_rectangle(0,0,16,16, fill='green')
            state[k] = s1 # propagate state to next iteration
        if s1 == 0:
            cell.create_rectangle(0,0,16,16, fill='black')
            state[k] = s1 # propagate state to next iteration

def next_period():
    c = 0
    for k in cells.keys():   
        apply_rules(k[0], k[1])
        c += 1
    print(f"Updated. cells_count={c}")
    update_display()

def clear_grid():
    c = 0
    for k in cells.keys():
        state[k] = 0
        state_next[k] = 0
        c += 1
    print(f"Cleared. cells_count={c}")
    update_display()

def mark_dead(grid_row, grid_col):
    """Mark the cell dead for next state."""
    state_next[(grid_row, grid_col)] = 0

def mark_alive(grid_row, grid_col):
    """Mark the cell alive in next state."""
    state_next[(grid_row, grid_col)] = 1

def  neighbors_of(grid_row, grid_col):
    """Returns the eight neighbors and the cell."""
    neighborhood = []
    neighborhood.append(state[(grid_row, grid_col)]) # self
    # out-of-bound grid check...
    if in_grid_range(grid_row-1, grid_col-1):
        neighborhood.append(state[(grid_row-1, grid_col-1)])
    if in_grid_range(grid_row-1, grid_col):
        neighborhood.append(state[(grid_row-1, grid_col)])
    if in_grid_range(grid_row, grid_col-1):
        neighborhood.append(state[(grid_row, grid_col-1)])
    if in_grid_range(grid_row+1, grid_col+1):
        neighborhood.append(state[(grid_row+1, grid_col+1)])
    if in_grid_range(grid_row+1, grid_col):
        neighborhood.append(state[(grid_row+1, grid_col)])
    if in_grid_range(grid_row, grid_col+1):
        neighborhood.append(state[(grid_row, grid_col+1)])
    if in_grid_range(grid_row+1, grid_col-1):
        neighborhood.append(state[(grid_row+1, grid_col-1)])
    if in_grid_range(grid_row-1, grid_col+1):
        neighborhood.append(state[(grid_row-1, grid_col+1)])
    return neighborhood

def apply_rules(grid_row, grid_col, debug=True):
    """The rules for Conway's game of life:
    1. living cell with fewer than two live neighbors die
    2. living cell with two to three live neighbors live
    3. living cell with more than three live neighbors die
    4. dead cell with three live neighbors become alive

    Initial value is null. When the ruleset is applied the region current state is calculated.
    The rule is applied for the current cell and then apply for the negihbors
    """
    the_region = neighbors_of(grid_row, grid_col)
    living_cells = sum(the_region[1:])
    if debug:
        print(f"{grid_row},{grid_col} state={the_region} live_neighbors={living_cells}")
    
    # apply rule to current cell
    current_state = state[(grid_row, grid_col)]
    if living_cells < 2 and current_state == 1: # to die (rule 1)
        mark_dead(grid_row, grid_col)
    if living_cells in [2,3] and current_state == 1: # stay alive (rule 2)
        mark_alive(grid_row, grid_col)
    if living_cells > 3 and current_state == 1: # to die (rule 3)
        mark_dead(grid_row, grid_col)
    if living_cells >= 3 and current_state == 0: # become alive (rule 4)
        mark_alive(grid_row, grid_col)

def toggle_cell(grid_row, grid_col):
    print(f"Toggle row={grid_row} col={grid_col}")
    # update state 
    cell_state = state[(grid_row, grid_col)]
    cell = cells[(grid_row, grid_col)]
    if cell_state == 0:  # Dead -> Alive
        cell.create_rectangle(0,0,16,16, fill='green')
        state[(grid_row, grid_col)] = 1
    if cell_state == 1:  # Alive -> Dead
        cell.create_rectangle(0,0,16,16, fill='black')
        state[(grid_row, grid_col)] = 0
    
def draw_initial_state(root, nrow, ncol):
    for i in range(nrow):
        for j in range(ncol):
            make_cell(root, grid_row=i, grid_col=j)

def main(args):
    global grid_size
    if args.grid:
        print(f"Grid specify to: {args.grid}")
        p = args.grid.split('x')
        nrow, ncol = int(p[0]), int(p[1])
        grid_size = (nrow, ncol)
    else:
        print(f"Grid : {grid_size}")
        nrow, ncol = grid_size
    window = tk.Tk()
    frame1 = tk.Frame(master=window, width=100, height=100, bg="red")
    frame1.pack()
    draw_initial_state(root=frame1, nrow=nrow, ncol=ncol)
    btn_frame = tk.Frame(master=window)
    btn_frame.pack()
    b1 = tk.Button(master=btn_frame, text="clear", command=clear_grid)
    b2 = tk.Button(master=btn_frame, text="next", command=next_period)
    b1.pack(side=tk.LEFT)
    b2.pack(side=tk.LEFT)
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