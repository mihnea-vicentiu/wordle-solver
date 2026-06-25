from wordle_game.ui.colors import colorTemp, colorTile

#this class will be used to draw the animation of the Worlde game
#the animations can be turned off
class Animations:
      #turn on/off animations
      def turn_off(self):
            self.active = False
      
      def turn_on(self):
            self.active = True

      """
      this function will be used to draw the animation when you insert a new letter
      to describe the process of how we draw the animation:
            we basically select the current position we intserted a letter to and expent the rectagle that 
      """
      def insert_animation(self, configs, tiles, letters, score):
            height, width = tiles.height, tiles.width
            lx, ly = letters.x, letters.y
            
            #zoom out/expand cell
            for rep in range(10):
                  #we skip the animation if we sought so
                  if self.active == False:
                        break

                  configs.event_handle_solver()
                  configs.screen_init_(score, True)

                  for i in range(height):
                        for j in range(width):
                              x, y = tiles.coord[i][j][0], tiles.coord[i][j][1]
                              color = colorTile[i][j]
                              if i == ly and j == lx:
                                    #coordinates were set in such a way that it just looks good to the naked eye when we draw the animation
                                    tiles.draw_tile(configs.screen, x - 5, y - 3, 60 + rep + 1, color)
                                    continue
                              tiles.draw_tile(configs.screen, x, y, 60, color)

                  letters.draw(configs.screen, configs.font)
                  configs.update_screen(120)

      """
      this function will be used to draw the animation when you insert a new guess
      to describe the process of how we draw the animation:
            we basically go from the first to the last cell in which we introduced the word and firstly we shrink the cell
            and then we expand the cell with its coresponding color after the guess 
      """
      def outcome_animation(self, configs, tiles, letters, score):
            height, width = tiles.height, tiles.width
            ly = letters.y
            #zoom in
            for lx in range(width):
                  #we skip the animation if we sought so
                  if self.active == False:
                        for j in range(width):
                              colorTile[ly][j] = colorTemp[j]
                        break

                  #zoom in/shrink cell
                  for rep in range(30):
                        configs.event_handle_solver()
                        configs.screen_init_(score, True)

                        for i in range(height):
                              for j in range(width):
                                    x, y = tiles.coord[i][j][0], tiles.coord[i][j][1]
                                    color = colorTile[i][j]
                                    if i == ly and j == lx:
                                          #coordinates were set in such a way that it just looks good to the naked eye when we draw the animation
                                          tiles.draw_tile(configs.screen, x + rep, y + rep + 1, 60 - (rep + 1) * 2, color)
                                          continue
                                    tiles.draw_tile(configs.screen, x, y, 60, color)

                        letters.draw(configs.screen, configs.font)
                        configs.update_screen(120)
                  
                  #zoom out/expand cell
                  for rep in range(30):
                        configs.event_handle_solver()
                        configs.screen_init_(score, True)

                        for i in range(height):
                              for j in range(width):
                                    x, y = tiles.coord[i][j][0], tiles.coord[i][j][1]
                                    txt = letters.str[i][j]
                                    color = colorTile[i][j]
                                    if i == ly and j == lx:
                                          #coordinates were set in such a way that it just looks good to the naked eye when we draw the animation
                                          tiles.draw_tile(configs.screen, x + (29 - rep + 1), y, (rep + 1) * 2, colorTemp[j])
                                          colorTile[i][j] = colorTemp[j]
                                          letters.draw_letter(configs.screen, x, y, txt, configs.font)
                                          continue

                                    tiles.draw_tile(configs.screen, x, y, 60, color)
                                    letters.draw_letter(configs.screen, x, y, txt, configs.font)

                        configs.update_screen(120)

                  configs.update_screen(120)


      #used for drawing the aniamtion when an invalid word is being introduced as a guess
      """
      this animation is used by the manual play workflow for invalid guesses
      to describe the basic process of how we draw the animation:
            we basically shift the position of the cells form left to right and the position of the letters in the cells as well using
            the matrix offset
      """
      def worng_animation(self, configs, tiles, letters, score):
            height, width = tiles.height, tiles.width
            ly = letters.y
            offset = [[[0, 0] for i in range(width)] for i in range(height)]
            #wigle around 3 times
            for rep in range(3):
                  #shift left
                  for rep in range(10):
                        configs.event_handle_solver()
                        configs.screen_init_(score, True)
                        for i in range(height):
                              for j in range(width):
                                    x, y = tiles.coord[i][j][0], tiles.coord[i][j][1]
                                    color = colorTile[i][j]
                                    if i == ly:
                                          offset[i][j][0], offset[i][j][1] = rep + 1, 0
                                          tiles.draw_tile(configs.screen, x + (rep + 1), y, 60, color)
                                          continue
                                    offset[i][j][0], offset[i][j][1] = 0, 0
                                    tiles.draw_tile(configs.screen, x, y, 60, colorTile[i][j])
                        
                        letters.draw_offset(configs.screen, configs.font, offset)
                        configs.update_screen(120)

                  #shift right
                  for rep in range(10):
                        configs.event_handle_solver()
                        configs.screen_init_(score, True)
                        for i in range(height):
                              for j in range(width):
                                    if i == letters.y:
                                          offset[i][j][0], offset[i][j][1] = -(rep + 1), 0 
                                          tiles.draw_tile(configs.screen, tiles.coord[i][j][0] - (rep + 1), tiles.coord[i][j][1], 60, colorTile[i][j])
                                          continue
                                    offset[i][j][0], offset[i][j][1] = 0, 0
                                    tiles.draw_tile(configs.screen, tiles.coord[i][j][0], tiles.coord[i][j][1], 60, colorTile[i][j])
                        letters.draw_offset(configs.screen, configs.font, offset)
                        configs.update_screen(120)
