from utils import Window, Line, Point, Cell

def main():
    win = Window(800, 600)
    # line1 = Line(Point(50,50), Point(150, 200))
    # line2 = Line(Point(0,0), Point(800, 500))
    # win.draw_line(line1, "black")
    # win.draw_line(line2, "red")
    cell = Cell(win)
    cell.has_bottom_wall = False
    cell.has_right_wall = False
    cell.draw(50,100,100,50)
    win.wait_for_close()
main()
