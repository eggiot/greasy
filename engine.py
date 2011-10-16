import grid as g
import input as i
import sound as s
import pygame, os, math

class Timer:
    def __init__(self):
        self.timeStart = 0
        self.timeFinish = 0

    def start(self):
        """
        Stores the current time in seconds.
        """
        self.timeStart = pygame.time.get_ticks()

    def finish(self, secs=False):
        """
        Returns time elapsed since pygame.init() or since Timer.start().
        was called
        
        Parameters
        ----------
        secs: bool, optional, default=False
            if True, return value is in seconds, else in milliseconds.
        
        
        """
        self.timeFinish = pygame.time.get_ticks()()
        elapsedTime = self.timeFinish - self.timeStart
        if secs:
            return elapsedTime / 1000
        else:
            return elapsedTime
    
    def wait(self, time, secs=True):
        """
        Pause the timer.
        
        Parameters
        ----------
        time: int / float
            length of time to wait
        secs: bool, optional, default=True
            if True, time is assumed to be in seconds else, milliseconds
        """
        if secs:
            pygame.time.wait(time * 1000)
        else:
            pygame.time.wait(time)

class Camera():
    def __init__(self,
                 focus,
                 area):
        self.focus = focus
        self.area = area
    
    def zoom(self, amount):
        """
        Positive amount values - zoom in
        Negative amount values - zoom out
        """
        pass
    
    def move(self, cell):
        self.focus = cell
    
    def rotate(self, amount):
        pass

class Character():
    def __init__(self,
                 starting_position,
                 sprite):
        self.position = starting_position
        self.sprite = sprite
    
    def move(self, cell):
        pass

class AnimatedCharacter(Character):
    def __init__(self,
                 starting_position,
                 sprite,
                 spritesheet_size):
        Character.__init__(starting_position, sprite)

