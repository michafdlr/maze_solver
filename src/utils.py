from tkinter import Tk, BOTH, Canvas, Button

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
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_top_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if not self._win:
            return
        if self.has_left_wall:
            line = Line(Point(self._x1,self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, fill_color="black")
        else:
            line = Line(Point(self._x1,self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, fill_color="white")
        if self.has_right_wall:
            line = Line(Point(self._x2,self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, fill_color="black")
        else:
            line = Line(Point(self._x2,self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, fill_color="white")
        if self.has_bottom_wall:
            line = Line(Point(self._x1,self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, fill_color="black")
        else:
            line = Line(Point(self._x1,self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, fill_color="white")
        if self.has_top_wall:
            line = Line(Point(self._x1,self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, fill_color="black")
        else:
            line = Line(Point(self._x1,self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, fill_color="white")

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        x_mid = (self._x1 + self._x2) / 2
        y_mid = (self._y1 + self._y2) / 2

        to_x_mid = (to_cell._x1 + to_cell._x2) / 2
        to_y_mid = (to_cell._y1 + to_cell._y2) / 2

        fill_color = "red"
        if undo:
            fill_color = "gray"

        # moving left
        if self._x1 > to_cell._x1:
            line = Line(Point(self._x1, y_mid), Point(x_mid, y_mid))
            self._win.draw_line(line, fill_color)
            line = Line(Point(to_x_mid, to_y_mid), Point(to_cell._x2, to_y_mid))
            self._win.draw_line(line, fill_color)

        # moving right
        elif self._x1 < to_cell._x1:
            line = Line(Point(x_mid, y_mid), Point(self._x2, y_mid))
            self._win.draw_line(line, fill_color)
            line = Line(Point(to_cell._x1, to_y_mid), Point(to_x_mid, to_y_mid))
            self._win.draw_line(line, fill_color)

        # moving up
        elif self._y1 > to_cell._y1:
            line = Line(Point(x_mid, y_mid), Point(x_mid, self._y1))
            self._win.draw_line(line, fill_color)
            line = Line(Point(to_x_mid, to_cell._y2), Point(to_x_mid, to_y_mid))
            self._win.draw_line(line, fill_color)

        # moving down
        elif self._y1 < to_cell._y1:
            line = Line(Point(x_mid, y_mid), Point(x_mid, self._y2))
            self._win.draw_line(line, fill_color)
            line = Line(Point(to_x_mid, to_y_mid), Point(to_x_mid, to_cell._y1))
            self._win.draw_line(line, fill_color)
