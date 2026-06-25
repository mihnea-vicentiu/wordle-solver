#colors thats will be used throughout the playing of the game
Green = "#538d4e"
Yellow = "#b59f3b"
Grey1 = "#3a3a3c"
Grey2 = "#565758"
Grey3 = "#3a3a3d"
Black = "#121213"
White = "#ffffff"
Red = "#cc0000"

#color red was used in an now deleted animation for the game, left it there beacuse it would involve a lot of reindexing on a lot of code so i was to lasy to modify it : )

#make an array of colors
colors_arr = [White, Black, Green, Yellow, Red, Grey1, Grey2, Grey3]

#this array wil be used for Animations.outcome_animation()
colorTemp = [colors_arr[7] for i in range(10)]

#this grid will tell what each tile color should be throughout the Worlde game
colorTile = [[colors_arr[7] for i in range(10)] for i in range(10)]


def reset_colors():
      for i in range(len(colorTemp)):
            colorTemp[i] = colors_arr[7]

      for i in range(len(colorTile)):
            for j in range(len(colorTile[i])):
                  colorTile[i][j] = colors_arr[7]
