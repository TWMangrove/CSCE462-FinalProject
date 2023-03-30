import random
import time

ROWS = 10
COLS = 24

global ledgrid

class LED: 
  def __init__(self):
    self.isON = False
  
  def turnOff(self):
    self.isON = False

  def turnOn(self):
    self.isON = True

  def display(self):
    if (self.isON):
      print("x", end= "")
    else:
      print("o", end= "")

class LEDMatrix:
  def __init__(self):
    self.grid = []
    for row in range(ROWS):
            self.grid.append([])
            for col in range(COLS):
                self.grid[row].append(LED())

  def display(self):
    for row in self.grid:
            for led in row:
                led.display()
            print()
  
  def displayTetrimino(self, tetri):
    refx, refy = tetri.getRef()
    if (tetri.type == "I"):
      self.setLEDon(refx, refy)
      self.setLEDon(refx, refy - 1)
      self.setLEDon(refx, refy - 2)
      self.setLEDon(refx, refy - 3)
    elif (tetri.type == "O"):
      self.setLEDon(refx, refy)
      self.setLEDon(refx, refy - 1)
      self.setLEDon(refx - 1, refy)
      self.setLEDon(refx - 1, refy - 1)
    elif (tetri.type == "T"):
      self.setLEDon(refx, refy)
      self.setLEDon(refx, refy - 1)
      self.setLEDon(refx - 1, refy - 1)
      self.setLEDon(refx + 1, refy - 1)
    elif (tetri.type == "S"):
      self.setLEDon(refx, refy)
      self.setLEDon(refx - 1, refy)
      self.setLEDon(refx - 1, refy - 1)
      self.setLEDon(refx - 2, refy - 1)
    elif (tetri.type == "Z"):
      self.setLEDon(refx, refy)
      self.setLEDon(refx + 1, refy)
      self.setLEDon(refx + 1, refy - 1)
      self.setLEDon(refx + 2, refy - 1)
    elif (tetri.type == "J"):
      self.setLEDon(refx, refy)
      self.setLEDon(refx - 1, refy)
      self.setLEDon(refx - 2, refy)
      self.setLEDon(refx - 2, refy - 1)
    elif (tetri.type == "L"):
      self.setLEDon(refx, refy)
      self.setLEDon(refx + 1, refy)
      self.setLEDon(refx + 2, refy)
      self.setLEDon(refx + 2, refy - 1)
    
  def clearTetrimino(self, tetri):
    refx, refy = tetri.getRef()
    if (tetri.type == "I"):
      self.setLEDoff(refx, refy)
      self.setLEDoff(refx, refy - 1)
      self.setLEDoff(refx, refy - 2)
      self.setLEDoff(refx, refy - 3)
    elif (tetri.type == "O"):
      self.setLEDoff(refx, refy)
      self.setLEDoff(refx, refy - 1)
      self.setLEDoff(refx - 1, refy)
      self.setLEDoff(refx - 1, refy - 1)
    elif (tetri.type == "T"):
      self.setLEDoff(refx, refy)
      self.setLEDoff(refx, refy - 1)
      self.setLEDoff(refx - 1, refy - 1)
      self.setLEDoff(refx + 1, refy - 1)
    elif (tetri.type == "S"):
      self.setLEDoff(refx, refy)
      self.setLEDoff(refx - 1, refy)
      self.setLEDoff(refx - 1, refy - 1)
      self.setLEDoff(refx - 2, refy - 1)
    elif (tetri.type == "Z"):
      self.setLEDoff(refx, refy)
      self.setLEDoff(refx + 1, refy)
      self.setLEDoff(refx + 1, refy - 1)
      self.setLEDoff(refx + 2, refy - 1)
    elif (tetri.type == "J"):
      self.setLEDoff(refx, refy)
      self.setLEDoff(refx - 1, refy)
      self.setLEDoff(refx - 2, refy)
      self.setLEDoff(refx - 2, refy - 1)
    elif (tetri.type == "L"):
      self.setLEDoff(refx, refy)
      self.setLEDoff(refx + 1, refy)
      self.setLEDoff(refx + 2, refy)
      self.setLEDoff(refx + 2, refy - 1)

  def setLEDon(self, x, y):
    if (y>= 0 and y < 24):
      if (x >= 0 and x < 10):
        self.grid[x][y].turnOn()

  def setLEDoff(self, x, y):
    if (y>= 0 and y < 24):
      if (x >= 0 and x < 10):
        self.grid[x][y].turnOff()
  

class Tetrimino:
  def __init__(self):
      self.refpoint = [5,0]
      self.static = False
      a = random.randint(1,7) 
      if (a == 1):
        self.type = "I"
      elif (a == 2):
        self.type = "O"
      elif (a == 3):
        self.type = "T"
      elif (a == 4):
        self.type = "S"
      elif (a == 5):
        self.type = "Z"
        self.refpoint = [4,0]
      elif (a == 6):
        self.type = "J"
      elif (a == 7):
        self.type = "L"
        self.refpoint = [3, 0]

  def getType(self):
    return self.type

  def getRef(self):
    return self.refpoint
  
  def moveDown(self): 
    if (not self.static):
      self.refpoint[1] = self.refpoint[1] + 1
      if (self.refpoint[1] == 23):
        self.static = True
  
  def moveLeft(self):
    if (not self.static):
      self.refpoint[0] = self.refpoint[0] + 1
      self.refpoint[1] = self.refpoint[1] + 1

  def moveRight(self):
    if (not self.static):
      self.refpoint[0] = self.refpoint[0] - 1
      self.refpoint[1] = self.refpoint[1] + 1

  def isStatic(self):
    return self.static

if __name__ == '__main__':
  ledgrid = LEDMatrix()

  player_input = ""
  while player_input != "Quit":
    ledgrid.display()
    print("loop")
    test = Tetrimino()
    print(test.getType())

    while True:
      movement = input("left (l), right (r), or down (d)?")
      
      if (movement == "l"):
        test.moveLeft()
        print("Moved left")
      
      if (movement == "r"):
        test.moveRight()
        print("Moved right")

      else:
        test.moveDown()
        print("Moved Down")
        
      ledgrid.displayTetrimino(test)
      ledgrid.display()
      print(test.getRef())
      print(test.isStatic())
      if (not test.isStatic()): 
        print("Cleared!")
        ledgrid.clearTetrimino(test)
      else:
        break
      print("\n")

    player_input = input("Quit?")