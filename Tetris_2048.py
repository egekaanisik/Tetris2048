import stddraw # the stddraw module is used as a basic graphics library
import random # used for creating tetrominoes with random types/shapes
from game_grid import GameGrid # class for modeling the game grid
from tetromino import Tetromino # class for modeling the tetrominoes
from picture import Picture # used representing images to display
import os # used for file and directory operations
from color import Color, RED, WHITE # used for coloring the game menu
import time
import sys
from audioplayer import AudioPlayer

# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution
def start():
   # set the dimensions of the game grid
   grid_h, grid_w = 20, 12
   # set the size of the drawing canvas
   canvas_h, canvas_w = 40 * grid_h+1, 40 * grid_w+160
   stddraw.setCanvasSize(canvas_w, canvas_h) 
   # set the scale of the coordinate system
   stddraw.setXscale(-1, grid_w + 4) # 17
   stddraw.setYscale(-1, grid_h) # 21
   
   # create the game grid
   grid = GameGrid(grid_h, grid_w)
   # create the first tetromino to enter the game grid 
   # by using the create_tetromino function defined below
   tetrominos = [create_tetromino(grid_h, grid_w), create_tetromino(grid_h, grid_w), create_tetromino(grid_h, grid_w), create_tetromino(grid_h, grid_w)]
   current_tetromino = tetrominos.pop(0)
   grid.current_tetromino = current_tetromino

   music_volume = 5
   effects_volume = 25

   current_dir = os.path.dirname(os.path.realpath(__file__)) + "/sounds"
   back_sound = current_dir + "/back.wav"
   move_sound = current_dir + "/move.wav"
   rotate_sound = current_dir + "/rotate.wav"
   place_sound = current_dir + "/place.wav"
   clear_sound = current_dir + "/clear.wav"

   player = AudioPlayer(back_sound)
   player.volume = music_volume

   move = AudioPlayer(move_sound)
   move.volume = effects_volume

   rotate = AudioPlayer(rotate_sound)
   rotate.volume = effects_volume

   place = AudioPlayer(place_sound)
   place.volume = effects_volume

   clear = AudioPlayer(clear_sound)
   clear.volume = effects_volume

   player.play(loop=True)
   # display a simple menu before opening the game
   difficulty = display_game_menu(grid_h, grid_w,player,rotate,move,place,clear)
   
   ms = (350 if difficulty == 0 else (250 if difficulty == 1 else (125 if difficulty == 2 else 75)))
   
   last_mouse_pos = -1
   mouse = False
   availability = time.time()*1000
   score = 0
   # main game loop (keyboard interaction for moving the tetromino) 
   while True:
      currentMilis = time.time()*1000
      pos = round(stddraw.mouseMotionX())
      dropped = False

      if (pos != last_mouse_pos):
         mouse = True
         last_mouse_pos = pos
      elif stddraw.hasNextKeyTyped():
         mouse = False

      if not mouse:
         # check user interactions via the keyboard
         if stddraw.hasNextKeyTyped():
            keys_typed = stddraw._keysTyped
            if "space" in keys_typed:
               count = 0
               while True:
                  sc = current_tetromino.move("down", grid, 1)

                  if not sc:
                     break
                  else:
                     count += 1
               dropped = True
               score += count * 2
            if "up" in keys_typed:
               can_rotate = current_tetromino.rotate(grid)
               if can_rotate:
                  rotate.play()
            # if the left arrow key has been pressed
            if "left" in keys_typed:
               # move the tetromino left by one
               can_left = current_tetromino.move("left", grid, 1)
               if can_left:
                  move.play()
            # if the right arrow key has been pressed
            if "right" in keys_typed:
               # move the tetromino right by one
               can_right = current_tetromino.move("right", grid, 1)
               if can_right:
                  move.play()
            # if the down arrow key has been pressed
            if "down" in keys_typed:
               # move the tetromino down by one 
               # (causes the tetromino to fall down faster)
               succ = current_tetromino.move("down", grid, 1)
               if succ:
                  score += 1
            # clear the queue that stores all the keys pressed/typed
            stddraw.clearKeysTyped()
      else:         
         if (pos + current_tetromino.column_count) > grid.grid_width:
            pos = grid.grid_width - current_tetromino.column_count
         
         diff = pos - current_tetromino.leftmost

         if diff < 0:
            for i in range(-diff):
               success_move = current_tetromino.move("left", grid, 1)
               
               if not success_move:
                  break
               else:
                  move.play()
         else:
            for i in range(diff):
               success_move = current_tetromino.move("right", grid, 1)
               
               if not success_move:
                  break
               else:
                  move.play()

         if stddraw.mouseRightPressed():
            success_rotate = current_tetromino.rotate(grid)
            if success_rotate:
               rotate.play()

         if stddraw.mouseLeftPressed():
            count = 0
            while True:
               sc = current_tetromino.move("down", grid, 1)

               if not sc:
                  break
               else:
                  count += 1
            dropped = True
            score += count * 2
         if stddraw.mouseScrollPressed(150):
            succ = current_tetromino.move("down", grid, 1)
            if succ:
               score += 1
      
      current_ghost = current_tetromino.copy(ghost=True)
      grid.current_ghost = current_ghost

      while True:
         sc = current_ghost.move("down", grid, 1)

         if not sc:
            break
         
      # move (drop) the tetromino down by 1 at each iteration 
      success=True
      if currentMilis > availability:
         success = current_tetromino.move("down", grid, 1)
         availability = currentMilis + ms

      # place the tetromino on the game grid when it cannot go down anymore
      game_over = False
      if not success or dropped:
         place.play()
         # get the tile matrix of the tetromino
         tiles_to_place = current_tetromino.tile_matrix
         # update the game grid by adding the tiles of the tetromino
         grid.current_ghost = None
         game_over = grid.update_grid(tiles_to_place)
         # end the main game loop if the game is over
         
         score = grid.delete_full_lines(clear, score, tetrominos[0], tetrominos[1], tetrominos[2], game_over, difficulty)

         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         tetromino = create_tetromino(grid_h, grid_w)
         tetrominos.append(tetromino)

         current_tetromino = tetrominos.pop(0)
         grid.current_tetromino = current_tetromino

      # display the game grid and as well the current tetromino
      grid.display(score, tetrominos[0], tetrominos[1], tetrominos[2], game_over)

# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
   # type (shape) of the tetromino is determined randomly
   tetromino_types = [ 'I', 'O', 'Z', 'S', 'L', 'J', 'T' ]
   #tetromino_types = [ 'I' ]
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   n = (4 if random_type == 'I' else (2 if random_type == 'O' else 3))
   bottom_x = random.randint(0, grid_width - n)

   # create and return the tetromino
   tetromino = Tetromino(random_type, grid_height, grid_width, bottom_x)
   return tetromino

# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width,player,rotate,move,place,clear):
   # colors used for the menu
   background_color = Color(25, 49, 90)
   button_color = Color(132, 132, 132)
   text_color = Color(31, 160, 239)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/images/menu_image.png"
   image_to_display = Picture(img_file)
   img_file = current_dir + "/images/tetris.png"
   tetris= Picture(img_file)
   img_file = current_dir + "/images/tetris2.png"
   tetris2= Picture(img_file)
   img_file = current_dir + "/images/2048.png"
   i2048 = Picture(img_file)
   img_file = current_dir + "/images/2048L.png"
   i2048L = Picture(img_file)
   img_file = current_dir + "/images/musicOn.png"
   musicOn = Picture(img_file)
   img_file = current_dir + "/images/musicOff.png"
   musicOff = Picture(img_file)
   img_file = current_dir + "/images/soundOff.png"
   soundOff = Picture(img_file)
   img_file = current_dir + "/images/soundOn.png"
   soundOn = Picture(img_file)
   img_file = current_dir + "/images/speed.png"
   speed = Picture(img_file)
   menu_sound = current_dir + "/sounds/menu.wav"
   menu = AudioPlayer(menu_sound)

   # center coordinates to display the image
   img_center_x, img_center_y = (17/2)-1,(21/2)-1
   # image is represented using the Picture class
   # display the image
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   # dimensions of the start game button
   # dimensions of the start game button
   button_w, button_h = (grid_width - 1.5), 2
   slider_w, slider_h = (grid_width - 2), 0.2
   # coordinates of the bottom left corner of the start game button 
   button_blc_x, button_blc_y = img_center_x-button_w/2, 4 # Tetris Button 
   button3_blc_x, button3_blc_y = img_center_x-button_w/2 , 1 # Tetris 2048 Button

   slider_start = button3_blc_x+((button_w-slider_w)/2)
   slider_end = slider_start+slider_w
   slider1location = slider_start + (slider_w/20)
   slider2location = slider_start + (slider_w/4)
   slider3location = slider_start + (slider_w / 6) * 2
   volume_percent = 5
   sound_percent = 25
   diff = 1
   menu.volume = sound_percent
   musicHold = False
   soundHold = False
   diffHold = False
   played = False
   # menu interaction loop
   while True:
      speedButtonPicture = speed
      soundButtonPicture = soundOn
      musicButtonPicture = musicOn
      tetrisButtonPicture = tetris
      i2048Picture = i2048
      
      
      # display the menu and wait for a short time (50 ms)

      # mouse_x, mouse_y = float(stddraw.mouseMotionX()), float(stddraw.mouseMotionY())
      mouse_x = stddraw.mouseMotionX() if stddraw.mouseMotionX() is not None else -1
      mouse_y = stddraw.mouseMotionY() if stddraw.mouseMotionY() is not None else -1
      
      
      if stddraw.mouseLeftHeldDown():
         if mouse_y >= 10 and mouse_y < 10.05 + slider_h:
            musicHold = True
         elif mouse_y >= 8.5 and mouse_y < 8.55 + slider_h:
            soundHold = True
         elif mouse_y >= 7 and mouse_y < 7.05 + slider_h:
            diffHold = True
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
         elif diffHold:
            if mouse_x >= slider_start and mouse_x <= slider_end:
               if mouse_x < slider_start + (slider_w / 6) * 1:
                  slider3location = slider_start
                  diff = 0
               elif mouse_x >= slider_start + (slider_w / 6) * 1 and mouse_x < slider_start + (slider_w / 6) * 3:
                  slider3location = slider_start + (slider_w / 6) * 2
                  diff = 1
               elif mouse_x >= slider_start + (slider_w / 6) * 3 and mouse_x < slider_start + (slider_w / 6) * 5:
                  slider3location = slider_start + (slider_w / 6) * 4
                  diff = 2
               elif mouse_x >= slider_start + (slider_w / 6) * 5:
                  slider3location = slider_end
                  diff = 3
            elif mouse_x < slider_start:
               slider3location = slider_start
               diff = 0
            else:
               slider3location = slider_end
               diff = 3

      else:
         musicHold = False
         soundHold = False
         diffHold = False

      diffStr = "Easy" if diff == 0 else ("Medium" if diff == 1 else ("Hard" if diff == 2 else "Extreme"))

      # MOUSE CLICKS ON BUTTONS
      if stddraw.mouseLeftPressed():
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h: 
               return diff
         if mouse_x >= button3_blc_x and mouse_x <= button3_blc_x + button_w:
            if mouse_y >= button3_blc_y and mouse_y <= button3_blc_y + button_h: 
               print("Work in Progress, Tetris 2048")    
      
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
      else:
         played = False
      

      if volume_percent == 0:
         musicButtonPicture=musicOff
      if sound_percent == 0:
         soundButtonPicture=soundOff

      # LOGO IMAGE
      stddraw.picture(image_to_display, img_center_x, img_center_y+6)
      # display the start game button as a filled rectangle

      # MUSIC SLIDER
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,10,slider_w,slider_h)
      stddraw.setPenColor(WHITE)
      stddraw.filledCircle(slider1location,10+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.text(slider1location-0.03,9.5,str(round(volume_percent)))
      stddraw.picture(musicButtonPicture,slider1location-0.03,10+(slider_h/2))

      # SOUND SLIDER
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,8.5,slider_w,slider_h)
      stddraw.setPenColor(WHITE)
      stddraw.filledCircle(slider2location,8.5+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.text(slider2location-0.03,8,str(round(sound_percent)))
      stddraw.picture(soundButtonPicture,slider2location-0.01,8.5+(slider_h/2))

      # DIFFICULTY SLIDER

      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(slider_start,7,slider_w,slider_h)
      stddraw.setPenColor(WHITE)
      stddraw.filledCircle(slider3location,7+(slider_h/2),0.3)
      stddraw.setPenColor(text_color)
      stddraw.text(slider3location-0.03,6.5,diffStr)
      stddraw.picture(speedButtonPicture,slider3location,7+(slider_h/2)+0.02)

      # stddraw.picture(tetrisButtonPicture,img_center_x/2, 5)
      #stddraw.text(img_center_x,5,"Start Tetris")
      stddraw.picture(tetrisButtonPicture,img_center_x,5)
      #stddraw.text(img_center_x,2,"Start 2048")
      stddraw.picture(i2048Picture,img_center_x,2)

      stddraw.show(0)
      stddraw.clear(background_color)
      
# start() function is specified as the entry point (main function) from which 
# the program starts execution
if __name__== '__main__':
   start()
