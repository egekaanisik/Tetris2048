#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ______________________________________________________________________________________________________
# |                                                                                                    |
# |                                             TETRIS 2048                                            |
# |____________________________________________________________________________________________________|
# 
# A Tetris game which includes the classic version and a custom version which is a combination of classic version and
# another iconic game 2048. The game uses a modified version of StdDraw to draw the GUI and get the user interactions.
# It also has Discord Rich Presence support.
#
# AUTHORS:
# ------------------------------
# Ege Kaan Isik (041901042)
# Davud Duran (041901049)


# PLATFORM CONTROL
# ------------------------------
# This section checks the platform for being Windows because the program works only on it for some limitations of UNIX-based systems.

import platform

if platform.system() != 'Windows':
    print("\nThis program is designed to work only on Windows systems.")
    input("Press \"Enter\" key to terminate the program.")
    print()
    exit()


# AUTO DEPENDENCY INSTALLER
# ------------------------------
# This part of the code checks the system and gets all the modules installed. If required modules are not installed, prompts user for installing them.
# If user agrees, installs are missing modules.

import os
import pkg_resources
import subprocess
import time
import sys

# Required dependicies list
dependencies = ['Pygame', 'NumPy', 'AudioPlayer', 'Pypresence']

# Gets installed modules
packages = pkg_resources.working_set
package_list = sorted([i.key for i in packages])

# Adds missing dependencies to a list
not_installed = []

for i in dependencies:
   if i.casefold() not in package_list:
      not_installed.append(i)

# If there are some missing modules, prompt user
if len(not_installed) != 0:
   print("There are some modules that are required to run this program.\n\nThese modules are not installed on your computer:")
   for i in not_installed:
      print("[*] " + i)
    
   # Keeps asking until there is a valid answer
   while True:
      yes_no = input("\nDo you want to install them? (y/n): ")

      if yes_no.casefold() == "yes" or yes_no.casefold() == 'y':
         # Installs every module one-by-one by calling a "pip install" command
         for i in not_installed:
            print("\n____________________________________________________________________________________________________\n\nInstalling " + i + "...\n____________________________________________________________________________________________________\n")
            subprocess.check_call([sys.executable, "-m", "pip", "install", i])
         print("\n____________________________________________________________________________________________________\n\nDone installing the modules. Launching the program...\n____________________________________________________________________________________________________\n")
         time.sleep(1)
         break
      elif yes_no.casefold() == "no" or yes_no.casefold() == 'n':
         exit()
      else:
         print("Please enter a valid answer.")

# INITIALIZE FUNCTIONALITY
# ------------------------------
# This part of the code contains the required variables, constants, and imports to give functionality to program.

# Gets the current directory
DIR = os.path.dirname(os.path.realpath(__file__))

# Adds the modules subfolder to the system path
sys.path.append(DIR + "/modules")

# Hides the terminal
import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Imports remaining required modules
import stddraw # StdDraw module is used as a basic graphics library
import random # Used for creating tetrominoes with random types/shapes
from game_grid import GameGrid # Class for modeling the game grid
from tetromino import Tetromino # Class for modeling the tetrominoes
from picture import Picture # Used representing images to display
from color import Color # Used for coloring the game menu
import base64 # Used for decoding some secrets
from data import DATAS # Imports some secret data
from audioplayer import AudioPlayer # Used for playing music and sound effects
from configparser import ConfigParser # Used for getting the user configuration
import tempfile # Used for getting the user temporary file
from pypresence import Presence
from threading import Timer
import urllib.request

# Gets the config file
config = ConfigParser()
config.read("config.ini")

# Checks the configuration for having game section
if not config.has_section("GAME"):
   config.add_section("GAME")
   config.set('GAME', "difficulty", "1")
else:
   if not config.has_option("GAME", "difficulty"):
      config.set('GAME', "difficulty", "1")

# Checks the configuration for having sound section
if not config.has_section("SOUND"):
   config.add_section("SOUND")
   config.set('SOUND', "music_volume", "5")
   config.set('SOUND', "effects_volume", "25")
else:
   if not config.has_option("SOUND", "music_volume"):
      config.set('SOUND', "music_volume", "5")
   if not config.has_option("SOUND", "effects_volume"):
      config.set('SOUND', "effects_volume", "25")

# Checks the configuration for having leaderboard section
if not config.has_section("LEADERBOARD"):
   config.add_section('LEADERBOARD')
   config.set('LEADERBOARD', "hs_tetris_easy", "0")
   config.set('LEADERBOARD', "hs_tetris_normal", "0")
   config.set('LEADERBOARD', "hs_tetris_hard", "0")
   config.set('LEADERBOARD', "hs_tetris_extreme", "0")
   config.set('LEADERBOARD', "hs_2048_easy", "0")
   config.set('LEADERBOARD', "hs_2048_normal", "0")
   config.set('LEADERBOARD', "hs_2048_hard", "0")
   config.set('LEADERBOARD', "hs_2048_extreme", "0")
else:
   if not config.has_option("LEADERBOARD", "hs_tetris_easy"):
      config.set('LEADERBOARD', "hs_tetris_easy", "0")
   if not config.has_option("LEADERBOARD", "hs_tetris_normal"):
      config.set('LEADERBOARD', "hs_tetris_normal", "0")
   if not config.has_option("LEADERBOARD", "hs_tetris_hard"):
      config.set('LEADERBOARD', "hs_tetris_hard", "0")
   if not config.has_option("LEADERBOARD", "hs_tetris_extreme"):
      config.set('LEADERBOARD', "hs_tetris_extreme", "0")
   if not config.has_option("LEADERBOARD", "hs_2048_easy"):
      config.set('LEADERBOARD', "hs_2048_easy", "0")
   if not config.has_option("LEADERBOARD", "hs_2048_normal"):
      config.set('LEADERBOARD', "hs_2048_normal", "0")
   if not config.has_option("LEADERBOARD", "hs_2048_hard"):
      config.set('LEADERBOARD', "hs_2048_hard", "0")
   if not config.has_option("LEADERBOARD", "hs_2048_extreme"):
      config.set('LEADERBOARD', "hs_2048_extreme", "0")

# Checks the configuration options and deletes unnecessary ones
for i in config.sections():
   if i == 'SOUND' or i == 'GAME' or i == 'LEADERBOARD':
      for j in config.options(i):
         if (i == 'SOUND' and j != "music_volume" and j != "effects_volume") or (i == 'GAME' and j != "difficulty") or (i == 'LEADERBOARD' and j != "hs_tetris_easy" and j != "hs_tetris_normal" and j != "hs_tetris_hard" and j != "hs_tetris_extreme" and j != "hs_2048_easy" and j != "hs_2048_normal" and j != "hs_2048_hard" and j != "hs_2048_extreme"):
            config.remove_option(i, j)
   else:
      config.remove_section(i)

# Checks the difficulty option for being valid
try:
   if int(config.get("GAME", "difficulty")) < 0 or int(config.get("GAME", "difficulty")) > 3:
      config.set('GAME', "difficulty", "1")
except ValueError:
   config.set('GAME', "difficulty", "1")

