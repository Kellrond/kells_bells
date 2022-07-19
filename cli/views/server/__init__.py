import curses
from modules import sys_info

from cli.views.server.widgets import CpuWidget

class View():
  def __init__(self, **kwargs):
    from cli import UI
    self.ui = kwargs.get('ui', UI)
    self.ui.createInputWindow(self.ui.view_w)
    self.screen = curses.newwin(self.ui.view_h, self.ui.view_w, self.ui.view_y, self.ui.view_x)
    self.system = kwargs.get('system', sys_info.System())
    self.viewing = True
    self.loop()

  def loop(self):
    while self.viewing:
      self.out()
      curses.doupdate()
      self.ui.getInput()
      # If last key was tab exit to menu
      if self.ui.last_key == 9 or self.ui.last_key == 353:
        self.viewing = False
        self.ui.exit_code = 'menu'    

  def out(self):
    height, width = self.screen.getmaxyx()
    # Prep everything
    self.system.refreshAll()
    self.setSystemStrings()
    self.genLineList()

    # Draw lines
    self.ui.view_line_count = len(self.lineList)
    self.screen.erase()
    i = 0
    while i < height - 1 and i < self.ui.view_line_count:
      self.screen.addstr(i, 1, self.lineList[self.ui.scroll_y + i][:width-2])
      i += 1

    self.screen.noutrefresh()

  def setSystemStrings(self):
    # CPU
    self.cpuStr   = f'{ self.system.cpu.perc }% of { self.system.cpu.logic_cores } logic core(s) at { self.system.cpu.freq_current } MHz'
    self.loadStr  = f'{ self.system.cpu.load_1m} 1 min - { self.system.cpu.load_5m } 5 min - { self.system.cpu.load_15m } 15 min'
    # Memory
    self.memStr   = f'{ self.system.memory.perc }% of { self.system.memory.total } GB - { self.system.memory.available } GB available'
    self.bufStr   = f'{ self.system.memory.buffers } buffers - { self.system.memory.cached } GB cached'
    self.swapStr  = f'{ self.system.memory.swap_perc }% of { self.system.memory.swap_total } GB '
    # Disks
    self.diskStr  = f'{ self.system.disk.perc }% used of { self.system.disk.total } GB - { self.system.disk.free } GB free'
    self.allDisks = [f'{ d.get("part") }: { d.get("perc") }% used of { d.get("total") } GB' for d in self.system.disk.drives]
  
  def genLineList(self):
    self.lineList = [
      f"Host: { self.system.host }",
      f"Time: { self.system.date_time}" ,
      " ",
      '  == CPU ==',
      f'CPU:  { self.cpuStr  }',
      f'Load: { self.loadStr  }',
      " ",
      '  == Memory ==',
      f'Mem:  { self.memStr  }',
      f'Swap: { self.swapStr  }',
      f'Buff: { self.bufStr  }',
      " ",
      '  == Disks ==',
      f'Total: { self.diskStr  }',
      " ",
      '  -- Partitions -- ',
    ]
    for disk in self.allDisks:
      self.lineList.append(disk)
      