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
import tempfile

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
WINDOW_TITLE = "OUR PROJECT"
INITIAL_MUSIC_VOLUME = 5
INITIAL_EFFECT_VOLUME = 25
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

slider1location = None
slider2location = None
slider3location = None

difficulty = 1
gamemode = None

# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution
def start():
   global gamemode
   global merge
   global player
   global move
   global rotate
   global place
   global clear
   global menu

   stddraw.setCanvasSize(CANVAS_W, CANVAS_H) 
   stddraw.setXscale(-1, GRID_W + 4) # 17
   stddraw.setYscale(-1, GRID_H) # 21
   stddraw.setWindowTitle(WINDOW_TITLE)
   stddraw.setWindowIcon(ICON)
   stddraw.setCloseAction(close)

   player.volume = INITIAL_MUSIC_VOLUME
   move.volume = INITIAL_EFFECT_VOLUME
   rotate.volume = INITIAL_EFFECT_VOLUME
   place.volume = INITIAL_EFFECT_VOLUME
   clear.volume = INITIAL_EFFECT_VOLUME
   menu.volume = INITIAL_EFFECT_VOLUME
   merge.volume = INITIAL_EFFECT_VOLUME

   player.play(loop=True)

   restart = False
   while True:
      if restart == False:
         # display a simple menu before opening the game
         gamemode = display_game_menu()
      restart = game()
   
   
