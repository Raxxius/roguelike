import random
import curses
from curses import wrapper
from curses.textpad import Textbox
import gspread
import time
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('roguelike')

# Classes

"""
class Dungeon(self, rooms, width, height):
    def __init__(self, rooms, width, height):
        self.rooms = rooms
        self.width = width
        self.height = height

# Dungeon subclasses


class Room(self, xcoord, ycoord, width, height, type):
    def __init__(self, xcoord, ycoord, width, height, type):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.width = width
        self.height = height

# class Character(self, health, max_health, mana, max_mana, xp, level):
#     def __init__(self, health, max_health, mana, max_mana, xp, level)

# class Monster(self, type, health, attack, defence):
    def __init__(self, health, attack, defence):
        self.type
        self.health = 
"""

# Main flow functions


def player_select(stdscr):
    """
    This function reads the google sheet for characters
    with the status = "alive", and allows the players
    to select an alive character or choose a new one
    """

    players = SHEET.worksheet("players")
    player_data = players.get_all_values()
    alive_characters = []
    dead_characters = []

    # Sets up the title screen

    for player_number in player_data:
        if player_number[1] == "alive":
            alive_characters.append(player_number[0])
        elif player_number[1] == "dead":
            dead_characters.append(player_number[0])
    character = opening_screen(stdscr, alive_characters, dead_characters)
    return character


def dungeon_size(stdscr, character):
    """
    This function decides the size of the map and runs all
    the individual dungeon generation functions
    if a map already exists for the character it will load that instead
    """

    # Fetch data from google sheets

    existing_map = str(SHEET.worksheets())
    character_map = f"'{character[0]}_map'"
    stdscr.clear()

    if character_map in existing_map:
        stdscr.addstr(2, 10, f"{character[0]} is already in a dungeon. Loading"
                      " the dungeon.")
    else:
        stdscr.addstr(2, 10, "defining dungeon size...")
        stdscr.addstr(4, 10, "how large would you like the dungeon to be? S, "
                      "M or L?")
        stdscr.refresh()
        input_size = Textbox(curses.newwin(1, 2, 5, 10))
        stdscr.refresh()
        size = input_size.edit().lower().strip()
        if size == "s":
            stdscr.addstr(7, 10, "Creating a small dungeon")
            x_size = 40
            y_size = 20
            stdscr.getch()
        elif size == "m":
            stdscr.addstr(7, 10, "Creating a medium dungeon")
            x_size = 50
            y_size = 50
        elif size == "l":
            stdscr.addstr(7, 10, "Creating a large dungeon")
            x_size = 100
            y_size = 100
        else:
            stdscr.addstr(7, 10, f"{size} is not a valid size you muppet")
            stdscr.addstr(9, 10, "please input a valid size")
            stdscr.addstr(11, 10, "press a key to continue")
            stdscr.getch()
            dungeon_size(stdscr, character)

        # create a blank dungeon map
        stdscr.clear()
        stdscr.addstr(5, 10, "Generating map")
        dungeon_map = init_dungeon(x_size, y_size)

        # add rooms to the dungeon map
        # total number of rooms are based on the size of the dungeon

        room_number = init_rooms(random.randint(round((x_size * y_size / 100)),
                                 round((x_size * y_size / ((2/3) * 100)))))

        position_rooms(stdscr, room_number, dungeon_map, x_size, y_size)

        # add player to room start
        dungeon_map = add_player(dungeon_map)
        # add boss to final room
        add_boss(dungeon_map)
        # add monsters to rooms
        # add_monster(dungeon_map, room_number)

        """
        # add loot to random rooms
        add_loot(room_number, dungeon_map, x_size, y_size)

        """

        # Upload new map to google sheets
        SHEET.add_worksheet(title=f"{character[0]}_map", rows=y_size,
                            cols=x_size)
        dungeon_list = list(dungeon_map.values())
        dungeon_passover = [dungeon_list[x:x+x_size]
                            for x in range(0, len(dungeon_list), x_size)]
        SHEET.worksheet(title=f"{character[0]}_map").update('A1', dungeon_passover)

        stdscr.addstr(7, 10, "Map Generated!")
        stdscr.addstr(9, 10, "Press a key to continue")
        stdscr.getch()


