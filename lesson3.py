# mengimport pygame
from pygame import *

# kelas gamesprite untuk sprite
class GameSprite(sprite.Sprite):
    # konstruktor
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # cara untuk memanggil konstruktor
        sprite.Sprite.__init__(self)
        # menyimpan gambar untuk setiap sprite
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        # menyimpan properti rect
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # metode untuk menggambar karakter di main window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# kelas pemain utama
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        # memanggli konstruktor gamesprite
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        # menyimpan kecepatan horizontal dan vertikal
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    # metode untuk update posisi pemain
    def update(self):
        # pergerakan horizontal
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        # deteksi tabrakan dengan dinding
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        # pergerakan vertikal
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)

    # metode untuk menembak peluru
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

# kelas musuh
class Enemy(GameSprite):
    side = "left"

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # memanggil konstruktor gamesprite
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    # memperbarui pergerakan musuh
    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

# kelas peluru
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # memanggil konstruktor gamesprite
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    # metode untuk memperbarui pergerakan peluru
    def update(self):
        self.rect.x += self.speed
        # menghapus peluru jika melewati batas layar
        if self.rect.x > win_width + 10:
            self.kill()

# membuat game window/ jendela permainan
win_width = 700
win_height = 500
display.set_caption("Maze")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223) # mengatur warna latar belakang

# membuat grup untuk dinding
barriers = sprite.Group()
# membuat grup untuk peluru 
bullets = sprite.Group()
# membuat grup untuk monster
monsters = sprite.Group()

# membuat objek dinding
w1 = GameSprite('platform2.png', win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)
barriers.add(w1)
barriers.add(w2)

# membuat sprite pemain dan objek akhir
packman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
final_sprite = GameSprite('pac-1.png', win_width - 85, win_height - 100, 80, 80)

# membuat monster
monster1 = Enemy('cyborg.png', win_width - 80, 150, 80, 80, 5)
monster2 = Enemy('cyborg.png', win_width - 80, 230, 80, 80, 5)
monsters.add(monster1)
monsters.add(monster2)

# variable untuk mengatur apakah permainan selesai
finish = False
run = True

# loop utama permainan
while run:
    time.delay(50) # mengatur delay waktu tiap iterasi
    for e in event.get(): # mengecek semua event
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0

    if not finish:
        window.fill(back) # mengatur warna belakang dengan warna
        packman.update() # memperbarui posisi pemain
        bullets.update() # memperbarui posisi peluru
        packman.reset() # menggambar ulang pemain
        bullets.draw(window) # menggambar semua peluru
        barriers.draw(window) # menggambar semua dinding 
        final_sprite.reset() # menggambar sprite akhir
        sprite.groupcollide(monsters, bullets, True, True) # cek tabrakan monster dan peluru
        monsters.update() # memperbarui posisi monster 
        monsters.draw(window) # memperbarui monster 
        sprite.groupcollide(bullets, barriers, True, False) # cek tabrakan peluru dan tembok

        # cek tabrakan antara pemain dengan monster
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            img = image.load('game-over_1.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

        # cek apakah pemain mencapai sprite akhir
        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
    display.update() # memperbarui tampilan layar