# Checks the music volume option for being valid
try:
   if int(config.get("SOUND", "music_volume")) < 0 or int(config.get("SOUND", "music_volume")) > 100:
      config.set('SOUND', "music_volume", "5")
except ValueError:
   config.set('SOUND', "music_volume", "5")

# Checks the effects volume option for being valid
try:
   if int(config.get("SOUND", "effects_volume")) < 0 or int(config.get("SOUND", "effects_volume")) > 100:
      config.set('SOUND', "effects_volume", "25")
except ValueError:
   config.set('SOUND', "effects_volume", "25")

# Checks the Tetris high score on easy mode for being valid
try:
   if int(config.get("LEADERBOARD", "hs_tetris_easy")) < 0:
      config.set('LEADERBOARD', "hs_tetris_easy", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_tetris_easy", "0")

# Checks the Tetris high score on normal mode for being valid
try:
   if int(config.get("LEADERBOARD", "hs_tetris_normal")) < 0:
      config.set('LEADERBOARD', "hs_tetris_normal", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_tetris_normal", "0")

# Checks the Tetris high score on hard mode for being valid
try:
   if int(config.get("LEADERBOARD", "hs_tetris_hard")) < 0:
      config.set('LEADERBOARD', "hs_tetris_hard", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_tetris_hard", "0")

# Checks the Tetris high score on extreme mode for being valid
try:
   if int(config.get("LEADERBOARD", "hs_tetris_extreme")) < 0:
      config.set('LEADERBOARD', "hs_tetris_extreme", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_tetris_extreme", "0")

# Checks the Tetris 2048 high score on easy mode for being valid
try:
   if int(config.get("LEADERBOARD", "hs_2048_easy")) < 0:
      config.set('LEADERBOARD', "hs_2048_easy", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_2048_easy", "0")

# Checks the Tetris 2048 high score on normal mode for being valid
try:
   if int(config.get("LEADERBOARD", "hs_2048_normal")) < 0:
      config.set('LEADERBOARD', "hs_2048_normal", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_2048_normal", "0")

# Checks the Tetris 2048 high score on hard mode for being valid
try:
   if int(config.get("LEADERBOARD", "hs_2048_hard")) < 0:
      config.set('LEADERBOARD', "hs_2048_hard", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_2048_hard", "0")

# Checks the Tetris 2048 high score on extreme mode for being valid
try:
   if int(config.get("LEADERBOARD", "hs_2048_extreme")) < 0:
      config.set('LEADERBOARD', "hs_2048_extreme", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_2048_extreme", "0")

# Writes the config file again
with open('config.ini', 'w') as f:
   config.write(f)

# Initializes constants
CLIENT_ID = '833177459209535538'
RPC = Presence(CLIENT_ID)
TEMP_FILE = tempfile.gettempdir()
ICON = DIR + "/images/icon.png"
TEMP_IMAGE = TEMP_FILE + "/canvas.png"
TEMP_INFO = TEMP_FILE + "/image.png"
GRID_H = 20
GRID_W = 12
CANVAS_H = 35 * GRID_H + 1
CANVAS_W = 35 * GRID_W + 140
CENTER_X = ((GRID_W + 4 + 1)/2)-1
CENTER_Y = ((GRID_H + 1)/2)-1
WINDOW_TITLE = "Tetris 2048"

# Initializes global variables for audio players
player = AudioPlayer(DIR + "/sounds/back.mp3")
move = AudioPlayer(DIR + "/sounds/move.wav")
rotate = AudioPlayer(DIR + "/sounds/rotate.wav")
place = AudioPlayer(DIR + "/sounds/place.wav")
clear = AudioPlayer(DIR + "/sounds/clear.wav")
menu = AudioPlayer(DIR + "/sounds/menu.wav")
merge = AudioPlayer(DIR + "/sounds/merge.wav")

# Initializes global variables for all game settings
difficulty = int(config.get("GAME", "difficulty"))
hs_tetris_easy = int(config.get("LEADERBOARD", "hs_tetris_easy"))
hs_tetris_normal = int(config.get("LEADERBOARD", "hs_tetris_normal"))
hs_tetris_hard = int(config.get("LEADERBOARD", "hs_tetris_hard"))
hs_tetris_extreme = int(config.get("LEADERBOARD", "hs_tetris_extreme"))
hs_2048_easy = int(config.get("LEADERBOARD", "hs_2048_easy"))
hs_2048_normal = int(config.get("LEADERBOARD", "hs_2048_normal"))
hs_2048_hard = int(config.get("LEADERBOARD", "hs_2048_hard"))
hs_2048_extreme = int(config.get("LEADERBOARD", "hs_2048_extreme"))
music_volume = int(config.get("SOUND", "music_volume"))
effects_volume = int(config.get("SOUND", "effects_volume"))
gamemode = None
timer = None
is_connected = None


# MAIN FUNCTION OF THE PROGRAM
# ------------------------------
# Main function where this program starts execution

def start():
   # Gets the globals
   global gamemode
   global music_volume
   global effects_volume
   global player
   global move
   global rotate
   global place
   global clear
   global menu
   global merge
   
   # Checks the temporary image files and deletes them
   if os.path.exists(TEMP_IMAGE):
      os.remove(TEMP_IMAGE)
   if os.path.exists(TEMP_INFO):
      os.remove(TEMP_INFO)

   # Creates the StdDraw canvas
   stddraw.setCanvasSize(CANVAS_W, CANVAS_H) 
   stddraw.setXscale(-1, GRID_W + 4) # 17
   stddraw.setYscale(-1, GRID_H) # 21
   stddraw.setWindowTitle(WINDOW_TITLE)
   stddraw.setWindowIcon(ICON)
   stddraw.setCloseAction(close)

   # Sets the audio players' volumes by settings
   player.volume = music_volume
   move.volume = effects_volume
   rotate.volume = effects_volume
   place.volume = effects_volume
   clear.volume = effects_volume
   menu.volume = effects_volume
   merge.volume = effects_volume

   # Starts music
   player.play(loop=True)

   # The main loop of the game that creates the game cycle
   restart = False
   while True:
      # If user wants to go to the main menu, display menu, else, restart game directly
      if restart == False:
         gamemode = display_game_menu()
      restart = game()


# GAME
# ------------------------------
# This method is the main part of the game. It displays the canvas differently based on the game mode.

def game():
   # Gets the globals
   global config
   global difficulty
   global hs_tetris_easy
   global hs_tetris_normal
   global hs_tetris_hard
   global hs_tetris_extreme
   global hs_2048_easy
   global hs_2048_normal
   global hs_2048_hard
   global hs_2048_extreme
   global gamemode
   global clear
   global merge

   # Modifies the canvas for more functionality and cleanness
   stddraw.setKeyRepeat(1)
   stddraw.clearKeysTyped()
   stddraw.clearMousePresses()
   stddraw.setSaveKey("y")

   # Gets the current timestamp
   current_time = time.time()*1000

   # Updates the Rich Presence
   detail = "Playing Classic Tetris" if gamemode == "tetris" else "Playing Tetris 2048"
   mode = "Easy Mode" if difficulty == 0 else ("Normal Mode" if difficulty == 1 else ("Hard Mode" if difficulty == 2 else "Extreme Mode"))
   update_presence(state=mode, details=detail, large_image="icon", start=current_time)

   # Sets the milliseconds of standart drop based on the difficulty
   ms = (350 if difficulty == 0 else (250 if difficulty == 1 else (125 if difficulty == 2 else 75)))

   # Creates the game grid
   grid = GameGrid(GRID_H, GRID_W, gamemode, difficulty)

   # Creates the current tetromino and the next three tetrominoes by using the create_tetromino function defined below
   tetrominos = [create_tetromino(GRID_H, GRID_W), create_tetromino(GRID_H, GRID_W), create_tetromino(GRID_H, GRID_W), create_tetromino(GRID_H, GRID_W)]

   # Sets the tetrominoes on the grid
   current_tetromino = tetrominos.pop(0)
   grid.current_tetromino = current_tetromino
   grid.next_tetromino1 = tetrominos[0]
   grid.next_tetromino2 = tetrominos[1]
   grid.next_tetromino3 = tetrominos[2]

   # Sets the high score of the current game mode and difficulty
   if gamemode == "tetris":
      grid.old_high_score = (hs_tetris_easy if difficulty == 0 else (hs_tetris_normal if difficulty == 1 else (hs_tetris_hard if difficulty == 2 else hs_tetris_extreme)))
   else:
      grid.old_high_score = (hs_2048_easy if difficulty == 0 else (hs_2048_normal if difficulty == 1 else (hs_2048_hard if difficulty == 2 else hs_2048_extreme)))
   
   # Sets the initial values of last mouse positions, click and drop situations
   last_mouse_posX = -1
   last_mouse_posY = -1
   mouse = None
   already_rotated = False
   already_dropped = False

   # The main game loop
   while True:
      # Gets the mouse positions and keys types
      posX = round(stddraw.mouseMotionX())
      posY = round(stddraw.mouseMotionY())
      keys_typed = stddraw.getKeysTyped()

      # Sets the drop situation of the current tetromino for checking hard drop
      dropped = False
      
      # Checks the mouse and keyboard interactions for switching the controls between mouse and keyboard
      if ((posX != last_mouse_posX) or (posY != last_mouse_posY) or stddraw.mouseLeftHeldDown() or stddraw.mouseRightHeldDown() or stddraw.mouseScrollHeldDown()) and grid.is_inside(posY, posX):
         mouse = True
         last_mouse_posX = posX
         last_mouse_posY = posY
      elif stddraw.hasNextKeyTyped():
         if "up" in keys_typed or "down" in keys_typed or "right" in keys_typed or "left" in keys_typed or "space" in keys_typed or "escape" in keys_typed or "w" in keys_typed or "a" in keys_typed or "s" in keys_typed or "d" in keys_typed:
            mouse = False

      # Checks the events for keyboard
      if not mouse:
         # Hard drop if user pressed Space
         if "space" in keys_typed:
            # Moves down the tetromino all the way down until it cannot go further
            if not already_dropped:
               count = 0
               while True:
                  sc = current_tetromino.move("down", grid, 1)
                  if not sc:
                     break
                  else:
                     count += 1
               dropped = True
               already_dropped = True
               # Increases the score by line count * 2
               grid.score += count * 2
         # Rotates if user pressed Up or W
         if "up" in keys_typed or "w" in keys_typed:
            if not already_rotated:
               can_rotate = current_tetromino.rotate(grid)
               if can_rotate:
                  rotate.play()
                  already_rotated = True
         # Moves left if user pressed Left or A
         if "left" in keys_typed or "a" in keys_typed:
            can_left = current_tetromino.move("left", grid, 1, delay=150)
            if can_left:
               move.play()
         # Moves right if user pressed Right or D
         if "right" in keys_typed or "d" in keys_typed:
            can_right = current_tetromino.move("right", grid, 1, delay=150)
            if can_right:
               move.play()
         # Soft drops if user pressed Down or S
         if "down" in keys_typed or "s" in keys_typed:
            succ = current_tetromino.move("down", grid, 1, delay=50)
            # Increases the score by 1 if tetromino can go down
            if succ:
               grid.score += 1
         # Pauses if user pressed Escape
         if "escape" in keys_typed:
            option = display_pause_menu()

            # If user wants to go the the menu, break the loop and go
            if option == "menu":
               return False
            # If user wants to restart the game, break the loop and restart
            elif option == "restart":
               return True
         # If user releases a key, check the statements below
         if stddraw.hasNextKeyReleased():
            # Gets the released keys
            keys_released = stddraw.getKeysReleased()

            # If user releases Up or W, set the already rotated value to false
            if "up" in keys_released or "w" in keys_released:
               already_rotated = False
            # If user releases Space, set the already dropped value to false
            if "space" in keys_released:
               already_dropped = False
      # Checks the events for mouse
      else:
         # Gets the middle index for the current tetromino
         middle = (0 if current_tetromino.column_count == 1 or current_tetromino.column_count == 2 else 1)

         # Sets the difference between the middle tile of the tetromino
         if (posX + middle) > grid.grid_width:
            posX = grid.grid_width - middle
         diff = posX - (current_tetromino.leftmost + middle)

         # Moves left if user pulls the mouse to the left
         if diff < 0:
            for i in range(-diff):
               success_move = current_tetromino.move("left", grid, 1)
               if not success_move:
                  break
               else:
                  if not already_rotated:
                     move.play()
         # Moves right if user pulls the mouse to the right
         else:
            for i in range(diff):
               success_move = current_tetromino.move("right", grid, 1)
               if not success_move:
                  break
               else:
                  if not already_rotated:
                     move.play()
         
         already_rotated = False

         # Rotates if user clicked the mouse right button
         if stddraw.mouseRightPressed():
            if grid.is_inside(round(stddraw.mouseRightY()), round(stddraw.mouseRightX())):
               success_rotate = current_tetromino.rotate(grid)
               if success_rotate:
                  rotate.play()
                  already_rotated = True
         # Hard drops if user clicked the mouse left button
         if stddraw.mouseLeftPressed():
            if grid.is_inside(round(stddraw.mouseLeftY()), round(stddraw.mouseLeftX())):
               # Moves down the tetromino all the way down until it cannot go further
               count = 0
               while True:
                  sc = current_tetromino.move("down", grid, 1)
                  if not sc:
                     break
                  else:
                     count += 1
               dropped = True
               # Increases the score by line count * 2
               grid.score += count * 2
         # Soft drops if user held down the scroll button
         if stddraw.mouseScrollHeldDown():
            if grid.is_inside(round(stddraw.mouseScrollY()), round(stddraw.mouseScrollX())):
               succ = current_tetromino.move("down", grid, 1, delay=50)
               # Increases the score by 1 if tetromino can go down
               if succ:
                  grid.score += 1

      # Clears all the user interactions
      stddraw.clearMousePresses()
      stddraw.clearKeysTyped()
      stddraw.clearKeysReleased()
      
      # If difficulty is not extreme, creates the ghost of the current tetromino and moves down the ghost all the way down until it cannot go further
      if difficulty != 3:
         current_ghost = current_tetromino.copy(ghost=True)
         grid.current_ghost = current_ghost
         
         while True:
            sc = current_ghost.move("down", grid, 1)
            if not sc:
               break
      
      # Moves the tetromino down by the determined milliseconds delay if it is not dropped
      if not dropped:
         success = current_tetromino.move("down", grid, 1, delay=ms, standart=True)

      # Places the tetromino on the game grid when it cannot go down anymore or dropped already
      if dropped or success == False:
         place.play()
         # Gets the tile matrix of the tetromino
         tiles_to_place = current_tetromino.tile_matrix
         # Deletes the ghost
         grid.current_ghost = None
         # Updates the game grid by adding the tiles of the tetromino
         grid.update_grid(tiles_to_place)

         # If game is over, writes the config if a new high score value exists and breaks the loop
         if grid.game_over:
            grid.display()
            if grid.new_high_score is not None:
               if gamemode == "tetris":
                  if difficulty == 0:
                     config.set("LEADERBOARD", "hs_tetris_easy", str(grid.new_high_score))
                     hs_tetris_easy = grid.new_high_score
                  elif difficulty == 1:
                     config.set("LEADERBOARD", "hs_tetris_normal", str(grid.new_high_score))
                     hs_tetris_normal = grid.new_high_score
                  elif difficulty == 2:
                     config.set("LEADERBOARD", "hs_tetris_hard", str(grid.new_high_score))
                     hs_tetris_hard = grid.new_high_score
                  else:
                     config.set("LEADERBOARD", "hs_tetris_extreme", str(grid.new_high_score))
                     hs_tetris_extreme = grid.new_high_score
               else:
                  if difficulty == 0:
                     config.set("LEADERBOARD", "hs_2048_easy", str(grid.new_high_score))
                     hs_2048_easy = grid.new_high_score
                  elif difficulty == 1:
                     config.set("LEADERBOARD", "hs_2048_normal", str(grid.new_high_score))
                     hs_2048_normal = grid.new_high_score
                  elif difficulty == 2:
                     config.set("LEADERBOARD", "hs_2048_hard", str(grid.new_high_score))
                     hs_2048_hard = grid.new_high_score
                  else:
                     config.set("LEADERBOARD", "hs_2048_extreme", str(grid.new_high_score))
                     hs_2048_extreme = grid.new_high_score
               
               with open('config.ini', 'w') as f:
                  config.write(f)
            break
         
         # Does chain merging and line clearing until it cannot if the game mode is 2048
         if gamemode == "2048":
            while True:
               grid.check_line_chain_merge(merge)
               score_before_line_delete = grid.score
               grid.delete_full_lines(clear)
               if score_before_line_delete == grid.score:
                  break
         # Checks the lines only if the game mode is Tetris
         else:
            grid.delete_full_lines(clear)

         # Creates the next tetromino to enter the game grid by using the create_tetromino function defined below
         tetromino = create_tetromino(GRID_H, GRID_W)
         tetrominos.append(tetromino)

         # Sets the current tetromino and the next tetrominoes
         current_tetromino = tetrominos.pop(0)
         grid.next_tetromino1 = tetrominos[0]
         grid.next_tetromino2 = tetrominos[1]
         grid.next_tetromino3 = tetrominos[2]
         grid.current_tetromino = current_tetromino

      # Display the game grid
      grid.display()
   
   # Disables repeated key events
   stddraw.setKeyRepeat()

   # Lets the user decide whether they want to restart or return to the main menu
   while True:
      keys_typed = stddraw.getKeysTyped()
      # Return to the main menu if user pressed Enter or Return
      if "enter" in keys_typed or "return" in keys_typed:
         stddraw.clearKeysTyped()
         return False
      # Restart the game if user pressed R
      elif "r" in keys_typed:
         stddraw.clearKeysTyped()
         return True
      stddraw.clearKeysTyped()
      stddraw.show(0)


# CLOSE HANDLER
# ------------------------------
# This method is used to replace the default close action of StdDraw. Method executes when the GUI window is terminated.

def close():
   # Gets the globals
   global config
   global timer
   global is_connected
   global player
   global move
   global rotate
   global place
   global clear
   global menu
   global merge

   if timer.is_alive():
      timer.cancel()

   # Writes the last changes into the config file
   with open('config.ini', 'w') as f:
      config.write(f)

   # Deletes the temporary files if they exist
   if os.path.exists(TEMP_IMAGE):
      os.remove(TEMP_IMAGE)
   if os.path.exists(TEMP_INFO):
      os.remove(TEMP_INFO)

   # Closes the audio players
   player.close()
   move.close()
   rotate.close()
   place.close()
   clear.close()
   menu.close()
   merge.close()

   # Unhides the terminal
   ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)

   # Terminates the system
   sys.exit()


# CREATE TETROMINO
# ------------------------------
# Function for creating random shaped tetrominoes to enter the game grid.

def create_tetromino(grid_height, grid_width):
   # Gets the global
   global gamemode

   # Determines a have random tetromino shape and bottom left corner position
   tetromino_types = [ 'I', 'O', 'Z', 'S', 'L', 'J', 'T' ]
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   n = (4 if random_type == 'I' else (2 if random_type == 'O' else 3))
   bottom_x = random.randint(0, grid_width - n)

   # Creates and returns a tetromino with the given shape and bottom left corner position
   return Tetromino(random_type, grid_height, grid_width, bottom_x, gamemode=gamemode)


# DISPLAY GAME MENU
# ------------------------------
# Function for displaying a simple menu before starting the game.

def display_game_menu():
   # Gets the globals
   global config
   global is_connected
   global difficulty
   global music_volume
   global effects_volume

   # Modifies the canvas for more functionality and cleanness
   stddraw.clearKeysTyped()
   stddraw.clearMousePresses()
   stddraw.setKeyRepeat()
   stddraw.setSaveKey()
   stddraw.setFontFamily("Arial")

   # Tries to connect to the Discord server if not connected
   connect_presence()

   # Updates the Rich Presence
   update_presence(state="Idling", details="In Main Menu", large_image='icon')
 
   # Creates colors for the menu
   background_color = Color(25, 49, 90)
   button_color = Color(132, 132, 132)
   text_color = Color(31, 160, 239)

   # Clears the background canvas to background color
   stddraw.clear(background_color)

   # Initializes picture objects with their paths
   image_to_display = Picture(DIR + "/images/menu_image.png")
   tetris= Picture(DIR + "/images/tetris.png")
   tetris2= Picture(DIR + "/images/tetris2.png")
   i2048 = Picture(DIR + "/images/2048.png")
   i2048L = Picture(DIR + "/images/2048L.png")
   musicOn = Picture(DIR + "/images/musicOn.png")
   musicOff = Picture(DIR + "/images/musicOff.png")
   soundOff = Picture(DIR + "/images/soundOff.png")
   soundOn = Picture(DIR + "/images/soundOn.png")
   easy = Picture(DIR + "/images/easy.png")
   normal = Picture(DIR + "/images/normal.png")
   hard = Picture(DIR + "/images/hard.png")
   extreme = Picture(DIR + "/images/extreme.png")
   help = Picture(DIR + "/images/help.png")
   scores = Picture(DIR + "/images/scores.png")
   connected = Picture(DIR + "/images/connected.png")
   disconnected = Picture(DIR + "/images/disconnected.png")

   # Dimensions of the buttons
   button_w, button_h = GRID_W, 2.30

   # Dimensions of the sliders
   slider_w, slider_h = GRID_W, 0.2

   # Coordinates of the bottom left corner of the buttons
   button_blc_x, button_blc_y = CENTER_X-button_w/2, 3.875 # Tetris Button 
   button3_blc_x, button3_blc_y = CENTER_X-button_w/2, 0.875 # Tetris 2048 Button

   # Coordinates of the center of the hover buttons
   help_x, help_y = CENTER_X + 7.75, CENTER_Y + 9.75
   scores_x, scores_y = CENTER_X - 7.75, CENTER_Y + 9.75
   status_x, status_y = CENTER_X - 8, CENTER_Y - 10.125,

   # Slider start and end coordinates
   slider_start = CENTER_X-button_w/2
   slider_end = slider_start+slider_w

   # Sets the slider thumbs' positions based on the volume levels
   slider1location = slider_start + (0 if music_volume == 0 else (slider_w/(100/music_volume)))
   slider2location = slider_start + (0 if effects_volume == 0 else (slider_w/(100/effects_volume)))
   slider3location = slider_start + ((slider_w / 3) * difficulty)

   # Variables for listener and hold handlers
   musicHold = False
   soundHold = False
   diffHold = False
   played = False
   string = ""

   # Main menu loop
   while True:
      # Checks for some secrets ;)
      if stddraw.hasNextKeyTyped():
         string += stddraw.nextKeyTyped()
      if get_data(1) in string:
         display_info()
         # Tries to connect to the Discord server if not connected
         connect_presence()
         # Updates the Rich Presence
         update_presence(state="Idling", details="In Main Menu", large_image='icon')
         string = ""
      
      # Sets the element images
      speedButtonPicture = normal
      soundButtonPicture = soundOn
      musicButtonPicture = musicOn
      tetrisButtonPicture = tetris
      i2048Picture = i2048
      status_image = connected if is_connected else disconnected
   
      # Gets the x and y positions of mouse
      mouse_x = stddraw.mouseMotionX() if stddraw.mouseMotionX() is not None else -1
      mouse_y = stddraw.mouseMotionY() if stddraw.mouseMotionY() is not None else -1
      
      # Checks the mouse held down event
      if stddraw.mouseLeftHeldDown():
         # If the held down thumb is music volume slider's thumb, update only its position
         if musicHold:
            if mouse_x >= slider_start and mouse_x <= slider_end:
               slider1location = mouse_x
               volume_percent = (slider1location-slider_start)/(slider_end-slider_start)*100
            elif mouse_x < slider_start:
               slider1location = slider_start
               volume_percent = 0
            else:
               slider1location = slider_end
               volume_percent = 100
            set_music_volume(round(volume_percent))
         # If the held down thumb is effects volume slider's thumb, update only its position
         elif soundHold:
            if mouse_x >= slider_start and mouse_x <= slider_end:
               slider2location = mouse_x
               sound_percent = (slider2location-slider_start)/(slider_end-slider_start)*100
            elif mouse_x < slider_start:
               slider2location = slider_start
               sound_percent = 0
            else:
               slider2location = slider_end
               sound_percent = 100
            set_effects_volume(round(sound_percent))
         # If the held down thumb is difficulty slider's thumb, update only its position
         elif diffHold:
            if mouse_x >= slider_start and mouse_x <= slider_end:
               if mouse_x < slider_start + (slider_w / 6) * 1:
                  slider3location = slider_start
                  difficulty = 0
               elif mouse_x >= slider_start + (slider_w / 6) * 1 and mouse_x < slider_start + (slider_w / 6) * 3:
                  slider3location = slider_start + (slider_w / 6) * 2
                  difficulty = 1
               elif mouse_x >= slider_start + (slider_w / 6) * 3 and mouse_x < slider_start + (slider_w / 6) * 5:
                  slider3location = slider_start + (slider_w / 6) * 4
                  difficulty = 2
               elif mouse_x >= slider_start + (slider_w / 6) * 5:
                  slider3location = slider_end
                  difficulty = 3
            elif mouse_x < slider_start:
               slider3location = slider_start
               difficulty = 0
            else:
               slider3location = slider_end
               difficulty = 3
            set_difficulty(difficulty)
         # If nothing is held down before, sets the held down thumb
         else:
            if mouse_y >= 10.52 and mouse_y < 10.54 + slider_h and mouse_x >= slider_start and mouse_x <= slider_end:
               musicHold = True
            elif mouse_y >= 9.02 and mouse_y < 9.04 + slider_h and mouse_x >= slider_start and mouse_x <= slider_end:
               soundHold = True
            elif mouse_y >= 7.52 and mouse_y < 7.54 + slider_h and mouse_x >= slider_start and mouse_x <= slider_end:
               diffHold = True
      # Resets handlers if nothing is held down
      else:
         musicHold = False
         soundHold = False
         diffHold = False

      # Updates the music and effects sliders' thumb photo if the desired volume is 0
      if music_volume == 0:
         musicButtonPicture=musicOff
      if effects_volume == 0:
         soundButtonPicture=soundOff

      # Updates the difficulty slider's thumb photo based on the difficulty level
      diffStr = "Easy" if difficulty == 0 else ("Normal" if difficulty == 1 else ("Hard" if difficulty == 2 else "Extreme"))
      speedButtonPicture = easy if difficulty == 0 else (normal if difficulty == 1 else (hard if difficulty == 2 else extreme))

      # Checks for the mouse left click events
      if stddraw.mouseLeftPressed():
         # If the click is in the boundaries of Tetris button, returns the selection as Tetris
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               return "tetris"
         # If the click is in the boundaries of 2048 button, returns the selection as 2048
         if mouse_x >= button3_blc_x and mouse_x <= button3_blc_x + button_w:
            if mouse_y >= button3_blc_y and mouse_y <= button3_blc_y + button_h:
               return "2048"

      # Draw a thin bar on the bottom of GUI
      stddraw.filledRectangle(-1, -1, CANVAS_W, 0.7)

      # Checks for the hover mouse event
      # If the mouse is on Tetris button, changes the picture
      if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w and mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
         tetrisButtonPicture = tetris2
         if not played:
            menu.play()
            played = True
      # If the mouse is on 2048 button, changes the picture
      elif mouse_x >= button3_blc_x and mouse_x <= button3_blc_x + button_w and mouse_y >= button3_blc_y and mouse_y <= button3_blc_y + button_h:
         i2048Picture = i2048L
         if not played:
            menu.play()
            played = True
      # If the mouse is on help hover, displays controls
      elif mouse_x >= help_x - 0.5 and mouse_x <= help_x + 0.5 and mouse_y >= help_y - 0.5 and mouse_y <= help_y + 0.5:
         if not played:
            menu.play()
            played = True
         display_controls(background_color)
         string = ""
      # If the mouse is on leaderboard hover, displays scores
      elif mouse_x >= scores_x - 0.5 and mouse_x <= scores_x + 0.5 and mouse_y >= scores_y - 0.5 and mouse_y <= scores_y + 0.5:
         if not played:
            menu.play()
            played = True
         display_scores()
         string = ""
      # If the mouse is on status hover, shows status string
      elif mouse_x >= status_x - 0.25 and mouse_x <= status_x + 0.25 and mouse_y >= status_y - 0.25 and mouse_y <= status_y + 0.25:
         if not is_connected:
            stddraw.setPenColor(stddraw.WHITE)
            stddraw.setFontSize(16)
            stddraw.text(status_x + 2.85, status_y, "Failed to connect Discord.")
         else:
            stddraw.setPenColor(stddraw.WHITE)
            stddraw.setFontSize(16)
            stddraw.text(status_x + 2.5, status_y, "Connected to Discord.")
      else:
         played = False

      # Sets the font size
      stddraw.setFontSize(20)

      # Draws music volume slider
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,10.5,slider_w,slider_h)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.filledCircle(slider1location,10.5+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.boldText(slider1location-0.03,10,str(music_volume))
      stddraw.picture(musicButtonPicture,slider1location-0.03,10.5+(slider_h/2))

      # Draws effects volume slider
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,9,slider_w,slider_h)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.filledCircle(slider2location,9+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.boldText(slider2location-0.03,8.5,str(effects_volume))
      stddraw.picture(soundButtonPicture,slider2location-0.01,9+(slider_h/2))

      # Draws difficulty slider
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,7.5,slider_w,slider_h)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.filledCircle(slider3location,7.5+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.boldText(slider3location-0.03,7,diffStr)
      gap = -0.025 if difficulty == 3 or difficulty == 1 else(0.025 if difficulty == 0 else 0) 
      stddraw.picture(speedButtonPicture,slider3location+gap,7.5+(slider_h/2)+0.02)

      # Draws buttons, hovers, and logo
      stddraw.picture(image_to_display, CENTER_X, CENTER_Y+6)
      stddraw.picture(tetrisButtonPicture,CENTER_X,5)
      stddraw.picture(i2048Picture,CENTER_X,2)
      stddraw.picture(help, help_x, help_y)
      stddraw.picture(scores, scores_x, scores_y)
      stddraw.picture(status_image, status_x, status_y)

      # Shows the canvas and clears it with the background color
      stddraw.show(0)
      stddraw.clear(background_color)


# GET DATA
# ------------------------------
# A method for getting some secret stuff. ;)

def get_data(number):
	return bytes.fromhex(base64.decodebytes(DATAS[number]).decode()).decode() if number != 0 else base64.decodebytes(DATAS[0])


# DISPLAY CONTROLS
# ------------------------------
# A method for showing the controls to the user.

def display_controls(background_color):
   # Initializes picture objects with their paths
   help = Picture(DIR + "/images/help.png")
   controls = Picture(DIR + "/images/controls.png")

   # Coordinates of the center of the hover button
   help_x, help_y = CENTER_X + 7.75, CENTER_Y + 9.75

   # Main loop for the controls
   while True:
      # Gets the mouse positions
      mouse_x = stddraw.mouseMotionX()
      mouse_y = stddraw.mouseMotionY()
      
      # Checks if the mouse is not in the boundaries of hover button
      if not (mouse_x >= help_x - 0.5 and mouse_x <= help_x + 0.5 and mouse_y >= help_y - 0.5 and mouse_y <= help_y + 0.5):
         # Clears the user interactions and breaks the loop
         stddraw.clearKeysTyped()
         stddraw.clearMousePresses()
         break
      
      # Clears the canvas and draws the elements to the canvas
      stddraw.clear(background_color)
      stddraw.picture(controls, CENTER_X, CENTER_Y)
      stddraw.picture(help, help_x, help_y)
      stddraw.show(0)


# DISPLAY PAUSE MENU
# ------------------------------
# A method for showing the pause menu.

def display_pause_menu():
   # Gets the globals
   global config
   global music_volume
   global effects_volume

   # Modifies the canvas for more functionality and cleanness
   stddraw.clearMousePresses()
   stddraw.setKeyRepeat()
   stddraw.clearKeysTyped()
   stddraw.setSaveKey()
   stddraw.setFontFamily("Arial")

   # Saves a screenshot of the canvas to make it a background for the pause menu
   stddraw.save(TEMP_IMAGE)

   # Sets color to be used
   background_color = stddraw.BLACK
   button_color = Color(132, 132, 132)
   text_color = stddraw.LIGHT_GRAY

   # Clears the background canvas to background_color
   stddraw.clear(background_color)

   # Initializes picture objects with their paths
   musicOn = Picture(DIR + "/images/musicOn.png")
   musicOff = Picture(DIR + "/images/musicOff.png")
   soundOff = Picture(DIR + "/images/soundOff.png")
   soundOn = Picture(DIR + "/images/soundOn.png")
   blur = Picture(DIR + "/images/pause_blur.png")
   canvas = Picture(TEMP_IMAGE)
   help = Picture(DIR + "/images/help.png")

   # Coordinates of the center of the hover button
   help_x, help_y = CENTER_X + 7.75, CENTER_Y + 9.75

   # Dimensions of the sliders and their start and end points
   slider_w, slider_h = GRID_W, 0.2
   slider_start = CENTER_X-GRID_W/2
   slider_end = slider_start+slider_w

   # Sets the thumb locations based on the volume levels
   slider1location = slider_start + (0 if music_volume == 0 else (slider_w/(100/music_volume)))
   slider2location = slider_start + (0 if effects_volume == 0 else (slider_w/(100/effects_volume)))

   # Variables for listener and hold handlers
   musicHold = False
   soundHold = False
   first = True
   played = False

   # Main loop for the pause menu
   while True:
      # Gets the keys typed
      keys_typed = stddraw.getKeysTyped()

      # Breaks the pause menu to continue if user pressed Escape
      if "escape" in keys_typed:
         if os.path.exists(TEMP_IMAGE):
            os.remove(TEMP_IMAGE)
         stddraw.setKeyRepeat(1)
         stddraw.clearKeysTyped()
         stddraw.clearMousePresses()
         stddraw.setSaveKey("y")
         break
      # Breaks the pause menu to return to main menu if user pressed Enter or Return
      elif "enter" in keys_typed or "return" in keys_typed:
         if os.path.exists(TEMP_IMAGE):
            os.remove(TEMP_IMAGE)
         stddraw.setKeyRepeat(1)
         stddraw.clearKeysTyped()
         stddraw.clearMousePresses()
         return "menu"
      # Breaks the pause menu to restart the game if user pressed R
      elif "r" in keys_typed:
         if os.path.exists(TEMP_IMAGE):
            os.remove(TEMP_IMAGE)
         stddraw.setKeyRepeat(1)
         stddraw.clearKeysTyped()
         stddraw.clearMousePresses()
         return "restart"

      # Sets the slider thumb pictures
      soundButtonPicture = soundOn
      musicButtonPicture = musicOn

      # Gets the mouse positions
      mouse_x = stddraw.mouseMotionX() if stddraw.mouseMotionX() is not None else -1
      mouse_y = stddraw.mouseMotionY() if stddraw.mouseMotionY() is not None else -1
      
      # Checks the mouse held down event
      if stddraw.mouseLeftHeldDown():
         # If the held down thumb is music volume slider's thumb, update only its position
         if musicHold:
            if mouse_x >= slider_start and mouse_x <= slider_end:
               slider1location = mouse_x
               volume_percent = (slider1location-slider_start)/(slider_end-slider_start)*100
            elif mouse_x < slider_start:
               slider1location = slider_start
               volume_percent = 0
            else:
               slider1location = slider_end
               volume_percent = 100
            set_music_volume(round(volume_percent))
         # If the held down thumb is effects volume slider's thumb, update only its position
         elif soundHold:
            if mouse_x >= slider_start and mouse_x <= slider_end:
               slider2location = mouse_x
               sound_percent = (slider2location-slider_start)/(slider_end-slider_start)*100
            elif mouse_x < slider_start:
               slider2location = slider_start
               sound_percent = 0
            else:
               slider2location = slider_end
               sound_percent = 100
            set_effects_volume(round(sound_percent))
         # If nothing is held down before, sets the held down thumb
         else:
            if mouse_y >= 4.52 and mouse_y < 4.54 + slider_h and mouse_x >= slider_start and mouse_x <= slider_end:
               musicHold = True
            elif mouse_y >= 3.02 and mouse_y < 3.04 + slider_h and mouse_x >= slider_start and mouse_x <= slider_end:
               soundHold = True
      # Resets handlers if nothing is held down
      else:
         musicHold = False
         soundHold = False

      # If the mouse is on help hover, displays controls
      if mouse_x >= help_x - 0.5 and mouse_x <= help_x + 0.5 and mouse_y >= help_y - 0.5 and mouse_y <= help_y + 0.5:
         if not played:
            menu.play()
            played = True
         display_controls(background_color)
      else:
         played = False
      
      # Updates the music and effects sliders' thumb photo if the desired volume is 0
      if music_volume == 0:
         musicButtonPicture=musicOff
      if effects_volume == 0:
         soundButtonPicture=soundOff

      # Clears the user interactions
      stddraw.clearKeysTyped()
      stddraw.clearMousePresses()

      # Draws the background picture and a black tint on top of it
      stddraw.picture(canvas,CENTER_X,CENTER_Y)
      stddraw.picture(blur,CENTER_X,CENTER_Y)

      # Writes the pause string
      stddraw.setFontSize(72)
      stddraw.boldText(CENTER_X, CENTER_Y+3, "Game Paused")

      # Writes the pause menu interaction options
      stddraw.setFontSize(24)
      stddraw.text(CENTER_X, CENTER_Y, "Press Esc to resume the game,")
      stddraw.text(CENTER_X, CENTER_Y-0.8, "press R to restart the game,")
      stddraw.text(CENTER_X, CENTER_Y-1.6, "or press Enter to return to the main menu.")

      # Draws music volume slider
      stddraw.setFontSize(20)
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,4.5,slider_w,slider_h)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.filledCircle(slider1location,4.5+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.boldText(slider1location-0.03,4,str(music_volume))
      stddraw.picture(musicButtonPicture,slider1location-0.03,4.5+(slider_h/2))

      # Draws effects volume slider
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,3,slider_w,slider_h)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.filledCircle(slider2location,3+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.boldText(slider2location-0.03,2.5,str(effects_volume))
      stddraw.picture(soundButtonPicture,slider2location-0.01,3+(slider_h/2))

      # Draws the help hover button
      stddraw.picture(help, help_x, help_y)

      # Shows the canvas and clears the background
      stddraw.show(0)
      if first:
         stddraw.clearKeysTyped()
         first = False
      stddraw.clear(background_color)


# DISPLAY INFO
# ------------------------------
# TOP SECRET. A method for displaying some good information.

def display_info():
   # Modifies the canvas for more functionality and cleanness
   stddraw.clearMousePresses()
   stddraw.setKeyRepeat()
   stddraw.clearKeysTyped()
   stddraw.setSaveKey()
   stddraw.setWindowTitle(get_data(2))

   # Writes some data into the temp information file
   with open(TEMP_INFO, "wb") as fh:
	   fh.write(get_data(0))

   # Initializes the picture object
   info = Picture(TEMP_INFO)

   # Updates the Rich Presence
   update_presence(state=get_data(2), details=get_data(2), large_image=get_data(1))
   
   # Sets the pen color to black
   stddraw.setPenColor(stddraw.BLACK)

   # Main loop
   while True:
      # Gets the keys that user typed
      keys_typed = stddraw.getKeysTyped()

      # Breaks the loop, deletes all evidences, and goes to the main menu if user pressed Escape
      if "escape" in keys_typed:
         if os.path.exists(TEMP_INFO):
            os.remove(TEMP_INFO)
         stddraw.clearKeysTyped()
         stddraw.clearMousePresses()
         stddraw.setWindowTitle(WINDOW_TITLE)
         break

      # Draws some extra information
      stddraw.setFontSize(52)
      stddraw.boldText(CENTER_X, CENTER_Y+9, get_data(2))
      stddraw.picture(info, CENTER_X, CENTER_Y+2.5)
      stddraw.square(CENTER_X, CENTER_Y+2.5, 5)
      stddraw.setFontSize(32)
      stddraw.boldText(CENTER_X, CENTER_Y-3.75, get_data(3))
      stddraw.setFontSize(24)
      stddraw.boldText(CENTER_X/2,CENTER_Y-5.25, get_data(4))
      stddraw.boldText(CENTER_X+(CENTER_X/2),CENTER_Y-5.25, get_data(7))
      stddraw.setFontSize(24)
      stddraw.text(CENTER_X/2, CENTER_Y-6.25, get_data(5))
      stddraw.text(CENTER_X/2, CENTER_Y-7.25, get_data(6))
      stddraw.text(CENTER_X+(CENTER_X/2), CENTER_Y-6.25, get_data(8))
      stddraw.text(CENTER_X+(CENTER_X/2), CENTER_Y-7.25, get_data(9))
      stddraw.text(CENTER_X+(CENTER_X/2), CENTER_Y-8.25, get_data(10))
      stddraw.setFontSize(16)
      stddraw.text(CENTER_X, CENTER_Y-9.75, get_data(11))

      # Shows and clears the canvas
      stddraw.show(0)
      stddraw.clear()


# SET MUSIC VOLUME
# ------------------------------
# This method changes the music volume and writes the volume data into the config.

def set_music_volume(volume):
   # Gets the globals
   global config
   global music_volume
   global player

   # Sets the volume
   music_volume = volume
   player.volume = volume

   # Changes config
   config.set("SOUND", "music_volume", str(volume))
   with open('config.ini', 'w') as f:
      config.write(f)


# SET EFFECTS VOLUME
# ------------------------------
# This method changes the effects volume and writes the volume data into the config.

def set_effects_volume(volume):
   # Gets the globals
   global config
   global effects_volume
   global move
   global rotate
   global place
   global clear
   global menu
   global merge

   # Sets the volume
   effects_volume = volume
   move.volume = volume
   rotate.volume = volume
   place.volume = volume
   clear.volume = volume
   menu.volume = volume
   merge.volume = volume

   # Changes config
   config.set("SOUND", "effects_volume", str(volume))
   with open('config.ini', 'w') as f:
      config.write(f)
   

# SET DIFFICULTY
# ------------------------------
# This method changes the difficulty and writes the difficulty data into the config.

def set_difficulty(index):
   # Gets the globals
   global config
   global difficulty

   # Sets the difficulty
   difficulty = index

   # Changes config
   config.set("GAME", "difficulty", str(index))
   with open('config.ini', 'w') as f:
      config.write(f)


# DISPLAY SCORES
# ------------------------------
# A method for showing the scoreboard.

def display_scores():
   # Gets the globals
   global config
   global hs_tetris_easy
   global hs_tetris_normal
   global hs_tetris_hard
   global hs_tetris_extreme
   global hs_2048_easy
   global hs_2048_normal
   global hs_2048_hard
   global hs_2048_extreme

   # Initializes the picture object with its path
   scores = Picture(DIR + "/images/scores.png")

   # Coordinates of the center of the hover button
   scores_x, scores_y = CENTER_X - 7.75, CENTER_Y + 9.75

   # Sets the background color
   background_color = Color(25, 49, 90)

   # Sets the font and the pen color
   stddraw.setFontFamily("Arial")
   stddraw.setPenColor(stddraw.WHITE)

   # Main loop
   while True:
      # Gets the mouse positions
      mouse_x = stddraw.mouseMotionX()
      mouse_y = stddraw.mouseMotionY()

      # Checks if the mouse is not in the boundaries of hover button
      if not (mouse_x >= scores_x - 0.5 and mouse_x <= scores_x + 0.5 and mouse_y >= scores_y - 0.5 and mouse_y <= scores_y + 0.5):
         stddraw.clearKeysTyped()
         stddraw.clearMousePresses()
         stddraw.setFontSize(20)
         break
      
      # Gets the keys typed
      keys_typed = stddraw.getKeysTyped()

      # Clears the scoreboard if user pressed Backspace
      if "backspace" in keys_typed:
         hs_tetris_easy = 0
         hs_tetris_normal = 0
         hs_tetris_hard = 0
         hs_tetris_extreme = 0
         hs_2048_easy = 0
         hs_2048_normal = 0
         hs_2048_hard = 0
         hs_2048_extreme = 0
         config.set('LEADERBOARD', "hs_tetris_easy", "0")
         config.set('LEADERBOARD', "hs_tetris_normal", "0")
         config.set('LEADERBOARD', "hs_tetris_hard", "0")
         config.set('LEADERBOARD', "hs_tetris_extreme", "0")
         config.set('LEADERBOARD', "hs_2048_easy", "0")
         config.set('LEADERBOARD', "hs_2048_normal", "0")
         config.set('LEADERBOARD', "hs_2048_hard", "0")
         config.set('LEADERBOARD', "hs_2048_extreme", "0")
         with open('config.ini', 'w') as f:
            config.write(f)

      # Clears the user interactions
      stddraw.clearKeysTyped()

      # Clears the canvas with background color
      stddraw.clear(background_color)

      # Draw the scores hover button
      stddraw.picture(scores, scores_x, scores_y)

      # Draws header
      stddraw.setFontSize(42)
      stddraw.boldText(CENTER_X, CENTER_Y+8.5, "High Scores")

      # Draws the scoreboard itself
      stddraw.setFontSize(36)
      stddraw.boldText(CENTER_X, CENTER_Y+6, "Classic Tetris")
      stddraw.boldText(CENTER_X, CENTER_Y-1.25, "Tetris 2048")
      stddraw.setFontSize(24)
      stddraw.text(CENTER_X-4, CENTER_Y+4.25, "Easy")
      stddraw.boldText(CENTER_X-4, CENTER_Y+3.25, str(hs_tetris_easy))
      stddraw.text(CENTER_X+4, CENTER_Y+4.25, "Normal")
      stddraw.boldText(CENTER_X+4, CENTER_Y+3.25, str(hs_tetris_normal))
      stddraw.text(CENTER_X-4, CENTER_Y+2, "Hard")
      stddraw.boldText(CENTER_X-4, CENTER_Y+1, str(hs_tetris_hard))
      stddraw.text(CENTER_X+4, CENTER_Y+2, "Extreme")
      stddraw.boldText(CENTER_X+4, CENTER_Y+1, str(hs_tetris_extreme))
      stddraw.text(CENTER_X-4, CENTER_Y-3, "Easy")
      stddraw.boldText(CENTER_X-4, CENTER_Y-4, str(hs_2048_easy))
      stddraw.text(CENTER_X+4, CENTER_Y-3, "Normal")
      stddraw.boldText(CENTER_X+4, CENTER_Y-4, str(hs_2048_normal))
      stddraw.text(CENTER_X-4, CENTER_Y-5.25, "Hard")
      stddraw.boldText(CENTER_X-4, CENTER_Y-6.25, str(hs_2048_hard))
      stddraw.text(CENTER_X+4, CENTER_Y-5.25, "Extreme")
      stddraw.boldText(CENTER_X+4, CENTER_Y-6.25, str(hs_2048_extreme))
      stddraw.setFontSize(20)
      stddraw.text(CENTER_X, CENTER_Y-9, "Press Backspace to reset high scores.")

      # Shows the canvas
      stddraw.show(0)


# CAN CONNECT
# ------------------------------
# Returns whether the program can open a URL, which means being connected to the internet.

def can_connect():
   # Tries to open the URL in 5 seconds, if it can, returns true
    try:
        urllib.request.urlopen('https://mrpanda.dev', timeout=5)
        return True
   # Else, returns false
    except:
        return False


# CONNECT PRESENCE
# ------------------------------
# Connects to the Discord Rich Presence server if the program is connected to the internet, and Discord client is open,
# but not connected to the server already.

def connect_presence():
   # Gets the global
   global is_connected

   # If connected to the internet and not connected to the server, tries to connect
   if can_connect():
      if not is_connected:
         try:
            RPC.connect()
            is_connected = True
         except:
            is_connected = False
   else:
      is_connected = False


# UPDATE PRESENCE
# ------------------------------
# Updates the Rich Presence with the given state, detail, image, and a start time after some time. It also accepts custom delay,
# but default is 10 seconds.

def update_presence(state=None, details=None, large_image=None, start=None, delay=10):
   # Gets the global
   global timer

   # If timer is initiated already, stops the timer
   if timer is not None and timer.is_alive():
      timer.cancel()

   # Initializes a new timer with the given arguments and starts it
   timer = Timer(delay, update_thread, args=[state, details, large_image, start])
   timer.start()


# UPDATE THREAD
# ------------------------------
# It is the main Rich Presence updating method. It updates the Rich Presence if the program connected to Discord.

def update_thread(state=None, details=None, large_image=None, start=None):
   # Gets the global
   global is_connected

   # Tries to update Rich Presence if connected to the server
   if is_connected:
      try:
         RPC.update(state=state, details=details, large_image=large_image, start=start)
      except:
         is_connected = False




# Calls the main method after defining all methods
if __name__== '__main__':
   start()
