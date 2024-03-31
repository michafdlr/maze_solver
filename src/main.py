from utils import Window, Line, Point

def main():
    win = Window(800, 600)
    line1 = Line(Point(50,50), Point(150, 200))
    line2 = Line(Point(0,0), Point(800, 500))
    win.draw_line(line1, "black")
    win.draw_line(line2, "red")
    win.wait_for_close()
main()
