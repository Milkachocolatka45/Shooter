from pygame import*

init()

W, H = 700, 700

window = display.set_mode([W, H])
display.set_caption("Shooter")

bg = transform.scale(image.load("images/galaxy.jpg"), (W, H))

clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__ (self, x, y, width, height, speed, img):
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

player = Player(W/2, H - 100, 30, 100, 5, "images/rocket.png")


game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(bg, (0, 0))
    player.draw()
    player.move()
    display.update()
    clock.tick(60)