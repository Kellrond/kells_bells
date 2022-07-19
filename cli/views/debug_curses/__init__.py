import curses


class View():
  def __init__(self, **kwargs):
    from cli import UI
    self.ui = kwargs.get('ui', UI)
    self.ui.createInputWindow(self.ui.view_w)
    self.screen = curses.newwin(self.ui.view_h, self.ui.view_w, self.ui.view_y, self.ui.view_x)
    self.viewing = True
    self.loop()

  def loop(self):
    while self.viewing == True:
      self.out()
      self.ui.drawInputBar()
      curses.doupdate()
      self.ui.getInput()

      # It tab escape program
      if self.ui.last_key == 9 or self.ui.last_key == 353:
        self.ui.destroyInputWindow()
        self.viewing = False
        self.ui.exit_code = 'menu'

  def out(self):
    height, width = self.screen.getmaxyx()
    self.screen.erase()
    self.screen.addstr(0, 0, "TL")
    self.screen.addstr(height - 1, 0, "BL")
    self.screen.addstr(0, width - 2, "R")
    self.screen.addstr(height - 1, width - 2, "R")
    self.screen.addstr(1,2, f"Screen size Lines: { height } Cols: { width }")
    self.screen.addstr(2,2, f'Last key: {self.ui.last_key}')
    self.screen.addstr(3,2, f'Menu num: {self.ui.menu_opt}')
    self.screen.addstr(4,2, f'Curs y x: {self.ui.cursor_y} {self.ui.cursor_x}')
    self.screen.addstr(5,2, f'Scroll y x: { self.ui.scroll_y } { self.ui.scroll_x }')
    self.screen.noutrefresh()