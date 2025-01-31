#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
import pygame_menu

init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_w, player_h, player_x, player_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (player_w, player_h))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.player_speed = player_speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.player_speed
        elif key_pressed[K_d] and self.rect.x < w - 100:
            self.rect.x += self.player_speed

    def fire(self):
        bullet = Bullet('bullet3.png', 10, 50, self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

    def super_fire(self):
        bullet2 = Bullet('bullet4.png', 10, 75, self.rect.centerx, self.rect.top, -20)
        bullets2.add(bullet2)

lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.player_speed
        global lost
        if self.rect.y > h:
            self.rect.y = 0
            self.rect.x = randint(50, 1100)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.player_speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.player_speed
        if self.rect.y > h:
            self.rect.y = 0
            self.rect.x = randint(50, 1100)

class Bar(sprite.Sprite):
    def __init__(self, c_1, bar_x, bar_y, bar_w, bar_h):
        super().__init__()
        self.c_1 = c_1
        self.w = bar_w
        self.h = bar_h
        self.image = Surface((self.w, self.h))
        self.image.fill(c_1)
        self.rect = self.image.get_rect()
        self.rect.x = bar_x
        self.rect.y = bar_y
    def draw_bar(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
w, h = 1200, 1000

window = display.set_mode((w, h))

background = transform.scale(image.load('bg.jpeg'), (w, h))

bullets = sprite.Group()
bullets2 = sprite.Group()

mixer.music.load('Game of Space.mp3')
mixer.music.play()
mixer.music.set_volume(0.1)

def main():
    finish = False

    hero = Player('player.png', 110, 100, 590, 900, 10)

    font1 = font.Font(None, 36)

    font_lose = font1.render('YOU LOSE', True, (255, 0, 0))

    font_win = font1.render('YOU WIN', True, (0, 255, 0))

    font_reload = font1.render('Wait...', True, (255, 0, 0))

    monsters = sprite.Group()
    for i in range(3):
        monster = Enemy('enemy1_2.png', 100, 100, randint(50, 1100), -20, randint(1, 5))
        monsters.add(monster)

    monsters2 = sprite.Group()
    monster2 = Enemy('enemy2_1.png', 100, 100, randint(50, 1100), -20, randint(1, 5))
    monsters2.add(monster2)

    monsters3 = sprite.Group()
    monster3 = Enemy('enemy2_2.png', 100, 100, randint(50, 1100), -20, randint(1, 5))
    monsters3.add(monster3)

    bar1 = Bar((0, 0, 0), 997, 47.5, 215, 55)
    bar2 = Bar((0, 255, 0), 1000, 50, 210, 50)
    bar3 = Bar((240, 166, 29), 1000, 50, 140, 50)
    bar4 = Bar((255, 0, 0), 1000, 50, 70, 50)

    bar1_1 = Bar((0, 0, 0), 497, 897.5, 215, 55)
    bar2_1 = Bar((0, 255, 0), 500, 900, 210, 50)
    bar3_1 = Bar((240, 166, 29), 500, 900, 140, 50)
    bar4_1 = Bar((255, 0, 0), 500, 900, 70, 50)

    hp = 3

    score = 0

    clock = time.Clock()
    FPS = 60

    num_fire = 0
    rel_time = False

    num_fire2 = 0
    rel_time2 = False

    while True:
        for e in event.get():
            if e.type == QUIT:
                return

            elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                if num_fire < 5 and rel_time == False:
                    hero.fire()
                    num_fire += 1
                
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start_time = timer()
            elif e.type == MOUSEBUTTONDOWN and e.button == 3:
                if num_fire2 < 5 and rel_time2 == False:
                    hero.super_fire()
                    num_fire2 += 1
                
                if num_fire2 >= 5 and rel_time2 == False:
                    rel_time2 = True
                    start_time2 = timer()
        
        if not finish:
            window.blit(background, (0, 0))
            hero.reset()

            hero.update()

            monsters.update()
            monsters.draw(window)

            monsters2.draw(window)
            monsters2.update()

            monsters3.draw(window)
            monsters3.update()

            bullets.draw(window)
            bullets.update()
            
            bullets2.draw(window)
            bullets2.update()

            if rel_time:
                finish_time = timer()
                if finish_time - start_time < 3:
                    window.blit(font_reload, (500, 900))
                    bar1_1.draw_bar()
                    bar4_1.draw_bar()
                    if finish_time - start_time < 2:  
                        bar1_1.draw_bar()
                        bar3_1.draw_bar()
                        if finish_time - start_time < 1:
                            bar1_1.draw_bar()
                            bar2_1.draw_bar()
                else:
                    num_fire = 0
                    rel_time = False

            if rel_time2:
                finish_time2 = timer()
                if finish_time2 - start_time2 < 3:
                    window.blit(font_reload, (500, 900))
                    bar1_1.draw_bar()
                    bar4_1.draw_bar()
                    if finish_time2 - start_time2 < 2:  
                        bar1_1.draw_bar()
                        bar3_1.draw_bar()
                        if finish_time2 - start_time2 < 1:
                            bar1_1.draw_bar()
                            bar2_1.draw_bar()
                else:
                    num_fire2 = 0
                    rel_time2 = False
                    

            score_font = font1.render(f'Пропущено: {lost}', True, (255, 255, 255))
            window.blit(score_font, (100, 0))

            score_win_font = font1.render(f'Сбито: {score}', True, (255, 255, 255))
            window.blit(score_win_font, (100, 40))

            sprites_list = sprite.groupcollide(monsters, bullets, True, True) or sprite.groupcollide(monsters, bullets2, True, True)
            sprites2_list = sprite.groupcollide(monsters2, bullets, True, True) or sprite.groupcollide(monsters2, bullets2, True, True)
            sprites3_list = sprite.groupcollide(monsters3, bullets2, True, True)

            for _ in sprites_list:
                score += 1
                monster = Enemy('enemy1_2.png', 100, 100, randint(50, 1100), -20, randint(1, 5))
                monsters.add(monster)

            for _ in sprites2_list:
                score += 1
                monster2 = Enemy('enemy2_1.png', 100, 100, randint(50, 1100), -20, randint(5, 10))
                monsters2.add(monster2)

            for _ in sprites3_list:
                score += 1
                monster3 = Enemy('enemy2_2.png', 100, 100, randint(50, 1100), -20, randint(10, 13))
                monsters3.add(monster3)

            if sprite.spritecollide(hero, monsters, True) or sprite.spritecollide(hero, monsters2, True) or sprite.spritecollide(hero, monsters3, True):
                hp -= 1
            if score >= 7:
                window.blit(font_win, (600, 500))
                finish = True

            if lost >= 6 or hp == 0:
                window.blit(font_lose, (600, 500))
                finish = True

            if hp == 3:
                bar1.draw_bar()
                bar2.draw_bar()
            elif hp == 2:
                bar1.draw_bar()
                bar3.draw_bar()
            elif hp == 1:
                bar1.draw_bar()
                bar4.draw_bar()
            elif hp <= 0:
                bar1.draw_bar()
            

        display.update()
        clock.tick(FPS)

def start():
    #font = pygame_menu.font.FONT_8BIT
    #my_theme = Theme(widget_font = font, theme = pygame_menu.themes.THEME_BLUE)
    menu = pygame_menu.Menu('Shooter', w, h)
    menu.add.label('Game')
    menu.add.button('Play', main)
    menu.add.button('Exit', pygame_menu.events.EXIT)
    menu.mainloop(window)

start()
