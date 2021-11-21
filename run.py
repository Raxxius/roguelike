def dungeon_width():
    """
    This function decides the size of the map and runs all
    the individual dungeon generation functions
    """
    print("defining dungeon size...\n")
    # dungeon_width = input("please enter dungeon width, e.g. 50\n")
    return 50


def dungeon_height():
    """
    This function decides the size of the map and runs all
    the individual dungeon generation functions
    If time permits this section will be multiple choice
    """
    print("defining dungeon size...\n")
    # dungeon_height = input("please enter dungeon height, e.g. 50\n")
    return 50


def init_dungeon(a, b):
    """
    This function sets every square in the dungeon to wall
    """
    print("Generating dungeon map...\n")

    dungeon_map = {}
    for x in range(a):
        for y in range(b):
            dungeon_map[x,y] = 0
    print(dungeon_map)
    print("map generated!")


def main():
    init_dungeon(dungeon_width(), dungeon_height())

main()

