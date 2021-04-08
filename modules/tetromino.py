import time
from modules.tile import Tile # used for representing each tile on the tetromino
from modules.point import Point # used for tile positions
import numpy as np # fundamental Python module for scientific computing
from modules.color import Color

_AVAILABILITY = time.time()*1000
_left_availability = _AVAILABILITY
_right_availability = _AVAILABILITY
_down_availability = _AVAILABILITY
_standart_availability = _AVAILABILITY

# Class used for representing tetrominoes with 3 out of 7 different types/shapes 
# as (I, O and Z)
class Tetromino:
   
   # Constructor to create a tetromino with a given type (shape)
   def __init__(self, type, grid_height, grid_width, bottom_x, bottom_y=None, ghost=False, grid=None):
      # set grid_height and grid_width from input parameters
      self.grid_height = grid_height
      self.grid_width = grid_width
      self.type = type
      # initial position of the bottom-left tile in the tile matrix just before 
      # the tetromino enters the game grid
      self.bottom_left_corner = Point()
      # upper side of the game grid
      self.bottom_left_corner.y = bottom_y if bottom_y != None else grid_height
      # a random horizontal position
      self.bottom_left_corner.x = bottom_x

      if type == 'I':
         if ghost:
            self.background_color = Color(0,0,0)
            self.boundary_color = Color(43,172,226)
         else:
            self.background_color = Color(43,172,226)
            self.boundary_color = Color(0,122,206)
      elif type == 'O':
         if ghost:
            self.background_color = Color(0,0,0)
            self.boundary_color = Color(253,225,0)
         else:
            self.background_color = Color(253,225,0)
            self.boundary_color = Color(239,170,0)
      elif type == 'Z':
         if ghost:
            self.background_color = Color(0,0,0)
            self.boundary_color = Color(238,39,51)
         else:
            self.background_color = Color(238,39,51)
            self.boundary_color = Color(153,0,0)
      elif type == 'S':
         if ghost:
            self.background_color = Color(0,0,0)
            self.boundary_color = Color(78,183,72)
         else:
            self.background_color = Color(78,183,72)
            self.boundary_color = Color(0,153,0)
      elif type == 'L':
         if ghost:
            self.background_color = Color(0,0,0)
            self.boundary_color = Color(248,150,34)
         else:
            self.background_color = Color(248,150,34)
            self.boundary_color = Color(180,87,0)
      elif type == 'J':
         if ghost:
            self.background_color = Color(0,0,0)
            self.boundary_color = Color(0,90,157)
         else:
            self.background_color = Color(0,90,157)
            self.boundary_color = Color(0,0,115)
      elif type == 'T':
         if ghost:
            self.background_color = Color(0,0,0)
            self.boundary_color = Color(146,43,140)
         else:
            self.background_color = Color(146,43,140)
            self.boundary_color = Color(102,0,102)

      if grid is None:
         # set the shape of the tetromino based on the given type
         occupied_tiles = []
         if type == 'I':
            n = 4  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino I in its initial orientation
            occupied_tiles.append((1, 0)) # (column_index, row_index)
            occupied_tiles.append((1, 1))
            occupied_tiles.append((1, 2))
            occupied_tiles.append((1, 3))
         elif type == 'O':
            n = 2  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino O in its initial orientation
            occupied_tiles.append((0, 0)) 
            occupied_tiles.append((1, 0))
            occupied_tiles.append((0, 1))
            occupied_tiles.append((1, 1))
         elif type == 'Z':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            occupied_tiles.append((0, 0)) 
            occupied_tiles.append((1, 0))
            occupied_tiles.append((1, 1))
            occupied_tiles.append((2, 1))
         elif type == 'S':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino S in its initial orientation
            occupied_tiles.append((0, 1)) 
            occupied_tiles.append((1, 0))
            occupied_tiles.append((1, 1))
            occupied_tiles.append((2, 0))
         elif type == 'L':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino L in its initial orientation
            occupied_tiles.append((0, 0)) 
            occupied_tiles.append((0, 1))
            occupied_tiles.append((1, 0))
            occupied_tiles.append((2, 0))
         elif type == 'J':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino J in its initial orientation
            occupied_tiles.append((0, 0)) 
            occupied_tiles.append((1, 0))
            occupied_tiles.append((2, 0))
            occupied_tiles.append((2, 1))
         elif type == 'T':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino T in its initial orientation
            occupied_tiles.append((0, 0)) 
            occupied_tiles.append((1, 0))
            occupied_tiles.append((1, 1))
            occupied_tiles.append((2, 0))
         # create a matrix of numbered tiles based on the shape of the tetromino
         self.tile_matrix = np.full((n, n), None)
         # create each tile by computing its position w.r.t. the game grid based on 
         # its bottom_left_corner
         columns = []
         rows = []
         for i in range(len(occupied_tiles)):
            col_index, row_index = occupied_tiles[i][0], occupied_tiles[i][1]
            position = Point()
            # horizontal position of the tile
            position.x = self.bottom_left_corner.x + col_index
            # vertical position of the tile
            position.y = self.bottom_left_corner.y + (n - 1) - row_index
            if position.x not in columns:
               columns.append(position.x)
            if position.y not in rows:
               rows.append(position.y)
            # create the tile on the computed position 
            self.tile_matrix[row_index][col_index] = Tile(position, background_color=self.background_color, boundary_color=self.boundary_color)
         
         self.column_count = len(columns)
         self.row_count = len(rows)
         self.leftmost = min(columns)
      else:
         self.tile_matrix = grid
         (nrows, ncols) = grid.shape
         rows = []
         cols = []
         for i in range(nrows):
            for j in range(ncols):
               if self.tile_matrix[i][j] != None:
                  pos = self.tile_matrix[i][j].get_position()

                  if pos.x not in cols:
                     cols.append(pos.x)
                  if pos.y not in rows:
                     rows.append(pos.y)
         self.column_count = len(cols)
         self.row_count = len(rows)
         self.leftmost = min(cols)
       
   # Method for drawing the tetromino on the game grid
   def draw(self):
      (nrows, ncols) = self.tile_matrix.shape
      for row in range(nrows):
         for col in range(ncols):
            # draw each occupied tile (not equal to None) on the game grid
            if self.tile_matrix[row][col] != None:
               # considering newly entered tetrominoes to the game grid that may 
               # have tiles with position.y >= grid_height
               position = self.tile_matrix[row][col].get_position()
               if position.y < self.grid_height:
                  self.tile_matrix[row][col].draw() 
   
   def rotate(self, grid):
      not_rotated_copy_matrix = self.tile_matrix.copy()
      copy_matrix = np.rot90(self.tile_matrix.copy())
      new_tile_matrix = np.full((len(copy_matrix), len(copy_matrix)), None)
      rightmost = 0
      leftmost = 0
      bottommost = 0
      columns = []
      rows = []
      for i in range(len(copy_matrix)):
         for j in range(len(copy_matrix)):
            if copy_matrix[i][j] != None:
               position = Point()
               position.x = self.bottom_left_corner.x + j
               position.y = self.bottom_left_corner.y + (len(copy_matrix) - 1) - i

               if grid.is_occupied(position.y, position.x):
                  return False

               new_tile_matrix[i][j] = Tile(position, background_color=self.background_color, boundary_color=self.boundary_color)

               if position.x > self.grid_width - 1 and position.x - (self.grid_width - 1) > rightmost:
                  rightmost = position.x - (self.grid_width - 1)
               elif position.x < 0 and -position.x > leftmost:
                  leftmost = -position.x

               if position.y < bottommost:
                  bottommost = position.y
      
      self.tile_matrix = new_tile_matrix

      if bottommost < 0:
         success = self.move("up", grid, -bottommost)

         if not success:
            self.tile_matrix = not_rotated_copy_matrix
            return False
      
      if rightmost != 0:
         success = self.move("left", grid, rightmost)

         if not success:
            self.tile_matrix = not_rotated_copy_matrix
            return False
      
      if leftmost != 0:
         success = self.move("right", grid, leftmost)

         if not success:
            self.tile_matrix = not_rotated_copy_matrix
            return False
      
      for i in range(len(new_tile_matrix)):
         for j in range(len(new_tile_matrix)):
            if new_tile_matrix[i][j] != None:
               pos = new_tile_matrix[i][j].get_position()

               if pos.x not in columns:
                  columns.append(pos.x)
               if pos.y not in rows:
                  rows.append(pos.y)
      self.column_count = len(columns)
      self.row_count = len(rows)
      self.leftmost = min(columns)
      return True
      
   # Method for moving the tetromino in a given direction by 1 on the game grid
   def move(self, direction, game_grid, amount, delay=None, standart=False):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      current_mil = time.time()*1000
      if direction == "left":
         global _left_availability
         if current_mil > _left_availability or delay is None:
            # check if the tetromino can be moved in the given direction by using the
            # can_be_moved method defined below
            if not(self.can_be_moved(direction, game_grid, amount)):
               return False  # tetromino cannot be moved in the given direction
            self.bottom_left_corner.x -= amount
            self.leftmost -= amount

            for row in range(n):
               for col in range(n):
                  if self.tile_matrix[row][col] != None:
                        self.tile_matrix[row][col].move(-amount, 0)
            if delay is not None:
               _left_availability = current_mil + delay
            return True
         else:
            return None
      elif direction == "right":
         global _right_availability
         if current_mil > _right_availability or delay is None:
            # check if the tetromino can be moved in the given direction by using the
            # can_be_moved method defined below
            if not(self.can_be_moved(direction, game_grid, amount)):
               return False  # tetromino cannot be moved in the given direction
            self.bottom_left_corner.x += amount
            self.leftmost += amount

            for row in range(n):
               for col in range(n):
                  if self.tile_matrix[row][col] != None:
                     self.tile_matrix[row][col].move(amount, 0)
            if delay is not None:
               _right_availability = current_mil + delay
            return True
         else:
            return None
      elif direction == "down":
         global _down_availability
         global _standart_availability
         if current_mil > (_standart_availability if standart else _down_availability) or delay is None:
            # check if the tetromino can be moved in the given direction by using the
            # can_be_moved method defined below
            if not(self.can_be_moved(direction, game_grid, amount)):
               return False  # tetromino cannot be moved in the given direction
            self.bottom_left_corner.y -= amount
            for row in range(n):
               for col in range(n):
                  if self.tile_matrix[row][col] != None:
                     self.tile_matrix[row][col].move(0, -amount)
            if delay is not None:
               if standart:
                  _standart_availability = current_mil + delay
               else:
                  _down_availability = current_mil + delay
            return True
         else:
            return None
      else:
         # check if the tetromino can be moved in the given direction by using the
         # can_be_moved method defined below
         if not(self.can_be_moved(direction, game_grid, amount)):
            return False  # tetromino cannot be moved in the given direction
         self.bottom_left_corner.y += amount
         for row in range(n):
            for col in range(n):
               if self.tile_matrix[row][col] != None:
                  self.tile_matrix[row][col].move(0, amount)
      return True  # successful move in the given direction
   
   # Method to check if the tetromino can be moved in the given direction or not
   def can_be_moved(self, dir, game_grid, amount):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      if dir == "left" or dir == "right" or dir == "up":
         for row in range(n):
            for col in range(n): 
               # direction = left --> check the leftmost tile of each row
               if dir == "left" and self.tile_matrix[row][col] != None:
                  leftmost = self.tile_matrix[row][col].get_position()
                  # tetromino cannot go left if any leftmost tile is at x = 0
                  if leftmost.x == 0:
                     return False
                  # skip each row whose leftmost tile is out of the game grid 
                  # (possible for newly entered tetrominoes to the game grid)
                  if leftmost.y >= self.grid_height:
                     break
                  # tetromino cannot go left if the grid cell on the left of any 
                  # of its leftmost tiles is occupied
                  if game_grid.is_occupied(leftmost.y, leftmost.x - amount):
                     return False
                  break  # end the inner for loop
               # direction = right --> check the rightmost tile of each row
               elif dir == "right" and self.tile_matrix[row][n - 1 - col] != None:
                  rightmost = self.tile_matrix[row][n - 1 - col].get_position()
                  # tetromino cannot go right if any of its rightmost tiles is 
                  # at x = grid_width - 1
                  if rightmost.x == self.grid_width - 1:
                     return False
                  # skip each row whose rightmost tile is out of the game grid 
                  # (possible for newly entered tetrominoes to the game grid)
                  if rightmost.y >= self.grid_height:
                     break
                  # tetromino cannot go right if the grid cell on the right of 
                  # any of its rightmost tiles is occupied
                  if game_grid.is_occupied(rightmost.y, rightmost.x + amount):
                     return False
                  break  # end the inner for loop
      # direction = down --> check the bottommost tile of each column
      else:
         for col in range(n):
            for row in range(n - 1, -1, -1):
               if self.tile_matrix[row][col] != None:
                  bottommost = self.tile_matrix[row][col].get_position()
                  # skip each column whose bottommost tile is out of the grid 
                  # (possible for newly entered tetrominoes to the game grid)
                  if bottommost.y > self.grid_height:
                     break
                  # tetromino cannot go down if any bottommost tile is at y = 0
                  if bottommost.y == 0:
                     return False 
                  # or the grid cell below any bottommost tile is occupied
                  if game_grid.is_occupied(bottommost.y - amount, bottommost.x):
                     return False
                  break  # end the inner for loop
      return True  # tetromino can be moved in the given direction

   def copy_grid(self, ghost=False, blcx=None, blcy=None, trim=None):
      matrix = self.tile_matrix if trim is None else self.trim()

      copy_matrix = matrix.copy()
      new_tile_matrix = np.full(copy_matrix.shape, None)

      blc_x = self.bottom_left_corner.x if blcx is None else blcx
      blc_y = self.bottom_left_corner.y if blcy is None else blcy

      (nrows, ncols) = copy_matrix.shape

      for i in range(nrows):
         for j in range(ncols):
            if copy_matrix[i][j] != None:
               position = Point()
               position.x = blc_x + j
               position.y = blc_y + (nrows - 1) - i

               if ghost:
                  background = Color(0,0,0)
                  boundaries = self.background_color
               else:
                  background = self.background_color
                  boundaries = self.boundary_color

               new_tile_matrix[i][j] = Tile(position, background_color=background, boundary_color=boundaries)
      return new_tile_matrix

   def copy(self, ghost=False, blcx=None, blcy=None, trim=None):
      grid = self.copy_grid(ghost, blcx, blcy, trim)
      return Tetromino(self.type, self.grid_height, self.grid_width, self.bottom_left_corner.x, self.bottom_left_corner.y, ghost, grid)

   def trim(self):
      new_arr = np.full((self.row_count, self.column_count), None)
      col = 0
      for i in range(len(self.tile_matrix)):
         row = 0
         empty = True
         for j in range(len(self.tile_matrix)):
            if self.tile_matrix[j][i] != None:
               if empty != False:
                  empty = False
               new_arr[row][col] = self.tile_matrix[j][i]
            row += 1
         if not empty:
            col += 1
      return new_arr
