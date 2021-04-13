import platform

if platform.system() != 'Windows':
    print("\nThis program is designed to work only on Windows systems.")
    input("Press \"Enter\" key to terminate the program.")
    print()
    exit()

import os
import pkg_resources
import subprocess
import time
import sys

# Required dependicies list
dependencies = ['Pygame', 'NumPy', 'AudioPlayer']

# Gets installed modules
packages = pkg_resources.working_set
package_list = sorted([i.key for i in packages])

# Adds missing dependencies to a list
not_installed = []

for i in dependencies:
   if i.casefold() not in package_list:
      not_installed.append(i)

# If there are some missing modules, prompt user.
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

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(DIR + "/modules")

import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
import stddraw # the stddraw module is used as a basic graphics library
import random # used for creating tetrominoes with random types/shapes
from game_grid import GameGrid # class for modeling the game grid
from tetromino import Tetromino # class for modeling the tetrominoes
from picture import Picture # used representing images to display
from color import Color # used for coloring the game menu
import base64
from data import DATAS
from audioplayer import AudioPlayer
from configparser import ConfigParser
import tempfile

config = ConfigParser()
config.read("config.ini")

if not config.has_section("GAME"):
   config.add_section("GAME")
   config.set('GAME', "difficulty", "1")
else:
   if not config.has_option("GAME", "difficulty"):
      config.set('GAME', "difficulty", "1")

if not config.has_section("SOUND"):
   config.add_section("SOUND")
   config.set('SOUND', "music_volume", "5")
   config.set('SOUND', "effects_volume", "25")
else:
   if not config.has_option("SOUND", "music_volume"):
      config.set('SOUND', "music_volume", "5")
   if not config.has_option("SOUND", "effects_volume"):
      config.set('SOUND', "effects_volume", "25")

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

for i in config.sections():
   if i == 'SOUND' or i == 'GAME' or i == 'LEADERBOARD':
      for j in config.options(i):
         if (i == 'SOUND' and j != "music_volume" and j != "effects_volume") or (i == 'GAME' and j != "difficulty") or (i == 'LEADERBOARD' and j != "hs_tetris_easy" and j != "hs_tetris_normal" and j != "hs_tetris_hard" and j != "hs_tetris_extreme" and j != "hs_2048_easy" and j != "hs_2048_normal" and j != "hs_2048_hard" and j != "hs_2048_extreme"):
            config.remove_option(i, j)
   else:
      config.remove_section(i)

try:
   if int(config.get("GAME", "difficulty")) < 0 or int(config.get("GAME", "difficulty")) > 3:
      config.set('GAME', "difficulty", "1")
except ValueError:
   config.set('GAME', "difficulty", "1")

try:
   if int(config.get("SOUND", "music_volume")) < 0 or int(config.get("SOUND", "music_volume")) > 100:
      config.set('SOUND', "music_volume", "5")
except ValueError:
   config.set('SOUND', "music_volume", "5")

try:
   if int(config.get("SOUND", "effects_volume")) < 0 or int(config.get("SOUND", "effects_volume")) > 100:
      config.set('SOUND', "effects_volume", "25")
except ValueError:
   config.set('SOUND', "effects_volume", "25")

