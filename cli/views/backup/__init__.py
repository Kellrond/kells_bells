import curses

class View():
  def __init__(self, **kwargs):
    from cli import UI
    self.ui = kwargs.get('ui', UI)
    self.screen = curses.newwin(self.ui.view_h, self.ui.view_w, self.ui.view_y, self.ui.view_x)
    
  def loop(self):
    self.out()
    self.ui.getInput()

  def out(self):
    height, width = self.screen.getmaxyx()
    self.screen.erase()
    self.screen.addstr(1,2, f"Backup homepage")
    self.screen.addstr(2,2, f'')
    self.screen.addstr(3,2, f'Get something new in here')
    self.screen.noutrefresh()
    curses.doupdate()