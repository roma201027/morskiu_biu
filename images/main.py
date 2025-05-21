from pygame import*
from random import randint
import math
from time import time as timer

img_back = "images/фон.png"
img_hero = "images/корабель2.png"
img_enemy = "images/корабель.png"
img_enemy2 = "images/корабель3.png"
img_cannonball = "images/ядро.png"
img_gun = "images/гармата.png"
img_torpedo = "images/торпеда.png"
img_fire = "images/приціл.png"
img_catch = "images/сітка.png"

win_width = 700
win_height = 500


display.set_caption("MorshuiBui")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


finish = False
run = True
mode = "fire"



mixer.init()
mixer.music.load('sounds/there-be-pirates-the-quest-323338.mp3')
mixer.music.play(-1)
fire_sound = mixer.Sound("sounds/pushechnyiy-odinochnyiy-zalp.mp3")


font.init()
counter_font = font.Font(None, 36)
font1 = font.SysFont(None, 80) # написи для перемоги та поразки
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))



score = 0
coins = 0
life = 5

sight = True
current_enemy = "pirate"

cannonballs = sprite.Group()
torpedos = sprite.Group()
pirates = sprite.Group()
kruisers = sprite.Group()
snarads = sprite.Group()
bonus_ships = sprite.Group()

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
        cannonball = Cannonball(img_cannonball, self.rect.centerx, self.rect.centery, 25, 25, 20)
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
    def __init__(self, img, x, y, size_x, size_y, speed):
        super().__init__(img, x, y, size_x, size_y, speed)
        self.shoot_time = timer()
        self.is_moving = True

    def update(self):
        # Логіка руху залишається, оскільки ворог рухається до зіткнення
        if not self.rect.centery > win_height // 2:
            self.rect.y += self.speed
        else:
            self.is_moving = False
        self.fire()

    def fire(self):
        # Ворог стріляє, якщо не рухається і не був знищений
        if not self.is_moving: # Немає потреби перевіряти is_hit, бо він одразу зникає
            if timer() - self.shoot_time >= 5:
                snarad = Torpedo(img_cannonball, self.rect.centerx, self.rect.centery, 15, 15, -10, self.rect.centerx)
                snarads.add(snarad)
                self.shoot_time = timer()


class BonusShip(GameSprite):
    def __init__(self, img, size_x, size_y, speed):
        side = randint(0, 1)
        y = randint(50, win_height // 2 - 50)
        if side == 0:
            x = -size_x
            self.direction = 1  # рух праворуч
        else:
            x = win_width
            self.direction = -1  # рух ліворуч
        super().__init__(img, x, y, size_x, size_y, speed)

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0 or self.rect.left > win_width:
            self.kill()


# class Button(GameSprite):
#     pass


player_boat = GameSprite(img_hero, 100, win_height - 100, win_width - 200, 100, 0)
button_fire = GameSprite(img_fire, 30, win_height - 70, 50, 50, 0)
button_catch = GameSprite(img_catch, win_width -80, win_height - 70, 50, 50, 0)
gun_x = player_boat.rect.centerx
gun_y = player_boat.rect.top
player_gun = Gun(img_gun, gun_x, gun_y, 50, 100)
bonus_spawn_time = timer()
enemies_start = timer()


while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN:
            x, y = mouse.get_pos()
            if button_fire.rect.collidepoint(x, y):
                mode = "fire"
            elif button_catch.rect.collidepoint(x, y):
                mode = "catch"
            elif mode == "fire":
                if e.button == 1:
                    player_gun.fire()
                elif e.button == 3:
                    mouse_x, mouse_y = mouse.get_pos()
                    torpedo = Torpedo(img_torpedo, mouse_x, win_height, 10, 25, 20, mouse_y)
                    torpedos.add(torpedo)
            elif mode == "catch":
                for bonus in bonus_ships:
                    if bonus.rect.collidepoint(x, y):
                        coins += 1
                        bonus.kill()


    if timer() - enemies_start >= 2:
        if current_enemy == "pirate":
            pirate = Enemy(img_enemy2, randint(50, win_width - 100), -100, 50, 100, randint(1, 3))
            current_enemy = "kruiser"
            enemies_start = timer()
            pirates.add(pirate)
        elif current_enemy == "kruiser":
            kruiser = Enemy(img_enemy, randint(50, win_width - 100), -100, 50, 100, randint(1, 3))
            current_enemy = "pirate"
            kruisers.add(kruiser)
            enemies_start = timer()
    if timer() - bonus_spawn_time >= 10:
        bonus = BonusShip(img_enemy2, 50, 50, randint(2, 4))  # використовується img_enemy2 або окрема картинка
        bonus_ships.add(bonus)
        bonus_spawn_time = timer()

    window.blit(background, (0, 0))
    player_boat.reset()

    button_fire.reset()
    button_catch.reset()
    if not finish:

        player_gun.update()
        cannonballs.update()
        cannonballs.draw(window)
        player_gun.reset()
        torpedos.draw(window)
        torpedos.update()
        snarads.draw(window)
        snarads.update()
        kruisers.update()
        kruisers.draw(window)
        pirates.update()
        pirates.draw(window)
        bonus_ships.update()
        bonus_ships.draw(window)

        text = counter_font.render("Рахунок:" + str(score), 1, (0, 0, 0))
        window.blit(text, (10, 20))

        text_lose = counter_font.render("Життя:" + str(life), 1, (0, 0, 0))
        window.blit(text_lose, (10, 50))

        text_coins = counter_font.render(f"Монети: {coins}", 1, (0, 0, 0))
        window.blit(text_coins, (10, 80))


        # Collision for pirates: now they disappear immediately
        collides_pirates = sprite.groupcollide(pirates, cannonballs, True, True)
        for p in collides_pirates:
            score += 1

        # Collision for kruisers: now they disappear immediately
        collides_kruisers = sprite.groupcollide(kruisers, torpedos, True, True)
        for k in collides_kruisers:
            score += 1

        if sprite.spritecollide(player_boat, snarads, False):
            sprite.spritecollide(player_boat, snarads, True)
            # sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        sprite.groupcollide(bonus_ships, cannonballs, True, True)
        sprite.groupcollide(bonus_ships, torpedos, True, True)

    if life <= 0:
        finish = True
        window.blit(lose, (200, 200))

    if coins >= 5 and score >= 40:
        finish = True
        window.blit(win, (200, 200))


    display.update()

    time.delay(50)
