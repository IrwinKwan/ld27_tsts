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
from constant import *
from characters import *

class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.color = Color('white')
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, 450)

    def update(self):
        if GameState.score != self.lastscore:
            self.lastscore = GameState.score
            msg = "Score: %d" % GameState.score
            self.image = self.font.render(msg, 0, self.color)


class Dialog(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.color = Color('black')
        self.text = ''

        self.update()
        self.rect = self.image.get_rect().move(40, 340)

    def set_text(self, text):
        self.text = text

    def update(self):
        msg = self.text
        self.image = self.font.render(msg, 0, self.color)

class DialogBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([400, 240])
        self.image.fill(Color('white'))
        self.update()
        self.rect = self.image.get_rect().move(40, 340)


def load_images():
    r = None
    Enemy.image_data = {}
    Enemy.image_data['butterfly'] = [0,0]
    Enemy.image_data['butterfly'][0], r = Asset.load_one_alpha_image("butterfly01.png", -1)
    Enemy.image_data['butterfly'][1], r = Asset.load_one_alpha_image("butterfly02.png", -1)

    Enemy.image_data['blob'] = [0,0]
    Enemy.image_data['blob'][0], r = Asset.load_one_alpha_image("blob01.png", -1)
    Enemy.image_data['blob'][1], r = Asset.load_one_alpha_image("blob02.png", -1)

    (Bullet.fastimage, Bullet.fastrect) = Asset.load_one_alpha_image("fastbullet.png", Color("white"))
    (Bullet.strongimage, Bullet.strongrect) = Asset.load_one_alpha_image("strongbullet.png", Color("white"))

    Player.images = Asset.load_image("player.png", [(0,0,32,32),(32,0,32,32)], -1)
    Player.images.append(pygame.transform.flip(Player.images[0], 1, 0))
    Player.images.append(pygame.transform.flip(Player.images[1], 1, 0))


def load_kill_sounds():
    soundfiles = ['3c', '3d', '3eb', '3f', '3g', '3ab', '3bb', '4c']
    p = []
    for s in soundfiles:
        p.append(Asset.load_sound("kill-" + s + ".ogg"))
    return p


def load_strong_sounds():
    soundfiles = ['3c', '3f', '3g', '4c']
    p = []
    for s in soundfiles:
        p.append(Asset.load_sound("shoot-" + s + ".ogg"))
    return p


def load_fast_sounds():
    p = []
    for s in range(1,2):
        p.append(Asset.load_sound("fast-" + str(s) + ".ogg"))
    return p


def title_screen(background):
    titleMsg, titleRect = Asset.load_one_alpha_image("title.png", Color("white"))
    titleRect = titleMsg.get_rect(midtop=(Constant.SCREEN_RECT.width/2, 0))
    background.blit(titleMsg, titleRect)
    return background

def story_page(background, screen, storyfile, dialog_list):
    m, r = Asset.load_one_alpha_image(storyfile, -1)
    r = m.get_rect(midtop=(Constant.SCREEN_RECT.width/2, 0))
    background.blit(m, r)

    fontfile = None
    font = None
    if pygame.font:
        fontfile = Asset.resource_path(os.path.join("assets", "freesansbold.ttf"))
        font = pygame.font.Font(fontfile, 16)

    for talking in dialog_list:
        if pygame.font:
            if type(talking) == str:
                dialog = pygame.draw.rect(background, Color("white"), (40, 400, 560, 60), 0)
                text = font.render(talking, 1, Color('black'))
                textpos = text.get_rect(topleft=(45, 405))
                background.blit(text, textpos)
            elif type(talking) == list:
                dialog = pygame.draw.rect(background, Color("white"), (40, 400, 560, 60), 0)
                text = font.render(talking[0], 1, Color('black'))
                textpos = text.get_rect(topleft=(45, 405))
                background.blit(text, textpos)

                # dialog = pygame.draw.rect(background, Color("white"), (40, 400, 560, 60), 0)
                text = font.render(talking[1], 1, Color('black'))
                textpos = text.get_rect(topleft=(45, 423))
                background.blit(text, textpos)

        screen.blit(background, (0,0))
        pygame.display.flip()

        waiting = True
        while waiting:
            event = pygame.event.wait()
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN or (event.type == KEYDOWN and event.key == K_SPACE):
                waiting = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                return

def story_page_advance(background, screen, storyfile, dialog_list):
    m, r = Asset.load_one_alpha_image(storyfile, -1)
    r = m.get_rect(midtop=(Constant.SCREEN_RECT.width/2, 0))
    background.blit(m, r)

    fontfile = None
    font = None
    if pygame.font:
        fontfile = Asset.resource_path(os.path.join("assets", "freesansbold.ttf"))
        font = pygame.font.Font(fontfile, 16)

    for talking in dialog_list:
        if pygame.font:
            dialog = pygame.draw.rect(background, Color("white"), (320 - 120, 456, 240, 25), 0)
            text = font.render(talking, 1, Color('black'))
            textpos = text.get_rect(center=(320, 465))
            background.blit(text, textpos)

        screen.blit(background, (0,0))
        pygame.display.flip()

        pygame.time.delay(1000)

        event = pygame.event.poll()
        if event.type == QUIT:
            pygame.quit()
            return
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            break

    # pygame.mixer.music.fadeout(1000)
    pygame.event.clear()

def game_background(background):
    m, r = Asset.load_one_alpha_image("background.jpg", Color("white"))
    r = m.get_rect(midtop=(Constant.SCREEN_RECT.width/2, 0))
    background.blit(m, r)
    return background

def score_screen(background):
    pass


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
    pygame.display.set_caption("Ten Seconds to Space")

    fontfile = None
    font = None
    if pygame.font:
        fontfile = Asset.resource_path(os.path.join("assets", "freesansbold.ttf"))
        font = pygame.font.Font(fontfile, 26)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    load_images()

    kill_sounds = load_kill_sounds()
    strong_sounds = load_strong_sounds()
    fast_sounds = load_fast_sounds()

    pygame.mixer.init(44100, -16, 2, 1024)

    sound = {}
    sound['fast'] = Asset.load_sound("hihat loop.wav")
    sound['strong'] = Asset.load_sound("OpenHH 909.wav")

    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    all = pygame.sprite.LayeredUpdates()
    Point.containers = all
    Player.containers = all
    Crosshairs.containers = all
    Bullet.containers = bullets, all
    Enemy.containers = enemies, all
    Score.containers = all

    player = Player()
    crosshairs = Crosshairs()

    cooldown = {}
    last_shot = {}
    cooldown['fast'] = 0
    last_shot['fast'] = 0
    cooldown['strong'] = 0
    last_shot['strong'] = 0
    cooldown['respawn'] = 0
    last_shot['respawn'] = 0

    shot_down = 0
    last_respawn = 0

    shot_mode = "fast"

    if pygame.font:
        all.add(Score())

    title_screen(background)
    screen.blit(background, (0,0))
    pygame.display.flip()

    # dialog = Dialog()
    # dialog_group = pygame.sprite.Group()
    # Dialog.containers = all
    # if pygame.font:
    #     dialog_group.add(dialog, DialogBox())

    on_title = True
    while on_title:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            return
        elif event.type == MOUSEBUTTONDOWN or (event.type == KEYDOWN and event.key == K_SPACE):
            on_title = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            return

    # pygame.mixer.music.fadeout(1000)
    pygame.event.clear()
    keystate = pygame.key.get_pressed()
    pygame.event.wait()


    # ========== story mode
    story = False
    if (story):
        story_page(background, screen, "_celine.jpg", [
            ["Lieutenant Celine Bodreaux: Commander! We've got a reading from", "our outer satelite permimeter."]])

        story_page(background, screen, "commander_celine.jpg", [
            "Commander Jeffrey Rotan: Put it on the display.",
            "Lieutenant Celine Bodreaux: It looks like the Insects are back, sir!",
            ["Commander Jeffrey Rotan: They won't get us this time. This",
              "time, we're prepared."]])

        story_page(background, screen, "commander_.jpg",
            ["Captain Yui!"])

        story_page(background, screen, "commander_yui.jpg", [
            "Captain Yui: Yes, sir!",
            ["Commander Jeffrey Rotan: You have TEN SECONDS to get to the ship!", "It's time for you to save the world."],
            "Captain Yui: I'm on it, sir!"])

        story_page(background, screen, "_yui.jpg",
            ["Prepare the launch!"])

        story_page_advance(background, screen, "rocket.jpg", ["T minus", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"])

        story_page_advance(background, screen, "launch.jpg", ["LIFT OFF!",
            "Defend our world, Captain!"])

    # ============ game mode

    game_background(background)
    screen.blit(background, (0,0))
    pygame.display.flip()

    Asset.play_music("LD27_120.wav")

    playing = True
    while playing:

        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        prev_mouse_position = pygame.mouse.get_pos()
        going = True

        while player.alive() and going == True:
            ticks_at_start = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
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

            if keystate[K_SPACE]:
                if shot_mode == "fast":
                    if Bullet.strong - cooldown['fast'] <= 0:
                        cooldown['fast'] = 0
                        last_shot['fast'] = ticks_at_start
                        Bullet(player.position, pygame.mouse.get_pos(), 0.05, "fast")
                        random.choice(fast_sounds).play()

                if shot_mode == "strong":
                    if Bullet.strong - cooldown['strong'] <= 0:
                        cooldown['strong'] = 0
                        last_shot['strong'] = ticks_at_start
                        Bullet(player.position, pygame.mouse.get_pos(), 0.05, "strong")
                        random.choice(strong_sounds).play()

                # close, mover, chaser, fastie

            if len(enemies) <= 0 or Enemy.respawn - cooldown['respawn'] <= 0 and len(enemies) < Enemy.limit:
                if GameState.score < 10:
                    Enemy(player.position, "blob", False, False, False, False)
                elif GameState.score < 30:
                    Enemy(player.position, "butterfly", False, True, False, False)
                    Enemy(player.position, "octopus", True, True, False, False)
                else:
                    Enemy(player.position, "bird", False, True, bool(random.getrandbits(1)), bool(random.getrandbits(1)))
                    Enemy(player.position, "octopus", True, True, bool(random.getrandbits(1)), bool(random.getrandbits(1)))

                last_shot['respawn'] = ticks_at_start

            cooldown['strong'] = ticks_at_start - last_shot['strong']
            cooldown['fast'] = ticks_at_start - last_shot['fast']
            cooldown['respawn'] = ticks_at_start - last_shot['respawn']

            for b, enemy_list in pygame.sprite.groupcollide(bullets, enemies, True, True).items():
                for e in enemy_list:
                    GameState.score += e.value
                    random.choice(kill_sounds).play()

            for e in enemies:
                e.move(player.position)

            dirty = all.draw(screen)
            pygame.display.update(dirty)

            clock.tick(60)
            prev_mouse_position = pygame.mouse.get_pos()

        print "Replay?"

    pygame.display.flip()

    if pygame.mixer:
        pygame.mixer.music.fadeout(2000)
        
    pygame.quit()

if __name__ == '__main__':
    main()