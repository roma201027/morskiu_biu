from pygame import*
from random import randint
import math
from time import time as timer

img_back = "images/фон.png"
img_hero = "images/корабель2.png"
img_enemy = "images/корабель.jpg"
img_enemy2 = "images/корабель3.jpg"
img_cannonball = "images/ядро.png"
img_gun = "images/гармата.png"
img_torpedo = "images/торпеда.png"


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

sight = True
current_enemy = "pirate"

cannonballs = sprite.Group()
torpedos = sprite.Group()
pirates = sprite.Group()
kruisers = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, size_x, size_y, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(img), (size_x, size_y))
        self.size_x = size_x
        self.size_y = size_y
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Gun(GameSprite):
    def __init__(self, img, x, y, size_x, size_y):
        super().__init__(img, x, y, size_x, size_y, 0)
        self.angle = 0

    def update(self):
        mouse_x, mouse_y = mouse.get_pos()
        delta_x = mouse_x - self.rect.centerx
        delta_y = mouse_y - self.rect.centery
        self.angle = math.degrees(math.atan2(delta_y, delta_x))
        self.image = transform.rotate(transform.scale(image.load(img_gun), (self.size_x, self.size_y)), -self.angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def fire(self):
        cannonball = Cannonball(img_cannonball, self.rect.centerx, self.rect.centery, 25, 30, 25)
        cannonball.angle = self.angle
        cannonballs.add(cannonball)
        fire_sound.play()


class Cannonball(GameSprite):
    def __init__(self, img, x, y, size_x, size_y, speed):
        super().__init__(img, x, y, size_x, size_y, speed)
        self.angle = 0

    def update(self):
        angle_rad = math.radians(self.angle)
        self.rect.x += self.speed * math.cos(angle_rad)
        self.rect.y += self.speed * math.sin(angle_rad)
        if self.rect.right < 0 or self.rect.left > win_width or self.rect.bottom < 0 or self.rect.top > win_height:
            self.kill()

class Torpedo(GameSprite):
    def __init__(self, img, x, y, size_x, size_y, speed, mouse_y):
        super().__init__(img, x, y, size_x, size_y, speed)
        self.mouse_y = mouse_y

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= self.mouse_y:
            # todo:перевірка зіткнення з якимось ворогом
            self.kill()

class Enemy(GameSprite):
    def update(self):
        if not self.rect.y > win_height // 3*2:
            self.rect.y += self.speed

    def fire(self):
        pass







class Button(GameSprite):
    pass


player_boat = GameSprite(img_hero, 100, win_height - 100, win_width - 200, 100, 0)
gun_x = player_boat.rect.centerx
gun_y = player_boat.rect.top
player_gun = Gun(img_gun, gun_x, gun_y, 50, 100)

enemies_start = timer()
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                player_gun.fire()
            elif e.button == 3:
                mouse_x, mouse_y = mouse.get_pos()
                torpedo = Torpedo(img_torpedo, mouse_x, win_height, 10, 25, 20, mouse_y)
                torpedos.add(torpedo)

    if timer() - enemies_start >= 1:
        if current_enemy == "pirate":
            pirate = Enemy(img_enemy, randint(50, win_width - 100), -100, 50, 100, randint(1, 5))

    window.blit(background, (0, 0))
    player_boat.reset()


    if not finish:

        player_gun.update()
        cannonballs.update()
        cannonballs.draw(window)
        player_gun.reset()
        torpedos.draw(window)
        torpedos.update()


        text = counter_font.render("Рахунок:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = counter_font.render("Життя:" + str(life), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_coins = counter_font.render(f"Монети: {coins}", 1, (255, 255, 255))
        window.blit(text_coins, (10, 80))

    display.update()

    time.delay(50)