class GreasyEngine():
    def __init__(self,
                 rows, columns,
                 imageWidth, imageHeight,
                 backgroundColour=(0,0,0),
                 windowPosition=(0,0),
                 centred=False,
                 title="Greasy Window",
                 fullscreen=False,
                 resizable=False,
                 icon=None):
        self.gameGrid = g.Grid(rows, columns)
        self.input = i.InputHandler()
        self.sound = s.SoundHandler()
        self.timer = Timer()
        self.imageWidth = imageWidth
        self.imageHeight = imageHeight
        self.columns = columns
        self.rows = rows
        if centred:
            os.environ['SDL_VIDEO_CENTERED'] = '1'
        else:
            os.environ['SDL_VIDEO_WINDOW_POS'] = str(windowPosition[0]) + "," + str(windowPosition[1])
        pygame.init()
        self.screen = pygame.display.set_mode((imageWidth * rows,
                                               imageHeight * columns))
        if icon != None:
            self.setIcon(icon)
        pygame.display.set_caption(title)
        self.base = None
        self.backgroundColour = backgroundColour
        self.fill()

    ##### OBJECTS #####
    def moveObject(self, start, target, replacement=0, gameGrid=None):
        """
        Moves the contents of one cell of the grid to another cell, replacing
        the contents of the original cell with a value.
        
        Parameters
        ----------
        start: tuple
            (x, y) coordinates of the cell containing the object
        target: tuple
            (x, y) coordinates of the cell to which to move the object
        replacement: any, optional, default=0
            the object with which to fill the cell referenced by start
        gameGrid: Greasy Grid, optional, default=self.gameGrid
            Greasy Grid
        """
        if not gameGrid:
            gameGrid = self.gameGrid
        # set gameGrid[target] to gameGrid[start]
        currentItem = gameGrid.getItem(start[0], start[1])
        gameGrid.setItem(replacement, start[0], start[1])
        gameGrid.setItem(currentItem, target[0], target[1])

    def newObject(self, filename, alpha=False, colourkey=None, resize=True):
        """
        Returns a new pygame surface.
        
        Parameters
        ----------
        filename: string
            image filename
        alpha: bool, optional, default=False
            include alpha channel
        colourkey: tuple, optional, default=None
            (R,G,B) colourkey
        resize: bool, optional, default=True
            resize the surface to the size of the cells
        """
        if alpha:
            # TODO: implement working colourkey mode
            image = pygame.image.load(filename).convert_alpha()
            if colourkey != None:
                image.set_colorkey(colourkey)
        else:
            image = pygame.image.load(filename).convert()
        
        if resize:
            size = image.get_size()
            if size[0] != self.imageWidth or size[1] != self.imageHeight:
                if size[0] != self.imageWidth:
                    newWidth = self.imageWidth
                else:
                    newWidth = size[0]
                if size[1] != self.imageHeight:
                    newHeight = self.imageHeight
                else:
                    newHeight = size[1]
                image = self.resizeObject(image, newWidth, newHeight)
        return image

    def addObject(self, item, row, column, gameGrid=None):
        """
        Adds a pygame surface to the grid
        
        Parameters
        ----------
        item: any
            item to add to Grid
        row: int
            row
        column: int
            column
        gameGrid: Greasy Grid
            Greasy Grid
        """
        if not gameGrid:
            gameGrid = self.gameGrid
        if row > self.rows-1 or row < 0 or column > self.columns-1 or column < 0:
            print "addObject could not add %s: \
            Location out of bounds" % str(item)
            return None
        gameGrid.setItem(item, row, column)

    def getObject(self, row, column, gameGrid=None):
        """
        Returns an object from the grid
        """
        if not gameGrid:
            gameGrid = self.gameGrid
        return gameGrid.getItem(row, column)

    def fillEmptyCells(self, item, gameGrid=None, emptyValue=0):
        """
        Fills all the empty cells of a grid
        """
        if not gameGrid:
            gameGrid = self.gameGrid
        for r, c in gameGrid:
            currentCell = gameGrid.getItem(r, c)
            if currentCell == emptyValue:
                self.addObject(item, r, c, gameGrid=gameGrid)
    
    def emptyCell (self, row, column, gameGrid=None, emptyValue=0):
        """
        Replaces the specified cell with the emptyValue
        """
        if not gameGrid:
            gameGrid = self.gameGrid
        self.addObject(emptyValue, row, column, gameGrid=gameGrid)
    
    def emptyGrid(self, gameGrid=None, emptyValue=0):
        """
        Replace all cells in the grid with the emptyValue
        """
        if not gameGrid:
            gameGrid = self.gameGrid
        for r, c in gameGrid:
            self.emptyCell(r, c, gameGrid=gameGrid, emptyValue=emptyValue)
    
    def limitValue(self, value, lowerLimit, upperLimit):
        """
        Limits the value of a variable to the range defined by lowerLimit
        and upperLimit.
        """
        if value > upperLimit:
            return upperLimit
        elif value < lowerLimit:
            return lowerLimit
        else:
            return value
    
    def testEmptyCell(self, row, column, gameGrid=None, emptyValue=0):
        """
        Tests if a cell contains the empty value
        """
        if not gameGrid:
            gameGrid = self.gameGrid
        row = self.limitValue(row, 0, self.rows-1)
        column = self.limitValue(column, 0, self.columns-1)
        if gameGrid.getItem(row, column) == emptyValue:
            return True
        else:
            return False

    ##### TRANSFORM #####
    def flipObject(self, object, vertical, horizontal):
        """
        Flips a pygame surface vertically, horizontally, or both.
        """
        try:
            # is object a grid reference?
            row = object[0]
            column = object[1]
        except TypeError:
            flipped = pygame.transform.flip(object, vertical, horizontal)
            return flipped
        flipped = pygame.transform.flip(self.getObject(row, column), vertical,
                                        horizontal)
        self.addObject(flipped, row, column)
        return flipped

    def resizeObject(self, object, width, height):
        """
        Scales a pygame surface
        """
        try:
            row = object[0]
            column = object[1]
        except TypeError:
            scaled = pygame.transform.scale(object, (width, height))
            return scaled
        scaled = pygame.transform.scale(self.getObject(row, column),
                                        (width, height))
        self.addObject(scaled, row, column)
        return scaled

    def rotateObject(self, object, angle):
        """
        Rotates a pygame surface
        """
        try:
            row = object[0]
            column = object[1]
        except TypeError:
            rotated = pygame.transform.rotate(object, angle)
            return rotated
        rotated = pygame.transform.rotate(self.getObject(row, column), angle)
        self.addObject(rotated, row, column)
        return rotated
    
    def getPixelColour(self, item, pixel):
        """
        Returns the RGBA colour value at the given pixel.
        
        Parameters
            item: pygame surface
            pixel: tuple
        """
        return item.get_at(pixel)

    ##### DISPLAY #####
    def setIcon(self, icon, alpha=False):
        """
        Sets the window icon
        """
        try:
            pygame.display.set_icon(icon)
        except TypeError:
            icon = self.newObject(icon, alpha)
            pygame.display.set_icon(icon)
    
    def setBackground(self, background, dest=None, empty=0):
        """
        Creates a tiled background from one pygame surface
        """
        if not dest:
            dest = self.screen
        self.base = pygame.display.set_mode(dest.get_size())
        backgroundGrid = g.Grid(self.rows, self.columns)
        self.fillEmptyCells(background, gameGrid=backgroundGrid)
            
        # blit tiled background image on background surface
        for r, c in backgroundGrid:
            x = r * self.imageWidth
            y = c * self.imageHeight
            currentItem = backgroundGrid.getItem(r, c)
            if currentItem != empty:
                self.base.blit(currentItem, (x, y))
        self.base = self.base.copy()
 
    def fill(self, screen=None, colour=None):
        """
        Fills the screen with a single colour
        """
        if not screen:
            screen = self.screen
        if not colour:
            colour = self.backgroundColour
        screen.fill(colour)

    def text(self, string,
             location,
             font, fontSize,
             antialias=False,
             colour=(0,0,0),
             newlinePad=5,
             screen=None):
        """
        Creates a pygame surface containing text and displays it.
        """
        if not screen:
            screen = self.screen
        x = location[0]
        y = location[1]
        font = pygame.font.Font(font, fontSize)
        lines = string.split("\n")
        counter = 0
        height = 0
        for line in lines:
            fontSurface = font.render(line, antialias, colour).convert()
            if counter == 0:
                screen.blit(fontSurface, location)
            else:
                newY = y * counter + newlinePad + height
                screen.blit(fontSurface, (x, newY))
            height = font.size(line)[1] + height + newlinePad
            counter += 1
       
    def updateDisplay(self, gameGrid=None,
                      dest=None,
                      background=None,
                      empty=0,
                      text=None,
                      text_location=(0,0),
                      font=None,
                      fontColour=(0,0,0),
                      fontAntialias=False,
                      fontSize=20):
        """
        Displays all surfaces on the screen. It also optionally displays a
        tiled background surface. Assumes that all non-zero cells of
        self.gameGrid contain a pygame Surface
        """
        if not gameGrid:
            gameGrid = self.gameGrid
        if not dest:
            dest = self.screen
        self.fill()
        if not self.base:
            """Blits the sprites to the screen surface"""
            if not background:
                for r, c in gameGrid:
                    x = r * self.imageWidth
                    y = c * self.imageHeight
                    currentItem = gameGrid.getItem(r, c)
                    if currentItem != empty:
                        dest.blit(currentItem, (x, y))
                    if text:
                        self.text(text, text_location, font, fontSize,
                                  antialias=fontAntialias, colour=fontColour)
                pygame.display.update()
                return None
            else:
                self.setBackground(background)

        # Blit the sprites to the background surface, then blit background
        # surface to destination surface
        baseCopy = self.base.copy()            
        # blit sprites to the background surface
        for r, c in gameGrid:
            x = r * self.imageWidth
            y = c * self.imageHeight
            currentItem = gameGrid.getItem(r, c)
            if currentItem !=empty:
                self.base.blit(currentItem, (x, y))
        # blit background surface to destination surface
        dest.blit(self.base, (0,0))
        self.base = baseCopy.copy()
        if text:
            self.text(text, text_location, font, fontSize,
                      antialias=fontAntialias, colour=fontColour)
        pygame.display.update()
    
    def showMessage(self, text, location, font, fontSize, colour=(255,255,255),
                    input=False, secs=None):
        """
        Displays a text message. It either waits a specified number of seconds
        or waits for user input.
        """
        self.fill()
        self.text(text, location, font, fontSize, colour=colour)
        pygame.display.update()
        if input:
            currentEvent = self.input.input()
            while not self.input.checkInput(currentEvent):
                currentEvent = self.input.input()
        if not secs:
            self.timer.wait(secs)
    
    ##### HIGH-LEVEL INTERACTION #####
    def arrowMoveObject(self, event, cell, spaces=1):
        """
        Checks for input from the arrow keys and moves an item in the
        specified direction
        """
        direction = self.input.checkDirectionInput(event)
        try:
            x = cell[0]
            y = cell[1]
        except TypeError:
            print "arrowMoveObject: cell is of type", type(cell)
            return None
        try:
            if direction == 1:
                if y + spaces <= self.rows - 1:
                    cell = (x, y+spaces)
                else:
                    cell = (x, self.rows-1)
            elif direction == 2:
                if y -spaces >= 0:
                    cell = (x, y-spaces)
                else:
                    cell = (x, 0)
            elif direction == 3:
                if x - spaces >= 0:
                    cell = (x-spaces, y)
                else:
                    cell = (0, y)
            elif direction == 4:
                if x + spaces <= self.columns - 1:
                    cell = (x+spaces, y)
                else:
                    cell = (self.columns-1, y)
        except IndexError:
            print "no dice"
            return cell
        
        self.moveObject((x, y), cell)
        return cell
    
    def clickCell(self, event):
        """
        Returns a tuple containing (x, y) coordinates of a mouse-clicked
        cell
        """
        position = self.input.checkMouseInput(event)
        if not position:
            return None
        x = math.floor(position[0] / self.imageWidth)
        y = math.floor(position[1] / self.imageHeight)
        return (int(x), int(y))

    def quit(self):
        """
        Return a pygame.QUIT event
        """
        return pygame.event.Event(pygame.QUIT)
    
    ##### MISC #####
    def __iter__(self):
        for r, c in self.gameGrid:
            yield (r, c)