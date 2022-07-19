import curses

todo = [
  'create system view',
  'create database view',
  'create email view',
  'create backup view',
  ]

class View():
  def __init__(self, **kwargs):
    from cli import UI
    self.ui = kwargs.get('ui', UI)
    self.screen = curses.newwin(self.ui.view_h, self.ui.view_w, self.ui.view_y, self.ui.view_x)
  
  def loop(self):
    self.out()
    curses.doupdate()
    self.ui.getInput()

  def out(self):
    height, width = self.screen.getmaxyx()
    self.screen.clear()
    self.screen.addstr(1,2, f"Server admin homepage")
    self.screen.addstr(2,2, f'')
    self.screen.addstr(3,2, f'== TODO ==')
    cur_y = 4
    for item in todo:
      self.screen.addstr(cur_y,2, f' - { item }')
      cur_y += 1
    self.screen.noutrefresh()
    curses.doupdate()