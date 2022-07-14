from curses import wrapper
from modules import cli

def main(stdscr):
    app = cli.Cli()

wrapper(main)


