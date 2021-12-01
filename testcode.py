import curses
from curses import wrapper
from curses.textpad import rectangle
import time

char_name = "Tazdarwin"
char_health = 90
char_max_health = 90

def main(stdscr):



    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_GREEN)
    GREEN_RED = curses.color_pair(1)
    RED_GREEN = curses.color_pair(2)

    character_stats = curses.newwin(1, 20, 1, 1)
    
    stdscr.clear()
    stdscr.addstr(1, 40, "this is a test")
    rectangle(stdscr, 0, 0, 28, 79)

    character_stats.clear()
    character_stats.addstr(f"{char_name}")



    stdscr.refresh()
    character_stats.refresh()
    stdscr.getch()


wrapper(main)
