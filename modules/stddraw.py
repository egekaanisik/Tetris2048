#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
stddraw.py

The stddraw module defines functions that allow the user to create a
drawing.  A drawing appears on the canvas.  The canvas appears
in the window.  As a convenience, the module also imports the
commonly used Color objects defined in the color module.
"""

import os
import sys

# Adds the current directory to the system path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import color
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import pygame.gfxdraw
import pygame.font

import tkinter as Tkinter
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as tkFileDialog
	
#-----------------------------------------------------------------------

# Define colors so clients need not import the color module.

from color import WHITE
from color import BLACK
from color import RED
from color import GREEN
from color import BLUE
from color import CYAN
from color import MAGENTA
from color import YELLOW
from color import DARK_RED
from color import DARK_GREEN
from color import DARK_BLUE
from color import GRAY
from color import DARK_GRAY
from color import LIGHT_GRAY
from color import ORANGE
from color import VIOLET
from color import PINK
from color import BOOK_BLUE
from color import BOOK_LIGHT_BLUE
from color import BOOK_RED

#-----------------------------------------------------------------------

# Default Sizes and Values

_BORDER = 0.0
#_BORDER = 0.05
_DEFAULT_XMIN = 0.0
_DEFAULT_XMAX = 1.0
_DEFAULT_YMIN = 0.0
_DEFAULT_YMAX = 1.0
_DEFAULT_CANVAS_SIZE = 512
_DEFAULT_PEN_RADIUS = .005  # Maybe change this to 0.0 in the future.
_DEFAULT_PEN_COLOR = color.BLACK
_DEFAULT_WINDOW_TITLE = 'stddraw window (press s to save)'
_DEFAULT_CLOSE_ACTION = sys.exit
_DEFAULT_CLOSE_ARGS = []

_DEFAULT_FONT_FAMILY = 'Helvetica'
_DEFAULT_FONT_SIZE = 12

_xmin = None
_ymin = None
_xmax = None
_ymax = None

_fontFamily = _DEFAULT_FONT_FAMILY
_fontSize = _DEFAULT_FONT_SIZE

_canvasWidth = float(_DEFAULT_CANVAS_SIZE)
_canvasHeight = float(_DEFAULT_CANVAS_SIZE)
_penRadius = None
_penColor = _DEFAULT_PEN_COLOR
_close_action = _DEFAULT_CLOSE_ACTION
_close_args = _DEFAULT_CLOSE_ARGS
_save_key = None
_keysTyped = []
_keysReleased = []

# Has the window been created?
_windowCreated = False

#-----------------------------------------------------------------------
# Begin added by Alan J. Broder
#-----------------------------------------------------------------------

# Keep track of mouse status

# Has the mouse been left-clicked since the last time we checked?
_mouseLeftPressed = False
_mouseRightPressed = False
_mouseScrollPressed = False
_mouseLeftHeld = False
_mouseRightHeld = False
_mouseScrollHeld = False

# The position of the mouse as of the most recent mouse click
_mouseLeftPos = None
_mouseRightPos = None
_mouseScrollPos = None
_mouseTrack = None
 
#-----------------------------------------------------------------------
# End added by Alan J. Broder
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

def _pygameColor(c):
    """
    Convert c, an object of type color.Color, to an equivalent object
    of type pygame.Color.  Return the result.
    """
    r = c.getRed()
    g = c.getGreen()
    b = c.getBlue()
    return pygame.Color(r, g, b)

#-----------------------------------------------------------------------

# Private functions to scale and factor X and Y values.

def _scaleX(x):
    return _canvasWidth * (x - _xmin) / (_xmax - _xmin)

def _scaleY(y):
    return _canvasHeight * (_ymax - y) / (_ymax - _ymin)

def _factorX(w):
    return w * _canvasWidth / abs(_xmax - _xmin)

def _factorY(h):
    return h * _canvasHeight / abs(_ymax - _ymin)

#-----------------------------------------------------------------------
# Begin added by Alan J. Broder
#-----------------------------------------------------------------------

def _userX(x):
    return _xmin + x * (_xmax - _xmin) / _canvasWidth

def _userY(y):
    return _ymax - y * (_ymax - _ymin) / _canvasHeight

#-----------------------------------------------------------------------
# End added by Alan J. Broder
#-----------------------------------------------------------------------
    
#-----------------------------------------------------------------------

def setCanvasSize(w=_DEFAULT_CANVAS_SIZE, h=_DEFAULT_CANVAS_SIZE):
    """
    Set the size of the canvas to w pixels wide and h pixels high.
    Calling this function is optional. If you call it, you must do
    so before calling any drawing function.
    """
    global _background
    global _surface
    global _canvasWidth
    global _canvasHeight
    global _windowCreated

    if _windowCreated:
        raise Exception('The stddraw window already was created')

    if (w < 1) or (h < 1):
        raise Exception('width and height must be positive')

    _canvasWidth = w
    _canvasHeight = h
    _background = pygame.display.set_mode([w, h])
    pygame.display.set_caption(_DEFAULT_WINDOW_TITLE)
    _surface = pygame.Surface((w, h))
    _surface.fill(_pygameColor(WHITE))
    _windowCreated = True

def setXscale(min=_DEFAULT_XMIN, max=_DEFAULT_XMAX):
    """
    Set the x-scale of the canvas such that the minimum x value
    is min and the maximum x value is max.
    """
    global _xmin
    global _xmax
    min = float(min)
    max = float(max)
    if min >= max:
        raise Exception('min must be less than max')
    size = max - min
    _xmin = min - _BORDER * size
    _xmax = max + _BORDER * size

def setYscale(min=_DEFAULT_YMIN, max=_DEFAULT_YMAX):
    """
    Set the y-scale of the canvas such that the minimum y value
    is min and the maximum y value is max.
    """
    global _ymin
    global _ymax
    min = float(min)
    max = float(max)
    if min >= max:
        raise Exception('min must be less than max')
    size = max - min
    _ymin = min - _BORDER * size
    _ymax = max + _BORDER * size

#-----------------------------------------------------------------------
# Begin added by Ege Kaan Isik
#-----------------------------------------------------------------------

def setWindowTitle(title=_DEFAULT_WINDOW_TITLE):
    """
    Set the title of canvas window.
    """
    pygame.display.set_caption(title)

def setWindowIcon(path=None):
    """
    Set the icon of canvas window.
    """
    programIcon = pygame.image.load(path)
    pygame.display.set_icon(programIcon)

def setCloseAction(func=_DEFAULT_CLOSE_ACTION, args=_DEFAULT_CLOSE_ARGS):
    """
    Set what is going to happen after the termination of canvas window.
    """
    global _close_action
    global _close_args
    _close_action = func
    _close_args = args

#-----------------------------------------------------------------------
# End added by Ege Kaan Isik
#-----------------------------------------------------------------------

def setPenRadius(r=_DEFAULT_PEN_RADIUS):
    """
    Set the pen radius to r, thus affecting the subsequent drawing
    of points and lines. If r is 0.0, then points will be drawn with
    the minimum possible radius and lines with the minimum possible
    width.
    """
    global _penRadius
    r = float(r)
    if r < 0.0:
        raise Exception('Argument to setPenRadius() must be non-neg')
    _penRadius = r * float(_DEFAULT_CANVAS_SIZE)

def setPenColor(c=_DEFAULT_PEN_COLOR):
    """
    Set the pen color to c, where c is an object of class color.Color.
    c defaults to stddraw.BLACK.
    """
    global _penColor
    _penColor = c

def setFontFamily(f=_DEFAULT_FONT_FAMILY):
    """
    Set the font family to f (e.g. 'Helvetica' or 'Courier').
    """
    global _fontFamily
    _fontFamily = f

def setFontSize(s=_DEFAULT_FONT_SIZE):
    """
    Set the font size to s (e.g. 12 or 16).
    """
    global _fontSize
    _fontSize = s

#-----------------------------------------------------------------------

def _makeSureWindowCreated():
    global _windowCreated
    if not _windowCreated:
        setCanvasSize()
        _windowCreated = True

#-----------------------------------------------------------------------

# Functions to draw shapes, text, and images on the background canvas.

def _pixel(x, y):
    """
    Draw on the background canvas a pixel at (x, y).
    """
    _makeSureWindowCreated()
    xs = _scaleX(x)
    xy = _scaleY(y)
    pygame.gfxdraw.pixel(
        _surface,
        int(round(xs)),
        int(round(xy)),
        _pygameColor(_penColor))

def point(x, y):
    """
    Draw on the background canvas a point at (x, y).
    """
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    # If the radius is too small, then simply draw a pixel.
    if _penRadius <= 1.0:
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.ellipse(
            _surface,
            _pygameColor(_penColor),
            pygame.Rect(
                xs-_penRadius,
                ys-_penRadius,
                _penRadius*2.0,
                _penRadius*2.0),
            0)

def line(x0, y0, x1, y1):
    """
    Draw on the background canvas a line from (x0, y0) to (x1, y1).
    """
    
    _makeSureWindowCreated()

    x0 = float(x0)
    y0 = float(y0)
    x1 = float(x1)
    y1 = float(y1)

    lineWidth = _penRadius
    if lineWidth == 0.0: lineWidth = 1.0
    x0s = _scaleX(x0)
    y0s = _scaleY(y0)
    x1s = _scaleX(x1)
    y1s = _scaleY(y1)
    pygame.draw.line(
       _surface,
       _pygameColor(_penColor),
       (x0s, y0s),
       (x1s, y1s),
       int(round(lineWidth)))

def circle(x, y, r):
    """
    Draw on the background canvas a circle of radius r centered on
    (x, y).
    """
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    r = float(r)
    ws = _factorX(2.0*r)
    hs = _factorY(2.0*r)
    # If the radius is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.ellipse(
            _surface,
            _pygameColor(_penColor),
            pygame.Rect(xs-ws/2.0, ys-hs/2.0, ws, hs),
            int(round(_penRadius)))

def filledCircle(x, y, r):
    """
    Draw on the background canvas a filled circle of radius r
    centered on (x, y).
    """
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    r = float(r)
    ws = _factorX(2.0*r)
    hs = _factorY(2.0*r)
    # If the radius is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.ellipse(
            _surface,
            _pygameColor(_penColor),
            pygame.Rect(xs-ws/2.0, ys-hs/2.0, ws, hs),
            0)

def rectangle(x, y, w, h):
    """
    Draw on the background canvas a rectangle of width w and height h
    whose lower left point is (x, y).
    """
    global _surface
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    ws = _factorX(w)
    hs = _factorY(h)
    # If the rectangle is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.rect(
            _surface,
            _pygameColor(_penColor),
            pygame.Rect(xs, ys-hs, ws, hs),
            int(round(_penRadius)))

def filledRectangle(x, y, w, h):
    """
    Draw on the background canvas a filled rectangle of width w and
    height h whose lower left point is (x, y).
    """
    global _surface
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    ws = _factorX(w)
    hs = _factorY(h)
    # If the rectangle is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.rect(
            _surface,
            _pygameColor(_penColor),
            pygame.Rect(xs, ys-hs, ws, hs),
            0)

def square(x, y, r):
    """
    Draw on the background canvas a square whose sides are of length
    2r, centered on (x, y).
    """
    _makeSureWindowCreated()
    rectangle(x-r, y-r, 2.0*r, 2.0*r)

def filledSquare(x, y, r):
    """
    Draw on the background canvas a filled square whose sides are of
    length 2r, centered on (x, y).
    """
    _makeSureWindowCreated()
    filledRectangle(x-r, y-r, 2.0*r, 2.0*r)

def polygon(x, y):
    """
    Draw on the background canvas a polygon with coordinates
    (x[i], y[i]).
    """
    global _surface
    _makeSureWindowCreated()
    # Scale X and Y values.
    xScaled = []
    for xi in x:
        xScaled.append(_scaleX(float(xi)))
    yScaled = []
    for yi in y:
        yScaled.append(_scaleY(float(yi)))
    points = []
    for i in range(len(x)):
        points.append((xScaled[i], yScaled[i]))
    points.append((xScaled[0], yScaled[0]))
    pygame.draw.polygon(
        _surface,
        _pygameColor(_penColor),
        points,
        int(round(_penRadius)))

def filledPolygon(x, y):
    """
    Draw on the background canvas a filled polygon with coordinates
    (x[i], y[i]).
    """
    global _surface
    _makeSureWindowCreated()
    # Scale X and Y values.
    xScaled = []
    for xi in x:
        xScaled.append(_scaleX(float(xi)))
    yScaled = []
    for yi in y:
        yScaled.append(_scaleY(float(yi)))
    points = []
    for i in range(len(x)):
        points.append((xScaled[i], yScaled[i]))
    points.append((xScaled[0], yScaled[0]))
    pygame.draw.polygon(_surface, _pygameColor(_penColor), points, 0)

def text(x, y, s):
    """
    Draw string s on the background canvas centered at (x, y).
    """
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    xs = _scaleX(x)
    ys = _scaleY(y)
    font = pygame.font.SysFont(_fontFamily, _fontSize)
    text = font.render(s, 1, _pygameColor(_penColor))
    textpos = text.get_rect(center=(xs, ys))
    _surface.blit(text, textpos)

def boldText(x, y, s):
    """
    Draw string s as a bold text on the background canvas centered at (x, y).
    """
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    xs = _scaleX(x)
    ys = _scaleY(y)
    font = pygame.font.SysFont(_fontFamily, _fontSize, True)
    text = font.render(s, 1, _pygameColor(_penColor))
    textpos = text.get_rect(center=(xs, ys))
    _surface.blit(text, textpos)

def picture(pic, x=None, y=None):
    """
    Draw pic on the background canvas centered at (x, y).  pic is an
    object of class picture.Picture. x and y default to the midpoint
    of the background canvas.
    """
    global _surface
    _makeSureWindowCreated()
    # By default, draw pic at the middle of the surface.
    if x is None:
        x = (_xmax + _xmin) / 2.0
    if y is None:
        y = (_ymax + _ymin) / 2.0
    x = float(x)
    y = float(y)
    xs = _scaleX(x)
    ys = _scaleY(y)
    ws = pic.width()
    hs = pic.height()
    picSurface = pic._surface # violates encapsulation
    _surface.blit(picSurface, [xs-ws/2.0, ys-hs/2.0, ws, hs])

def clear(c=WHITE):
    """
    Clear the background canvas to color c, where c is an
    object of class color.Color. c defaults to stddraw.WHITE.
    """
    _makeSureWindowCreated()
    _surface.fill(_pygameColor(c))

def save(f):
    """
    Save the window canvas to file f.
    """
    _makeSureWindowCreated()

    #if sys.hexversion >= 0x03000000:
    #    # Hack because Pygame without full image support
    #    # can handle only .bmp files.
    #    bmpFileName = f + '.bmp'
    #    pygame.image.save(_surface, bmpFileName)
    #    os.system('convert ' + bmpFileName + ' ' + f)
    #    os.system('rm ' + bmpFileName)
    #else:
    #    pygame.image.save(_surface, f)

    pygame.image.save(_surface, f)

#-----------------------------------------------------------------------

def _show():
    """
    Copy the background canvas to the window canvas.
    """
    _background.blit(_surface, (0, 0))
    pygame.display.flip()
    _checkForEvents()

def _showAndWaitForever():
    """
    Copy the background canvas to the window canvas. Then wait
    forever, that is, until the user closes the stddraw window.
    """
    _makeSureWindowCreated()
    _show()
    QUANTUM = .1
    while True:
        time.sleep(QUANTUM)
        _checkForEvents()

def show(msec=float('inf')):
    """
    Copy the background canvas to the window canvas, and
    then wait for msec milliseconds. msec defaults to infinity.
    """
    if msec == float('inf'):
        _showAndWaitForever()

    _makeSureWindowCreated()
    _show()
    _checkForEvents()

    # Sleep for the required time, but check for events every
    # QUANTUM seconds.
    QUANTUM = .01
    sec = msec / 1000.0
    if sec < QUANTUM:
        time.sleep(sec)
        return
    secondsWaited = 0.0
    while secondsWaited < sec:
        time.sleep(QUANTUM)
        secondsWaited += QUANTUM
        _checkForEvents()

#-----------------------------------------------------------------------

def _saveToFile():
    """
    Display a dialog box that asks the user for a file name.  Save the
    drawing to the specified file.  Display a confirmation dialog box
    if successful, and an error dialog box otherwise.  The dialog boxes
    are displayed using Tkinter, which (on some computers) is
    incompatible with Pygame. So the dialog boxes must be displayed
    from child processes.
    """
    import subprocess
    _makeSureWindowCreated()

    stddrawPath = os.path.realpath(__file__)

    childProcess = subprocess.Popen(
        [sys.executable, stddrawPath, 'getFileName'],
        stdout=subprocess.PIPE)
    so, se = childProcess.communicate()
    fileName = so.strip()

    if sys.hexversion >= 0x03000000:
        fileName = fileName.decode('utf-8')

    if not fileName:
        return

    if not fileName.endswith(('.jpg', '.png')):
        fileName += ".png"

    try:
        save(fileName)
        childProcess = subprocess.Popen(
            [sys.executable, stddrawPath, 'confirmFileSave'])
    except (pygame.error) as e:
        childProcess = subprocess.Popen(
            [sys.executable, stddrawPath, 'reportFileSaveError', str(e)])

def _checkForEvents():
    """
    Check if any new event has occured (such as a key typed or button
    pressed).  If a key has been typed, then put that key in a queue.
    """
    global _surface
    global _keysTyped
    global _close_action
    global _close_args
    global _keysReleased
    global _save_key
    
    #-------------------------------------------------------------------
    # Begin added by Alan J. Broder
    #-------------------------------------------------------------------
    global _mouseLeftPos
    global _mouseRightPos
    global _mouseScrollPos
    global _mouseLeftPressed
    global _mouseRightPressed
    global _mouseScrollPressed
    global _mouseLeftHeld
    global _mouseRightHeld
    global _mouseScrollHeld
    global _mouseTrack
    #-------------------------------------------------------------------
    # End added by Alan J. Broder
    #-------------------------------------------------------------------
    
    _makeSureWindowCreated()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            func = _close_action
            func(*_close_args)
        elif (event.type == pygame.KEYUP) and _save_key is not None and (pygame.key.name(event.key) == _save_key):
            _saveToFile()
        elif event.type == pygame.KEYDOWN:
            _keysTyped = [pygame.key.name(event.key)] + _keysTyped
        elif event.type == pygame.KEYUP:
            _keysReleased = [pygame.key.name(event.key)] + _keysReleased
            
        #---------------------------------------------------------------
        # Begin added by Ege Kaan Isik
        #---------------------------------------------------------------
        # Every time the mouse button is pressed, remember
        # the mouse position as of that press.
        elif (event.type == pygame.MOUSEBUTTONDOWN) and \
            (event.button == 1): 
            _mouseLeftPressed = True
            _mouseLeftHeld = True
            _mouseLeftPos = event.pos
        elif (event.type == pygame.MOUSEBUTTONUP) and \
            (event.button == 1): 
            _mouseLeftHeld = False                   
        elif (event.type == pygame.MOUSEBUTTONDOWN) and \
            (event.button == 3): 
            _mouseRightPressed = True
            _mouseRightHeld = True
            _mouseRightPos = event.pos
        elif (event.type == pygame.MOUSEBUTTONUP) and \
            (event.button == 3): 
            _mouseRightHeld = False
        elif (event.type == pygame.MOUSEBUTTONDOWN) and \
            (event.button == 2): 
            _mouseScrollPressed = True
            _mouseScrollHeld = True
            _mouseScrollPos = event.pos
        elif (event.type == pygame.MOUSEBUTTONUP) and \
            (event.button == 2): 
            _mouseScrollHeld = False
        elif (event.type == pygame.MOUSEMOTION):
            _mouseTrack = event.pos
        
        #---------------------------------------------------------------
        # End added by Ege Kaan Isik
        #---------------------------------------------------------------

#-----------------------------------------------------------------------

# Functions for retrieving keys

#---------------------------------------------------------------
# Begin added by Ege Kaan Isik
#---------------------------------------------------------------

def setKeyRepeat(delay=0):
    """
    Set the key read delay in milliseconds to make the key can send multiple events.
    """
    pygame.key.set_repeat(delay)

def setSaveKey(key=None):
    """
    Set the key for saving the canvas as an image.
    """
    global _save_key
    _save_key = key

def hasNextKeyTyped():
    """
    Return True if the queue of the keys the user typed is not empty.
    Otherwise return False.
    """
    global _keysTyped
    return _keysTyped != []

def hasNextKeyReleased():
    """
    Return True if the queue of the keys the user released is not empty.
    Otherwise return False.
    """
    global _keysReleased
    return _keysReleased != []

def nextKeyTyped():
    """
    Remove the first key from the queue of the keys that the user typed,
    and return that key.
    """
    global _keysTyped
    return _keysTyped.pop()

def nextKeyReleased():
    """
    Remove the first key from the queue of the keys that the user released,
    and return that key.
    """
    global _keysReleased
    return _keysReleased.pop()

def clearKeysTyped():
    """
    Clear all the keys in the queue of the keys that the user typed.
    """
    global _keysTyped
    _keysTyped = []

def clearKeysReleased():
    """
    Clear all the keys in the queue of the keys that the user released.
    """
    global _keysReleased
    _keysReleased = []

def getKeysTyped():
    """
    Return all the keys in the queue of the keys that the user typed.
    """
    global _keysTyped
    return _keysTyped

def getKeysReleased():
    """
    Return all the keys in the queue of the keys that the user released.
    """
    global _keysReleased
    return _keysReleased

# Functions for dealing with mouse clicks

def mouseLeftPressed():
    """
    Return if the mouse left button is pressed, and if it is pressed, clear
    the mouse press.
    """
    global _mouseLeftPressed
    if _mouseLeftPressed:
        _mouseLeftPressed = False
        return True
    return False

def mouseRightPressed():
    """
    Return if the mouse right button is pressed, and if it is pressed, clear
    the mouse press.
    """
    global _mouseRightPressed
    if _mouseRightPressed:
        _mouseRightPressed = False
        return True
    return False

def mouseScrollPressed():
    """
    Return if the mouse scroll button is pressed, and if it is pressed, clear
    the mouse press.
    """
    global _mouseScrollPressed
    if _mouseScrollPressed:
        _mouseScrollPressed = False
        return True
    return False

def clearMousePresses():
    """
    Clear all the mouse presses.
    """
    global _mouseLeftPressed
    global _mouseRightPressed
    global _mouseScrollPressed
    _mouseLeftPressed = False
    _mouseRightPressed = False
    _mouseScrollPressed = False

def mouseLeftHeldDown():
    """
    Return if the mouse left button is pressed and not released. To clear the event as well,
    use mouseLeftPressed() instead.
    """
    global _mouseLeftHeld
    return _mouseLeftHeld

def mouseRightHeldDown():
    """
    Return if the mouse right button is pressed and not released. To clear the event as well,
    use mouseRightPressed() instead.
    """
    global _mouseRightHeld
    return _mouseRightHeld

def mouseScrollHeldDown():
    """
    Return if the mouse scroll button is pressed and not released. To clear the event as well,
    use mouseScrollPressed() instead.
    """
    global _mouseScrollHeld
    return _mouseScrollHeld

def mouseLeftX():
    """
    Return the x coordinate in user space of the location at
    which the mouse was most recently left-clicked. If a left-click
    hasn't happened yet, raise an exception, since mouseLeftX() shouldn't
    be called until mouseLeftPressed() returns True.
    """
    global _mouseLeftPos
    if _mouseLeftPos:
        return _userX(_mouseLeftPos[0])      
    raise Exception(
        "Can't determine mouse position if a click hasn't happened")
    
def mouseLeftY():
    """
    Return the y coordinate in user space of the location at
    which the mouse was most recently left-clicked. If a left-click
    hasn't happened yet, raise an exception, since mouseLeftY() shouldn't
    be called until mouseLeftPressed() returns True.
    """
    global _mouseLeftPos
    if _mouseLeftPos:
        return _userY(_mouseLeftPos[1]) 
    raise Exception(
        "Can't determine mouse position if a click hasn't happened")

def mouseRightX():
    """
    Return the x coordinate in user space of the location at
    which the mouse was most recently right-clicked. If a right-click
    hasn't happened yet, raise an exception, since mouseRightX() shouldn't
    be called until mouseRightPressed() returns True.
    """
    global _mouseRightPos
    if _mouseRightPos:
        return _userX(_mouseRightPos[0])      
    raise Exception(
        "Can't determine mouse position if a click hasn't happened")
    
def mouseRightY():
    """
    Return the y coordinate in user space of the location at
    which the mouse was most recently right-clicked. If a right-click
    hasn't happened yet, raise an exception, since mouseRightY() shouldn't
    be called until mouseRightPressed() returns True.
    """
    global _mouseRightPos
    if _mouseRightPos:
        return _userY(_mouseRightPos[1]) 
    raise Exception(
        "Can't determine mouse position if a click hasn't happened")

def mouseScrollX():
    """
    Return the x coordinate in user space of the location at
    which the mouse was most recently scroll-clicked. If a scroll-click
    hasn't happened yet, raise an exception, since mouseScrollX() shouldn't
    be called until mouseScrollPressed() returns True.
    """
    global _mouseScrollPos
    if _mouseScrollPos:
        return _userX(_mouseScrollPos[0])      
    raise Exception(
        "Can't determine mouse position if a click hasn't happened")
    
def mouseScrollY():
    """
    Return the y coordinate in user space of the location at
    which the mouse was most recently scroll-clicked. If a scroll-click
    hasn't happened yet, raise an exception, since mouseScrollY() shouldn't
    be called until mouseScrollPressed() returns True.
    """
    global _mouseScrollPos
    if _mouseScrollPos:
        return _userY(_mouseScrollPos[1]) 
    raise Exception(
        "Can't determine mouse position if a click hasn't happened")

def mouseMotionX():
    """
    Return the x coordinate of current mouse position.
    """
    global _mouseTrack
    if _mouseTrack is not None:
        return _userX(_mouseTrack[0])
    else: return None

def mouseMotionY():
    """
    Return the y coordinate of current mouse position.
    """
    global _mouseTrack
    if _mouseTrack is not None:
        return _userY(_mouseTrack[1])
    else: return None
    
#-----------------------------------------------------------------------
# End added by Ege Kaan Isik
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

# Initialize the x scale, the y scale, and the pen radius.

setXscale()
setYscale()
setPenRadius()
pygame.font.init()

#-----------------------------------------------------------------------

# Functions for displaying Tkinter dialog boxes in child processes.

def _getFileName():
    """
    Display a dialog box that asks the user for a file name.
    """
    root = Tkinter.Tk()
    root.withdraw()
    reply = tkFileDialog.asksaveasfilename(filetypes=[('PNG File', '*.png')], initialdir='.')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdout.write(reply)
    sys.stdout.flush()
    sys.exit()

def _confirmFileSave():
    """
    Display a dialog box that confirms a file save operation.
    """
    root = Tkinter.Tk()
    root.withdraw()
    tkMessageBox.showinfo(title='File Save Confirmation',
        message='The drawing was saved to the file.')
    sys.exit()

def _reportFileSaveError(msg):
    """
    Display a dialog box that reports a msg.  msg is a string which
    describes an error in a file save operation.
    """
    root = Tkinter.Tk()
    root.withdraw()
    tkMessageBox.showerror(title='File Save Error', message=msg)
    sys.exit()

#-----------------------------------------------------------------------

def _regressionTest():
    """
    Perform regression testing.
    """

    clear()

    setPenRadius(.5)
    setPenColor(ORANGE)
    point(0.5, 0.5)
    show(0.0)

    setPenRadius(.25)
    setPenColor(BLUE)
    point(0.5, 0.5)
    show(0.0)

    setPenRadius(.02)
    setPenColor(RED)
    point(0.25, 0.25)
    show(0.0)

    setPenRadius(.01)
    setPenColor(GREEN)
    point(0.25, 0.25)
    show(0.0)

    setPenRadius(0)
    setPenColor(BLACK)
    point(0.25, 0.25)
    show(0.0)

    setPenRadius(.1)
    setPenColor(RED)
    point(0.75, 0.75)
    show(0.0)

    setPenRadius(0)
    setPenColor(CYAN)
    for i in range(0, 100):
        point(i / 512.0, .5)
        point(.5, i / 512.0)
    show(0.0)

    setPenRadius(0)
    setPenColor(MAGENTA)
    line(.1, .1, .3, .3)
    line(.1, .2, .3, .2)
    line(.2, .1, .2, .3)
    show(0.0)

    setPenRadius(.05)
    setPenColor(MAGENTA)
    line(.7, .5, .8, .9)
    show(0.0)

    setPenRadius(.01)
    setPenColor(YELLOW)
    circle(.75, .25, .2)
    show(0.0)

    setPenRadius(.01)
    setPenColor(YELLOW)
    filledCircle(.75, .25, .1)
    show(0.0)

    setPenRadius(.01)
    setPenColor(PINK)
    rectangle(.25, .75, .1, .2)
    show(0.0)

    setPenRadius(.01)
    setPenColor(PINK)
    filledRectangle(.25, .75, .05, .1)
    show(0.0)

    setPenRadius(.01)
    setPenColor(DARK_RED)
    square(.5, .5, .1)
    show(0.0)

    setPenRadius(.01)
    setPenColor(DARK_RED)
    filledSquare(.5, .5, .05)
    show(0.0)

    setPenRadius(.01)
    setPenColor(DARK_BLUE)
    polygon([.4, .5, .6], [.7, .8, .7])
    show(0.0)

    setPenRadius(.01)
    setPenColor(DARK_GREEN)
    setFontSize(24)
    text(.2, .4, 'hello, world')
    show(0.0)

    #import picture as p
    #pic = p.Picture('saveIcon.png')
    #picture(pic, .5, .85)
    #show(0.0)
    
    # Test handling of mouse and keyboard events.
    setPenColor(BLACK)
    print('Left click with the mouse or type a key')
    while True:
        if mouseLeftPressed():
            filledCircle(mouseLeftX(), mouseLeftY(), .02)
        if hasNextKeyTyped():
            print(nextKeyTyped())
        show(0.0)
        
    # Never get here.
    show()

#-----------------------------------------------------------------------

def _main():
    """
    Dispatch to a function that does regression testing, or to a
    dialog-box-handling function.
    """
    import sys
    if len(sys.argv) == 1:
        _regressionTest()
    elif sys.argv[1] == 'getFileName':
        _getFileName()
    elif sys.argv[1] == 'confirmFileSave':
        _confirmFileSave()
    elif sys.argv[1] == 'reportFileSaveError':
        _reportFileSaveError(sys.argv[2])

if __name__ == '__main__':
    _main()
