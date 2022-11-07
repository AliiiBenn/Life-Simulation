import pygame as py

from game import Screen, Game

if __name__ == '__main__':
    screen = Screen(800, 600)
    game = Game(screen)
    py.init()
    game.run()