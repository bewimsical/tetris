import pygame
import random
import time


black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
grey = pygame.Color(128, 128, 128)

lime_green = pygame.Color(151, 221, 27)
pink = pygame.Color(178, 41, 174)
goldenrod = pygame.Color(231, 182, 15)
light_blue = pygame.Color(43, 205, 217)
blue = pygame.Color(26, 109, 217)
purple = pygame.Color(63, 60, 223)
dark_purple = pygame.Color(46, 16, 151)

class Block:
  shapes = [
      {
          "color": lime_green,
          "shape": [[4, 5, 6, 7], [1, 5, 9, 13]]
      },
      {
          "color": pink,
          "shape": [[4, 5, 9, 10], [2, 5, 6, 9]]
      },
      {
          "color": goldenrod,
          "shape": [[6, 7, 9, 10], [1, 5, 6, 10]]
      },
      {
          "color": light_blue,
          "shape": [[4, 5, 6, 10], [1, 2, 5, 9], [0, 4, 5, 6], [
              1,
              5,
              8,
              9,
          ]]
      },
      {
          "color": blue,
          "shape": [[5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7], [1, 2, 6, 10]]
      },
      {
          "color": purple,
          "shape": [[4, 5, 6, 9], [1, 5, 6, 9], [1, 4, 5, 6], [1, 4, 5, 9]]
      },
      {
          "color": dark_purple,
          "shape": [[1, 2, 5, 6]]
      },
  ]

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.type = random.randint(0, len(self.shapes) - 1)
    self.rotation = 0
    self.color = self.shapes[self.type]["color"]
    

  def image(self):
    return self.shapes[self.type]["shape"][self.rotation]

  def rotate(self, dir):
    self.rotation = (self.rotation + dir) % len(
        self.shapes[self.type]["shape"])


class Tetris:

  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.zoom = 20
    self.x = 100
    self.y = 60
    self.board = []
    self.current = None
    self.hold = None
    self.gameover = False
    self.counter = 0
    self.level = 1  #increase to speed up blocks falling
    self.score = 0
    self.lines = 0
    self.next = Block(3,0)

    for i in range(height):
      new_line = []
      for j in range(width):
        new_line.append(0)
      self.board.append(new_line)

  def break_lines(self):
    lines = 0
    for i in range(1, self.height):
      for j in range(self.width):
        if self.board[i][j] == 0:
          break
        if j == self.width - 1:
          lines += 1
          self.board.pop(i)
          self.board.insert(0, [0] * self.width)
    self.score += lines**2
    prev_lines = self.lines
    self.lines += lines
    if prev_lines // 10 != self.lines // 10:
      print("increasing level")
      self.level += 1
    

  
  def freeze(self):
    for i in range(4):
      for j in range(4):
        if i * 4 + j in self.current.image():
          self.board[i + self.current.y][j + self.current.x] = self.current.color
    self.break_lines()
    self.New_Block()
    if self.collision_detect():
      self.gameover = True

  def collision_detect(self):
    collision = False
    for i in range(4):
      for j in range(4):
        if i * 4 + j in self.current.image() and\
        (i + self.current.y > self.height -1 or\
        j + self.current.x < 0 or\
        j + self.current.x > self.width -1 or\
        game.board[i + self.current.y][j + self.current.x] != 0):
          collision = True
    return collision

  def New_Block(self):
    self.current = self.next
    self.next = Block(3,0)

  def hold_block(self):
    if self.hold is None:
      self.hold = self.current
    else:
      place_holder = self.current
      self.current = self.hold
      self.hold = place_holder
      self.current.x = 3
      self.current.y = 0
      
  def move(self, dx):
    self.current.x += dx 
    if self.collision_detect():
      self.current.x += -dx 

  def movedown(self):
    self.current.y += 1 
    if self.collision_detect():
      self.current.y -= 1
      self.freeze()

  def rotate(self, dir):
    current_rotation = self.current.rotation
    self.current.rotate(dir)
    if self.collision_detect():
      self.current.rotate(-1 * dir)


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Tetris.wav')
pygame.mixer.music.play(-1)
window = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Tetris?")
game = Tetris(20, 10)
clock = pygame.time.Clock()
fps = 21
start = False
playing  = True
paused = False
info = False
get_info_font = pygame.font.Font('Orbitron-Regular.ttf', 20)
get_info_text = get_info_font.render("I      Info", True, black)

