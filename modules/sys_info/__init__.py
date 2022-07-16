import curses, os, psutil, socket, sys 
from datetime import datetime as dt

# Calculations
bytes_per_gb = 1024 ** 3

class Cpu():
  def __init__(self):
    # Available stats
    self.perc = 0
    self.freq_current = 0
    self.freq_min = 0
    self.freq_max = 0
    self.load_1m  = 0
    self.load_5m  = 0
    self.load_15m = 0
    self.logic_cores    = psutil.cpu_count()
    self.physical_cores = psutil.cpu_count(logical=False)
    # Load statistics
    self.refreshStats()

  def refreshStats(self):
    self.refreshPercent()
    self.refreshFrequency()
    self.refreshLoad()

  def refreshPercent(self):
    self.perc =  psutil.cpu_percent()
  
  def refreshFrequency(self):
    current_min_max   = psutil.cpu_freq()
    self.freq_current = current_min_max[0]
    self.freq_min     = current_min_max[1]
    self.freq_max     = current_min_max[2]
  
  def refreshLoad(self):
    cpu_load = [x / (self.logic_cores * 100) for x in psutil.getloadavg()]
    self.load_1m  = "{:.1%}".format(cpu_load[0])
    self.load_5m  = "{:.1%}".format(cpu_load[1])
    self.load_15m = "{:.1%}".format(cpu_load[2])


class Disk():
  ''' drives hold a list of all the mount points and their stats
      the total, used, free, perc are a total of the mount points'''
  def __init__(self) -> None:
    # Available stats
    self.drives = []
    self.total = 0
    self.used = 0
    self.free = 0
    self.perc = 0
    # Load statistics
    self.refresh()

  def refresh(self):
    self.refreshDrives()

  def refreshDrives(self):
    # Init all values
    self.drives = []
    self.total = 0
    self.used = 0
    self.free = 0
    self.perc = 0
    for part in psutil.disk_partitions(all=False):
      if os.name == 'nt':
        if 'cdrom' in part.opts or part.fstype == '':
          # skip cd-rom drives with no disk in it; they may raise
          # ENOENT, pop-up a Windows GUI error for a non-ready
          # partition or just hang.
          continue
      usage = psutil.disk_usage(part.mountpoint)
      drive = {
        'device': part.device,
        'total': usage.total / bytes_per_gb,
        'used': usage.used / bytes_per_gb,
        'free': usage.free / bytes_per_gb,
        'perc': usage.percent,
        'type': part.fstype,
        'part': part.mountpoint,
      }
      self.drives.append(drive)
    for drive in self.drives:
      self.total += drive.get('total')
      self.used += drive.get('used')
      self.free += drive.get('free')
    self.perc = ((self.total - self.free) / self.total) * 100


class Memory():
  ''' Data stored in GB '''
  def __init__(self) -> None:
    # Available stats
    self.total     = 0
    self.available = 0
    self.perc      = 0
    self.buffers   = 0
    self.cached    = 0
    self.swap_total = 0
    self.swap_used  = 0
    self.swap_free  = 0
    self.swap_perc  = 0
    # Load statistics
    self.refresh()

  def refresh(self):
    self.refreshMemory()
    self.refreshSwap()

  def refreshMemory(self):
    mem = psutil.virtual_memory()
    self.total     = mem.total / bytes_per_gb
    self.available = mem.available / bytes_per_gb
    self.perc      = mem.percent
    self.buffers   = mem.buffers / bytes_per_gb
    self.cached    = mem.cached / bytes_per_gb

  def refreshSwap(self):
    swap = psutil.swap_memory()
    self.swap_total = swap.total / bytes_per_gb
    self.swap_used  = swap.used / bytes_per_gb
    self.swap_free  = swap.free / bytes_per_gb
    self.swap_perc  = swap.percent