#!/usr/bin/env python

import pygame
import objects
import library
import random
import math

#pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()
pygame.mixer.init()
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.toggle_fullscreen()

COLOR_BLACK = (0, 0, 0)
library.make_image_library()

clock = pygame.time.Clock()
arial_font = pygame.font.SysFont('Arial', int(0.06 * HEIGHT))

GOOSE_INTERVAL_BASE = 300
GOOSE_INTERVAL_SPREAD = 150
SPEEDUP_RATE = 0.0003

score = 0

def make_players():
    players = []
    players.append(objects.Player(0.2 *  WIDTH, HEIGHT, pygame.K_q, 'viljami1'))
    players.append(objects.Player(0.1 *  WIDTH, HEIGHT, pygame.K_w, 'viljami2'))

    return players

STATE_MENU = 1
STATE_GAME = 2
STATE_OVER = 3
STATE_QUIT = 4
def main():
    pygame.mixer.music.set_volume(0.5)
    state = STATE_MENU
    while state != STATE_QUIT:
        if state == STATE_MENU:
            state = state_menu()
        elif state == STATE_GAME:
            state = state_game()
        elif state == STATE_OVER:
            state = state_over()

def state_menu():
    background = objects.Background()
    menu = objects.StaticImage(0.5, 0.5, WIDTH, HEIGHT, 'menu')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_QUIT

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            return STATE_GAME
        if keys[pygame.K_ESCAPE]:
            return STATE_QUIT

        background.draw(screen)
        menu.draw(screen)
        pygame.display.update()


def state_game():
    global score
    pygame.mixer.music.play(-1)

    counter = 1
    players = make_players()
    geese = []
    background = objects.Background()
    warning = objects.StaticImage(0.5, 0.25, WIDTH, HEIGHT, 'warning')
    goose_interval = GOOSE_INTERVAL_BASE
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_QUIT

        background.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return STATE_QUIT

        if counter >= goose_interval:
            geese.append(objects.Goose(WIDTH, HEIGHT))
            goose_interval = GOOSE_INTERVAL_BASE + random.randrange(-GOOSE_INTERVAL_SPREAD / 2, GOOSE_INTERVAL_SPREAD / 2)
            goose_interval *= math.exp(-SPEEDUP_RATE * score)
            counter = 0

        for player in players:
            player_jump = keys[player.jump_key]
            player.update(player_jump)

        for goose in geese:
            goose.update()

        for player in players:
            if player.rect.collidelist(list(map(lambda goose: goose.hitbox, geese))) != -1:
                pygame.mixer.music.stop()
                library.sound_library['goose'].play()
                return STATE_OVER

        background.draw(screen)
        for player in players:
            player.draw(screen)

        for goose in geese:
            goose.draw(screen)

        if counter >= 0.8 * goose_interval:
            warning.draw(screen)

        score_text = arial_font.render('SCORE: ' + str(score), False, (0, 0, 0))
        screen.blit(score_text, (0.1 * WIDTH, 0.1 * HEIGHT))
            
        pygame.display.update()
        clock.tick(60)
        counter += 1
        score += 1

def state_over():
    global score
    background = objects.Background()
    gameover = objects.StaticImage(0.5, 0.4, WIDTH, HEIGHT, 'gameover')
    score_text = arial_font.render('FINAL SCORE: ' + str(score), False, (0, 0, 0))
    score_rect = score_text.get_rect()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_QUIT

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return STATE_QUIT
        if keys[pygame.K_RETURN]:
            score = 0
            return STATE_MENU

        background.draw(screen)
        gameover.draw(screen)

        screen.blit(score_text, (0.5 * WIDTH - 0.5 * score_rect.w, 0.6 * HEIGHT))
        pygame.display.update()

if __name__ == '__main__':
    main()