#draw title screen
while not start:
  window.fill(white)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
            pygame.quit()
    elif event.type == pygame.MOUSEBUTTONUP:
      if event.button == pygame.BUTTON_LEFT:
        start = True
        # print(pygame.mouse.get_pos())
  pygame.draw.rect(window, light_blue, [74, 202, 346, 134],2)
  pygame.draw.rect(window, lime_green, [69, 197, 356, 144],2)
  pygame.draw.rect(window, goldenrod, [64, 192, 366, 154],2)
  pygame.draw.rect(window, pink, [59, 187, 376, 164],2)
  large_font = pygame.font.Font('Orbitron-Regular.ttf', 75)
  small_font = pygame.font.Font('Orbitron-Regular.ttf', 30)
  title_text = large_font.render("TETRIS", True, black)
  start_text = small_font.render("click to start", True, black)
  window.blit(title_text, [94,200])
  window.blit(start_text, [148,285])
  pygame.display.flip()

  #start game
while playing:
  while not info and not paused:
  
    if game.current is None:
      game.New_Block()
    window.fill(white)
    
    #add keyboard input
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
            pygame.quit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
          game.movedown()
        elif event.key == pygame.K_a:
          game.rotate(-1)
        elif event.key == pygame.K_d:
          game.rotate(1)
        elif event.key == pygame.K_c:
          if game.hold is None:
            game.hold_block()
            del game.current
            game.New_Block()
          else:
            game.hold_block()
          
        elif event.key == pygame.K_LEFT:
          game.move(-1)
        elif event.key == pygame.K_RIGHT:
          game.move(1)
        elif event.key == pygame.K_KP_PLUS:
          game.level += 1
        elif event.key == pygame.K_KP_MINUS:
          game.level -= 1
        elif event.key == pygame.K_p:
          paused = not paused
        elif event.key == pygame.K_i:
          info = not info
      
          
    
    #draw board
    for i in range(game.height):
      for j in range(game.width):
        pygame.draw.rect(window,
                         grey, 
                         [game.x + game.zoom * j,
                          game.y + game.zoom * i, 
                          game.zoom,
                          game.zoom],
                         1)
        #draw shapes when they are frozen
        if game.board[i][j] != 0:
          pygame.draw.rect(window,
                           game.board[i][j],
                           [game.x + game.zoom * j,
                            game.y + game.zoom * i,
                            game.zoom - 1,
                            game.zoom - 1])
  
    #draw shapes as they are falling
    if game.current is not None:
      for i in range(4):
        for j in range(4):
          p = i * 4 + j
          if p in game.current.image():
            pygame.draw.rect(window,
                             game.current.color,
                             [game.x + game.zoom * (j + game.current.x) +1,
                              game.y + game.zoom * (i + game.current.y) +1,
                              game.zoom - 1, 
                              game.zoom - 1])
          #pygame.draw.rect(location, color, [x coordinate, y coordinate, width, height])
  
    #draw next block
    for i in range(4):
      for j in range(4):
        p = i * 4 + j
        if p in game.next.image():
          pygame.draw.rect(window,
           game.next.color,
           [game.x + (game.width * game.zoom) + 10 + game.zoom * j,
            game.y + 40 + game.zoom * i,
            game.zoom, game.zoom])
  
    #draw hold block
    if game.hold is not None:
      for i in range(4):
        for j in range(4):
          p = i * 4 + j
          if p in game.hold.image():
            pygame.draw.rect(window,\
             game.hold.color,\
             [game.x + (game.width * game.zoom) + 10 + game.zoom * j,\
              game.y + 290 + game.zoom * i,\
              game.zoom, game.zoom])
  
    #add in game text
    font = pygame.font.Font('Orbitron-Regular.ttf', 20)
    score_text = font.render("Score: " + str(game.score), True, black)
    level_text = font.render("Level: " + str(game.level), True, black)
    lines_text = font.render("Lines: " + str(game.lines), True, black)
    next_text = font.render("Next", True, black)
    hold_text = font.render("Hold", True, black)
  
    window.blit(next_text, [game.x + (game.width * game.zoom) + 20, game.y])
    window.blit(score_text,
                [game.x + (game.width * game.zoom) + 20, game.y + 130])
    window.blit(level_text,
                [game.x + (game.width * game.zoom) + 20, game.y + 170])
    window.blit(lines_text,
                [game.x + (game.width * game.zoom) + 20, game.y + 210])
    window.blit(hold_text,
      [game.x + (game.width * game.zoom) + 20, game.y + 250])

    window.blit(get_info_text, [180, 550])
    pygame.draw.rect(window,black,[165,546,35,35],2)
    
    #sets game speed
    game.counter += 1 
    if game.counter % max(1, 11 - game.level) == 0:
      game.counter = 0
      game.movedown()
  
    #draw gameover screen
    if game.gameover:
      waiting = True
      while waiting:
        window.fill(white)  
    
        pygame.draw.rect(window, light_blue, [74, 202, 346, 134],2)
        pygame.draw.rect(window, lime_green, [69, 197, 356, 144],2)
        pygame.draw.rect(window, goldenrod, [64, 192, 366, 154],2)
        pygame.draw.rect(window, pink, [59, 187, 376, 164],2)
        large_font = pygame.font.Font('Orbitron-Regular.ttf', 45)
        small_font = pygame.font.Font('Orbitron-Regular.ttf', 30)
        gameover_text = large_font.render("GAME OVER", True, black)
        restart_text = small_font.render("play again? y/n", True, black)
        window.blit(gameover_text, [91,220])
        window.blit(restart_text, [121,275])
        pygame.display.flip()
        
        for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
              game = Tetris(20, 10)
              waiting = False
            elif event.key == pygame.K_n:
              waiting = False
              playing = False
              break
          # if event.type == pygame.MOUSEBUTTONUP:
          #   if event.button == pygame.BUTTON_LEFT:
          #     print(pygame.mouse.get_pos())
    pygame.display.flip()
    clock.tick(fps)
  while paused:   
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
        paused = not paused
      elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == pygame.BUTTON_LEFT:
          print(pygame.mouse.get_pos())
        
    window.fill(white)
    small_font = pygame.font.Font('Orbitron-Regular.ttf', 30)
    paused_text = small_font.render("paused", True, black)
    window.blit(paused_text, [187,285])
    pygame.display.flip()
  #display info screen  
  while info:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
        info = not info
      elif event.type == pygame.MOUSEBUTTONUP:
          if event.button == pygame.BUTTON_LEFT:
            print(pygame.mouse.get_pos())

      window.fill(white)
      key_x = 95
      value_x = key_x + 100
      y = 160
      
      arrow_font = pygame.font.Font('WorkSans-Regular.ttf', 25)
      small_font = pygame.font.Font('Orbitron-Regular.ttf', 25)
      large_font = pygame.font.Font('Orbitron-Regular.ttf', 30)

      info_text = large_font.render("HOW TO PLAY", True, black)
      
      right_arrow_text = arrow_font.render("→", True, black)
      left_arrow_text = arrow_font.render("←", True, black)
      down_arrow_text = arrow_font.render("↓", True, black)
      A_text = small_font.render("A", True, black)
      D_text = small_font.render("D", True, black)
      C_text = small_font.render("C", True, black)
      P_text = small_font.render("P", True, black)

      ra_value_text = small_font.render("MOVE RIGHT", True, black)
      la_value_text = small_font.render("MOVE LEFT", True, black)
      da_value_text = small_font.render("MOVE DOWN", True, black)
      A_value_text = small_font.render("ROTATE LEFT", True, black)
      D_value_text = small_font.render("ROTATE RIGHT", True, black)
      C_value_text = small_font.render("SWAP", True, black)
      P_value_text = small_font.render("PAUSE", True, black)
     
      keys = [right_arrow_text,
              left_arrow_text,
              down_arrow_text,
              A_text,
              D_text,
              C_text,
              P_text]
      values = [ra_value_text,
               la_value_text,
               da_value_text,
               A_value_text,
               D_value_text,
               C_value_text,
               P_value_text]

      window.blit(info_text, [129,50])
      
      for i in range(len(keys)):
        window.blit(keys[i],[key_x, y])
        window.blit(values[i],[value_x, y])
        pygame.draw.rect(window, black, [key_x - 10, y-4, 40, 40],2)
        y += 50
      
      #window.blit(paused_text, [187,285])
      pygame.display.flip()



'''
→ 
←
↓

''' 
