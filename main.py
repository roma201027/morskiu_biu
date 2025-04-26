from pygame import*
from random import randit

img_back = "фон.png"
img_hero = "корабель2.jpg"
img_enemy = "корабель.jpg"
img_enemy2 = "корабель3.jpg"

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("фон.png"),(win_width, win_height))


game = True
finish = False

mixer.init()
mixer.music.load('')
mixer.music.play(-1)








while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0, 0))

    display.update()
    time.delay(50)

