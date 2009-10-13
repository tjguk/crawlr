import pygame
from pygame.locals import *
from constants import *
from map import Map
from characters import Player, Monster
from monsters import *
from random import choice

class Scene(object):
    """A scene in the game that loads and manages a level."""

    def __init__(self, window, level):
        self.window = window
        self.camera = pygame.Rect((0,0), CAMERA_SIZE)
        self.map = Map(level)
        self.player = Player(self)
        self.monster = choice(MONSTER_LIST)(self)
        self.layers = pygame.sprite.LayeredDirty()

        # Add items to the scene.
        self.add()

        # Scroll the map to the player's starting location.
        self.scroll()

    def add(self):
        """Add sprites to the scene in the correct order."""

        # Characters to be drawn.
        characters = pygame.sprite.Group([self.player, self.monster])

        # All sprites to be drawn in order.
        self.all_sprites = pygame.sprite.OrderedUpdates([
            self.map.layers['terrain'],
            characters,
            self.map.layers['foreground']
            ])

        # Add all of the sprites to the scene.
        for sprite in self.all_sprites:
            self.layers.add(sprite)

    def draw(self):
        """Draws the sprites to the scene and updates the window."""

        self.layers.update()
        rects = self.layers.draw(self.window)
        pygame.display.update(rects)

    def scroll(self):
        """Scroll the map to keep the player visible."""

        b_x, b_y = self.player.rect.center
        self.camera.center = (b_x, b_y)
        b_x, b_y = self.camera.topleft
        camera_w, camera_h = (self.camera.width, self.camera.height)
        map_w, map_h = (self.map.get_size())
        if b_x < 0:
            b_x = 0
        if b_x > map_w - camera_w:
            b_x = map_w - camera_w
        if b_y < 0:
            b_y = 0
        if b_y > map_h - camera_h:
            b_y = map_h - camera_h
        if map_h < camera_h:
            b_y = (map_h - camera_h) / 2
        if map_w < camera_w:
            b_x - (map_w - camera_w) / 2
        self.camera.topleft = [ -b_x, -b_y ]
        self.map.move_map([ self.camera[0], self.camera[1] ])
        self.player.rect.move_ip([ self.camera[0], self.camera[1] ])
        self.player.scroll_pos = [ self.camera[0], self.camera[1] ]

    def destroy(self):
        """Destroy the current scene."""

        for sprite in self.all_sprites:
            sprite.kill()
