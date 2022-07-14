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
    self.screen.addstr(1,2, f"Backup homepage")
    self.screen.addstr(2,2, f'')
    self.screen.addstr(3,2, f'Get something new in here')
    self.screen.refresh()