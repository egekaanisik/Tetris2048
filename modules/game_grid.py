import modules.stddraw as stddraw # the stddraw module is used as a basic graphics library
from modules.color import Color # used for coloring the game grid
import numpy as np # fundamental Python module for scientific computing
from modules.tile import Tile

# Class used for modelling the game grid
class GameGrid:
	# Constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create the tile matrix to store the tiles placed on the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      self.current_ghost = None
      # game_over flag shows whether the game is over/completed or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(0, 0, 0)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(30, 30, 30) 
      self.boundary_color = Color(30, 30, 30) 
      # thickness values used for the grid lines and the grid boundaries 
      self.line_thickness = 0.002
      self.box_thickness = 8 * self.line_thickness

   # Method used for displaying the game grid
   def display(self, score, next_tetromino1, next_tetromino2, next_tetromino3, game_over):
      # clear the background canvas to empty_cell_color
      stddraw.clear(self.empty_cell_color)
      # draw the game grid
      self.draw_boundaries()
      self.draw_grid()
      # draw the current (active) tetromino
      if self.current_ghost != None:
         self.current_ghost.draw()
         
      if self.current_tetromino != None:
         self.current_tetromino.draw()
      # draw a box around the game grid 
      

      if not game_over:
         stddraw.setPenColor(stddraw.WHITE)
         stddraw.setFontFamily("Arial")
         stddraw.setFontSize(30)
         stddraw.text(13.75, 19, "Score")
         stddraw.boldText(13.75, 17.75, str(score))
         stddraw.text(13.75, 15, "Next")
         stddraw.text(13.75, 14, "Tetrominoes")

         stddraw.setPenColor(self.boundary_color)
         stddraw.filledRectangle(12,-0.25,3.5,13.5)

         stddraw.setPenRadius(0.001)
         stddraw.setPenColor(stddraw.DARK_GRAY)
         stddraw.line(12.25, 8.75, 15.25, 8.75)
         stddraw.line(12.25, 4.25, 15.25, 4.25)
         next_tetromino1.copy(blcx=(14.25 - (next_tetromino1.column_count/2)),blcy=9.5 + (4-next_tetromino1.row_count)/2,trim=True).draw()
         next_tetromino2.copy(blcx=(14.25 - (next_tetromino2.column_count/2)),blcy=5 + (4-next_tetromino2.row_count)/2,trim=True).draw()
         next_tetromino3.copy(blcx=(14.25 - (next_tetromino3.column_count/2)),blcy=0.5 + (4-next_tetromino3.row_count)/2,trim=True).draw()
         stddraw.show(0)
      else:
         stddraw.setPenColor(stddraw.WHITE)
         stddraw.setFontFamily("Arial")
         stddraw.setFontSize(30)
         stddraw.text(13.75, 11.5, "Game Over!")
         stddraw.text(13.75, 9.5, "Final Score:")
         stddraw.boldText(13.75, 8.5, str(score))
         stddraw.setFontSize(20)
         stddraw.text(13.75,2,"Press Enter to")
         #stddraw.boldText(14.5,2.5,"Enter")
         stddraw.text(13.75,1.5,"return to the")
         stddraw.text(13.75,1,"main menu.")
         stddraw.show(0)
         
   # Method for drawing the cells and the lines of the grid
   def draw_grid(self): 
      # draw the inner lines of the grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      # draw each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # draw the tile if the grid cell is occupied by a tile
            if self.tile_matrix[row][col] != None:
               self.tile_matrix[row][col].draw()
      stddraw.setPenRadius()  # reset the pen radius to its default value            
      
   # Method for drawing the boundaries around the game grid 
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible 
      # for the bounding box as its lines lie on the boundaries of the canvas)
      #stddraw.setPenRadius(self.box_thickness)
      # coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.75, -0.75
      stddraw.filledRectangle(pos_x, pos_y, self.grid_width+0.50, self.grid_height+0.50)
      stddraw.setPenColor(self.empty_cell_color)
      pos_x, pos_y = -0.5, -0.5
      stddraw.filledRectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # Method used for checking whether the grid cell with given row and column 
   # indexes is occupied by a tile or empty
   def is_occupied(self, row, col):
      # return False if the cell is out of the grid
      if not self.is_inside(row, col):
         return False
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] != None
      
   # Method used for checking whether the cell with given row and column indexes 
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   def has_line_empty_cell(self, line):
      if None in self.tile_matrix[line]:
         return True
      else:
         False

   def delete_full_lines(self, clear, score, next_tetromino1, next_tetromino2, next_tetromino3, game_over, diff):
      paint_indexes = []
      indexes = []
      for i in range(self.grid_height):
         if not self.has_line_empty_cell(i):
            paint_indexes.append(i)
            indexes.append(i - len(indexes))

      if len(indexes) != 0:
         clear.play()

         if diff == 0:
            score += (1200 if len(indexes) == 4 else (300 if len(indexes) == 3 else (100 if len(indexes) == 2 else 40)))
         elif diff == 1:
            score += (2400 if len(indexes) == 4 else (600 if len(indexes) == 3 else (200 if len(indexes) == 2 else 80)))
         elif diff == 2:
            score += (3600 if len(indexes) == 4 else (900 if len(indexes) == 3 else (300 if len(indexes) == 2 else 120)))
         elif diff == 3:
            score += (4800 if len(indexes) == 4 else (1200 if len(indexes) == 3 else (400 if len(indexes) == 2 else 160)))
         
         for color in reversed(range(0, 256, 15)):
            for l in paint_indexes:
               for k in range(self.grid_width):
                  self.tile_matrix[l][k].background_color = Color(color, color, color)
                  self.tile_matrix[l][k].boundary_color = Color(color, color, color)
            self.display(score, next_tetromino1, next_tetromino2, next_tetromino3, game_over)

         for r in indexes:
            self.tile_matrix = np.delete(self.tile_matrix, (r), axis=0)
            self.tile_matrix = np.append(self.tile_matrix, np.full((1, self.grid_width), None), axis=0)
                     
            for i in range(r, self.grid_height):
               for j in range(self.grid_width):
                  if self.tile_matrix[i][j] != None:
                     self.tile_matrix[i][j].move(0, -1)

      return score

   # Method for updating the game grid by placing the given tiles of a stopped 
   # tetromino and checking if the game is over due to having tiles above the 
   # topmost game grid row. The method returns True when the game is over and
   # False otherwise.
   def update_grid(self, tiles_to_place):
      # place all the tiles of the stopped tetromino onto the game grid 
      n_rows, n_cols = len(tiles_to_place), len(tiles_to_place[0])
      for col in range(n_cols):
         for row in range(n_rows):            
            # place each occupied tile onto the game grid
            if tiles_to_place[row][col] != None:
               pos = tiles_to_place[row][col].get_position()
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_place[row][col]
               # the game is over if any placed tile is out of the game grid
               else:
                  self.game_over = True
      # return the game_over flag
      return self.game_over