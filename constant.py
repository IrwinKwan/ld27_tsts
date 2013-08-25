#!/usr/bin/env python

import pygame
from pygame.locals import *

class Constant:
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    SCREEN_RECT = Rect(0, 0, 640, 480)

class V:
    cooldown = {}
    cooldown['fast'] = 10
    cooldown['spread'] = 1000
    cooldown['strong'] = 500

class GameState:
	enemies_spawned = 0
	score = 0