# This program is for the game Pong
# References: Python 3 and Pygame Documentation
# Author: Urvi Patel

import pygame


# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Pong')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game():
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True 
      
      # === game specific objects
      self.ball = Ball('white', 5, [250, 200], [4, 1], self.surface)
      self.paddle_y = 175
      self.paddle_width = 10
      self.paddle_height = 40
      self.left_paddle = pygame.Rect(100, self.paddle_y, self.paddle_width, self.paddle_height)
      self.right_paddle = pygame.Rect(390, self.paddle_y, self.paddle_width, self.paddle_height)
      self.l_score = 0
      self.r_score = 0
      pygame.key.set_repeat(20, 20)
      
   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      self.list_of_events = pygame.key.get_pressed()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         elif event.type == pygame.KEYDOWN and self.continue_game:
            self.handle_keydown(event)
         elif event.type == pygame.KEYUP and self.continue_game:
            self.handle_keyup(event)
              
   def handle_keydown(self,event):
      # handle keydown event
      # - self is the Game whose keydown events will be handled
      
      self.paddle_min_height = 0
      self.paddle_max_height = self.surface.get_height()- self.paddle_height 
      self.paddle_velocity = 10
      if self.list_of_events[pygame.K_a] and self.left_paddle.y < self.paddle_max_height:
         self.left_paddle.y += self.paddle_velocity
      if self.list_of_events[pygame.K_q] and self.left_paddle.y > self.paddle_min_height:
         self.left_paddle.y -= self.paddle_velocity    
      if self.list_of_events[pygame.K_l] and self.right_paddle.y < self.paddle_max_height:
         self.right_paddle.y += self.paddle_velocity
      if self.list_of_events[pygame.K_p] and self.right_paddle.y > self.paddle_min_height:
         self.right_paddle.y -= self.paddle_velocity
   
   def handle_keyup(self, event):
      # handle keyup event
      # - self is the Game whose keyup events will be handled
      
      if event.key == pygame.K_a or event.key == pygame.K_q:
         self.left_paddle.y += 0 
      if event.key == pygame.K_l or event.key == pygame.K_p:
         self.right_paddle.y += 0        

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.ball.draw()
      pygame.draw.rect(self.surface, pygame.Color('white'), self.left_paddle)
      pygame.draw.rect(self.surface, pygame.Color('white'), self.right_paddle)
      self.draw_score()
      pygame.display.update() # make the updated surface appear on the display
   
   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      
      self.ball.move()
      self.collision()
      self.update_score()     
       
   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check  
      
      max_score = 11
      if self.l_score == max_score or self.r_score == max_score:
         self.continue_game = False

   def draw_score(self):
      # draw left and right score
      self.score_font = pygame.font.SysFont('',75)
      self.score_fg_color = pygame.Color('white')
      self.l_score_image = self.score_font.render(str(self.l_score), True, self.score_fg_color)
      self.surface.blit(self.l_score_image, (0,0))
      self.r_score_image = self.score_font.render(str(self.r_score), True, self.score_fg_color)
      self.width = self.surface.get_width() - self.r_score_image.get_width()
      self.r_score_location = (self.width,0)
      if self.r_score >=10:
         self.width = self.surface.get_width() - self.r_score_image.get_width()
         self.r_score_location = (self.width,0)
      self.surface.blit(self.r_score_image, (self.r_score_location))
      
   def update_score(self):
      # updates scores if ball hit opposite edge
      # - self is the Game where the scores will be updated
      
      w_size = self.surface.get_size()
      if self.ball.center[0] < self.ball.radius:
         self.r_score += 1
      if self.ball.center[0] > w_size[0] - self.ball.radius:
         self.l_score += 1  
         
   def collision(self):
      # test to see if ball collides with paddles
      # - self is the Game where collision will be checked
      
      self.test_left_paddle = self.ball.velocity[0] < 0 and self.left_paddle.collidepoint(self.ball.center)
      self.test_right_paddle = self.ball.velocity[0] > 0 and self.right_paddle.collidepoint(self.ball.center)
      if self.test_left_paddle or self.test_right_paddle:
         self.ball.velocity[0] =  - self.ball.velocity[0]

class Ball:
   # An object in this class represents a Ball that moves 
   
   def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
      # Initialize a Ball.
      # - self is the Ball to initialize
      # - color is the pygame.Color of the ball
      # - center is a list containing the x and y int
      #   coords of the center of the ball
      # - radius is the int pixel radius of the ball
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object

      self.color = pygame.Color(ball_color)
      self.radius = ball_radius
      self.center = ball_center
      self.velocity = ball_velocity
      self.surface = surface
      
   def move(self):
      # Change the location of the ball by adding the corresponding 
      # speed values to the x and y coordinate of its center
      # - self is the Ball
      
      w_size = self.surface.get_size()
      for index in range(len(self.center)):
         self.center[index] = self.center[index] + self.velocity[index] 
         if (self.center[index] < self.radius 
             or self.center[index] > w_size[index] - self.radius): # check top/left edge and bottom/right edge
               self.velocity[index] = - self.velocity[index] # "bounce"
            
   def draw(self):
      # Draw the ball on the surface
      # - self is the Ball
      
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)


main()