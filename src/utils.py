from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze solver")
        self.canvas = Canvas()
        self.canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
    def close(self):
        self.running = False
    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

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
        canvas.pack()

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
