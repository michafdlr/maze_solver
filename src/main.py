from utils import Window, Line, Point, Cell
from maze_funcs import Maze
def main():
    WIDTH, HEIGHT = 800, 600
    num_rows = 20
    num_cols = 20
    offset = 5
    win = Window(WIDTH, HEIGHT)
    maze = Maze(offset,offset,num_rows,num_cols,(WIDTH-offset)//num_cols,(HEIGHT-0.5*offset)//num_rows,win, 0)
    win.wait_for_close()
main()
