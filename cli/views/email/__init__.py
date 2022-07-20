import curses

from db.mailserver import Mailserver
from cli.views.email.widgets import Home, Domains, Aliases, Users

class View:
  def __init__(self, **kwargs):
    from cli import UI
    self.ui = kwargs.get('ui', UI)
    self.ui.createInputWindow(self.ui.view_w)

    self.menu_w = 10  
    self.menu = curses.newwin(self.ui.view_h, self.menu_w, self.ui.view_y, self.ui.view_x)
    self.menu_list = [
      {'title': 'Home', 'widget': Home},
      {'title': 'Users', 'widget': Users},
      {'title': 'Aliases', 'widget': Aliases},
      {'title': 'Domains', 'widget': Domains}
    ]
    self.menu_cur = 'Home'

    self.screen = curses.newwin(self.ui.view_h, self.ui.view_w - self.menu_w, self.ui.view_y, self.ui.view_x + self.menu_w - 1)
    self.mailserver = Mailserver()
    self.viewing = True

  def loop(self):
    self.ui.stdscr.nodelay(False)
    while self.viewing == True:
      self.drawMenu()
      self.out()

      self.ui.drawInputBar()
      curses.doupdate()
      self.ui.getInput()

      # It tab escape program
      if self.ui.last_key == 9 or self.ui.last_key == 353:
        self.ui.destroyInputWindow()
        self.viewing = False
        self.ui.exit_code = 'menu'

      if self.ui.last_key == 10:
        input_len = len(self.ui.input_str)
        for menu in self.menu_list:
          title = menu.get('title')
          if input_len > 0 and self.ui.input_str.lower().strip() == title[:input_len].lower():
            self.menu_cur = title
            self.ui.resetInput()

  def out(self):
    height, width = self.screen.getmaxyx()

    # Draw lines
    widget_class = self.getCurrentWidget()
    widget = widget_class(self.ui, *self.screen.getmaxyx())
    self.line_list = widget.draw()

    self.ui.view_line_count = len(self.line_list)
    self.screen.erase()
    i = 0
    while i < height - 1 and i < self.ui.view_line_count:
      self.screen.addstr(i, 0, self.line_list[self.ui.scroll_y + i][:width-2])
      i += 1

    self.screen.noutrefresh()

  def getCurrentWidget(self):
    for menu in self.menu_list:
      if menu.get('title') == self.menu_cur:
        return menu.get('widget')

  def drawMenu(self):
    height, width = self.menu.getmaxyx()
    menu_len = len(self.menu_list)

    for i in range(height):
      if i < menu_len:
        title = self.menu_list[i].get('title')
        spacing = " " * (width - len(title) - 1)

        input_len = len(self.ui.input_str)
        if input_len > 0 and self.ui.input_str.lower().strip() == title[:input_len].lower():
          color = self.ui.colors.NAV_BAR
        else:
          color = self.ui.colors.NAV_SELECT 

        self.menu.addstr(i, 0, title + spacing, color)
      else:
        self.menu.addstr(i, 0, " " * (width - 1), self.ui.colors.NAV_SELECT)

    self.menu.noutrefresh()
