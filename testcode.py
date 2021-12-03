import curses
from curses import wrapper
from curses.textpad import rectangle
import time

char_name = "Tazdarwin"
char_health = 9
char_max_health = 90
char_mana = 16
char_max_mana = 40
skill_1 = ""
skill_2 = ""
skill_3 = ""
skill_4 = ""
skill_5 = ""
skill_6 = ""
char_weap = "Longsword"
char_armour = "Chainmail"

#     max and min coordinates (y, x) 0, 0, 23, 79 but 23,79 will cause an error!
def main(stdscr):
    """ this function loads the main game screen curses overlay."""

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_GREEN)
    GREEN_RED = curses.color_pair(1)
    RED_GREEN = curses.color_pair(2)

    character_stats = curses.newwin(21, 20, 0, 0)
    
    stdscr.clear()
    stdscr.addstr(1, 60, "this is a test")
    rectangle(stdscr, 0, 0, 22, 79)

    character_stats.clear()
    health_gap_len = 8 - (len(str(char_health)) + len(str(char_max_health)))
    health_gap = " " * health_gap_len
    weap_gap_len = 11 - (len(str(char_weap)))
    weap_gap = " " * weap_gap_len

    character_stats.addstr(f"{char_name}\n"
                           "\n"
                           "HEALTH   MANA\n" 
                           f"{char_health}/{char_max_health}{health_gap}{char_mana}/{char_max_mana}\n"
                           "\n"
                           "SKILLS\n"
                           f"1. {skill_1}\n"
                           f"2. {skill_2}\n"
                           f"3. {skill_3}\n"
                           f"4. {skill_4}\n"
                           f"5. {skill_5}\n"
                           f"6. {skill_6}\n"
                           "\n"
                           "WEAPON     ARMOUR\n"
                           f"{char_weap}{weap_gap}{char_armour}" )



    stdscr.refresh()
    character_stats.refresh()
    stdscr.getch()


wrapper(main)
