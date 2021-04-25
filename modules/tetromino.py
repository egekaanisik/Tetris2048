#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# add the current directory to the system path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import time # used for getting the current time
from tile import Tile # used for representing each tile on the tetromino
from point import Point # used for tile positions
import numpy as np # fundamental Python module for scientific computing

# availability holders for moving the tile with a delay but not pausing the canvas
_AVAILABILITY = time.time()*1000
_left_availability = _AVAILABILITY
_right_availability = _AVAILABILITY
_down_availability = _AVAILABILITY
_standart_availability = _AVAILABILITY

# Class used for representing tetrominoes with 7 different types/shapes
class Tetromino:
   # Constructor to create a tetromino with a given type (shape)
   def __init__(self, type, grid_height, grid_width, bottom_x, bottom_y=None, ghost=False, grid=None, gamemode=None):
      # set grid_height, grid_width, tetromino type, game mode, and ghost from input parameters
      self.grid_height = grid_height
      self.grid_width = grid_width
      self.type = type
      self.gamemode = gamemode
      self.ghost = ghost
      # initial position of the bottom-left tile in the tile matrix
      self.bottom_left_corner = Point()
      # give x and y coordinates to the bottom-left corner
      self.bottom_left_corner.y = bottom_y if bottom_y != None else grid_height
      self.bottom_left_corner.x = bottom_x

      # if the grid is not initialized already
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
         # containers for column and row positions
         columns = []
         rows = []
         for i in range(len(occupied_tiles)):
            col_index, row_index = occupied_tiles[i][0], occupied_tiles[i][1]
            position = Point()
            # horizontal position of the tile
            position.x = self.bottom_left_corner.x + col_index
            # vertical position of the tile
            position.y = self.bottom_left_corner.y + (n - 1) - row_index
            # add positions to the containers
            if position.x not in columns:
               columns.append(position.x)
            if position.y not in rows:
               rows.append(position.y)
            # create the tile on the computed position
            self.tile_matrix[row_index][col_index] = Tile(position, gamemode, ghost, type=self.type)
         # initialize column and row count fields
         self.column_count = len(columns)
         self.row_count = len(rows)
         # initialize the leftmost tile
         self.leftmost = min(columns)
      # if the grid is initialized
      else:
         # set the grid
         self.tile_matrix = grid
         (nrows, ncols) = grid.shape
         # containers for column and row positions
         rows = []
         cols = []
         for i in range(nrows):
            for j in range(ncols):
               if self.tile_matrix[i][j] != None:
                  pos = self.tile_matrix[i][j].get_position()
                  # add positions to the containers
                  if pos.x not in cols:
                     cols.append(pos.x)
                  if pos.y not in rows:
                     rows.append(pos.y)
         # initialize column and row count fields
         self.column_count = len(cols)
         self.row_count = len(rows)
         # initialize the leftmost tile
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
   
   # Method for rotating the tetromino
   def rotate(self, grid):
      # copy the tile matrix
      not_rotated_copy_matrix = self.tile_matrix.copy()
      # rotate the copied matrix 90 degrees
      copy_matrix = np.rot90(self.tile_matrix.copy())
      # create a new array with the same shape of the copied matrix
      new_tile_matrix = np.full((len(copy_matrix), len(copy_matrix)), None)
      # containers for checking the leftmost, rightmost, and the bottommost tiles
      rightmost = 0
      leftmost = 0
      bottommost = 0
      # iterate over every cell
      for i in range(len(copy_matrix)):
         for j in range(len(copy_matrix)):
            # if the cell has a tile init
            if copy_matrix[i][j] != None:
               # create a new position of current cell
               position = Point()
               position.x = self.bottom_left_corner.x + j
               position.y = self.bottom_left_corner.y + (len(copy_matrix) - 1) - i

               # if the cell is occupied already, do not rotate
               if grid.is_occupied(position.y, position.x):
                  return False

               # copy tile tile to the new tile matri with a new position
               new_tile_matrix[i][j] = copy_matrix[i][j].copy(position)

               # get the leftmost, rightmost, and bottommost tiles
               if position.x > self.grid_width - 1 and position.x - (self.grid_width - 1) > rightmost:
                  rightmost = position.x - (self.grid_width - 1)
               elif position.x < 0 and -position.x > leftmost:
                  leftmost = -position.x

               if position.y < bottommost:
                  bottommost = position.y
      
      # change the tile matrix to the new one
      self.tile_matrix = new_tile_matrix

      # if the rotated tile goes below the grid, move up
      if bottommost < 0:
         success = self.move("up", grid, -bottommost)

         # if it cannot move, revert the changes
         if not success:
            self.tile_matrix = not_rotated_copy_matrix
            return False
      
      # if the rotated tile goes beyond the right limit of the grid, move left
      if rightmost != 0:
         success = self.move("left", grid, rightmost)

         # if it cannot move, revert the changes
         if not success:
            self.tile_matrix = not_rotated_copy_matrix
            return False
      
      # if the rotated tile goes beyond the left limit of the grid, move right
      if leftmost != 0:
         success = self.move("right", grid, leftmost)
         
         # if it cannot move, revert the changes
         if not success:
            self.tile_matrix = not_rotated_copy_matrix
            return False

      # containers for column and row positions
      columns = []
      rows = []
      
      for i in range(len(new_tile_matrix)):
         for j in range(len(new_tile_matrix)):
            if new_tile_matrix[i][j] != None:
               pos = new_tile_matrix[i][j].get_position()
               # add positions to the containers
               if pos.x not in columns:
                  columns.append(pos.x)
               if pos.y not in rows:
                  rows.append(pos.y)
      # initialize column and row count fields
      self.column_count = len(columns)
      self.row_count = len(rows)
      # initialize the leftmost tile
      self.leftmost = min(columns)
      # return that the tetromino is rotated
      return True
      
   # Method for moving the tetromino in a given direction by the given amount on the game grid
   def move(self, direction, game_grid, amount, delay=None, standart=False):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      # get the current time as milliseconds
      current_mil = time.time()*1000
      # if the direction is left
      if direction == "left":
         # get the left availability
         global _left_availability
         # if the tetromino is available for moving
         if current_mil > _left_availability or delay is None:
            # check if the tetromino can be moved in the given direction by using the
            # can_be_moved method defined below
            if not(self.can_be_moved(direction, game_grid, amount)):
               return False  # tetromino cannot be moved in the given direction
            # modify the position-related fields
            self.bottom_left_corner.x -= amount
            self.leftmost -= amount
            # move every tile in the tetromino to the left by the amount
            for row in range(n):
               for col in range(n):
                  if self.tile_matrix[row][col] != None:
                        self.tile_matrix[row][col].move(-amount, 0)
            # if the specified delay is not none, modify the left availability
            if delay is not None:
               _left_availability = current_mil + delay
            return True # successful move in the given direction
         else:
            return None # invalid operation
      # if the direction is right
      elif direction == "right":
         # get the right availability
         global _right_availability
         # if the tetromino is available for moving
         if current_mil > _right_availability or delay is None:
            # check if the tetromino can be moved in the given direction by using the
            # can_be_moved method defined below
            if not(self.can_be_moved(direction, game_grid, amount)):
               return False  # tetromino cannot be moved in the given direction
            # modify the position-related fields
            self.bottom_left_corner.x += amount
            self.leftmost += amount
            # move every tile in the tetromino to the right by the amount
            for row in range(n):
               for col in range(n):
                  if self.tile_matrix[row][col] != None:
                     self.tile_matrix[row][col].move(amount, 0)
            # if the specified delay is not none, modify the right availability
            if delay is not None:
               _right_availability = current_mil + delay
            return True # successful move in the given direction
         else:
            return None # invalid operation
      # if the direction is down
      elif direction == "down":
         # get the down and standart moving availability
         global _down_availability
         global _standart_availability
         # if the tetromino is available for moving
         if current_mil > (_standart_availability if standart else _down_availability) or delay is None:
            # check if the tetromino can be moved in the given direction by using the
            # can_be_moved method defined below
            if not(self.can_be_moved(direction, game_grid, amount)):
               return False  # tetromino cannot be moved in the given direction
            # modify the position-related field
            self.bottom_left_corner.y -= amount
            # move every tile in the tetromino down by the amount
            for row in range(n):
               for col in range(n):
                  if self.tile_matrix[row][col] != None:
                     self.tile_matrix[row][col].move(0, -amount)
            # if the specified delay is not none, modify the related availability
            if delay is not None:
               if standart:
                  _standart_availability = current_mil + delay
               else:
                  _down_availability = current_mil + delay
            return True # successful move in the given direction
         else:
            return None # invalid operation
      # if the direction is up
      else:
         # check if the tetromino can be moved in the given direction by using the
         # can_be_moved method defined below
         if not(self.can_be_moved(direction, game_grid, amount)):
            return False  # tetromino cannot be moved in the given direction
         # modify the position-related field
         self.bottom_left_corner.y += amount
         # move every tile in the tetromino up by the amount
         for row in range(n):
            for col in range(n):
               if self.tile_matrix[row][col] != None:
                  self.tile_matrix[row][col].move(0, amount)
         return True # successful move in the given direction
   
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
   
   # Method for copying the tile matrix, user can specify new bottom-left-corner positions
   def copy_grid(self, ghost=False, blcx=None, blcy=None, trim=None):
      # get the tile matrix
      matrix = self.tile_matrix if trim is None else self.trim()
      
      # copy the matrix
      copy_matrix = matrix.copy()
      # create a new empty array with the same shape of copied matrix
      new_tile_matrix = np.full(copy_matrix.shape, None)

      # specify the bottom-left-corner positions
      blc_x = self.bottom_left_corner.x if blcx is None else blcx
      blc_y = self.bottom_left_corner.y if blcy is None else blcy

      # get the dimensions of the copied array
      (nrows, ncols) = copy_matrix.shape

      # iterate over every cell
      for i in range(nrows):
         for j in range(ncols):
            # if the current cell has a tile init
            if copy_matrix[i][j] != None:
               # create the position object
               position = Point()
               position.x = blc_x + j
               position.y = blc_y + (nrows - 1) - i

               # copy the tile
               new_tile_matrix[i][j] = copy_matrix[i][j].copy(position, ghost)
      # return the new tile matrix
      return new_tile_matrix

   # Method for copying the current tetromino
   def copy(self, ghost=False, blcx=None, blcy=None, trim=None):
      # initalize the grid
      grid = self.copy_grid(ghost, blcx, blcy, trim)
      # create and return a copy of current tetromino
      return Tetromino(self.type, self.grid_height, self.grid_width, self.bottom_left_corner.x, self.bottom_left_corner.y, ghost, grid)

   # Method for trimming the empty rows and columns in the tile matrix
   def trim(self):
      # create a new array with the row and column count of current tetromino
      new_arr = np.full((self.row_count, self.column_count), None)
      # fill the new array with the non-empty rows and columns
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
      # return the new array
      return new_arr
