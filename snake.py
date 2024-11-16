#!/bin/env python3
import pygame
import random
from pygame.locals import *

class Snake:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self, pos):
        self.tail = []
        self.tail.append(Rect(pos, (25, 25)))
        self.last_dir = self.UP
        self.can_move = True

    def move(self):
        if self.last_dir == self.UP:
            new_pos = self.tail[0].copy()
            new_pos.y -= self.tail[0].height
            self.tail.insert(0, new_pos)
        elif self.last_dir == self.DOWN:
            new_pos = self.tail[0].copy()
            new_pos.y += self.tail[0].height
            self.tail.insert(0, new_pos)
        elif self.last_dir == self.LEFT:
            new_pos = self.tail[0].copy()
            new_pos.x -= self.tail[0].width
            self.tail.insert(0, new_pos)
        elif self.last_dir == self.RIGHT:
            new_pos = self.tail[0].copy()
            new_pos.x += self.tail[0].width
            self.tail.insert(0, new_pos)

        self.tail.pop()

        print(self.tail)
        for t in self.tail[1:]:
            if self.tail[0].colliderect(t):
                pygame.quit()

    def grow(self):
        self.tail.append(self.tail[0].copy())

class Food:
    def __init__(self, width, height):
        pos = (random.randrange(25, width-25, 25), random.randrange(25, height-25, 25))
        self.rect = Rect(pos, (25, 25))

class Game:
    FOOD_SPAWN = 2000
    MOVE_SPEED = 250

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")

        self.screen = pygame.display.set_mode((650, 450))
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Snake((self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.food = []
        self.food.append(Food(self.screen.get_width(), self.screen.get_height()))

        self.spawn_event = pygame.USEREVENT + 1
        self.move_event = pygame.USEREVENT + 2

        pygame.time.set_timer(self.spawn_event, self.FOOD_SPAWN)
        pygame.time.set_timer(self.move_event, self.MOVE_SPEED)

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.spawn_event:
                    if len(self.food) <= 10:
                        self.food.append(Food(self.screen.get_width(), self.screen.get_height()))
                if event.type == self.move_event:
                    self.player.move()

            self.process_keyboard()
            self.screen.fill((50, 50, 50))

            for t in self.player.tail:
                pygame.draw.rect(self.screen, (0, 255, 0), t, 0)

            for f in self.food:
                if f.rect.colliderect(self.player.tail[0]):
                    self.food.remove(f)
                    self.player.grow()
                    continue
                pygame.draw.rect(self.screen, (255, 0, 0), f.rect, 0)

            pygame.draw.rect(self.screen, (0, 255, 0), self.player.tail[0], 0)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def process_keyboard(self):
        keys = pygame.key.get_pressed()

        if keys[K_w]:
            self.player.last_dir = self.player.UP
        if keys[K_s]:
            self.player.last_dir = self.player.DOWN
        if keys[K_a]:
            self.player.last_dir = self.player.LEFT
        if keys[K_d]:
            self.player.last_dir = self.player.RIGHT
        if keys[K_ESCAPE]:
            self.running = False

if __name__ == '__main__':
    game = Game()
    game.start()