def game():
   global difficulty
   global gamemode
   global player
   global move
   global rotate
   global place
   global clear
   global merge

   stddraw.setKeyRepeat(1)
   stddraw.clearKeysTyped()
   stddraw.clearMousePresses()
   stddraw.setSaveKey("y")

   ms = (350 if difficulty == 0 else (250 if difficulty == 1 else (125 if difficulty == 2 else 75)))

   # create the game grid
   grid = GameGrid(GRID_H, GRID_W, gamemode)
   # create the first tetromino to enter the game grid 
   # by using the create_tetromino function defined below
   tetrominos = [create_tetromino(GRID_H, GRID_W), create_tetromino(GRID_H, GRID_W), create_tetromino(GRID_H, GRID_W), create_tetromino(GRID_H, GRID_W)]
   current_tetromino = tetrominos.pop(0)
   grid.current_tetromino = current_tetromino
   
   last_mouse_posX = -1
   last_mouse_posY = -1
   mouse = None
   score = 0
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
               score += count * 2
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
               score += 1
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
               score += count * 2
         if stddraw.mouseScrollHeldDown():
            if grid.is_inside(round(stddraw.mouseScrollY()), round(stddraw.mouseScrollX())):
               succ = current_tetromino.move("down", grid, 1, delay=50)
               if succ:
                  score += 1

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
      game_over = False
      if success == False or dropped:
         place.play()
         # get the tile matrix of the tetromino
         tiles_to_place = current_tetromino.tile_matrix
         # update the game grid by adding the tiles of the tetromino
         grid.current_ghost = None
         game_over = grid.update_grid(tiles_to_place)
         # end the main game loop if the game is over
         
         if gamemode == "2048":
            while True:
               score = grid.check_line_chain_merge(score, difficulty, merge, tetrominos[0], tetrominos[1], tetrominos[2], game_over)
               score_before_line_delete = score
               score = grid.delete_full_lines(clear, score, tetrominos[0], tetrominos[1], tetrominos[2], game_over, difficulty)
               if score_before_line_delete == score:
                  break
         else:
            score = grid.delete_full_lines(clear, score, tetrominos[0], tetrominos[1], tetrominos[2], game_over, difficulty)

         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         tetromino = create_tetromino(GRID_H, GRID_W)
         tetrominos.append(tetromino)

         current_tetromino = tetrominos.pop(0)
         grid.current_tetromino = current_tetromino

      # display the game grid and as well the current tetromino
      grid.display(score, tetrominos[0], tetrominos[1], tetrominos[2], game_over)
      if game_over:
         break
   
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
   global player
   global move
   global rotate
   global place
   global clear
   global menu
   global merge

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
   global slider1location
   global slider2location
   global slider3location
   global difficulty
   global player
   global move
   global rotate
   global place
   global clear
   global menu
   global merge

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
   img_file = DIR + "/images/medium.png"
   medium = Picture(img_file)
   img_file = DIR + "/images/hard.png"
   hard = Picture(img_file)
   img_file = DIR + "/images/extreme.png"
   extreme = Picture(img_file)
   img_file = DIR + "/images/help.png"
   help = Picture(img_file)

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
   help_x, help_y = img_center_x + 7.5, img_center_x + 11.5

   slider_start = img_center_x-button_w/2
   slider_end = slider_start+slider_w

   if slider1location == None and slider2location == None and slider3location == None:
      slider1location = slider_start + (slider_w/20)
      slider2location = slider_start + (slider_w/4)
      slider3location = slider_start + (slider_w / 6) * 2
   
   volume_percent = player.volume
   sound_percent = menu.volume

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
      
      speedButtonPicture = medium
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

            player.volume = round(volume_percent)
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
            rotate.volume = round(sound_percent)
            move.volume = round(sound_percent)
            place.volume = round(sound_percent)
            clear.volume = round(sound_percent)
            menu.volume = round(sound_percent)
            merge.volume = round(sound_percent)
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

      diffStr = "Easy" if difficulty == 0 else ("Medium" if difficulty == 1 else ("Hard" if difficulty == 2 else "Extreme"))
      speedButtonPicture = easy if difficulty == 0 else (medium if difficulty == 1 else (hard if difficulty == 2 else extreme))

      # MOUSE CLICKS ON BUTTONS
      if stddraw.mouseLeftPressed():
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h: 
               return "tetris"
         if mouse_x >= button3_blc_x and mouse_x <= button3_blc_x + button_w:
            if mouse_y >= button3_blc_y and mouse_y <= button3_blc_y + button_h: 
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
      elif mouse_x >= help_x - 0.6 and mouse_x <= help_x + 0.6 and mouse_y >= help_y - 0.6 and mouse_y <= help_y + 0.6:
         if not played:
            menu.play()
            played = True
         display_controls(background_color)
      else:
         played = False

      if volume_percent == 0:
         musicButtonPicture=musicOff
      if sound_percent == 0:
         soundButtonPicture=soundOff

      # MUSIC SLIDER
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,10.5,slider_w,slider_h)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.filledCircle(slider1location,10.5+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.boldText(slider1location-0.03,10,str(round(volume_percent)))
      stddraw.picture(musicButtonPicture,slider1location-0.03,10.5+(slider_h/2))

      # SOUND SLIDER
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,9,slider_w,slider_h)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.filledCircle(slider2location,9+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.boldText(slider2location-0.03,8.5,str(round(sound_percent)))
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
   help_x, help_y = img_center_x + 7.5, img_center_x + 11.5

   while True:
      mouse_x = stddraw.mouseMotionX()
      mouse_y = stddraw.mouseMotionY()

      if not (mouse_x >= help_x - 0.6 and mouse_x <= help_x + 0.6 and mouse_y >= help_y - 0.6 and mouse_y <= help_y + 0.6):
         stddraw.clearKeysTyped()
         stddraw.clearMousePresses()
         break

      stddraw.clear(background_color)
      stddraw.picture(controls, img_center_x, img_center_y)
      stddraw.picture(help, help_x, help_y)
      stddraw.show(0)

def display_pause_menu():
   global slider1location
   global slider2location
   global player
   global move
   global rotate
   global place
   global clear
   global menu
   global merge

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

   help_x, help_y = img_center_x + 7.5, img_center_x + 11.5

   stddraw.setFontFamily("Arial")

   # dimensions of the slider
   slider_w, slider_h = GRID_W, 0.2

   slider_start = img_center_x-GRID_W/2
   slider_end = slider_start+slider_w
   
   volume_percent = player.volume
   sound_percent = menu.volume

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
         stddraw.clearMousePresses()
         break
      elif "enter" in keys_typed or "return" in keys_typed:
         if os.path.exists(TEMP_IMAGE):
            os.remove(TEMP_IMAGE)
         stddraw.setKeyRepeat(1)
         stddraw.clearMousePresses()
         return "menu"
      elif "r" in keys_typed:
         if os.path.exists(TEMP_IMAGE):
            os.remove(TEMP_IMAGE)
         stddraw.setKeyRepeat(1)
         stddraw.clearMousePresses()
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

            player.volume = round(volume_percent)
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
            rotate.volume = round(sound_percent)
            move.volume = round(sound_percent)
            place.volume = round(sound_percent)
            clear.volume = round(sound_percent)
            menu.volume = round(sound_percent)
            merge.volume = round(sound_percent)
         else:
            if mouse_y >= 4.52 and mouse_y < 4.54 + slider_h and mouse_x >= slider_start and mouse_x <= slider_end:
               musicHold = True
            elif mouse_y >= 3.02 and mouse_y < 3.04 + slider_h and mouse_x >= slider_start and mouse_x <= slider_end:
               soundHold = True
      else:
         musicHold = False
         soundHold = False

      if mouse_x >= help_x - 0.6 and mouse_x <= help_x + 0.6 and mouse_y >= help_y - 0.6 and mouse_y <= help_y + 0.6:
         if not played:
            menu.play()
            played = True
         display_controls(background_color)
      else:
         played = False

      if volume_percent == 0:
         musicButtonPicture=musicOff
      if sound_percent == 0:
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
      stddraw.boldText(slider1location-0.03,4,str(round(volume_percent)))
      stddraw.picture(musicButtonPicture,slider1location-0.03,4.5+(slider_h/2))

      # SOUND SLIDER
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,3,slider_w,slider_h)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.filledCircle(slider2location,3+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.boldText(slider2location-0.03,2.5,str(round(sound_percent)))
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

      
# start() function is specified as the entry point (main function) from which 
# the program starts execution
if __name__== '__main__':
   start()
