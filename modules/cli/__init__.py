import curses, os, psutil, socket, sys 
from datetime import datetime as dt

from views import backup, database, debug_curses, email, home, server 


class Cli():
  def __init__(self) -> None:
    self.inputStr = ''
    self.lastKey  = 0
    self.menu_num = 0
    self.small_screen = False
    # Init the screen
    self.stdscr = curses.initscr()
    # Configure curses to respond to keystrokes
    curses.noecho()
    curses.cbreak()
    self.stdscr.keypad(True)  

    self.initColors()
    self.initWindows()
    self.initNavList()
    self.mainLoop()

  def initColors(self):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    self.STATUS_COLORS = curses.color_pair(1)
    self.NAV_OPTION = curses.color_pair(2)
    self.NAV_SELECT = curses.color_pair(3)
    self.INPUT_COLORS = curses.color_pair(4)

  def initWindows(self):
    self.height, self.width = self.stdscr.getmaxyx()    
    self.small_screen = True if self.width < 90 else False

    self.status_bar_height = 2 if not self.small_screen else 3
    self.nav_bar_width     = 14
    self.input_bar_height  = 1

    self.statusBar = curses.newwin(self.status_bar_height, self.width,     0,0)
    self.navBar    = curses.newwin(self.height - self.status_bar_height, self.nav_bar_width,     self.status_bar_height,0)
    self.inputBar  = curses.newwin(self.input_bar_height, self.width - self.nav_bar_width + 1,     self.height - 1, self.nav_bar_width - 1)

  def initNavList(self):
    self.navList = [
      {
        'title': 'Home',
        'view': home.View
      },
      {
        'title': 'Server',
        'view': server.View
      },
      {
        'title': 'Email',
        'view': email.View
      },
      {
        'title': 'Database',
        'view': database.View
      },
      {
        'title': 'Backup',
        'view': backup.View
      },
      {
        'title': 'Curses debug',
        'view': debug_curses.View
      }
    ]

  def mainLoop(self):
    exit = False
    while exit == False:
      self.height, self.width = self.stdscr.getmaxyx()

      self.drawStatusBar()
      self.drawNavMenu()
      self.drawInputBar()
      
      view = self.navList[self.menu_num].get('view')
      h = self.height - self.status_bar_height - self.input_bar_height
      w = self.width - self.nav_bar_width + 1
      y = self.status_bar_height
      x = self.nav_bar_width - 1
      view(h,w,y,x, **self.__dict__)

      self.inputHandler()
    
    self.quit()

  def quit(self):
    curses.nocbreak()
    self.stdscr.keypad(False)
    curses.echo()
    curses.endwin()

  def drawStatusBar(self):
    height, width = self.statusBar.getmaxyx()

    # Calculations
    bytes_per_gb = 1024 ** 3
    # Memory
    memory = psutil.virtual_memory()
    mem_str  = f'Memory: { memory[2] }% of { "{:.2f}".format(memory[0] / bytes_per_gb) } GB'
    
    # CPU
    cpu_perc = psutil.cpu_percent()
    cpu_core = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()[0]
    cpu_str  = f'Cpu: { cpu_perc }% of { cpu_core } x { cpu_freq } MHz'
    
    # CPU load 
    cpu_load = [x / (psutil.cpu_count() * 100) for x in psutil.getloadavg()]
    load1 = "{:.1%}".format(cpu_load[0])
    load5 = "{:.1%}".format(cpu_load[1])
    load15 = "{:.1%}".format(cpu_load[2])
    if self.small_screen:
      load_str = f'Load: { load1 } { load5 } { load15 }'
    else:
      load_str = f'Load: { load1 } 1m { load5 } 5m { load15 } 15m'
    
    # Date time
    date_time_str = dt.strftime(dt.now(), '%B %d %Y %H:%M %S')
    
    # Disk
    df = os.statvfs('/')
    perc_free   = "{0:.1%}".format(df.f_bfree / df.f_blocks)
    total_space = "{:.2f}".format((df.f_frsize * df.f_blocks) / bytes_per_gb)
    df_str = f'Disk: { perc_free } of { total_space } GB'
  
    # Host
    host_str = f'Host: { socket.gethostname() }'
  
    top_spacing   = ' ' * ((width - len(mem_str + cpu_str + date_time_str) - 3) // 2)

    fix_top_align = ''
    if len(mem_str + top_spacing + cpu_str + top_spacing + date_time_str) + 2 < width -1:
      fix_top_align = ' '

    if self.small_screen:
      layout = [
        [host_str, date_time_str],
        [mem_str, cpu_str],
        [df_str, load_str]
      ]
    else:
      layout = [
        [mem_str, date_time_str, cpu_str],
        [df_str, host_str, load_str]
      ]

    for i, line in enumerate(layout):
      line_lens = [len(x) for x in line]
      spaces_left = width - sum(line_lens)

      if self.small_screen:
        spacing = ' ' * (spaces_left - 1)
        print_str = ''.join([line[0],spacing,line[1]]) 
        self.statusBar.addstr(i,0,print_str, self.STATUS_COLORS)
      else:
        spacing = ' ' * (spaces_left // 2 - 1)
        xtr_space = '  ' if spaces_left % 2 != 0 else ' '
        print_str = ''.join([line[0],spacing,line[1],spacing,xtr_space,line[2]]) 
        self.statusBar.addstr(i,0,print_str[:width-1], self.STATUS_COLORS)

    self.statusBar.refresh()

  def drawNavMenu(self):
    height, width = self.navBar.getmaxyx()
    self.navBar.clear()

    for i in range(0,height):
      menu_name = ''
      color = self.NAV_OPTION
      if i < len(self.navList):
        menu_name = self.navList[i].get('title')
        if i == self.menu_num:
          color = self.NAV_SELECT
      self.navBar.addstr(i,0,f"{menu_name}{' ' * (width - len(menu_name) - 1)}", color)

    self.navBar.refresh()

  def drawInputBar(self):
    height, width = self.inputBar.getmaxyx()
    prompt_str    = f'Input:'
    spacing       = ' ' * (width - (len(prompt_str) + len(self.inputStr)) - 3)

    self.inputBar.addstr(0,0,f' { prompt_str }{ self.inputStr }{ spacing } ', self.INPUT_COLORS)
    self.inputBar.refresh()

  def inputHandler(self):
    self.lastKey = self.stdscr.getch()

    # UP and DOWN handler 
    if self.lastKey == 258 and self.menu_num < len(self.navList) - 1:
      self.menu_num += 1
    elif self.lastKey == 259 and self.menu_num > 0:
      self.menu_num -= 1
    elif self.lastKey == curses.KEY_RESIZE:
      curses.resizeterm(*self.stdscr.getmaxyx())
      self.initWindows()
      self.stdscr.clear()
      self.stdscr.refresh()
    
    # Must be a character, write to screen
    elif self.lastKey >= 32 and self.lastKey <= 126:
      self.inputStr += chr(self.lastKey)
