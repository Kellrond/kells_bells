import curses

from db.mailserver import Mailserver

class View:
  def __init__(self, **kwargs):
    from cli import UI
    self.ui = kwargs.get('ui', UI)
    self.screen = curses.newwin(self.ui.view_h, self.ui.view_w, self.ui.view_y, self.ui.view_x)
    self.databases = [Mailserver]

  def loop(self):
    self.ui.stdscr.nodelay(False)
    self.genLineList()
    self.out()
    curses.doupdate()
    self.ui.getInput()

  def out(self):
    height, width = self.screen.getmaxyx()

    # Draw lines
    self.ui.view_line_count = len(self.line_list)
    self.screen.erase()
    i = 0
    while i < height - 1 and i < self.ui.view_line_count:
      self.screen.addstr(i, 1, self.line_list[self.ui.scroll_y + i][:width-2])
      i += 1

    self.screen.noutrefresh()

  def genLineList(self):
    

    self.line_list = [
      'Database admin',
      '',
    ]

    for db_class in self.databases:
      db = db_class()
      connect_str = 'Connect okay' if db.test_connection() else 'Connect failed'
      self.line_list.append(f"{ db.__name__ } - { connect_str }")