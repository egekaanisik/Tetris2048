import stddraw # the stddraw module is used as a basic graphics library
import random # used for creating tetrominoes with random types/shapes
from game_grid import GameGrid # class for modeling the game grid
from tetromino import Tetromino # class for modeling the tetrominoes
from picture import Picture # used representing images to display
import os # used for file and directory operations
from color import Color # used for coloring the game menu
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
   canvas_h, canvas_w = 40 * grid_h, 40 * grid_w
   stddraw.setCanvasSize(canvas_w, canvas_h) 
   # set the scale of the coordinate system
   stddraw.setXscale(-0.5, grid_w - 0.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)
   
   # create the game grid
   grid = GameGrid(grid_h, grid_w)
   # create the first tetromino to enter the game grid 
   # by using the create_tetromino function defined below
   tetrominos = [create_tetromino(grid_h, grid_w), create_tetromino(grid_h, grid_w)]
   current_tetromino = tetrominos.pop(0)
   grid.current_tetromino = current_tetromino

   current_dir = os.path.dirname(os.path.realpath(__file__)) + "/sounds"
   back_sound = current_dir + "/back.wav"
   move_sound = current_dir + "/move.wav"
   rotate_sound = current_dir + "/rotate.wav"
   place_sound = current_dir + "/place.wav"
   clear_sound = current_dir + "/clear.wav"

   player = AudioPlayer(back_sound)
   player.volume = 5

   move = AudioPlayer(move_sound)
   move.volume = 30

   rotate = AudioPlayer(rotate_sound)
   rotate.volume = 30

   place = AudioPlayer(place_sound)
   place.volume = 30

   clear = AudioPlayer(clear_sound)
   clear.volume = 30

   player.play(loop=True)
   # display a simple menu before opening the game
   display_game_menu(grid_h, grid_w)

   
   print("Next Tetromino: " + tetrominos[0].type)
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
               while True:
                  sc = current_tetromino.move("down", grid, 1)

                  if not sc:
                     break
               dropped = True
            
            if "up" in keys_typed:
               current_tetromino.rotate(grid)
               rotate.play()
            # if the left arrow key has been pressed
            if "left" in keys_typed:
               # move the tetromino left by one
               current_tetromino.move("left", grid, 1)
               move.play()
            # if the right arrow key has been pressed
            if "right" in keys_typed:
               # move the tetromino right by one
               current_tetromino.move("right", grid, 1)
               move.play()
            # if the down arrow key has been pressed
            if "down" in keys_typed:
               # move the tetromino down by one 
               # (causes the tetromino to fall down faster)
               current_tetromino.move("down", grid, 1)
            # clear the queue that stores all the keys pressed/typed
            stddraw.clearKeysTyped()
      else:         
         if (pos + current_tetromino.column_count) > grid.grid_width:
            pos = grid.grid_width - current_tetromino.column_count
         
         diff = pos - current_tetromino.leftmost

         if diff < 0:
            for i in range(-diff):
               success_move = current_tetromino.move("left", grid, 1)
               move.play()

               if not success_move:
                  break
         else:
            for i in range(diff):
               success_move = current_tetromino.move("right", grid, 1)
               move.play()

               if not success_move:
                  break

         if stddraw.mouseRightPressed():
            current_tetromino.rotate(grid)
            rotate.play()

         if stddraw.mouseLeftPressed():
            while True:
               sc = current_tetromino.move("down", grid, 1)

               if not sc:
                  break
            dropped = True

         if stddraw.mouseScrollPressed(150):
            current_tetromino.move("down", grid, 1)
            
      current_ghost = current_tetromino.copy(ghost=True)
      grid.current_ghost = current_ghost

      while True:
         sc = current_ghost.move("down", grid, 1)

         if not sc:
            break
         
      # move (drop) the tetromino down by 1 at each iteration 
      success=True
      if currentMilis>availability:
         success = current_tetromino.move("down", grid, 1)
         availability=currentMilis+300

      # place the tetromino on the game grid when it cannot go down anymore
      if not success or dropped:
         place.play()
         # get the tile matrix of the tetromino
         tiles_to_place = current_tetromino.tile_matrix
         # update the game grid by adding the tiles of the tetromino
         grid.current_ghost = None
         game_over = grid.update_grid(tiles_to_place)
         # end the main game loop if the game is over
         if game_over:
            break

         line_count = grid.delete_full_lines(clear)

         if line_count != 0:
            score += (1200 if line_count == 4 else (300 if line_count == 3 else (100 if line_count == 2 else 40)))
            print("New Score: " + str(score))

         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         tetromino = create_tetromino(grid_h, grid_w)
         tetrominos.append(tetromino)

         current_tetromino = tetrominos.pop(0)
         grid.current_tetromino = current_tetromino
         print("Next Tetromino: " + tetrominos[0].type)

      # display the game grid and as well the current tetromino  
      grid.display(0)

   print("Game Over! Score is " + str(score) + ".")

# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
   # type (shape) of the tetromino is determined randomly
   tetromino_types = [ 'I', 'O', 'Z', 'S', 'L', 'J', 'T' ]
   #tetromino_types = [ 'Z' ]
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   n = (4 if random_type == 'I' else (2 if random_type == 'O' else 3))
   bottom_x = random.randint(0, grid_width - n)

   # create and return the tetromino
   tetromino = Tetromino(random_type, grid_height, grid_width, bottom_x)
   return tetromino

# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
   # colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/menu_image.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
# dimensions of the start game button
   button_w, button_h = (grid_width - 1.5)/2, 2
   # coordinates of the bottom left corner of the start game button 
   button_blc_x, button_blc_y = img_center_x/2-0.2 - button_w / 2, 4 # Tetris Button 
   button2_blc_x, button2_blc_y = img_center_x/2-0.2 - button_w / 2 , 1 #Settings Button
   button3_blc_x, button3_blc_y = img_center_x+(img_center_x/2)-button_w/2 , 4 # Tetris 2048 Button
   button4_blc_x, button4_blc_y = img_center_x+(img_center_x/2)-button_w/2 , 1 #Settings Button
   # display the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   stddraw.filledRectangle(button2_blc_x,button2_blc_y,button_w,button_h)
   stddraw.filledRectangle(button3_blc_x,button3_blc_y,button_w,button_h)
   stddraw.filledRectangle(button4_blc_x,button4_blc_y,button_w,button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   stddraw.text(img_center_x/2-0.2, 5, "Start Tetris")
   stddraw.text(img_center_x/2-0.2,2,"Settings")
   stddraw.text(img_center_x+(img_center_x/2),5,"Start Tetris 2048")
   stddraw.text(img_center_x+(img_center_x/2),2,"Quit")
   availability = 0
   # menu interaction loop
   while True:
      # display the menu and wait for a short time (50 ms)
      currentMilis = time.time()*1000
      stddraw.show(50)
      # mouse_x, mouse_y = float(stddraw.mouseMotionX()), float(stddraw.mouseMotionY())
      mouse_x = stddraw.mouseMotionX()
      mouse_y = stddraw.mouseMotionY()

      mouse_x = (round(mouse_x) if mouse_x is not None else -1)
      mouse_y = (round(mouse_y) if mouse_y is not None else -1)

      # check if the mouse has been left-clicked
      if stddraw.mouseLeftPressed():
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h: 
               break # break the loop to end the method and start the game
         if mouse_x >= button2_blc_x and mouse_x <= button2_blc_x + button_w:
            if mouse_y >= button2_blc_y and mouse_y <= button2_blc_y + button_h: 
               print("Work in Progress, Settings")
         if mouse_x >= button3_blc_x and mouse_x <= button3_blc_x + button_w:
            if mouse_y >= button3_blc_y and mouse_y <= button3_blc_y + button_h: 
               print("Work in Progress, Tetris 2048")
         if mouse_x >= button4_blc_x and mouse_x <= button4_blc_x + button_w:
            if mouse_y >= button4_blc_y and mouse_y <= button4_blc_y + button_h: 
               print("Work in Progress, Quit")
               sys.exit()
      
      if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
         if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h: 
            if currentMilis>availability:
               print("Mouse is on Tetris")
               availability=currentMilis+500
      if mouse_x >= button2_blc_x and mouse_x <= button2_blc_x + button_w:
         if mouse_y >= button2_blc_y and mouse_y <= button2_blc_y + button_h: 
            if currentMilis > availability:
               print("Mouse is on Settings")
               availability=currentMilis+500
      if mouse_x >= button3_blc_x and mouse_x <= button3_blc_x + button_w:
         if mouse_y >= button3_blc_y and mouse_y <= button3_blc_y + button_h: 
            if currentMilis > availability:
               print("Mouse is on Tetris 2048")
               availability=currentMilis+500
      if mouse_x >= button4_blc_x and mouse_x <= button4_blc_x + button_w:
         if mouse_y >= button4_blc_y and mouse_y <= button4_blc_y + button_h: 
            if currentMilis > availability:
               print("Mouse is on Quit")
               availability=currentMilis+500
      
               



# start() function is specified as the entry point (main function) from which 
# the program starts execution
if __name__== '__main__':
   start()
