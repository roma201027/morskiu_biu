from pygame import*
from random import randint


img_back = "images/фон.png"
img_hero = "images/корабель2-removebg-preview.png"
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
mixer.music.load('sounds/there-be-pirates-the-quest-323338.mp3')
mixer.music.play(-1)
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
    window.blit(background, (0, 0))
    player_boat.reset()

    if not finish:


        text = counter_font.render("Рахунок:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = counter_font.render("Життя:" + str(life), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_coins = counter_font.render(f"Монети: {coins}", 1, (255, 255, 255))
        window.blit(text_coins, (10, 80))

    display.update()

    time.delay(50)
