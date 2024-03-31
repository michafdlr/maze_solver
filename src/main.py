from utils import Window, Line, Point, Cell

def main():
    win = Window(800, 600)
    # line1 = Line(Point(50,50), Point(150, 200))
    # line2 = Line(Point(0,0), Point(800, 500))
    # win.draw_line(line1, "black")
    # win.draw_line(line2, "red")
    cell1 = Cell(win)
    cell1.has_right_wall=False
    cell1.draw(50,100,100,150)
    cell2 = Cell(win)
    cell2.has_top_wall=False
    cell2.has_left_wall=False
    cell2.draw(100,100,150,150)
    cell3 = Cell(win)
    cell3.has_bottom_wall=False
    cell3.draw(100,50,150,100)
    cell1.draw_move(cell2)
    cell3.draw_move(cell2)
    win.wait_for_close()
main()
