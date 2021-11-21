# Roguelike Dungeon Crawler Tribute  

## Overview  

Ever since my parents bought me HeroQuest as a young child, I have always had a special place in my heart for the venerable dungeon crawler game.  

I have played many games, including board games, many from GamesWorkshop including HeroQuest, Advanced HeroQuest, SpaceCrusade, WarhammerQuest, and others like Descent, Zombiecide and Darklight.  

As well as playing with friends on cardboard, I have also played many computer games, including the genre defining Rogue, and expanded experience, Angband.  

[The subreddit Roguelikes](https://www.reddit.com/r/roguelikes/)

[Click here to see the Angband webpage](https://rephial.org/)  

This program is a tribute to Rogue and roguelike games, and will exhibit a number of the features of the classic Rogue game, ascii art, random dungeons, and D&D inspired combat mechanics.

## Design features

The progam has a number of features that are inspired by the rougelike genre, to create a simple single level dungeon crawler:

1. Random map generation - Eachtime a game is started a new random map will be generated.
2. Character permadeath - Characters will be stored on a googlesheets document.
3. Simultaneous turn based gameplay - Each input from the user will progress the game 1 turn.
4. Feedback - The player will not be able to walk through walls, and will be told they are trying to do so, walking through a monster will initiate combat.
5. Final Boss - The player will win the game by eliminating the final boss, or the player will die trying.

## Coding 

The components of the games code are broken down to smaller individual components 

Overall program loop is as follows:

![overviewflow](docs/screenshots/function_flow.png)




