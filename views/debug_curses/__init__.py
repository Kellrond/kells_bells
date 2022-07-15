import curses

class View():
  def __init__(self, h, w, y, x, **kwargs):
    self.screen = curses.newwin(h, w, y, x)
    for k,v in kwargs.items():
      setattr(self, k, v)
    self.out()

  def out(self):
    height, width = self.screen.getmaxyx()
    self.screen.erase()
    self.screen.addstr(0, 0, "TL")
    self.screen.addstr(height - 1, 0, "BL")
    self.screen.addstr(0, width - 2, "R")
    self.screen.addstr(height - 1, width - 2, "R")
    self.screen.addstr(1,2, f"Screen size Lines: { height } Cols: { width }")
    self.screen.addstr(2,2, f'Last key: {self.lastKey}')
    self.screen.addstr(3,2, f'Menu num: {self.menu_num}')
    self.screen.addstr(4,2, f'Curs y x: {self.cur_y} {self.cur_x}')
    self.screen.refresh()