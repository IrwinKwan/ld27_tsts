#!/bin/env python

"""
Ludum Dare 27
A 48 hour compo starting April 26, 2013.

The theme? Dunno yet.

Game written by Arcana (c 2013).

Code license: BSD
"""

import os
import sys
import math
import random

import pygame
from pygame.locals import *
from pygame.compat import geterror

from asset import *
from constant import Constant, V
from characters import *


def main(winstyle = 0):
    pygame.mixer.quit()
    pygame.init()
    if not pygame.font:
        print ('Warning, fonts disabled')

    if not pygame.mixer:
        print ('Warning, sound disabled')

    winstyle = 0  # |FULLSCREEN
    screen_rect = pygame.Rect(0, 0, Constant.SCREEN_WIDTH, Constant.SCREEN_HEIGHT)
    bestdepth = pygame.display.mode_ok(screen_rect.size, winstyle, 32)
    screen = pygame.display.set_mode(screen_rect.size, winstyle, bestdepth)
    screen = pygame.display.set_mode(screen_rect.size)
    pygame.mouse.set_visible(False)
    pygame.display.set_caption("LD27 by Arcana")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    (Bullet.fastimage, Bullet.fastrect) = Asset.load_one_alpha_image("fastbullet.png", Color("white"))
    (Bullet.strongimage, Bullet.strongrect) = Asset.load_one_alpha_image("strongbullet.png", Color("white"))

    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    all = pygame.sprite.LayeredUpdates()
    Point.containers = all
    Player.containers = all
    Crosshairs.containers = all
    Bullet.containers = all

    Enemy.containers = all

    player = Player()
    crosshairs = Crosshairs()

    shoot_cooldown = 0
    last_cooldown = 0

    shot_down = 0
    last_respawn = 0

    shot_mode = "fast"

    playing = True
    while playing:

        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        prev_mouse_position = pygame.mouse.get_pos()
        going = True

        while player.alive() and going == True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    going = False

            keystate = pygame.key.get_pressed()

            all.clear(screen, background)
            all.update()

            if keystate[K_LEFT] or keystate[K_a]:
                player.move("left")
            elif keystate[K_RIGHT] or keystate[K_d]:
                player.move("right")
            elif keystate[K_UP] or keystate[K_w]:
                player.move("up")
            elif keystate[K_DOWN] or keystate[K_s]:
                player.move("down")

            if keystate[K_1]:
                shot_mode = "fast"
            elif keystate[K_2]:
                shot_mode = "strong"

            if shot_mode == "fast":
                if Bullet.fast - shoot_cooldown <= 0:
                    shoot_cooldown = 0
                    last_cooldown = pygame.time.get_ticks()
                    Bullet(player.position, pygame.mouse.get_pos(), 0.05, "fast")

            # if shot_mode == "spread":
            #     if V.cooldown['spread'] - shoot_cooldown <= 0:
            #         shoot_cooldown = 0
            #         last_cooldown = pygame.time.get_ticks()

            #         mouse_pos = pygame.mouse.get_pos()
            #         SpreadBullet(player.position, mouse_pos, 0.1)

            #         left_bullet = PVector(player.position
            #         SpreadBullet(player.position, , 0.1)

            #         right_bullet
            #         SpreadBullet(player.position, , 0.1)

            if shot_mode == "strong":
                if Bullet.strong - shoot_cooldown <= 0:
                    shoot_cooldown = 0
                    last_cooldown = pygame.time.get_ticks()
                    Bullet(player.position, pygame.mouse.get_pos(), 0.01, "strong")

            shoot_cooldown = pygame.time.get_ticks() - last_cooldown

            if len(enemies) <= 0:
                last_respawn = pygame.time.get_ticks()
                Enemy(player.position, False, False, False, False)
                # close, mover, chaser, fastie



            for b, enemy_list in pygame.sprite.groupcollide(bullets, enemies, True, True).items():
                for e in enemy_list:
                    if e.rect.contains(b.rect):
                        shot_down += 1

            for e in enemies:
                e.move(player.position)

            dirty = all.draw(screen)
            pygame.display.update(dirty)

            clock.tick(60)
            prev_mouse_position = pygame.mouse.get_pos()



    pygame.display.flip()

    if pygame.mixer:
        pygame.mixer.music.fadeout(2000)
        
    pygame.quit()

if __name__ == '__main__':
    main()