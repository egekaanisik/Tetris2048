#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# add the current directory to the system path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import stddraw # the stddraw module is used as a basic graphics library
from color import Color # used for coloring the tile and the number on it
from point import Point # used for representing the position of the tile
import random # used for getting random objects
import copy as cp # the copy module is used for copying tile positions

# Class used for representing numbered tiles as in 2048
class Tile: 
   # Class attributes shared among all Tile objects
   # ---------------------------------------------------------------------------
   # value used for the thickness of the boxes (boundaries) around the tiles
   boundary_thickness = 0.004
   # font family and size used for displaying the tile number
   font_family, font_size = "Arial", 12

   # Constructor that creates a tile at a given position, game mode, number, and type. Tile can be a ghost as well.
   def __init__(self, position=Point(0, 0), gamemode=None, ghost=None, number=None, type=None): # (0, 0) is the default position
      # set the background and boundary color if the game mode is classic tetris
      if gamemode == "tetris":
         # set the colors based on the tetromino shape
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
         # set the number to None
         self.number = None
      # set all the colors and number if the game mode is tetris 2048
      else:
         # give number to the tile if tile is not ghost
         if not ghost:
            # if there is no number specified in construction of tile, give it a random number
            # which can be 2 or 4 only
            num = None
            if number is None:
               num = random.randint(1,2) * 2
            else:
               num = number
            
            # change number as well as its colors
            self.change_number(num)
         # give only a background color and boundary color if the tile is ghost
         else:
            self.background_color = Color(198,184,171)
            self.boundary_color = Color(158,138,120) 

      # set the fields
      self.position = cp.copy(position)
      self.gamemode = gamemode
      self.ghost = ghost
      self.type = type

   # Setter method for the position of the tile
   def set_position(self, position):
      # set the position of the tile as the given position
      self.position = cp.copy(position) 

   # Getter method for the position of the tile
   def get_position(self):
      # return the position of the tile
      return cp.copy(self.position) 

   # Method for moving the tile by dx along the x axis and by dy along the y axis
   def move(self, dx, dy):
      self.position.translate(dx, dy)

   # Method for changing the number on the tile as well as its colors. (2048 mode only.)
   def change_number(self, number):
      # change the number
      self.number = number

      # change the background color based on the number
      if self.number == 2:
         self.background_color = Color(239,230,221)
      elif self.number == 4:
         self.background_color = Color(239,227,205)
      elif self.number == 8:
         self.background_color = Color(245,179,127)
      elif self.number == 16:
         self.background_color = Color(247,152,107)
      elif self.number == 32:
         self.background_color = Color(247,124,90)
      elif self.number == 64:
         self.background_color = Color(247,93,59)
      elif self.number == 128:
         self.background_color = Color(239,205,115)
      elif self.number == 256:
         self.background_color = Color(239,206,99)
      elif self.number == 512:
         self.background_color = Color(239,198,82)
      elif self.number == 1024:
         self.background_color = Color(238,198,66)
      elif self.number == 2048:
         self.background_color = Color(239,194,49)
      else:
         self.background_color = Color(61,58,51)

      # change the foreground color based on the number
      if self.number < 8:
         self.foreground_color = Color(121,114,104)
      else:
         self.foreground_color = Color(255,255,255)

      # change the boundary color
      self.boundary_color = Color(188,174,161)

   # Method for drawing the tile
   def draw(self):
      # draw the tile as a filled square
      if self.background_color == None or self.boundary_color == None:
         return
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(self.position.x, self.position.y, 0.5)
      # draw the bounding box of the tile as a square
      stddraw.setPenColor(self.boundary_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(self.position.x, self.position.y, 0.5)
      stddraw.setPenRadius()  # reset the pen radius to its default value

      # draw the number on the tile
      if self.gamemode == "2048" and self.ghost == False:
         stddraw.setPenColor(self.foreground_color)
         stddraw.setFontFamily(Tile.font_family)
         stddraw.setFontSize(Tile.font_size)
         stddraw.boldText(self.position.x, self.position.y, str(self.number))
   
   # Method for copying the tile, user can specify a new position to the copied tile 
   def copy(self, position=None, ghost=None):
      gh = ghost if ghost is not None else self.ghost
      if position == None:
         return Tile(self.position, self.gamemode, gh, self.number, self.type)
      else:
         return Tile(position, self.gamemode, gh, self.number, self.type)