def gamescreen(stdscr, character):
    """ this function loads the main game screen curses overlay."""

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_GREEN)
    # GREEN_RED = curses.color_pair(1)
    # RED_GREEN = curses.color_pair(2)

    character_stats = curses.newwin(21, 20, 0, 0)

    stdscr.clear()
    # how to use the last character in the window
    # try:
    #    rectangle(stdscr, 0, 0, 23, 79)
    # except curses.error:
    #    pass

    # adds the character stats to the characters stats window
    character_stats.clear()
    health_gap_len = 8 - (len(str(character[4])) + len(str(character[14])))
    health_gap = " " * health_gap_len
    weap_gap_len = 11 - (len(str(character[12])))
    weap_gap = " " * weap_gap_len

    character_stats.addstr(f"{character[0]}\n"
                           "\n"
                           "HEALTH   MANA\n"
                           f"{character[4]}/{character[14]}{health_gap}"
                           f"{character[5]}/{character[15]}\n"
                           "\n"
                           "SKILLS\n"
                           f"1. {character[6]}\n"
                           f"2. {character[7]}\n"
                           f"3. {character[8]}\n"
                           f"4. {character[9]}\n"
                           f"5. {character[10]}\n"
                           f"6. {character[11]}\n"
                           "\n"
                           "WEAPON     ARMOUR\n"
                           f"{character[12]}{weap_gap}{character[13]}")

    padmap = map_conversion(character)
    # sets up the map pad - note needs to be updated to scale with the dungeon size
    gamemap = curses.newpad(20, 40)
    stdscr.refresh()
    # test code
    for i in range(len(padmap)):
        try:
            gamemap.addstr(padmap[i])
        except curses.error:
            pass
    try:
        gamemap.refresh(0, 0, 0, 26, 23, 79)
    except curses.error:
        pass

    stdscr.refresh()
    character_stats.refresh()
    stdscr.getch()

# Game generation functions


def opening_screen(stdscr, alive_characters, dead_characters):
    """
    Checks to see if a character already exists in the database
    if the players selects a name that already exists but is dead, the user
    will be asked to pick another character.
    """

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # WHITE_BLACK = curses.color_pair(1)

    stdscr.addstr(2, 10, "Welcome to the roguelike dungeon")
    stdscr.addstr(3, 10, "The following characters are alive:")
    stdscr.addstr(5, 10, f"{alive_characters}")
    stdscr.addstr(7, 10, "you can select one of these characters or create a")
    stdscr.addstr(8, 10, "new one by typing a name")
    stdscr.addstr(10, 10, "Type the name of your character")

    stdscr.refresh()

    character_scr = Textbox(curses.newwin(1, 23, 12, 10))

    select_character = character_scr.edit().strip().capitalize()

    if select_character in alive_characters:
        character_info = player_select_existing(select_character)
        stdscr.addstr(13, 10, f"{select_character} returns to fight!")
        stdscr.addstr(14, 10, "Press a key to continue")
        stdscr.getch()

    elif select_character in dead_characters:
        stdscr.addstr(13, 10, f"Sorry, {select_character} is dead! please select another name.")
        stdscr.addstr(14, 10, "Press a key to continue")
        stdscr.getch()
        stdscr.clear()
        opening_screen(stdscr, alive_characters, dead_characters)

    else:
        character_info = player_select_new(select_character)
        stdscr.addstr(13, 10, f"{select_character} enters the dungeon!")
        stdscr.addstr(14, 10, "Press a key to continue")
        stdscr.getch()

    return character_info


def player_select_existing(character):
    """
    This function selects a character from the googlesheet and loads
    their stats
    """
    for player_x in SHEET.worksheet("players").get_all_values():
        if player_x[0] == character:
            character_info = player_x
    return character_info


