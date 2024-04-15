from utils import Window
from maze_funcs import Maze
import time
def main():
    WIDTH, HEIGHT = 800, 600
    num_rows = 10
    num_cols = 10
    offset = 5
    win = Window(WIDTH, HEIGHT)
    win.redraw()
    maze = Maze(offset,offset,num_rows,num_cols,(WIDTH-offset)//num_cols,(HEIGHT-0.5*offset)//num_rows,win)
    t_start = time.time()
    win.start_dfs_timer()
    maze.solve(0.1)
    t_end = time.time()
    win.stop_dfs_timer()
    print(f"Time to solve: {t_end-t_start}")
    win.start_bfs_timer()
    t_start = time.time()
    maze.solve_bfs(0.1)
    t_end = time.time()
    win.stop_bfs_timer()
    print(f"Time to solve: {t_end-t_start}")
    win.wait_for_close()
main()
