import pygame
import os

image_library = {}
sound_library = {}
def make_image_library():
    global image_library
    global sound_library
    image_library = {'player':  pygame.image.load(os.path.join('res', 'player.png')),
                     'bg':      pygame.image.load(os.path.join('res', 'bg.png')).convert(),
                     'goose':   pygame.image.load(os.path.join('res', 'goose.png')),
                     'warning':   pygame.image.load(os.path.join('res', 'warning.png')),
                     'viljami1':   pygame.image.load(os.path.join('res', 'viljami.png')),
                     'viljami2':   pygame.image.load(os.path.join('res', 'viljami2.png')),
                     'gameover':   pygame.image.load(os.path.join('res', 'gameover.png')),
                     'menu':   pygame.image.load(os.path.join('res', 'menu.png'))}

    sound_library = {'bg':  pygame.mixer.music.load(os.path.join('res', 'faijonii.mp3')),
                     'jump': pygame.mixer.Sound(os.path.join('res', 'jump.wav')),
                     'goose': pygame.mixer.Sound(os.path.join('res', 'goose.wav'))}