def player_select_new(character):
    """
    This function selects a new chracter and adds them to the googlesheet
    """
    character_info = [character, "alive", 1, 0, 16, 10, "", "", "", "", "", "",
                      "Shortsword", "Chainmail", 16, 10]
    SHEET.worksheet("players").append_row(character_info)
    return character_info


def init_dungeon(d_width, d_height):
    """
    This function sets every square in the dungeon to wall
    dungeon size generated by the dungeon size function.

    Function creates a paired dictonary with an x,y coordinate: and True
    This will create a rectangle with all squares set to wall(True).
    """
    dungeon_map = {}
    for ycoord in range(d_height):
        for xcoord in range(d_width):
            # creates a dungeon tile with an x,y coord and sets True.
            dungeon_map[xcoord, ycoord] = "wall"
    return dungeon_map


def init_rooms(room_number):
    """
    This function creates a dictonary of rooms with the room number,
    length and height.
    The number of rooms added is dependant upon the dungeon_size() function.
    Rooms have a random size betweem 4 and 6 tiles.
    Dungeon_width is called to allow for change of room size based
    on dungeon size.
    """

    rooms = {}
    for room in range(room_number):
        room_height = random.randint(4, 6)
        room_width = random.randint(4, 6)
        rooms[room] = f"room {room}", room_height, room_width
    return rooms


def position_rooms(stdscr, rooms, dungeon_map, dungeon_width, dungeon_height):
    """
    This function puts the rooms generated in the init_rooms function
    into the dungeon, rooms are added by changing the "wall" value in the
    dungeon_map dict to "room {number}".

    Rooms are added in a semi-randomised way - room 1 is the spawn room,
    and will be added near to the upper left of the map (0,0).

    the last room (containing the boss) is added to be near the lower
    right of the map.

    Rooms are populated in quarters.
    """

    # last room is len - 1 due to dic starting at 0
    total_rooms = len(rooms) - 1
    q1 = round(total_rooms / 4)
    q2 = q1 + round(total_rooms / 4)
    q3 = q2 + round(total_rooms / 4)

    # Add starting room
    xcoord = 1
    ycoord = 1
    for xvar in range(rooms[0][1]):
        xnew = xcoord + xvar
        for yvar in range(rooms[0][2]):
            ynew = ycoord + yvar
            dungeon_map[xnew, ynew] = "room start"

    # Add boss room
    xcoord, ycoord = room_pos_check(dungeon_width - 4, dungeon_width - 1, dungeon_height - 4,
                                    dungeon_height - 1, dungeon_width, dungeon_height, 
                                    total_rooms, rooms, dungeon_map,)
    for xvar in range(rooms[total_rooms][1]):
        xnew = xcoord + xvar
        for yvar in range(rooms[total_rooms][2]):
            ynew = ycoord + yvar
            dungeon_map[xnew, ynew] = "room end"

    # Add other rooms
    for room in rooms:
        if room == 0:
            continue
        elif room == total_rooms + 1:
            continue
        elif room <= q1:
            xcoord, ycoord = room_pos_check(1, round(dungeon_width / 2), 1, round(dungeon_height / 2),
                                            dungeon_width, dungeon_height, room, rooms, dungeon_map)

        elif room <= q2:
            xcoord, ycoord = room_pos_check(round(dungeon_width / 2), dungeon_width, 1, round(dungeon_height / 2),
                                            dungeon_width, dungeon_height, room, rooms, dungeon_map)

        elif room <= q3:
            xcoord, ycoord = room_pos_check(1, round(dungeon_width / 2), round(dungeon_height / 2), dungeon_height,
                                            dungeon_width, dungeon_height, room, rooms, dungeon_map)

        elif room <= total_rooms:
            xcoord, ycoord = room_pos_check(round(dungeon_width / 2), dungeon_width, round(dungeon_height / 2), dungeon_height,
                                            dungeon_width, dungeon_height, room, rooms, dungeon_map)
            # xcoord, ycoord = room_overlap_check(xcoord, ycoord, dungeon_map)
        else:
            print("Error in map generation")
        for xvar in range(rooms[room][1]):
            xnew = xcoord + xvar
            for yvar in range(rooms[room][2]):
                ynew = ycoord + yvar
                dungeon_map[xnew, ynew] = f"room {room}"


    return dungeon_map


