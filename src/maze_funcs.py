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
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.005)

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

    # Alternative Recursion
    def _break_walls_ra(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # if there is nowhere to go from here
            # just break out
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_ra(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._cells[col][row].visited = False
