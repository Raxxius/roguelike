def dungeon_width():
    """
    This function decides the size of the map and runs all
    the individual dungeon generation functions
    """
    print("defining dungeon size...\n")
    dungeon_width = input("please enter dungeon width, e.g. 50\n")
    return dungeon_width

def dungeon_height():
    """
    This function decides the size of the map and runs all
    the individual dungeon generation functions
    """
    print("defining dungeon size...\n")
    dungeon_height = input("please enter dungeon height, e.g. 50\n")
    return dungeon_height


def init_dungeon(a, b):
    """
    This function sets every square in the dungeon to wall
    """
    print("Generating dungeon map...\n")
    print(a)
    print(b)


def main():
    init_dungeon(dungeon_width(), dungeon_height())

main()