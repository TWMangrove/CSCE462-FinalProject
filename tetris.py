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

  def isOn(self):
    return self.isON

  def display(self):
    if (self.isON):
      print("x ", end= "")
    else:
      print("o ", end= "")

class LEDMatrix:
  def __init__(self):
    self.grid = []
    self.activePoints = []
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
    points = tetri.getPoints()
    for pair in points:
      x, y = pair
      self.setLEDon(x, y)
    
  def clearTetrimino(self, tetri):
    points = tetri.getPoints()
    for pair in points:
      x, y = pair
      self.setLEDoff(x, y)

  def setLEDon(self, x, y):
    if (y>= 0 and y < 24):
      if (x >= 0 and x < 10):
        self.grid[x][y].turnOn()

  def setLEDoff(self, x, y):
    if (y>= 0 and y < 24):
      if (x >= 0 and x < 10):
        self.grid[x][y].turnOff()

  def getActiveBlock(self):
    return self.activePoints

  def detectVerticalCollision(self, tetri):
    points = tetri.getPoints()
    for pair in points:
      x, y = pair
      y += 1
      if ((self.activePoints.count([x, y]) != 0) or (y == 24)):
        for active in points:
          aX, aY = active
          self.activePoints.append([aX, aY])
        tetri.setStatic()
        if (self.detectFullLine(y - 1)):
          print("-------------Full Line--------------")
        return True
    return False
  
  def detectHorizontalCollisionL(self, tetri):
    points = tetri.getPoints()
    for pair in points:
      x, y = pair
      x += 1
      if ((self.activePoints.count([x, y]) != 0) or (x == 10)):
        return True
    return False

  def detectHorizontalCollisionR(self, tetri):
    points = tetri.getPoints()
    for pair in points:
      x, y = pair
      x -= 1
      if ((self.activePoints.count([x, y]) != 0) or (x == -1)):
        return True
    return False

  def detectFullLine(self, line):
    count = 0
    print(line)
    for pair in self.activePoints:
        x, y = pair
        if (y == line):
          count += 1
    if (count == 10):
      return True
    print(count)
    return False


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
  
  def getPoints(self):
    points = [(self.refpoint[0], self.refpoint[1])]
    if (self.type == "I"):
      points.append([self.refpoint[0], self.refpoint[1] - 1])
      points.append([self.refpoint[0], self.refpoint[1] - 2])
      points.append([self.refpoint[0], self.refpoint[1] - 3])
    elif (self.type == "O"):
      points.append([self.refpoint[0], self.refpoint[1] - 1])
      points.append([self.refpoint[0] - 1, self.refpoint[1]])
      points.append([self.refpoint[0] - 1, self.refpoint[1] - 1])
    elif (self.type == "T"):
      points.append([self.refpoint[0], self.refpoint[1] - 1])
      points.append([self.refpoint[0] - 1, self.refpoint[1] - 1])
      points.append([self.refpoint[0] + 1, self.refpoint[1] - 1])
    elif (self.type == "S"):
      points.append([self.refpoint[0] - 1, self.refpoint[1]])
      points.append([self.refpoint[0] - 1, self.refpoint[1] - 1])
      points.append([self.refpoint[0] - 2, self.refpoint[1] - 1])
    elif (self.type == "Z"):
      points.append([self.refpoint[0] + 1, self.refpoint[1]])
      points.append([self.refpoint[0] + 1, self.refpoint[1] - 1])
      points.append([self.refpoint[0] + 2, self.refpoint[1] - 1])
    elif (self.type == "J"):
      points.append([self.refpoint[0] - 1, self.refpoint[1]])
      points.append([self.refpoint[0] - 2, self.refpoint[1]])
      points.append([self.refpoint[0] - 2, self.refpoint[1] - 1])
    elif (self.type == "L"):
      points.append([self.refpoint[0] + 1, self.refpoint[1]])
      points.append([self.refpoint[0] + 2, self.refpoint[1]])
      points.append([self.refpoint[0] + 2, self.refpoint[1] - 1])
    return points

  def moveDown(self): 
    if (not self.static):
      self.refpoint[1] = self.refpoint[1] + 1
      if (self.refpoint[1] == 23):
        self.static = True
  
  def moveLeft(self):
    if (not self.static):
      self.refpoint[0] = self.refpoint[0] + 1

  def moveRight(self):
    if (not self.static):
      self.refpoint[0] = self.refpoint[0] - 1

  def setStatic(self):
     self.static = True

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
      movement = input("left (l), right (r), down (d), or drop?")
      
      if (movement == "l"):
        if (not ledgrid.detectHorizontalCollisionL(test)):
          test.moveLeft()
        print("Moved left")
        test.moveDown()
      
      if (movement == "r"):
        if (not ledgrid.detectHorizontalCollisionR(test)):   
          test.moveRight()
          test.moveDown()
        print("Moved right")
        test.moveDown()

      if (movement == "drop"):
        while (not ledgrid.detectVerticalCollision(test)):
          test.moveDown()

      else:
          test.moveDown()


      ledgrid.displayTetrimino(test)
      ledgrid.display()
      if (not test.isStatic()): 
        ledgrid.clearTetrimino(test)
      else:
        break
      print("\n")

    player_input = input("Quit?")