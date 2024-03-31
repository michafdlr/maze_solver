from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed by user!")
    def close(self):
        self.__running = False
    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1=Point(), p2=Point()):
        self.p1 = p1
        self.p2 = p2
    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y,
            fill=fill_color,
            width=2
        )
        canvas.pack(fill=BOTH, expand=1)

class Cell:
    def __init__(self, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_top_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if self.has_left_wall:
            line = Line(Point(self._x1,self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, fill_color="black")
        if self.has_right_wall:
            line = Line(Point(self._x2,self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, fill_color="black")
        if self.has_bottom_wall:
            line = Line(Point(self._x1,self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, fill_color="black")
        if self.has_top_wall:
            line = Line(Point(self._x1,self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, fill_color="black")

    def draw_move(self, to_cell, undo=False):
        mid_x_from = (self._x1 + self._x2)/2
        mid_y_from = (self._y1 + self._y2)/2
        mid_x_to = (to_cell._x1 + to_cell._x2)/2
        mid_y_to = (to_cell._y1 + to_cell._y2)/2
        fill_color = "red"
        if undo:
            fill_color = "gray"
        # move right
        if self._x1 < to_cell._x1:
            line = Line(Point(mid_x_from, mid_y_from), Point(self._x2, mid_y_from))
            self._win.draw_line(line, fill_color=fill_color)
            line = Line(Point(to_cell._x1, mid_y_to), Point(mid_x_to, mid_y_to))
            self._win.draw_line(line, fill_color=fill_color)
        # move left
        elif self._x1 > to_cell._x1:
            line = Line(Point(self._x1, mid_y_from), Point(mid_x_from, mid_y_from))
            self._win.draw_line(line, fill_color=fill_color)
            line = Line(Point(mid_x_to, mid_y_to), Point(self._x2, mid_y_to))
            self._win.draw_line(line, fill_color=fill_color)
        #moving up
        elif self._y1 > to_cell._y1:
            line = Line(Point(mid_x_from, mid_y_from), Point(mid_x_from, self._y1))
            self._win.draw_line(line, fill_color)
            line = Line(Point(mid_x_to, to_cell._y2), Point(mid_x_to, mid_y_to))
            self._win.draw_line(line, fill_color)

        # moving down
        elif self._y1 < to_cell._y1:
            line = Line(Point(mid_x_from, mid_y_from), Point(mid_x_from, self._y2))
            self._win.draw_line(line, fill_color)
            line = Line(Point(mid_x_to, mid_y_to), Point(mid_x_to, to_cell._y1))
            self._win.draw_line(line, fill_color)
