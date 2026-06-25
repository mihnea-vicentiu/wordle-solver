"""
This class was made to clean up and improve readability for the code of animations and the main program
TLDR; most of this functions were implemented in assets.animations but after some thought I decided that is best to separate them into different classes
It handles events and basic window mangements
"""
import pygame
from wordle_game.paths import IMAGES_DIR
from wordle_game.ui.colors import colors_arr
from wordle_game.ui.interactor import push_exit

class GameConfig:
      def __init__(self, uses_solver=False):
            self.uses_solver = uses_solver
            #here we initialize the game window
            self.screen = pygame.display.set_mode((800, 700))
            pygame.display.set_caption("Wordle!")
            icon = pygame.image.load(str(IMAGES_DIR / "Icon.png"))
            pygame.display.set_icon(icon)

            #title of the game
            self.title = pygame.image.load(str(IMAGES_DIR / "title.png")).convert()
            #font of each letter/to be able to use it dowload each .ttf from the zip attachement in assets/font
            self.font = pygame.font.SysFont('Clear Sans', 40)
            #clock is used to drag out the animation of the wordle game
            self.clock = pygame.time.Clock()

      #funtions draws text at the bottom of the screen keeping track of the number of guessed made so far
      def draw_cur_guesses(self, score):
            textsur = self.font.render("Number of guesses:", True, colors_arr[0])
            textrect = textsur.get_rect()
            textrect.center = (370, 530)
            self.screen.blit(textsur, textrect)

            cntsur = self.font.render(str(score), True, colors_arr[0])
            cntrect = cntsur.get_rect()
            cntrect.center = (370, 570)
            self.screen.blit(cntsur, cntrect)

      def draw_tot_guesses(self, score):
            textsur = self.font.render("Total number of guesses:", True, colors_arr[0])
            textrect = textsur.get_rect()
            textrect.center = (370, 530)
            self.screen.blit(textsur, textrect)

            cntsur = self.font.render(str(score), True, colors_arr[0])
            cntrect = cntsur.get_rect()
            cntrect.center = (370, 570)
            self.screen.blit(cntsur, cntrect)

      #this function will be called when we want to draw something on the screen
      def screen_init_(self, score, is_running):
            self.screen.fill(colors_arr[1])
            self.screen.blit(self.title, (300, 25))

            #if the game is running display current nr. of guesses otherwise display total nr. of guesses
            if is_running == True:
                  self.draw_cur_guesses(score)
                  return
            
            self.draw_tot_guesses(score)
      
      #update the screen after we draw everything
      def update_screen(self, nr_ticks=60):
            pygame.display.update()
            self.clock.tick(nr_ticks)

      #handles screen events
      def event_handle_solver(self):
             for event in pygame.event.get():
                  #click on the X to close the program
                  if event.type == pygame.QUIT:
                        if self.uses_solver:
                              push_exit()
                        pygame.quit()
                        exit()

