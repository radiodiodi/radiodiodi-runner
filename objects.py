import pygame
import os
import library
import utils
import copy

class Player(pygame.sprite.Sprite):
    GRAVITY = 0.7
    JUMP_STR = 45 * GRAVITY

    def __init__(self, x, screen_height, jump_key, image_str):
        pygame.sprite.Sprite.__init__(self)

        self.vel_y = 0
        self.jump_key = jump_key
        self.ground = 0.85 * screen_height
        self.image = library.image_library[image_str]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = self.ground - self.rect.h

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, should_jump):
        if should_jump and self.rect.y >= self.ground - self.rect.h:
            self.vel_y -= Player.JUMP_STR
            library.sound_library['jump'].play()

        self.vel_y += min(Player.GRAVITY, self.ground - self.rect.y - self.rect.h)

        if self.rect.y + self.vel_y < self.ground - self.rect.h:
            self.rect.y += self.vel_y
        else:
            self.rect.y = self.ground - self.rect.h
            self.vel_y = 0

class Background(pygame.sprite.Sprite):
    VEL_X = 12

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(0, 0, 3840, 1080)
        self.image1 = library.image_library['bg']
        self.image2 = library.image_library['bg']

    def draw(self, screen):
        w = self.rect.w
        x = self.rect.x
        y = self.rect.y
        screen.blit(self.image1, (-((x + w) %  (2 * w) - w), y))
        screen.blit(self.image2, (-(x % (2 * w) - w), y))

    def update(self):
        self.rect.x += Background.VEL_X


class Goose(pygame.sprite.Sprite):
    VEL_X = -12

    def __init__(self, x, screen_height):
        pygame.sprite.Sprite.__init__(self)

        self.image = library.image_library['goose']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0.85 * screen_height - self.rect.h
        self.hitbox = copy.copy(self.rect)
        self.hitbox.w /= 2

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x += Goose.VEL_X
        self.hitbox.x = self.rect.x

class StaticImage(pygame.sprite.Sprite):
    def __init__(self, px, py, screen_width, screen_height, image_str):
        self.image = library.image_library[image_str]
        self.rect = self.image.get_rect()
        self.rect.x = screen_width * px - self.rect.w / 2
        self.rect.y = screen_height * py - self.rect.h / 2

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y)) 

