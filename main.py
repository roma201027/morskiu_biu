from pygame import*
from random import randint


img_back = "images/фон.png"
img_hero = "images/корабель2.jpg"
img_enemy = "images/корабель.jpg"
img_enemy2 = "images/корабель3.jpg"


win_width = 700
win_height = 500


display.set_caption("MorshuiBui")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


finish = False
run = True


mixer.init()
# mixer.music.load('pushechnyiy-odinochnyiy-zalp.mp3')
# mixer.music.play(-1)
fire_sound = mixer.Sound("sounds/pushechnyiy-odinochnyiy-zalp.mp3")


font.init()
counter_font = font.Font(None, 36)

score = 0
coins = 0
life = 5


class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, size_x, size_y, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(img), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Gun(GameSprite):
    pass

player_boat = GameSprite(img_hero, 100, win_height - 100, win_width - 200, 100, 0)


while run:

    for e in event.get():
        if e.type == QUIT:
            run = False


    if not finish:
        window.blit(background, (0, 0))

        text_score = counter_font.render("Рахунок:" + str(score), 1, (255, 255, 255))
        window.blit(text_score, (win_width - 100, 20))

        text_life =  counter_font.render("Життя:" + str(life), 1, (255, 255, 255))
        window.blit(text_life, (win_width - 100, 50))


        player_boat.reset()

        # monsters.update()
        # monsters.draw(window)

        display.update()

    time.delay(50)
