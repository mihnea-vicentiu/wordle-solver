import pygame
from wordle_game.ui.colors import colors_arr, colorTile

"""
Tiles draws each a 5x6 grid on the screen and has limited use for animations/drawing purposes
"""
class Tiles:
      #will initialize the coordinates on the screen of each tile
      def __init__(self, width, height):
            self.width, self.height = width, height
            self.coord = [[[0, 0] for i in range(width)] for i in range(height)]

            for i in range(self.height):
                  for j in range(self.width):
                        if i == 0 and j == 0:
                              self.coord[i][j][0], self.coord[i][j][1] = 210, 100
                        elif i > 0 and j == 0:
                              self.coord[i][j][0], self.coord[i][j][1] = self.coord[i - 1][j][0], self.coord[i - 1][j][1] + 65
                        else:
                              self.coord[i][j][0], self.coord[i][j][1] = self.coord[i][j - 1][0] + 65, self.coord[i][j - 1][1]

      #function will be used to draw a tile of the Wordle table
      def draw_tile(self, screen, x, y, sz, color):
            tile = pygame.Rect(x, y, sz, sz)
            if color == colors_arr[7] or color == colors_arr[6]:
                  pygame.draw.rect(screen, color, tile, 2)
                  return
            pygame.draw.rect(screen, color, tile)

      #function will be used to draw each tile of the Wordle table
      def draw_table(self, screen):
            height, width = self.height, self.width
            for i in range(height):
                  for j in range(width):
                        self.draw_tile(screen, self.coord[i][j][0], self.coord[i][j][1], 60, colorTile[i][j])
