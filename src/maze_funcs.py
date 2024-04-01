from utils import Cell
import time
import random

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = [[Cell(self._win) for _ in range(self._num_rows)] for _ in range(self._num_cols)]
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._draw_cell(col, row)

    def _draw_cell(self, i, j):
        x_cell = self._x1 + i*self._cell_size_x
        y_cell = self._y1 + j*self._cell_size_y
        self._cells[i][j].draw(x_cell, y_cell, x_cell+self._cell_size_x, y_cell+self._cell_size_y)
        self._animate(0.0001)

    def _animate(self, sec=0.05):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(sec)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[-1][-1].has_bottom_wall=False
        self._draw_cell(0,0)
        self._draw_cell(self._num_cols-1,self._num_rows-1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            neighbors = []
            if i == 0:
                if j == 0:
                    neighbors = [(i+1, j), (i,j+1)]
                elif 0<j<self._num_rows-1:
                    neighbors = [(i,j+1), (i+1,j), (i,j-1)]
                else:
                    neighbors = [(i,j-1), (i+1, j)]
            elif i == self._num_cols-1:
                if j == 0:
                    neighbors = [(i,j+1), (i-1, j)]
                elif 0<j<self._num_rows-1:
                    neighbors = [(i,j+1), (i-1,j), (i,j-1)]
                else:
                    neighbors = [(i-1, j), (i, j-1)]
                    return
            else:
                if j == 0:
                    neighbors = [(i,j+1), (i+1, j), (i-1, j)]
                elif 0<j<self._num_rows-1:
                    neighbors = [(i,j+1), (i-1,j), (i,j-1), (i+1, j)]
                else:
                    neighbors = [(i-1,j), (i,j-1), (i+1,j)]
            neighbors = [neighbor for neighbor in neighbors if not self._cells[neighbor[0]][neighbor[1]].visited]
            if not neighbors:
                self._draw_cell(i,j)
                return
            rand_int = random.randrange(len(neighbors))
            new_i, new_j = neighbors.pop(rand_int)
            if new_i==i:
                if new_j<j:
                    self._cells[i][j].has_top_wall = False
                    self._cells[new_i][new_j].has_bottom_wall = False
                else:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[new_i][new_j].has_top_wall = False
            elif new_i>i:
                self._cells[i][j].has_right_wall=False
                self._cells[new_i][new_j].has_left_wall = False
            else:
                self._cells[i][j].has_left_wall=False
                self._cells[new_i][new_j].has_right_wall = False
            #self._draw_cell(i,j)
            #self._draw_cell(new_i, new_j)
            self._break_walls_r(new_i, new_j)


    def _reset_cells_visited(self):
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._cells[col][row].visited = False

    def solve(self, sec=0.1):
        self._reset_cells_visited()
        return self._solve_r(0,0, sec)

    def _solve_r(self, i, j, sec=0.1):
        self._animate(sec)
        self._cells[i][j].visited = True
        if i==self._num_cols-1 and j==self._num_rows-1:
            return True
        for (i_n, j_n) in [(i+1, j), (i-1,j), (i, j+1), (i,j-1)]:
            if (
                0<=i_n<self._num_cols
                and 0<=j_n<self._num_rows
                and not self._cells[i_n][j_n].visited
            ):
                # move right
                if i_n>i and not self._cells[i][j].has_right_wall and not self._cells[i_n][j_n].has_left_wall:
                    self._cells[i][j].draw_move(self._cells[i_n][j_n])
                    if self._solve_r(i_n,j_n):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[i_n][j_n], undo=True)
                # move left
                if i_n<i and not self._cells[i][j].has_left_wall and not self._cells[i_n][j_n].has_right_wall:
                    self._cells[i][j].draw_move(self._cells[i_n][j_n])
                    if self._solve_r(i_n,j_n):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[i_n][j_n], undo=True)
                # move down
                if j_n>j and not self._cells[i][j].has_bottom_wall and not self._cells[i_n][j_n].has_top_wall:
                    self._cells[i][j].draw_move(self._cells[i_n][j_n])
                    if self._solve_r(i_n,j_n):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[i_n][j_n], undo=True)
                # move up
                if j_n<j and not self._cells[i][j].has_top_wall and not self._cells[i_n][j_n].has_bottom_wall:
                    self._cells[i][j].draw_move(self._cells[i_n][j_n])
                    if self._solve_r(i_n,j_n):
                        return True
                    else:
                        self._cells[i][j].draw_move(self._cells[i_n][j_n], undo=True)
        return False


    ## Add BFS algo
    def solve_bfs(self, sec = 0.1, color = "green"):
        self._reset_cells_visited()
        queue = [(0,0)]
        while queue:
            i,j = queue.pop(0)
            if i == self._num_cols-1 and j == self._num_rows-1:
                return
            for (i_n, j_n) in [(i+1, j), (i-1,j), (i, j+1), (i,j-1)]:
                if (
                    0<=i_n<self._num_cols
                    and 0<=j_n<self._num_rows
                    and not self._cells[i_n][j_n].visited
                ):
                    # move right
                    if i_n>i and not self._cells[i][j].has_right_wall and not self._cells[i_n][j_n].has_left_wall:
                        self._animate(sec)
                        self._cells[i_n][j_n].visited = True
                        self._cells[i][j].draw_move(self._cells[i_n][j_n], color)
                        queue.append((i_n, j_n))
                    # move left
                    if i_n<i and not self._cells[i][j].has_left_wall and not self._cells[i_n][j_n].has_right_wall:
                        self._animate(sec)
                        self._cells[i_n][j_n].visited = True
                        self._cells[i][j].draw_move(self._cells[i_n][j_n], color)
                        queue.append((i_n, j_n))
                    # move down
                    if j_n>j and not self._cells[i][j].has_bottom_wall and not self._cells[i_n][j_n].has_top_wall:
                        self._animate(sec)
                        self._cells[i_n][j_n].visited = True
                        self._cells[i][j].draw_move(self._cells[i_n][j_n], color)
                        queue.append((i_n, j_n))
                    # move up
                    if j_n<j and not self._cells[i][j].has_top_wall and not self._cells[i_n][j_n].has_bottom_wall:
                        self._animate(sec)
                        self._cells[i_n][j_n].visited = True
                        self._cells[i][j].draw_move(self._cells[i_n][j_n], color)
                        queue.append((i_n, j_n))