def room_pos_check(x_start, x_end, y_start, y_end, dungeon_width, dungeon_height, room, rooms, dungeon_map):
    """
    Makes sure that the rooms do not go outside the boundries of the map
    and that the edges of the map are always walls.
    """

    # generates random coords within limits based on the q value
    xcoord = random.randint(x_start, x_end)
    ycoord = random.randint(y_start, y_end)

    # checks that rooms don't go out of bounds pushes them up and to the left
    if xcoord + rooms[room][1] >= dungeon_width:
        xcoord = dungeon_width - rooms[room][1] - 1
    if ycoord + rooms[room][2] >= dungeon_height:
        ycoord = dungeon_height - rooms[room][2] - 1

    for i in range(rooms[room][1]):
        for e in range(rooms[room][2]):
            if "room" in dungeon_map[(xcoord + i), (ycoord + e)]:
                xcoord, ycoord = room_pos_check(x_start, x_end, y_start, y_end, dungeon_width, dungeon_height, room, rooms, dungeon_map)
            else:
                continue

    return xcoord, ycoord

def add_player(dungeon_map):
    """
    add player to the map
    """
    room_start = []

    for value in dungeon_map:
        if dungeon_map[value] != "room start":
           continue
        else:
            room_start.append([value, dungeon_map[value]]) 

    start_point = int(len(room_start) / 2)
    start_key = room_start[start_point]
    dungeon_map[start_key[0]] = "room start character"

    return dungeon_map


def add_boss(dungeon_map):
    """
    add boss to the map
    """
    room_start = []

    for value in dungeon_map:
        if dungeon_map[value] != "room end":
           continue
        else:
            room_start.append([value, dungeon_map[value]]) 

    start_point = int(len(room_start) / 2)
    start_key = room_start[start_point]
    dungeon_map[start_key[0]] = "room end boss"

    return dungeon_map


def add_monster(dungeon_map, rooms):
    """
    add monster to the map
    """
    
    for room in rooms:
        if room == 0:
            continue
        elif room == len(rooms):
            continue
        else:
            room_start = []
            for value in dungeon_map:
                
                if dungeon_map[value] != f"room {room}":
                    continue
                else:
                    room_start.append([value, dungeon_map[value]]) 

            start_point = random.randint(1, len(room_start))
            start_key = room_start[start_point]
            dungeon_map[start_key[0]] = f"room {room} monster"

    return dungeon_map


def add_loot(dungeon_map, rooms):
    """
    add loot to the map
    """


# Gameplay functions

def map_conversion(character):
    """ takes the character and pulls the map from the google sheet,
    converts the map to # and .s to be inserted to the map pad """
    print(character)
    coremap = SHEET.worksheet(f"{character[0]}_map").get_all_values()
    newmap = []
    for x_coord in range(len(coremap)):
        for y_coord in range(len(coremap[0])):
            if str(coremap[x_coord][y_coord]) == "wall":
                newmap.append("#")
            elif "character" in str(coremap[x_coord][y_coord]):
                newmap.append("@")
            elif "boss" in str(coremap[x_coord][y_coord]):
                newmap.append("B")
            elif "monster" in str(coremap[x_coord][y_coord]):
                newmap.append("m")
            else:
                newmap.append(".")
    return(newmap)


def ignore_turn():
    """
    This function is called to let the user know that they can't pass through a wall
    and reset the turn without advancing the turn counter
    """


def combat():
    """
    The combat module selects random numbers and creates...
    """


def move():
    """
    moves the character and then the monsters.
    """


def loot():
    """
    loot module
    """


def win():
    """
    module to update stats etc when player wins
    """


def dead():
    """
    updates stats based on character dying
    """


def main(stdscr):
    """
    main function to call other functions
    """
    character = player_select(stdscr)
    dungeon_size(stdscr, character)
    gamescreen(stdscr, character)


wrapper(main)
