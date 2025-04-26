from pygame import*
from random import randit
import sys

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
mixer.music.load('pushechnyiy-odinochnyiy-zalp.mp3')
mixer.music.play(-1)








while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0, 0))

    display.update()
    time.delay(50)





pygame.init()

# Налаштування екрана
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Кнопка з малюнком в Pygame')

# Кольори
WHITE = (255, 255, 255)

# Завантаження малюнка
# Увага: помісти свій малюнок у ту ж папку і назви його 'button_image.png'
button_image = pygame.image.load('button_image.png')
button_size = 100
button_image = pygame.transform.scale(button_image, (button_size, button_size))

# Створення кнопки
button_rect = pygame.Rect(250, 150, button_size, button_size)

# Основний цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                print('Кнопка з малюнком натиснута!')

    screen.fill(WHITE)
    screen.blit(button_image, button_rect.topleft)
    pygame.display.flip()
