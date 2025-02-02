from pygame import*
from random import randint

init()

W, H = 700, 700
FPS = 60

mixer.init()
mixer.music.load('sounds/space.ogg')
mixer.music.set_volume(0.7)
mixer.music.play()

fire_snd = mixer.Sound('sounds/fire.ogg')

font.init()
font1 = font.SysFont('fonts/Bebas_Neue_Cyrillic.ttf', 35,bold=True)
font2 = font.SysFont('fonts/Bebas_Neue_Cyrillic.ttf', 100, bold=True)

window = display.set_mode([W, H])
display.set_caption("Shooter")

bg = transform.scale(image.load("images/kocmoc.png"), (W, H))

clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__ (self, x, y, width, height, speed, img):#констуктор класу
        super().__init__()#Виклик базового констуктора класу
        self.width = width #властивості
        self.height = height
        self.speed = speed
        self.image = transform.scale(image.load(img), (width, height))# завантаження і маштабування зображення
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self): # метод для відображення спрайту
        window.blit(self.image, (self.rect.x, self.rect.y))#малювання спрайту на вікні

class Player(GameSprite):
    def move(self):# метод для руху гравця
        keys_pressed = key.get_pressed()# отримання натиснутих клавіш
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < W - self.width:
            self.rect.x += self.speed
        
    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 15, 20, 20, 'images/bullet.png')
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):#метод для оновлення положення ворога
        global skipped #глобальна зиінна для підрахунку пропущених
        self.rect.y += self.speed #вниз
        if self.rect.y > H - self.height:#ворог вийшов за межі екрану
            self.rect.x = randint(0, W - self.width) #рандомна позиція після ріткнення або вбиття риби по х
            self.rect.y = 0 #скидання позиції по у
            skipped += 1 #збільшення пропущених ворогів

class Asteroid(GameSprite):
    def __init__ (self, x, y, width, height, speed, img):
        super().__init__( x, y, width, height, speed, img)#стоворення базових властиврстей
        self.angle = 0
        self.original_image = self.image

    def update(self):
        self.rect.y += self.speed
        self.angle += 2.5
        self.image = transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.y > H - self.height:
            self.rect.x = randint(0, W - self.width)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


player = Player(W/2, H - 100, 70, 100, 5, "images/kot1.png")
enemies = sprite.Group()
for i in range(10):
    enemy = Enemy (randint (0, W-70), randint(-35, 10), 70, 35, randint(1, 3), 'images/puba1.png')
    enemies.add(enemy)

asteroids = sprite.Group()
for i in range(3):
    asteroid1 = Asteroid (randint (0, W-70), randint(-35, 10), 70, 35, randint(1, 3), 'images/asteroid1.png')
    asteroids.add(asteroid1)

bullets = sprite.Group()


life = 3
killed = 0
skipped = 0
shoot_count = 30
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if shoot_count > 0:
                    fire_snd.play()  
                    player.fire()
                    shoot_count -=1  
            if e.key == K_r:
                finish = False
    if not finish:
        window.blit(bg, (0, 0))
        player.draw()
        player.move()

        enemies.draw(window)
        enemies.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()

        if sprite.groupcollide(bullets, enemies, True, True):#зіткнення куль з ворогами
            killed += 1 
            enemy = Enemy (randint (0, W-70), randint(-35, 10), 70, 35, randint(1, 3), 'images/puba1.png')
            enemies.add(enemy)

        if sprite.groupcollide (bullets, asteroids, True, False):#зіткнення куль з астероїдами
            pass

        if sprite.spritecollide(player, asteroids, True):#зіткнення ворога з астероїдами
            life -= 1
            asteroid1 = Asteroid (randint (0, W-70), randint(-35, 10), 70, 35, randint(1, 3), 'images/asteroid1.png')
            asteroids.add(asteroid1)

        if life < 0:
            finish = True

        if sprite.spritecollide(player, enemies, True):#зіткнення гравця з воргами
            life -= 1
            enemy = Enemy (randint (0, W-70), randint(-35, 10), 70, 35, randint(1, 3), 'images/puba1.png')
            enemies.add(enemy)

        skipped_txt = font1.render(f'Пропущено: {skipped}', True, (255, 255, 255))
        window.blit(skipped_txt, (10, 10))
        
        killed_txt = font1.render(f'Вбито: {killed}', True, (255, 255, 255))
        window.blit(killed_txt, (10, 35))
        
        life_txt = font2.render(f'Життя: {life}', True, (255, 255, 255))
        window.blit(life_txt, (400, 10))

        bullets_txt = font1.render(f'Кулі: {shoot_count}', True, (255, 255, 255))
        window.blit(bullets_txt, (10, 60))

    else:
        life = 3
        skipped = 0
        killed = 0
        shoot_count = 30
        for enemy in enemies:
            enemy.kill()
        for asteroid in asteroids:
            asteroid.kill()
        for bullet in bullets:
            bullets.kill()
        for i in range(10):
            enemy = Enemy (randint (0, W-70), randint(-35, 10), 70, 35, randint(1, 3), 'images/puba1.png')
            enemies.add(enemy)
        for i in range(3): 
            asteroid1 = Asteroid (randint (0, W-70), randint(-35, 10), 70, 35, randint(1, 3), 'images/asteroid1.png')
            asteroids.add(asteroid1)
    
    
    display.update()
    clock.tick(FPS)