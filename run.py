import random
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import gspread
# import time
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


# Main flow functions


def player_select():
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
    character = opening_screen(alive_characters, dead_characters)
    return character


def dungeon_size(character):
    """
    This function decides the size of the map and runs all
    the individual dungeon generation functions
    if a map already exists for the character it will load that instead
    """

    existing_map = str(SHEET.worksheets())
    character_map = f"'{character[0]}_map'"
    if character_map in existing_map:
        print(f"{character[0]} is already in a dungeon. Loading the dungeon.")
    else:
        print("defining dungeon size...\n")
        size = input("how large would you like the dungeon to be? S, M or L?\n")
        sizef = size[0]
        if "s" in sizef.lower():
            print("Creating a small dungeon")
            x_size = 40
            y_size = 20
        elif "m" in sizef.lower():
            print("Creating a medium dungeon")
            x_size = 50
            y_size = 50
        elif "l" in sizef.lower():
            print("Creating a large dungeon")
            x_size = 100
            y_size = 100
        else:
            print("that's not a valid size you muppet")
            dungeon_size(character)

        # create a blank dungeon map
        dungeon_map = init_dungeon(x_size, y_size)
        
        # add rooms to the dungeon map
        room_number = init_rooms(random.randint(8, 12))
        position_rooms(room_number, dungeon_map, x_size, y_size)
        

        SHEET.add_worksheet(title=f"{character[0]}_map", rows=y_size, cols=x_size)
        dungeon_list = list(dungeon_map.values())
        dungeon_passover = [dungeon_list[x:x+x_size] for x in range(0, len(dungeon_list), x_size)]
        SHEET.worksheet(title=f"{character[0]}_map").update('A1', dungeon_passover)


def gamescreen(stdscr, character):
    """ this function loads the main game screen curses overlay."""

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_GREEN)
    GREEN_RED = curses.color_pair(1)
    RED_GREEN = curses.color_pair(2)

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
                           f"{character[4]}/{character[14]}{health_gap}{character[5]}/{character[15]}\n"
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

    padmap = mapconversion(character)
    # sets up the map pad
    gamemap = curses.newpad(40, 20)
    stdscr.refresh()
    # test code
    for i in range(len(padmap)):
        try:
            gamemap.addstr(padmap[i])
        except curses.error:
            pass

    gamemap.refresh(0, 0, 0, 26, 23, 79)

    stdscr.refresh()
    character_stats.refresh()
    stdscr.getch()


# Game generation functions


def opening_screen(alive_characters, dead_characters):
    """
    Checks to see if a character already exists in the database
    if the players selects a name that already exists but is dead, the user
    will be asked to pick another character.
    """
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    WHITE_BLACK = curse.init_pair(1)

 
    stdscr.addstr (3, 5, f'''
    Welcome to the roguelike dungeon
    The following characters are alive
    {alive_characters}
    you can select one of these characters or create a new one by typing a name
    ''')
    """
    print(f'''
    Welcome to the roguelike dungeon
    The following characters are alive
    {alive_characters}
    you can select one of these characters or create a new one by typing a name
    ''')
    """
    select_character = input("Type the name of your character\n")
    if select_character in alive_characters:
        character_info = player_select_existing(select_character)
    elif select_character in dead_characters:
        print(f"Sorry, {select_character} is dead! please select another name.")
        opening_screen(alive_characters, dead_characters)
    else:
        character_info = player_select_new(select_character)
    return character_info


def player_select_existing(character):
    """
    This function selects a character from the googlesheet and loads
    their stats
    """
    print(f"{character} returns to fight!")
    for player_x in SHEET.worksheet("players").get_all_values():
        if player_x[0] == character:
            character_info = player_x
    return character_info


def player_select_new(character):
    """
    This function selects a new chracter and adds them to the googlesheet
    """
    print(f"A new hero, {character} enters the fight!")
    character_info = [character, "alive", 1, 16, 10, "", "", "", "", "", "", "Shortsword", "Chainmail", 16, 10]
    SHEET.worksheet("players").append_row(character_info)
    return character_info


def init_dungeon(d_width, d_height):
    """
    This function sets every square in the dungeon to wall
    dungeon size generated by the dungeon size function.

    Function creates a paired dictonary with an x,y coordinate: and True
    This will create a rectangle with all squares set to wall(True).
    """

    print("Generating dungeon map...")
    dungeon_map = {}
    for ycoord in range(d_height):
        for xcoord in range(d_width):
            # creates a dungeon tile with an x,y coord and sets True.
            dungeon_map[xcoord, ycoord] = "wall"
    print("map generated!")
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


def position_rooms(rooms, dungeon_map, dungeon_width, dungeon_height):
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

    for room in rooms:
        xcoord = random.randint(0, dungeon_width)
        ycoord = random.randint(0, dungeon_height)
        xcoord, ycoord = room_pos_check(xcoord, ycoord, dungeon_width,
                                        dungeon_height, room, rooms)
        for xvar in range(rooms[room][1]):
            xnew = xcoord + xvar
            for yvar in range(rooms[room][2]):
                ynew = ycoord + yvar
                dungeon_map[xnew, ynew] = f"room {room}"
    return dungeon_map


def room_pos_check(xcoord, ycoord, dungeon_width, dungeon_height, room, rooms):
    """
    Makes sure that the rooms do not go outside the boundries of the map
    and that the edges (0 coordinates, end of map coordinates) are always
    walls
    """

    if xcoord == 0:
        xcoord = 1
    if ycoord == 0:
        ycoord = 1
    if xcoord + rooms[room][1] >= dungeon_width:
        xcoord = dungeon_width - rooms[room][1] - 1
    if ycoord + rooms[room][2] >= dungeon_height:
        ycoord = dungeon_height - rooms[room][2] - 1
    return xcoord, ycoord


def add_player():
    """
    add player to the map
    """


def add_monsters():
    """
    add monster to the map
    """


def add_loot():
    """
    add loot to the map
    """


# Gameplay functions


def mapconversion(character):
    """ takes the character and pulls the map from the google sheet,
    converts the map to # and .s to be inserted to the map pad """
    print(character)
    coremap = SHEET.worksheet(f"{character[0]}_map").get_all_values()
    newmap = []
    for x_coord in range(len(coremap)):
        for y_coord in range(len(coremap[0])):
            if str(coremap[x_coord][y_coord]) == "wall":
                newmap.append("#")
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


def main():
    """
    main function to call other functions
    """
    character = player_select()
    dungeon_size(character)
    gamescreen(character)


wrapper(main)
