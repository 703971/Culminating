#Saheli Saha
#Decemeber 6th 2022
#Flappy Bird
#A program that allows users to play flappy bird with added sounds, highscore, restart. It also randomizes in bird colors and in backgrounds/pipes The user is able to find instructions using the instruction button on the main menu. The quit button can be used to quit the entire program and obviously, the play button is used to play flappy bird. 


import pygame
from pygame.locals import *
from itertools import cycle
import random
import sys
from button import Button

# main menu creation: https://www.youtube.com/watch?v=GMBqjxcKogA
# main menu: https://github.com/baraltech/Menu-System-PyGame/blob/main/main.py
# https://www.youtube.com/watch?v=z26fTadq_jI --> coins
# https://youtu.be/rO_UU_Uu8EQ 
# https://www.youtube.com/watch?v=69KRrxcn77s

# click play button on main menu and flappy bird is displayed and ready to play. Runs full code of flappy bird with included restart, highscore and going back to main menu as well as sounds and randomized birds and backgrounds.
def play():
  FPS = 30
  screenWidth  = 288
  screenHeight = 512
  pipegapSize  = 100 # gap between upper and lower part of pipe
  baseY       = screenHeight * 0.79
  # image, sound and hitmask  dicts
  images, sounds, hitMasks = {}, {}, {}
  
  # list of all possible players (tuple of 3 positions of flap)
  playersList = (
      # red bird animation images
      (
          'assets/sprites/redbird-upflap.png',
          'assets/sprites/redbird-midflap.png',
          'assets/sprites/redbird-downflap.png',
      ),
      # blue bird animation images
      (
          'assets/sprites/bluebird-upflap.png',
          'assets/sprites/bluebird-midflap.png',
          'assets/sprites/bluebird-downflap.png',
      ),
      # yellow bird animation images
      (
          'assets/sprites/yellowbird-upflap.png',
          'assets/sprites/yellowbird-midflap.png',
          'assets/sprites/yellowbird-downflap.png',
      ),
  )
  
  # list of backgrounds images
  backgroundsList = (
      'assets/sprites/background-day.png',
      'assets/sprites/background-night.png',
  )
  
  # list of pipes images
  pipesList = (
      'assets/sprites/pipe-green.png',
      'assets/sprites/pipe-red.png',
  )
  

  # loops all the images that are in a sequence, for instance the birds will have a particular range between 1 to 3, those number indicate the images that need to be looped."Used to iterate a certain number of times in for loops in Python". Thus creating an animation.
  try:
      xrange
  except NameError:
      xrange = range
  
  # main game play where the code runs everything. Beginning with the welcome animation and then the actual game play and the game over screen as well. It also includes the animation of the birds, the pipes, the scores, sounds and randomizes between the different birds and bacgrounds (night and day mode). It also tracks the movement of the pipes, bird and check for collisions. 
  def main():
      global screen, FpsClock
      pygame.init()
      FpsClock = pygame.time.Clock()
      screen = pygame.display.set_mode((screenWidth, screenHeight))
      pygame.display.set_caption('Flappy Bird')
  
      # numbers sprites for score display
      images['numbers'] = (
          pygame.image.load('assets/sprites/0.png').convert_alpha(),
          pygame.image.load('assets/sprites/1.png').convert_alpha(),
          pygame.image.load('assets/sprites/2.png').convert_alpha(),
          pygame.image.load('assets/sprites/3.png').convert_alpha(),
          pygame.image.load('assets/sprites/4.png').convert_alpha(),
          pygame.image.load('assets/sprites/5.png').convert_alpha(),
          pygame.image.load('assets/sprites/6.png').convert_alpha(),
          pygame.image.load('assets/sprites/7.png').convert_alpha(),
          pygame.image.load('assets/sprites/8.png').convert_alpha(),
          pygame.image.load('assets/sprites/9.png').convert_alpha()
      )
  
      # game over sprite
      images['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
      # message sprite for welcome screen
      images['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
      # base (ground) sprite
      images['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()
  
      # sounds
      if 'win' in sys.platform:
          soundExt = '.wav'
      else:
          soundExt = '.ogg'
  
      sounds['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
      sounds['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
      sounds['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
      sounds['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
      sounds['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)
  
      while True:
          # select random background sprites
          randBackGround = random.randint(0, len(backgroundsList) - 1)
          images['background'] = pygame.image.load(backgroundsList[randBackGround]).convert()
  
          # select random player sprites
          randPlayer = random.randint(0, len(playersList) - 1)
          images['player'] = (
              pygame.image.load(playersList[randPlayer][0]).convert_alpha(),
              pygame.image.load(playersList[randPlayer][1]).convert_alpha(),
              pygame.image.load(playersList[randPlayer][2]).convert_alpha(),
          )
  
          # select random pipe sprites
          pipeIndex = random.randint(0, len(pipesList) - 1)
          images['pipe'] = (
              pygame.transform.flip(
            pygame.image.load(pipesList[pipeIndex]).convert_alpha(), False, True),
              pygame.image.load(pipesList[pipeIndex]).convert_alpha(),
          )
  
          # hismask for pipes
          hitMasks['pipe'] = (
              getHitmask(images['pipe'][0]),
              getHitmask(images['pipe'][1]),
          )
  
          # hitmask for player
          hitMasks['player'] = (
              getHitmask(images['player'][0]),
              getHitmask(images['player'][1]),
              getHitmask(images['player'][2]),
          )
  
          movementInfo = showWelcomeAnimation()
          crashInfo = mainGame(movementInfo)
          showGameOverScreen(crashInfo)
  
  # In the beginning of the game, a welcome animation screen is displayed in order to indicate user the start of the play. It includes a bird animation (looping of ird through different postions to create animated flying) and an image depicting the instructions of how to play the game. Once user presses the space bar, the game begins. 
  def showWelcomeAnimation():
      #Shows welcome screen animation of flappy bird
      # index of player to blit on screen
      playerIndex = 0
      playerIndexGen = cycle([0, 1, 2, 1])
      # iterator used to change playerIndex after every 5th iteration
      loopIter = 0
  
      playerX = int(screenWidth * 0.2)
      playerY = int((screenHeight - images['player'][0].get_height()) / 2)
  
      messageX = int((screenWidth - images['message'].get_width()) / 2)
      messageY = int(screenHeight * 0.12)
  
      baseX = 0
      # amount by which base can maximum shift to left
      baseShift = images['base'].get_width() - images['background'].get_width()
  
      # player shm for up-down motion on welcome screen
      playerShmVals = {'val': 0, 'dir': 1}
  
      while True:
          for event in pygame.event.get():
              if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                  pygame.quit()
                  sys.exit()
              if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                  # make first flap sound and return values for mainGame
                  sounds['wing'].play()
                  return {
                      'playerY': playerY + playerShmVals['val'],
                      'baseX': baseX,
                      'playerIndexGen': playerIndexGen,
                  }
  
          # adjust playerY, playerIndex, baseX
          if (loopIter + 1) % 5 == 0:
              playerIndex = next(playerIndexGen)
          loopIter = (loopIter + 1) % 30
          baseX = -((-baseX + 4) % baseShift)
          playerShm(playerShmVals)
  
          # draw sprites
          screen.blit(images['background'], (0,0))
          screen.blit(images['player'][playerIndex],
                      (playerX, playerY + playerShmVals['val']))
          screen.blit(images['message'], (messageX, messageY))
          screen.blit(images['base'], (baseX, baseY))
  
          pygame.display.update()
          FpsClock.tick(FPS)
  
  #Creates text file and reads the score and updates high score when passed the intial high score. 
  def highestScoreFile():
    with open("highest score.txt","r") as f:
      return f.read()
  
  # Using the movement of the bird (the x and y coordinates) from the welcome animation, the function begins to spawn the next two pipes after it goes through a pipe and randomizes the colors and heights between the upper pipes and lower pipes (however the height between pipes stays the same). It also tracks the score as it passes through a particular area of the pipes and if the score passes high score, it updates the high score to current score, displaying the high score during play. It checks for collsions with the coordinates of the bird and checks to see if bird hit ground or pipe. It collision occurs the bird goes towards the ground, indicating the game over over. Other wise during play, the bird continues to jump at an angle of 45 degrees with a certain velocity and goes down with gravity and ang ange of 45 degrees downwards until it hits ground where it fullly changes it rotation to 90 degrees. 
  def mainGame(movementInfo):
      score = playerIndex = loopIter = 0
      playerIndexGen = movementInfo['playerIndexGen']
      playerX, playerY = int(screenWidth * 0.2), movementInfo['playerY']
  
      baseX = movementInfo['baseX']
      baseShift = images['base'].get_width() - images['background'].get_width()
  
      # get 2 new pipes to add to upperPipes lowerPipes list
      newPipe1 = getRandomPipe()
      newPipe2 = getRandomPipe()
  
      # list of upper pipes
      upperPipes = [
          {'x': screenWidth + 200, 'y': newPipe1[0]['y']},
          {'x': screenWidth + 200 + (screenWidth / 2), 'y': newPipe2[0]['y']},
      ]
  
      # list of lowerpipe
      lowerPipes = [
          {'x': screenWidth + 200, 'y': newPipe1[1]['y']},
          {'x': screenWidth + 200 + (screenWidth / 2), 'y': newPipe2[1]['y']},
      ]
  
      pipeVelX = -4
  
      # player velocity, max velocity, downward accleration, accleration on flap
      playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
      playerMaxVelY =  10   # max vel along Y, max descend speed
      playerMinVelY =  -8   # min vel along Y, max ascend speed
      playerAccY    =   1   # players downward accleration
      playerRot     =  45   # player's rotation
      playerVelRot  =   3   # angular speed
      playerRotThr  =  20   # rotation threshold
      playerFlapAcc =  -9   # players speed on flapping
      playerFlapped = False # True when player flaps

      try:
        highestScore = int(highestScoreFile()) #Highest integer/score in game acheived
      except:
        highestScore = 0 #starts at zero before play

      #displays the highest score during play 
      def showHighestScore():
        highestScoreText = getFont(14).render(f"Highest Score: {highestScore}", True, "White")
        highestScoreRect = highestScoreText.get_rect(center=(150, 20))
        screen.blit(highestScoreText, highestScoreRect)
  
      while True:
          for event in pygame.event.get():
              if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                  pygame.quit()
                  sys.exit()
              if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                  if playerY > -2 * images['player'][0].get_height():
                      playerVelY = playerFlapAcc
                      playerFlapped = True
                      sounds['wing'].play()
  
          # check for crash here
          crashTest = checkCrash({'x': playerX, 'y': playerY, 'index': playerIndex},
                                 upperPipes, lowerPipes)
          if crashTest[0]:
              return {
                  'y': playerY,
                  'groundCrash': crashTest[1],
                  'baseX': baseX,
                  'upperPipes': upperPipes,
                  'lowerPipes': lowerPipes,
                  'score': score,
                  'playerVelY': playerVelY,
                  'playerRot': playerRot
              }
  
          # check for score
          playerMidPos = playerX + images['player'][0].get_width() / 2
          playerMidPos = playerX + images['player'][0].get_width() / 3
      
          for pipe in upperPipes:
              pipeMidPos = pipe['x'] + images['pipe'][0].get_width() / 2
              if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                  score += 1
                  sounds['point'].play()
              if (highestScore < score):
                highestScore = score
              with open("highest score.txt","w") as f:
                f.write(str(highestScore))
              
  
          # playerIndex baseX change
          if (loopIter + 1) % 3 == 0:
              playerIndex = next(playerIndexGen)
          loopIter = (loopIter + 1) % 30
          baseX = -((-baseX + 100) % baseShift)
  
          # rotate the player
          if playerRot > -90:
              playerRot -= playerVelRot
  
          # player's movement
          if playerVelY < playerMaxVelY and not playerFlapped:
              playerVelY += playerAccY
          if playerFlapped:
              playerFlapped = False
  
              # more rotation to cover the threshold (calculated in visible rotation)
              playerRot = 45
  
          playerHeight = images['player'][playerIndex].get_height()
          playerY += min(playerVelY, baseY - playerY - playerHeight)
  
          # move pipes to left
          for uPipe, lPipe in zip(upperPipes, lowerPipes):
              uPipe['x'] += pipeVelX
              lPipe['x'] += pipeVelX
  
          # add new pipe when first pipe is about to touch left of screen
          if len(upperPipes) > 0 and 0 < upperPipes[0]['x'] < 5:
              newPipe = getRandomPipe()
              upperPipes.append(newPipe[0])
              lowerPipes.append(newPipe[1])
  
          # remove first pipe if its out of the screen
          if len(upperPipes) > 0 and upperPipes[0]['x'] < -images['pipe'][0].get_width():
              upperPipes.pop(0)
              lowerPipes.pop(0)
  
          # draw sprites
          screen.blit(images['background'], (0,0))
  
          for uPipe, lPipe in zip(upperPipes, lowerPipes):
              screen.blit(images['pipe'][0], (uPipe['x'], uPipe['y']))
              screen.blit(images['pipe'][1], (lPipe['x'], lPipe['y']))
  
          screen.blit(images['base'], (baseX, baseY))
          # print score so player overlaps the score
          showScore(score)
          showHighestScore()

        
          # Player rotation has a threshold
          visibleRot = playerRotThr
          if playerRot <= playerRotThr:
              visibleRot = playerRot
          
          playerSurface = pygame.transform.rotate(images['player'][playerIndex], visibleRot)
          screen.blit(playerSurface, (playerX, playerY))
  
          pygame.display.update()
          FpsClock.tick(FPS)
  
  # After collision with ground or pipe, the game over display is shown with the crash infos; the score last acheived by the bird before collision. Displays a game over message as well as includes a back to main menu button that leads back to the main menu if user does not want to play anymore and displays a text to indicate to users what to do if they want to restart (e.g "press space bar to restart") 
  def showGameOverScreen(crashInfo):
      #crashes the player down ans shows gameover image
      score = crashInfo['score']
      playerX = screenWidth * 0.2
      playerY = crashInfo['y']
      playerHeight = images['player'][0].get_height()
      playerVelY = crashInfo['playerVelY']
      playerAccY = 2
      playerRot = crashInfo['playerRot']
      playerVelRot = 7
  
      baseX = crashInfo['baseX']
  
      upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']
  
      # play hit and die sounds
      sounds['hit'].play()
      if not crashInfo['groundCrash']:
          sounds['die'].play()
  
      while True:
          for event in pygame.event.get():
              if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                  pygame.quit()
                  sys.exit()
              if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                  if playerY + playerHeight >= baseY - 1:
                      return
  
          # player y shift
          if playerY + playerHeight < baseY - 1:
              playerY += min(playerVelY, baseY - playerY - playerHeight)
  
          # player velocity change
          if playerVelY < 15:
              playerVelY += playerAccY
  
          # rotate only when it's a pipe crash
          if not crashInfo['groundCrash']:
              if playerRot > -90:
                  playerRot -= playerVelRot
  
          # draw sprites
          screen.blit(images['background'], (0,0))
  
          for uPipe, lPipe in zip(upperPipes, lowerPipes):
              screen.blit(images['pipe'][0], (uPipe['x'], uPipe['y']))
              screen.blit(images['pipe'][1], (lPipe['x'], lPipe['y']))
  
          screen.blit(images['base'], (baseX, baseY))
          showScore(score)
          backMenuMousePos = pygame.mouse.get_pos() 
          playerSurface = pygame.transform.rotate(images['player'][1], playerRot)
          restartText = getFont(9).render("Press Space Bar to Restart Game", True, "Black")
          restartRect = restartText.get_rect(center=(144, 256))
          screen.blit(playerSurface, (playerX,playerY))
          screen.blit(images['gameover'], (50, 180))
          
          screen.blit(restartText, restartRect)
          backMenu = Button(image=None, pos=(145, 295), textInput="MENU", font=getFont(30), baseColor="Orange", hoveringColor="White")

          backMenu.changeColor(backMenuMousePos)
          backMenu.update(screen)

          for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backMenu.checkForInput(backMenuMousePos):
                  mainMenu()

        

        
          FpsClock.tick(FPS)
          pygame.display.update()
  
  #oscillates the value of playerShm['val'] between 8 and -8
  def playerShm(playerShm):
      if abs(playerShm['val']) == 8:
          playerShm['dir'] *= -1
  
      if playerShm['dir'] == 1:
           playerShm['val'] += 1
      else:
          playerShm['val'] -= 1
  
  #generates randomheights between the lower and upper pipes with the height between pipes staying the same
  def getRandomPipe():
      #returns a randomly generated pipe
      # y of gap between upper and lower pipe
      gapY = random.randrange(0, int(baseY * 0.6 - pipegapSize))
      gapY += int(baseY * 0.2)
      pipeHeight = images['pipe'][0].get_height()
      pipeX = screenWidth + 10
  
      return [
          {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
          {'x': pipeX, 'y': gapY + pipegapSize}, # lower pipe
      ]
  
  #displays score with number images and uses these number from 0 to 9 in order to make digits like double or triple digits with the same font/images
  def showScore(score):
      #displays score in center of screen
      scoreDigits = [int(x) for x in list(str(score))]
      totalWidth = 0 # total width of all numbers to be printed
  
      for digit in scoreDigits:
          totalWidth += images['numbers'][digit].get_width()
  
      Xoffset = (screenWidth - totalWidth) / 2
  
      for digit in scoreDigits:
          screen.blit(images['numbers'][digit], (Xoffset, screenHeight * 0.1))
          Xoffset += images['numbers'][digit].get_width()
  
# Overall of checkCrash, pixelCollision, get Hitmask: checks if bird has crashed into an upper or lower pipes or if it crahes the ground in order to stop the game and display the game over function. Using pygame's mask which is useful for fast pixel perfect collision detection. If bird has not crash, it returns false and continues to play and if crashed, returns true and game over display appears as mentioned before. 
  def checkCrash(player, upperPipes, lowerPipes):
      #returns True if player collders with base or pipes.
      pi = player['index']
      player['w'] = images['player'][0].get_width()
      player['h'] = images['player'][0].get_height()
  
      # if player crashes into ground
      if player['y'] + player['h'] >= baseY - 1:
          return [True, True]
      else:
  
          playerRect = pygame.Rect(player['x'], player['y'],
                        player['w'], player['h'])
          pipeW = images['pipe'][0].get_width()
          pipeH = images['pipe'][0].get_height()
  
          for uPipe, lPipe in zip(upperPipes, lowerPipes):
              # upper and lower pipe rects
              uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
              lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)
  
              # player and upper/lower pipe hitmasks
              pHitMask = hitMasks['player'][pi]
              uHitmask = hitMasks['pipe'][0]
              lHitmask = hitMasks['pipe'][1]
  
              # if bird collided with upipe or lpipe
              uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
              lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)
  
              if uCollide or lCollide:
                  return [True, False]
  
      return [False, False]
  
  def pixelCollision(rect1, rect2, hitmask1, hitmask2):
      #Checks if two objects collide and not just their rects
      rect = rect1.clip(rect2)
  
      if rect.width == 0 or rect.height == 0:
          return False
  
      x1, y1 = rect.x - rect1.x, rect.y - rect1.y
      x2, y2 = rect.x - rect2.x, rect.y - rect2.y
  
      for x in xrange(rect.width):
          for y in xrange(rect.height):
              if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                  return True
      return False
  
  def getHitmask(image):
      #returns a hitmask using an image's alpha.
      mask = []
      for x in xrange(image.get_width()):
          mask.append([])
          for y in xrange(image.get_height()):
              mask[x].append(bool(image.get_at((x,y))[3]))
      return mask
  
  if __name__ == '__main__':
      main()
  
  
#If user clicks instruction button on main menu, a new screen pops up with  an image display (created in canva) discussing the rules of how to play the game, once the user is done with the information they are able to click the back button (when hovering over the button, it will trun green), returning to the main menu. 
def instruction():
    while True:
        screen = pygame.display.set_mode((288, 512)) 
        pygame.display.set_caption("Instruction Page")
        instructionMousePos = pygame.mouse.get_pos()

        screen.fill("white")

        instructionText = pygame.image.load('instructions.png')
        instructionRect = instructionText.get_rect(center=(144, 256))
        screen.blit(instructionText, instructionRect)

        instructionBack = Button(image=None, pos=(144, 456), 
        textInput="BACK", font=getFont(30), baseColor="Black", hoveringColor="Green")

        instructionBack.changeColor(instructionMousePos)
        instructionBack.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if instructionBack.checkForInput(instructionMousePos):
                    mainMenu()

        pygame.display.update()



# The main menu appears when the user runs the code, it includes the options of playing flappy bird, the instructions of how to play the game and the quit button. Each button will lead to a new pagem for instance the instruction button will create a new screen and display the instructions. The play button will display the game of flappy bird and finally the quit button will end the entire program. A hovering color around these buttons is feature to let users know the postion of where to click the button, e.g play button turn green when mouse position is near the play button (vice versa). 

pygame.init()

screen = pygame.display.set_mode((288, 512))
pygame.display.set_caption("Main Menu")

backGround = pygame.image.load("mainmenu.png") #background image 

def getFont(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font (4).ttf", size)
  
                                     
def mainMenu():
    while True:
        screen.blit(backGround, (0, 0))

        menuMousePos = pygame.mouse.get_pos()

        playButton = Button(image=None, pos=(155, 160), 
                            textInput="PLAY", font=getFont(23), baseColor="#d7fcd4", hoveringColor="Green")
        instructionButton = Button(image=None, pos=(155, 265), 
                            textInput="INSTRUCTIONS", font=getFont(15), baseColor="#d7fcd4", hoveringColor="Blue")
        quitButton = Button(image=None, pos=(155, 375), 
                            textInput="QUIT", font=getFont(23), baseColor="#d7fcd4", hoveringColor="Red")


        for button in [playButton, instructionButton, quitButton]:
            button.changeColor(menuMousePos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.checkForInput(menuMousePos):
                    play()
                if instructionButton.checkForInput(menuMousePos):
                    instruction()
                if quitButton.checkForInput(menuMousePos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

mainMenu()