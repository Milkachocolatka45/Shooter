from pygame import*
from random import randint

init()

W, H = 700, 700

window = display.set_mode([W, H])
display.set_caption("Shooter")

bg = transform.scale(image.load("images/kocmoc.png"), (W, H))

clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__ (self, x, y, width, height, speed, img):
        super().__init__()
        self.width = width
        self.height = height
        self.speed = speed
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x < W - self.width:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < W + self.width:
            self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        global killed 
        self.rect.y += self.speed
        if self.rect.y > H - self.height:
            self.rect.x = randit(0, W - self.width)
            self.rect.y = 0
            killed += 1

class Asteroid(GameSprite):
    def __init__ (self, x, y, width, height, speed, img):
        super().__init__( x, y, width, height, speed, img)
        self.angle = 0
        self.original_image = self.image


    def update(self):
        self.rect.y += self.speed
        self.angle += 2.5
        self.image = transform.rotate(self.original_image, self.angle)
        if self.rect.y > H - self.height:
            self.rect.x = randit(0, W - self.width)
            self.rect.y = 0





player = Player(W/2, H - 100, 200, 100, 5, "images/kot1.png")
enemies = sprite.Group()
for i in range(5):
    enemy = Enemy (randint (0, W-70), randint(-35, 10), 70, 35, randint(1, 3), 'images/puba1.png')
    enemies.add(enemy)
asteroid1 = Asteroid (randint (0, W-70), randint(-35, 10), 70, 35, randint(1, 3), 'images/ufo.png')


life = 3
kill = 0
skipped = 0
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False




    

    window.blit(bg, (0, 0))
    player.draw()
    player.move()

    enemies.draw(window)
    enemies.update()

    asteroid1.draw()
    asteroid1.update()

    display.update()
    clock.tick(60)