try:
   if int(config.get("LEADERBOARD", "hs_tetris_easy")) < 0:
      config.set('LEADERBOARD', "hs_tetris_easy", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_tetris_easy", "0")

try:
   if int(config.get("LEADERBOARD", "hs_tetris_normal")) < 0:
      config.set('LEADERBOARD', "hs_tetris_normal", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_tetris_normal", "0")

try:
   if int(config.get("LEADERBOARD", "hs_tetris_hard")) < 0:
      config.set('LEADERBOARD', "hs_tetris_hard", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_tetris_hard", "0")

try:
   if int(config.get("LEADERBOARD", "hs_tetris_extreme")) < 0:
      config.set('LEADERBOARD', "hs_tetris_extreme", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_tetris_extreme", "0")

try:
   if int(config.get("LEADERBOARD", "hs_2048_easy")) < 0:
      config.set('LEADERBOARD', "hs_2048_easy", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_2048_easy", "0")

try:
   if int(config.get("LEADERBOARD", "hs_2048_normal")) < 0:
      config.set('LEADERBOARD', "hs_2048_normal", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_2048_normal", "0")

try:
   if int(config.get("LEADERBOARD", "hs_2048_hard")) < 0:
      config.set('LEADERBOARD', "hs_2048_hard", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_2048_hard", "0")

try:
   if int(config.get("LEADERBOARD", "hs_2048_extreme")) < 0:
      config.set('LEADERBOARD', "hs_2048_extreme", "0")
except ValueError:
   config.set('LEADERBOARD', "hs_2048_extreme", "0")

with open('config.ini', 'w') as f:
   config.write(f)

ICON = DIR + "/images/icon.png"
PLAYER_DIR = DIR + "/sounds/back.mp3"
MOVE_DIR = DIR + "/sounds/move.wav"
ROTATE_DIR = DIR + "/sounds/rotate.wav"
PLACE_DIR = DIR + "/sounds/place.wav"
CLEAR_DIR = DIR + "/sounds/clear.wav"
MENU_DIR = DIR + "/sounds/menu.wav"
MERGE_DIR = DIR + "/sounds/merge.wav"
GRID_H = 20
GRID_W = 12
CANVAS_H = 35 * GRID_H + 1
CANVAS_W = 35 * GRID_W + 140
WINDOW_TITLE = "Tetris 2048"
TEMP_FILE = tempfile.gettempdir()
TEMP_IMAGE = TEMP_FILE + "/canvas.png"
TEMP_INFO = TEMP_FILE + "/image.png"

player = AudioPlayer(PLAYER_DIR)
move = AudioPlayer(MOVE_DIR)
rotate = AudioPlayer(ROTATE_DIR)
place = AudioPlayer(PLACE_DIR)
clear = AudioPlayer(CLEAR_DIR)
menu = AudioPlayer(MENU_DIR)
merge = AudioPlayer(MERGE_DIR)

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

# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution
def start():
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

   stddraw.setCanvasSize(CANVAS_W, CANVAS_H) 
   stddraw.setXscale(-1, GRID_W + 4) # 17
   stddraw.setYscale(-1, GRID_H) # 21
   stddraw.setWindowTitle(WINDOW_TITLE)
   stddraw.setWindowIcon(ICON)
   stddraw.setCloseAction(close)

   player.volume = music_volume
   move.volume = effects_volume
   rotate.volume = effects_volume
   place.volume = effects_volume
   clear.volume = effects_volume
   menu.volume = effects_volume
   merge.volume = effects_volume

   player.play(loop=True)

   restart = False
   while True:
      if restart == False:
         # display a simple menu before opening the game
         gamemode = display_game_menu()
      restart = game()
   
def game():
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

   stddraw.setKeyRepeat(1)
   stddraw.clearKeysTyped()
   stddraw.clearMousePresses()
   stddraw.setSaveKey("y")

   ms = (350 if difficulty == 0 else (250 if difficulty == 1 else (125 if difficulty == 2 else 75)))

   # create the game grid
   grid = GameGrid(GRID_H, GRID_W, gamemode, difficulty)
   # create the first tetromino to enter the game grid 
   # by using the create_tetromino function defined below
   tetrominos = [create_tetromino(GRID_H, GRID_W), create_tetromino(GRID_H, GRID_W), create_tetromino(GRID_H, GRID_W), create_tetromino(GRID_H, GRID_W)]
   current_tetromino = tetrominos.pop(0)
   grid.current_tetromino = current_tetromino
   grid.next_tetromino1 = tetrominos[0]
   grid.next_tetromino2 = tetrominos[1]
   grid.next_tetromino3 = tetrominos[2]
   if gamemode == "tetris":
      grid.old_high_score = (hs_tetris_easy if difficulty == 0 else (hs_tetris_normal if difficulty == 1 else (hs_tetris_hard if difficulty == 2 else hs_tetris_extreme)))
   else:
      grid.old_high_score = (hs_2048_easy if difficulty == 0 else (hs_2048_normal if difficulty == 1 else (hs_2048_hard if difficulty == 2 else hs_2048_extreme)))
   
   last_mouse_posX = -1
   last_mouse_posY = -1
   mouse = None
   rotated = False
   already_dropped = False

   # main game loop (keyboard interaction for moving the tetromino) 
   while True:
      posX = round(stddraw.mouseMotionX())
      posY = round(stddraw.mouseMotionY())
      keys_typed = stddraw.getKeysTyped()
      dropped = False

      if ((posX != last_mouse_posX) or (posY != last_mouse_posY) or stddraw.mouseLeftHeldDown() or stddraw.mouseRightHeldDown() or stddraw.mouseScrollHeldDown()) and grid.is_inside(posY, posX):
         mouse = True
         last_mouse_posX = posX
         last_mouse_posY = posY
      elif stddraw.hasNextKeyTyped():
         if "up" in keys_typed or "down" in keys_typed or "right" in keys_typed or "left" in keys_typed or "space" in keys_typed or "escape" in keys_typed or "w" in keys_typed or "a" in keys_typed or "s" in keys_typed or "d" in keys_typed:
            mouse = False

      if not mouse:
         # check user interactions via the keyboard
         if "space" in keys_typed:
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
               grid.score += count * 2
         if "up" in keys_typed or "w" in keys_typed:
            if not rotated:
               can_rotate = current_tetromino.rotate(grid)
               if can_rotate:
                  rotate.play()
                  rotated = True
         # if the left arrow key has been pressed
         if "left" in keys_typed or "a" in keys_typed:
            # move the tetromino left by one
            can_left = current_tetromino.move("left", grid, 1, delay=150)
            if can_left:
               move.play()
         # if the right arrow key has been pressed
         if "right" in keys_typed or "d" in keys_typed:
            # move the tetromino right by one
            can_right = current_tetromino.move("right", grid, 1, delay=150)
            if can_right:
               move.play()
         # if the down arrow key has been pressed
         if "down" in keys_typed or "s" in keys_typed:
            # move the tetromino down by one 
            # (causes the tetromino to fall down faster)
            succ = current_tetromino.move("down", grid, 1, delay=50)
            if succ:
               grid.score += 1
         if "escape" in keys_typed:
            option = display_pause_menu()

            if option == "menu":
               return False
            elif option == "restart":
               return True
         # clear the queue that stores all the keys pressed/typed

         if stddraw.hasNextKeyReleased():
            keys_released = stddraw.getKeysReleased()
            if "up" in keys_released or "w" in keys_released:
               rotated = False
            if "space" in keys_released:
               already_dropped = False
      else:         
         middle = (0 if current_tetromino.column_count == 1 or current_tetromino.column_count == 2 else 1)
         if (posX + middle) > grid.grid_width:
            posX = grid.grid_width - middle
         
         diff = posX - (current_tetromino.leftmost + middle)

         if diff < 0:
            for i in range(-diff):
               success_move = current_tetromino.move("left", grid, 1)
               if not success_move:
                  break
               else:
                  if not rotated:
                     move.play()
         else:
            for i in range(diff):
               success_move = current_tetromino.move("right", grid, 1)
               if not success_move:
                  break
               else:
                  if not rotated:
                     move.play()
         
         rotated = False

         if stddraw.mouseRightPressed():
            if grid.is_inside(round(stddraw.mouseRightY()), round(stddraw.mouseRightX())):
               success_rotate = current_tetromino.rotate(grid)
               if success_rotate:
                  rotate.play()
                  rotated = True
         if stddraw.mouseLeftPressed():
            if grid.is_inside(round(stddraw.mouseLeftY()), round(stddraw.mouseLeftX())):
               count = 0
               while True:
                  sc = current_tetromino.move("down", grid, 1)
                  if not sc:
                     break
                  else:
                     count += 1
               dropped = True
               grid.score += count * 2
         if stddraw.mouseScrollHeldDown():
            if grid.is_inside(round(stddraw.mouseScrollY()), round(stddraw.mouseScrollX())):
               succ = current_tetromino.move("down", grid, 1, delay=50)
               if succ:
                  grid.score += 1

      stddraw.clearMousePresses()
      stddraw.clearKeysTyped()
      stddraw.clearKeysReleased()
      
      if difficulty != 3:
         current_ghost = current_tetromino.copy(ghost=True)
         grid.current_ghost = current_ghost
         
         while True:
            sc = current_ghost.move("down", grid, 1)
            if not sc:
               break
         
      # move (drop) the tetromino down by 1 at each iteration 
      success = current_tetromino.move("down", grid, 1, delay=ms, standart=True)

      # place the tetromino on the game grid when it cannot go down anymore
      if success == False or dropped:
         place.play()
         # get the tile matrix of the tetromino
         tiles_to_place = current_tetromino.tile_matrix
         # update the game grid by adding the tiles of the tetromino
         grid.current_ghost = None
         grid.update_grid(tiles_to_place)
         # end the main game loop if the game is over

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
         
         if gamemode == "2048":
            while True:
               grid.check_line_chain_merge(merge)
               score_before_line_delete = grid.score
               grid.delete_full_lines(clear)
               if score_before_line_delete == grid.score:
                  break
         else:
            grid.delete_full_lines(clear)

         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         tetromino = create_tetromino(GRID_H, GRID_W)
         tetrominos.append(tetromino)
         current_tetromino = tetrominos.pop(0)
         grid.next_tetromino1 = tetrominos[0]
         grid.next_tetromino2 = tetrominos[1]
         grid.next_tetromino3 = tetrominos[2]
         grid.current_tetromino = current_tetromino

      # display the game grid and as well the current tetromino
      grid.display()
   
   stddraw.setKeyRepeat()

   while True:
      keys_typed = stddraw.getKeysTyped()
      if "enter" in keys_typed or "return" in keys_typed:
         stddraw.clearKeysTyped()
         return False
      elif "r" in keys_typed:
         stddraw.clearKeysTyped()
         return True
      stddraw.clearKeysTyped()
      stddraw.show(0)

def close():
   global config
   global player
   global move
   global rotate
   global place
   global clear
   global menu
   global merge

   with open('config.ini', 'w') as f:
      config.write(f)

   if os.path.exists(TEMP_IMAGE):
      os.remove(TEMP_IMAGE)
   if os.path.exists(TEMP_INFO):
      os.remove(TEMP_INFO)

   player.close()
   move.close()
   rotate.close()
   place.close()
   clear.close()
   menu.close()
   merge.close()

   ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
   sys.exit()

# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
   global gamemode

   # type (shape) of the tetromino is determined randomly
   tetromino_types = [ 'I', 'O', 'Z', 'S', 'L', 'J', 'T' ]
   #tetromino_types = [ 'Z' ]
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   n = (4 if random_type == 'I' else (2 if random_type == 'O' else 3))
   bottom_x = random.randint(0, grid_width - n)

   # create and return the tetromino
   tetromino = Tetromino(random_type, grid_height, grid_width, bottom_x, gamemode=gamemode)
   return tetromino

# Function for displaying a simple menu before starting the game
def display_game_menu():
   global config
   global difficulty
   global music_volume
   global effects_volume

   stddraw.clearKeysTyped()
   stddraw.clearMousePresses()
   stddraw.setKeyRepeat()
   stddraw.setSaveKey()

   # colors used for the menu
   background_color = Color(25, 49, 90)
   button_color = Color(132, 132, 132)
   text_color = Color(31, 160, 239)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # path of the image file
   img_file = DIR + "/images/menu_image.png"
   image_to_display = Picture(img_file)
   img_file = DIR + "/images/tetris.png"
   tetris= Picture(img_file)
   img_file = DIR + "/images/tetris2.png"
   tetris2= Picture(img_file)
   img_file = DIR + "/images/2048.png"
   i2048 = Picture(img_file)
   img_file = DIR + "/images/2048L.png"
   i2048L = Picture(img_file)
   img_file = DIR + "/images/musicOn.png"
   musicOn = Picture(img_file)
   img_file = DIR + "/images/musicOff.png"
   musicOff = Picture(img_file)
   img_file = DIR + "/images/soundOff.png"
   soundOff = Picture(img_file)
   img_file = DIR + "/images/soundOn.png"
   soundOn = Picture(img_file)
   img_file = DIR + "/images/easy.png"
   easy = Picture(img_file)
   img_file = DIR + "/images/normal.png"
   normal = Picture(img_file)
   img_file = DIR + "/images/hard.png"
   hard = Picture(img_file)
   img_file = DIR + "/images/extreme.png"
   extreme = Picture(img_file)
   img_file = DIR + "/images/help.png"
   help = Picture(img_file)
   img_file = DIR + "/images/scores.png"
   scores = Picture(img_file)

   # center coordinates to display the image
   img_center_x, img_center_y = (17/2)-1,(21/2)-1
   # image is represented using the Picture class
   # display the image
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(20)
   # dimensions of the start game button
   # dimensions of the start game button
   button_w, button_h = GRID_W, 2.30
   slider_w, slider_h = GRID_W, 0.2
   # coordinates of the bottom left corner of the start game button 
   button_blc_x, button_blc_y = img_center_x-button_w/2, 3.875 # Tetris Button 
   button3_blc_x, button3_blc_y = img_center_x-button_w/2, 0.875 # Tetris 2048 Button
   help_x, help_y = img_center_x + 7.75, img_center_y + 9.75
   scores_x, scores_y = img_center_x - 7.75, img_center_y + 9.75

   slider_start = img_center_x-button_w/2
   slider_end = slider_start+slider_w

   slider1location = slider_start + (0 if music_volume == 0 else (slider_w/(100/music_volume)))
   slider2location = slider_start + (0 if effects_volume == 0 else (slider_w/(100/effects_volume)))
   slider3location = slider_start + ((slider_w / 3) * difficulty)

   musicHold = False
   soundHold = False
   diffHold = False
   played = False
   string = ""
   # menu interaction loop
   while True:
      if stddraw.hasNextKeyTyped():
         string += stddraw.nextKeyTyped()
      if get_data(1) in string:
         display_info()
         string = ""
      
      speedButtonPicture = normal
      soundButtonPicture = soundOn
      musicButtonPicture = musicOn
      tetrisButtonPicture = tetris
      i2048Picture = i2048

      mouse_x = stddraw.mouseMotionX() if stddraw.mouseMotionX() is not None else -1
      mouse_y = stddraw.mouseMotionY() if stddraw.mouseMotionY() is not None else -1
      
      
      if stddraw.mouseLeftHeldDown():
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
         else:
            if mouse_y >= 10.52 and mouse_y < 10.54 + slider_h and mouse_x >= slider_start and mouse_x <= slider_end:
               musicHold = True
            elif mouse_y >= 9.02 and mouse_y < 9.04 + slider_h and mouse_x >= slider_start and mouse_x <= slider_end:
               soundHold = True
            elif mouse_y >= 7.52 and mouse_y < 7.54 + slider_h and mouse_x >= slider_start and mouse_x <= slider_end:
               diffHold = True
      else:
         musicHold = False
         soundHold = False
         diffHold = False

      diffStr = "Easy" if difficulty == 0 else ("Normal" if difficulty == 1 else ("Hard" if difficulty == 2 else "Extreme"))
      speedButtonPicture = easy if difficulty == 0 else (normal if difficulty == 1 else (hard if difficulty == 2 else extreme))

      # MOUSE CLICKS ON BUTTONS
      if stddraw.mouseLeftPressed():
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               with open('config.ini', 'w') as f:
                  config.write(f)
               return "tetris"
         if mouse_x >= button3_blc_x and mouse_x <= button3_blc_x + button_w:
            if mouse_y >= button3_blc_y and mouse_y <= button3_blc_y + button_h:
               with open('config.ini', 'w') as f:
                  config.write(f)
               return "2048"   
      
      # MOUSE LISTENERS ON BUTTONS
      if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w and mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
         tetrisButtonPicture = tetris2
         if not played:
            menu.play()
            played = True
      elif mouse_x >= button3_blc_x and mouse_x <= button3_blc_x + button_w and mouse_y >= button3_blc_y and mouse_y <= button3_blc_y + button_h:
         i2048Picture = i2048L
         if not played:
            menu.play()
            played = True
      elif mouse_x >= help_x - 0.5 and mouse_x <= help_x + 0.5 and mouse_y >= help_y - 0.5 and mouse_y <= help_y + 0.5:
         if not played:
            menu.play()
            played = True
         display_controls(background_color)
         string = ""
      elif mouse_x >= scores_x - 0.5 and mouse_x <= scores_x + 0.5 and mouse_y >= scores_y - 0.5 and mouse_y <= scores_y + 0.5:
         if not played:
            menu.play()
            played = True
         display_scores()
         string = ""
      else:
         played = False

      if music_volume == 0:
         musicButtonPicture=musicOff
      if effects_volume == 0:
         soundButtonPicture=soundOff

      # MUSIC SLIDER
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,10.5,slider_w,slider_h)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.filledCircle(slider1location,10.5+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.boldText(slider1location-0.03,10,str(music_volume))
      stddraw.picture(musicButtonPicture,slider1location-0.03,10.5+(slider_h/2))

      # SOUND SLIDER
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,9,slider_w,slider_h)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.filledCircle(slider2location,9+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.boldText(slider2location-0.03,8.5,str(effects_volume))
      stddraw.picture(soundButtonPicture,slider2location-0.01,9+(slider_h/2))

      # DIFFICULTY SLIDER
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,7.5,slider_w,slider_h)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.filledCircle(slider3location,7.5+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.boldText(slider3location-0.03,7,diffStr)
      gap = -0.025 if difficulty == 3 or difficulty == 1 else(0.025 if difficulty == 0 else 0) 
      stddraw.picture(speedButtonPicture,slider3location+gap,7.5+(slider_h/2)+0.02)

      # Draw Buttons and Logo
      stddraw.picture(image_to_display, img_center_x, img_center_y+6)
      stddraw.picture(tetrisButtonPicture,img_center_x,5)
      stddraw.picture(i2048Picture,img_center_x,2)

      stddraw.picture(help, help_x, help_y)
      stddraw.picture(scores, scores_x, scores_y)

      stddraw.show(0)
      stddraw.clear(background_color)

def get_data(number):
	return bytes.fromhex(base64.decodebytes(DATAS[number]).decode()).decode() if number != 0 else base64.decodebytes(DATAS[0])

def display_controls(background_color):
   img_file = DIR + "/images/help.png"
   help = Picture(img_file)
   img_file = DIR + "/images/controls.png"
   controls = Picture(img_file)
   img_center_x, img_center_y = (17/2)-1,(21/2)-1
   help_x, help_y = img_center_x + 7.75, img_center_y + 9.75

   while True:
      mouse_x = stddraw.mouseMotionX()
      mouse_y = stddraw.mouseMotionY()

      if not (mouse_x >= help_x - 0.5 and mouse_x <= help_x + 0.5 and mouse_y >= help_y - 0.5 and mouse_y <= help_y + 0.5):
         stddraw.clearKeysTyped()
         stddraw.clearMousePresses()
         break

      stddraw.clear(background_color)
      stddraw.picture(controls, img_center_x, img_center_y)
      stddraw.picture(help, help_x, help_y)
      stddraw.show(0)

def display_pause_menu():
   global config
   global music_volume
   global effects_volume

   stddraw.clearMousePresses()
   stddraw.setKeyRepeat()
   stddraw.clearKeysTyped()
   stddraw.save(TEMP_IMAGE)

   # colors used for the menu
   background_color = stddraw.BLACK
   button_color = Color(132, 132, 132)
   text_color = stddraw.LIGHT_GRAY
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # path of the image file
   img_file = DIR + "/images/musicOn.png"
   musicOn = Picture(img_file)
   img_file = DIR + "/images/musicOff.png"
   musicOff = Picture(img_file)
   img_file = DIR + "/images/soundOff.png"
   soundOff = Picture(img_file)
   img_file = DIR + "/images/soundOn.png"
   soundOn = Picture(img_file)
   img_file = DIR + "/images/pause_blur.png"
   blur = Picture(img_file)
   canvas = Picture(TEMP_IMAGE)
   img_file = DIR + "/images/help.png"
   help = Picture(img_file)

   # center coordinates to display the image
   img_center_x, img_center_y = (17/2)-1,(21/2)-1
   # image is represented using the Picture class
   # display the image

   help_x, help_y = img_center_x + 7.75, img_center_y + 9.75

   stddraw.setFontFamily("Arial")

   # dimensions of the slider
   slider_w, slider_h = GRID_W, 0.2

   slider_start = img_center_x-GRID_W/2
   slider_end = slider_start+slider_w

   slider1location = slider_start + (0 if music_volume == 0 else (slider_w/(100/music_volume)))
   slider2location = slider_start + (0 if effects_volume == 0 else (slider_w/(100/effects_volume)))

   musicHold = False
   soundHold = False

   first = True
   played = False
   # menu interaction loop
   while True:
      keys_typed = stddraw.getKeysTyped()
      if "escape" in keys_typed:
         if os.path.exists(TEMP_IMAGE):
            os.remove(TEMP_IMAGE)
         stddraw.setKeyRepeat(1)
         stddraw.clearKeysTyped()
         stddraw.clearMousePresses()
         with open('config.ini', 'w') as f:
            config.write(f)
         break
      elif "enter" in keys_typed or "return" in keys_typed:
         if os.path.exists(TEMP_IMAGE):
            os.remove(TEMP_IMAGE)
         stddraw.setKeyRepeat(1)
         stddraw.clearKeysTyped()
         stddraw.clearMousePresses()
         with open('config.ini', 'w') as f:
            config.write(f)
         return "menu"
      elif "r" in keys_typed:
         if os.path.exists(TEMP_IMAGE):
            os.remove(TEMP_IMAGE)
         stddraw.setKeyRepeat(1)
         stddraw.clearKeysTyped()
         stddraw.clearMousePresses()
         with open('config.ini', 'w') as f:
            config.write(f)
         return "restart"
      stddraw.clearKeysTyped()

      soundButtonPicture = soundOn
      musicButtonPicture = musicOn

      mouse_x = stddraw.mouseMotionX() if stddraw.mouseMotionX() is not None else -1
      mouse_y = stddraw.mouseMotionY() if stddraw.mouseMotionY() is not None else -1
      
      if stddraw.mouseLeftHeldDown():
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
         else:
            if mouse_y >= 4.52 and mouse_y < 4.54 + slider_h and mouse_x >= slider_start and mouse_x <= slider_end:
               musicHold = True
            elif mouse_y >= 3.02 and mouse_y < 3.04 + slider_h and mouse_x >= slider_start and mouse_x <= slider_end:
               soundHold = True
      else:
         musicHold = False
         soundHold = False

      if mouse_x >= help_x - 0.5 and mouse_x <= help_x + 0.5 and mouse_y >= help_y - 0.5 and mouse_y <= help_y + 0.5:
         if not played:
            menu.play()
            played = True
         display_controls(background_color)
      else:
         played = False

      if music_volume == 0:
         musicButtonPicture=musicOff
      if effects_volume == 0:
         soundButtonPicture=soundOff

      stddraw.picture(canvas,img_center_x,img_center_y)
      stddraw.picture(blur,img_center_x,img_center_y)

      stddraw.setFontSize(72)
      stddraw.boldText(img_center_x, img_center_y+3, "Game Paused")

      stddraw.setFontSize(24)
      stddraw.text(img_center_x, img_center_y, "Press Esc to resume the game,")
      stddraw.text(img_center_x, img_center_y-0.8, "press R to restart the game,")
      stddraw.text(img_center_x, img_center_y-1.6, "or press Enter to return to the main menu.")

      stddraw.setFontSize(20)
      # MUSIC SLIDER
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,4.5,slider_w,slider_h)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.filledCircle(slider1location,4.5+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.boldText(slider1location-0.03,4,str(music_volume))
      stddraw.picture(musicButtonPicture,slider1location-0.03,4.5+(slider_h/2))

      # SOUND SLIDER
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,3,slider_w,slider_h)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.filledCircle(slider2location,3+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.boldText(slider2location-0.03,2.5,str(effects_volume))
      stddraw.picture(soundButtonPicture,slider2location-0.01,3+(slider_h/2))

      stddraw.picture(help, help_x, help_y)

      # Draw Buttons and Logo
      stddraw.show(0)
      if first:
         stddraw.clearKeysTyped()
         first = False
      stddraw.clear(background_color)

def display_info():
   stddraw.clearMousePresses()
   stddraw.setKeyRepeat()
   stddraw.clearKeysTyped()
   stddraw.setSaveKey()
   stddraw.setWindowTitle(get_data(2))

   img_center_x, img_center_y = (17/2)-1,(21/2)-1

   with open(TEMP_INFO, "wb") as fh:
	   fh.write(get_data(0))

   pic = Picture(TEMP_INFO)
   stddraw.setPenColor(stddraw.BLACK)
   while True:
      keys_typed = stddraw.getKeysTyped()
      if "escape" in keys_typed:
         if os.path.exists(TEMP_INFO):
            os.remove(TEMP_INFO)
         stddraw.clearKeysTyped()
         stddraw.clearMousePresses()
         stddraw.setWindowTitle(WINDOW_TITLE)
         break
      stddraw.setFontSize(52)
      stddraw.boldText(img_center_x, img_center_y+9, get_data(2))
      stddraw.picture(pic, img_center_x, img_center_y+2.5)
      stddraw.square(img_center_x, img_center_y+2.5, 5)
      stddraw.setFontSize(32)
      stddraw.boldText(img_center_x, img_center_y-3.75, get_data(3))
      stddraw.setFontSize(24)
      stddraw.boldText(img_center_x/2,img_center_y-5.25, get_data(4))
      stddraw.boldText(img_center_x+(img_center_x/2),img_center_y-5.25, get_data(8))
      stddraw.setFontSize(24)
      stddraw.text(img_center_x/2, img_center_y-6.25, get_data(5))
      stddraw.text(img_center_x/2, img_center_y-7.25, get_data(6))
      stddraw.text(img_center_x/2, img_center_y-8.25, get_data(7))
      stddraw.text(img_center_x+(img_center_x/2), img_center_y-6.25, get_data(9))
      stddraw.text(img_center_x+(img_center_x/2), img_center_y-7.25, get_data(10))
      stddraw.text(img_center_x+(img_center_x/2), img_center_y-8.25, get_data(11))
      stddraw.setFontSize(16)
      stddraw.text(img_center_x, img_center_y-9.75, get_data(12))
      stddraw.show(0)
      stddraw.clear()

def set_music_volume(volume):
   global config
   global music_volume
   global player
   music_volume = volume
   player.volume = volume
   config.set("SOUND", "music_volume", str(volume))

def set_effects_volume(volume):
   global config
   global effects_volume
   global move
   global rotate
   global place
   global clear
   global menu
   global merge
   effects_volume = volume
   move.volume = volume
   rotate.volume = volume
   place.volume = volume
   clear.volume = volume
   menu.volume = volume
   merge.volume = volume
   config.set("SOUND", "effects_volume", str(volume))

def set_difficulty(index):
   global config
   global difficulty
   difficulty = index
   config.set("GAME", "difficulty", str(index))

def display_scores():
   global config
   global hs_tetris_easy
   global hs_tetris_normal
   global hs_tetris_hard
   global hs_tetris_extreme
   global hs_2048_easy
   global hs_2048_normal
   global hs_2048_hard
   global hs_2048_extreme

   img_file = DIR + "/images/scores.png"
   scores = Picture(img_file)
   img_center_x, img_center_y = (17/2)-1,(21/2)-1
   scores_x, scores_y = img_center_x - 7.75, img_center_y + 9.75
   background_color = Color(25, 49, 90)
   stddraw.setFontFamily("Arial")
   stddraw.setPenColor(stddraw.WHITE)
   while True:
      mouse_x = stddraw.mouseMotionX()
      mouse_y = stddraw.mouseMotionY()

      if not (mouse_x >= scores_x - 0.5 and mouse_x <= scores_x + 0.5 and mouse_y >= scores_y - 0.5 and mouse_y <= scores_y + 0.5):
         stddraw.clearKeysTyped()
         stddraw.clearMousePresses()
         stddraw.setFontSize(20)
         break

      keys_typed = stddraw.getKeysTyped()
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

      stddraw.clearKeysTyped()
      stddraw.clear(background_color)
      stddraw.picture(scores, scores_x, scores_y)
      stddraw.setFontSize(42)
      stddraw.boldText(img_center_x, img_center_y+8.5, "High Scores")
      stddraw.setFontSize(36)
      stddraw.boldText(img_center_x, img_center_y+6, "Classic Tetris")
      stddraw.boldText(img_center_x, img_center_y-1.25, "Tetris 2048")
      stddraw.setFontSize(24)
      stddraw.text(img_center_x-4, img_center_y+4.25, "Easy")
      stddraw.boldText(img_center_x-4, img_center_y+3.25, str(hs_tetris_easy))
      stddraw.text(img_center_x+4, img_center_y+4.25, "Normal")
      stddraw.boldText(img_center_x+4, img_center_y+3.25, str(hs_tetris_normal))
      stddraw.text(img_center_x-4, img_center_y+2, "Hard")
      stddraw.boldText(img_center_x-4, img_center_y+1, str(hs_tetris_hard))
      stddraw.text(img_center_x+4, img_center_y+2, "Extreme")
      stddraw.boldText(img_center_x+4, img_center_y+1, str(hs_tetris_extreme))

      stddraw.text(img_center_x-4, img_center_y-3, "Easy")
      stddraw.boldText(img_center_x-4, img_center_y-4, str(hs_2048_easy))
      stddraw.text(img_center_x+4, img_center_y-3, "Normal")
      stddraw.boldText(img_center_x+4, img_center_y-4, str(hs_2048_normal))
      stddraw.text(img_center_x-4, img_center_y-5.25, "Hard")
      stddraw.boldText(img_center_x-4, img_center_y-6.25, str(hs_2048_hard))
      stddraw.text(img_center_x+4, img_center_y-5.25, "Extreme")
      stddraw.boldText(img_center_x+4, img_center_y-6.25, str(hs_2048_extreme))
      stddraw.setFontSize(20)
      stddraw.text(img_center_x, img_center_y-9, "Press Backspace to reset high scores.")

      stddraw.show(0)

# start() function is specified as the entry point (main function) from which 
# the program starts execution
if __name__== '__main__':
   start()
