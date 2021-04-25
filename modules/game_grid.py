#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# add the current directory to the system path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import stddraw # the stddraw module is used as a basic graphics library
from color import Color # used for coloring the game grid
import numpy as np # fundamental Python module for scientific computing

# Class used for modelling the game grid
class GameGrid:
	# Constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w, gamemode, difficulty):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # set the game mode and difficulty
      self.gamemode = gamemode
      self.difficulty = difficulty
      # set the old high score
      self.old_high_score = None
      # create the tile matrix to store the tiles placed on the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      # the tetromino that is currently ghost
      self.current_ghost = None
      # game_over flag shows whether the game is over/completed or not
      self.game_over = False
      # set the initial score
      self.score = 0
      # create a new high score field to hold if the new score is highest
      self.new_high_score = None
      # create fields to hold upcoming tetrominoes
      self.next_tetromino1 = None
      self.next_tetromino2 = None
      self.next_tetromino3 = None

      # if the game mode is classic tetris
      if gamemode == "tetris":
         # set the color used for the empty grid cells
         self.empty_cell_color = Color(0, 0, 0)
         self.background_color = Color(0, 0, 0)
         # set the colors used for the grid lines and the grid boundaries
         self.line_color = Color(30, 30, 30) 
         self.boundary_color = Color(30, 30, 30)
      # if the game mode is tetris 2048
      else:
         self.background_color = Color(255,251,239)
         # set the color used for the empty grid cells
         self.empty_cell_color = Color(214,205,196)
         # set the colors used for the grid lines and the grid boundaries
         self.line_color = Color(188,174,161) 
         self.boundary_color = Color(158,138,120)
         self.reached_2048 = False
      # thickness values used for the grid lines and the grid boundaries 
      self.line_thickness = 0.002
      self.box_thickness = 8 * self.line_thickness

   # Method used for displaying the game grid
   def display(self, delay=0):
      # clear the background canvas to empty_cell_color
      stddraw.clear(self.background_color)
      # draw a box around the game grid 
      self.draw_boundaries()
      # draw the game grid
      self.draw_grid()
      # draw the current (active) tetromino ghost
      if self.current_ghost != None:
         self.current_ghost.draw()
      
      # draw the current (active) tetromino
      if self.current_tetromino != None:
         self.current_tetromino.draw()
      
      # draw the normal game cycle GUI
      if not self.game_over:
         # set pen color based on game mode
         if self.gamemode == "tetris":
            stddraw.setPenColor(stddraw.WHITE)
         else:
            stddraw.setPenColor(self.boundary_color)

         # set font and its size
         stddraw.setFontFamily("Arial")
         stddraw.setFontSize(24)

         # draw score
         if self.gamemode == "2048" and self.reached_2048:
            stddraw.boldText(13.75, 19, "Congrats!")
            stddraw.text(13.75, 17.75, "Score")
            stddraw.boldText(13.75, 16.75, str(self.score))
         else:
            stddraw.text(13.75, 19, "Score")
            stddraw.boldText(13.75, 18, str(self.score))

         # draw upcoming tetrominoes
         stddraw.text(13.75, 15, "Upcoming")
         stddraw.text(13.75, 14, "Tetrominoes")
         stddraw.setPenColor(self.boundary_color)
         stddraw.filledRectangle(12,-0.25,3.5,13.5)
         stddraw.setPenRadius(0.001)
         if self.gamemode == "tetris":
            stddraw.setPenColor(stddraw.DARK_GRAY)
         else:
            stddraw.setPenColor(self.empty_cell_color)
         stddraw.line(12.25, 8.75, 15.25, 8.75)
         stddraw.line(12.25, 4.25, 15.25, 4.25)
         self.next_tetromino1.copy(blcx=(14.25 - (self.next_tetromino1.column_count/2)),blcy=9.5 + (4-self.next_tetromino1.row_count)/2,trim=True).draw()
         self.next_tetromino2.copy(blcx=(14.25 - (self.next_tetromino2.column_count/2)),blcy=5 + (4-self.next_tetromino2.row_count)/2,trim=True).draw()
         self.next_tetromino3.copy(blcx=(14.25 - (self.next_tetromino3.column_count/2)),blcy=0.5 + (4-self.next_tetromino3.row_count)/2,trim=True).draw()

         # show the canvas
         stddraw.show(delay)
      # draw the game over GUI
      else:
         # set pen color based on game mode
         if self.gamemode == "tetris":
            stddraw.setPenColor(stddraw.WHITE)
         else:
            stddraw.setPenColor(self.boundary_color)
         
         # set font and its size
         stddraw.setFontFamily("Arial")
         stddraw.setFontSize(24)

         # draw game over text and and final score
         stddraw.text(13.75, 12, "Game Over!")
         stddraw.text(13.75, 10, "Final Score:")
         stddraw.boldText(13.75, 9, str(self.score))

         # draw the high score conclusion
         stddraw.setFontSize(18)
         if self.score > self.old_high_score:
            stddraw.text(13.75, 7.75, "New High Score!")
            self.new_high_score = self.score
         else:
            stddraw.text(13.75, 7.75, "High Score:")
            stddraw.boldText(13.75, 7, str(self.old_high_score))

         # draw the after-game controls
         stddraw.setFontSize(16)
         stddraw.text(13.75,2,"Press R to")
         stddraw.text(13.75,1.5,"restart the game,")
         stddraw.text(13.75,1,"or press Enter to")
         stddraw.text(13.75,0.5,"return to the")
         stddraw.text(13.75,0,"main manu.")

         # show the canvas
         stddraw.show(delay)
         
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

   # Method for checking line for having an empty cell
   def has_line_empty_cell(self, line):
      # If line has None, that means it has an empty cell
      if None in self.tile_matrix[line]:
         return True
      else:
         False

   # Method for deleting the lines that is all occupied
   def delete_full_lines(self, clear):
      paint_indexes = []
      indexes = []
      # check every line for having an empty cell
      for i in range(self.grid_height):
         # if that line do not have any empty cells
         if not self.has_line_empty_cell(i):
            # add the line index to the lines to be painted
            paint_indexes.append(i)
            # add the line index - length of all indexes before to delete the line by its updated index
            indexes.append(i - len(indexes))

      # if there is full lines, begin deleting
      if len(indexes) != 0:
         # play the effect
         clear.play()
         
         # if the game mode is classic tetris
         if self.gamemode == "tetris":
            # update the score
            self.score += (1200 if len(indexes) == 4 else (300 if len(indexes) == 3 else (100 if len(indexes) == 2 else 40))) * (self.difficulty+1)

            # update the color of every tile in the line to go from white to black
            for color in reversed(range(0, 256, 4)):
               for l in paint_indexes:
                  for k in range(self.grid_width):
                     self.tile_matrix[l][k].background_color = Color(color, color, color)
                     self.tile_matrix[l][k].boundary_color = Color(color, color, color)
                     self.tile_matrix[l][k].foreground_color = Color(color, color, color)
               self.display()
         # if the game mode is tetris 2048
         else:
            # update the color of every tile in the line to white and get the number on every tile to set score
            for l in paint_indexes:
               line_score = 0
               for k in range(self.grid_width):
                  line_score += self.tile_matrix[l][k].number
                  self.tile_matrix[l][k].background_color = Color(255,255,255)
                  self.tile_matrix[l][k].boundary_color = Color(255,255,255)
                  self.tile_matrix[l][k].foreground_color = Color(255,255,255)
               self.score += (line_score * (self.difficulty + 1))
            self.display()
            
            # update the color of every tile in the line to go from white to the background color
            for color in reversed(range(215, 256, 5)):
               for l in paint_indexes:
                  for k in range(self.grid_width):
                     self.tile_matrix[l][k].background_color = Color(color, color-10, color-20)
                     self.tile_matrix[l][k].boundary_color = Color(color, color-10, color-20)
                     self.tile_matrix[l][k].foreground_color = Color(color, color-10, color-20)
               self.display()
            
            # make the color of every tile None
            for l in paint_indexes:
                  for k in range(self.grid_width):
                     self.tile_matrix[l][k].background_color = None

         # delete the full lines and add new empty lines on the top of the grid
         for r in indexes:
            self.tile_matrix = np.delete(self.tile_matrix, (r), axis=0)
            self.tile_matrix = np.append(self.tile_matrix, np.full((1, self.grid_width), None), axis=0)
            
            # move every tile above the deleted line down
            for i in range(r, self.grid_height):
               for j in range(self.grid_width):
                  if self.tile_matrix[i][j] != None:
                     self.tile_matrix[i][j].move(0, -1)

   # Method for merging the tiles that have the same number and on top of each other, after every merging,
   # it also move down the floating tiles and check the tiles again to make the chain merge happen
   def check_line_chain_merge(self, merge):
      # copy the matrix and rotate it 90 degrees
      matrix = self.tile_matrix.copy()
      rotated = np.rot90(matrix)

      # loop through every tile until there is no merging to happen
      while True:
         # for every line on the rotated matrix
         for i in range(len(rotated)):
            # check the line until there is no merging to happen
            while True:
               # set an indicator
               have_dupes = False

               # check every tile
               for j in range(len(rotated[i]) - 1):
                  # if there are tiles on top of each other
                  if rotated[i][j] != None and rotated[i][j+1] != None:
                     # if the tiles have same number on them
                     if rotated[i][j].number == rotated[i][j+1].number:
                        # play the effect
                        merge.play()

                        # update the color of tiles to white
                        rotated[i][j].background_color = Color(255,255,255)
                        rotated[i][j].boundary_color = Color(255,255,255)
                        rotated[i][j].foreground_color = Color(255,255,255)
                        rotated[i][j+1].background_color = Color(255,255,255)
                        rotated[i][j+1].boundary_color = Color(255,255,255)
                        rotated[i][j+1].foreground_color = Color(255,255,255)
                        self.tile_matrix = np.rot90(rotated, -1)
                        self.display()
                        
                        # update the color of tiles from white to the background color
                        for color in reversed(range(215, 256, 5)):
                           rotated[i][j].background_color = Color(color, color-10, color-20)
                           rotated[i][j].boundary_color = Color(color, color-10, color-20)
                           rotated[i][j].foreground_color = Color(color, color-10, color-20)
                           rotated[i][j+1].background_color = Color(color, color-10, color-20)
                           rotated[i][j+1].boundary_color = Color(color, color-10, color-20)
                           rotated[i][j+1].foreground_color = Color(color, color-10, color-20)
                           self.tile_matrix = np.rot90(rotated, -1)
                           self.display()

                        # make the upper tile invisible
                        rotated[i][j+1].background_color = None
                        rotated[i][j+1].boundary_color = None
                        rotated[i][j+1].foreground_color = None

                        # set the have duplicate tiles indicator to true to malke to loop run again
                        have_dupes = True

                        # change the number of bottom tile and add the number to the score
                        rotated[i][j].change_number(rotated[i][j].number*2)
                        self.score += rotated[i][j].number * (self.difficulty+1)

                        # if the number is 2048, set the related field to true
                        if rotated[i][j].number == 2048:
                           self.reached_2048 = True
                        
                        # delete the upper tile
                        rotated[i][j+1] = None

                        # update the tile matrix
                        self.tile_matrix = np.rot90(rotated, -1)
                        self.display()
                        break
               # if there are no duplicate tiles, go to the next line
               if not have_dupes:
                  break
         # check if there are floating tiles and move them down
         have_floating = self.move_floating_tiles()

         # if there are no floating tiles, break the loop, otherwise, check the matrix again
         if not have_floating:
            break

      # clear user interactions
      stddraw.clearKeysTyped()
      stddraw.clearMousePresses()

   # Method for moving the tiles that are not connected to the bottom of the game grid
   def move_floating_tiles(self):
      # binarize the tile matrix
      arr = self.binarize_tile_matrix()

      # label the binarized array by the 4-connected labeling method
      array, label_count = self.label_array(arr)

      # delete the excess columns and lines that are added to make the labeling happen
      first_line_removed = np.delete(array, 0, axis=0)
      base_line_removed = np.delete(first_line_removed, 0, axis=0)
      last_line_removed = np.delete(base_line_removed, base_line_removed.shape[0]-1, axis=0)
      first_column_removed = np.delete(last_line_removed, 0, axis=1)
      trimmed = np.delete(first_column_removed, first_column_removed.shape[1]-1, axis=1)

      # get the shape of the labeled and trimmed array
      (nrows, ncols) = trimmed.shape

      # move down every tile that has a different label from the bottomest tiles' label
      for i in range(nrows):
         for j in range(ncols):
            if trimmed[i][j] != 1 and trimmed[i][j] != 0:
               self.move_tile_down(i, j)

      # return true if there are tiles that are not connected to the bottom
      return True if label_count > 1 else False
   
   # Method for dropping the tile to bottom until it reaches a tile or bottom
   def move_tile_down(self, i, j):
      index = 0
      # loop until the bottom of the tile do not touch another tile or bottom
      while True:
         if self.tile_matrix[i-(index+1)][j] == None and i-index != 0:
            # move down the tile
            self.tile_matrix[i-index][j].move(0, -1)
            self.tile_matrix[i-(index+1)][j] = self.tile_matrix[i-index][j]
            self.tile_matrix[i-index][j] = None
            # display the canvas each time
            self.display(delay=50)
            index += 1
         else:
            break
               
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

   # Method for binarizing the tile matrix
   # The cells that are empty becomes 0 and the cells that have tiles becomes 1
   def binarize_tile_matrix(self):
      # get the shape of the tile matrix
      (nrows, ncols) = self.tile_matrix.shape

      # create a new array filled with zeros that has the 2 more columns and 3 more rows
      arr = np.full((nrows+3, ncols+2), 0)

      # make a base line filled with ones to understand the tiles that are connected to bottom
      arr[1] = np.full((1,ncols+2), 1)
      arr[1][0] = 0
      arr[1][ncols+1] = 0

      # make the non-empty cells one
      for i in range(nrows):
         for j in range(ncols):
            if self.tile_matrix[i][j] != None:
               arr[i+2][j+1] = 1

      # return binarized array
      return arr

   # Method for labeling the binarized tile matrix to distinguish the tiles that are not connected to the bottom
   # of the matrix
   def label_array(self, binarized):
      max_label = int(10000)
      nrow = binarized.shape[0]
      ncol = binarized.shape[1]

      # create a new array that will hold the labels and that has the same shape with the binarized array
      im = np.full(shape=(nrow,ncol), dtype = int, fill_value=max_label)

      # create an label holder array
      a = np.arange(0,max_label, dtype = int)

      k = 0
      # start labeling by checking connected tiles
      for i in range(1, nrow - 1):
         for j in range(1, ncol - 1):
            # get the related tiles
            c   = binarized[i][j]
            label_u  = im[i-1][j]
            label_l  = im[i][j-1]

            # check if the tile exists
            if c == 1:
               # get the minimum labeled tile around the current one
               min_label = min(label_u, label_l)
                    
               # if the minimum labeled tile has the maximum label value, give it a temp value
               # else, update the array with the label
               if min_label == max_label:  # u = l = 0
                  k += 1
                  im[i][j] = k
               else:
                  im[i][j] = min_label
                  if min_label != label_u and label_u != max_label:
                     self.update_labeled_array(a, min_label, label_u)

                  if min_label != label_l and label_l != max_label:
                     self.update_labeled_array(a, min_label, label_l)


      # initialize an array for labels
      labels = []

      # final reduction in the label array, also add the labels into the label list
      for i in range(k+1):
         index = i
         while a[index] != index:
            index = a[index]
         a[i] = a[index]
         labels.append(a[i])

      # Removes duplicates drom the list
      labels = list(dict.fromkeys(labels))
      labels.pop(0)
   
      # second pass to resolve labels
      for i in range(nrow):
         for j in range(ncol):
            if binarized[i][j] == 1 and im[i][j] != max_label:
                im[i][j] = a[im[i][j]]
            else:
                im[i][j] = 0

      # return the labeled array, label list
      return im, len(labels)

   def update_labeled_array(self, a, label1, label2):
      index = lab_small = lab_large = 0
      if label1 < label2 :
         lab_small = label1
         lab_large = label2
      else:
         lab_small = label2
         lab_large = label1
      index = lab_large
      while index > 1 and a[index] != lab_small:
         if a[index] < lab_small:
            temp = index
            index = lab_small
            lab_small = a[temp]
         elif a[index] > lab_small:
            temp = a[index]
            a[index] = lab_small
            index = temp
         else:
            break
      