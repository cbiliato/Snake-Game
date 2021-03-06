# My version of a Snake Game
# Movement is controlled by the arrow keys
# Done on PyCharm with pygame to provide the visuals

# Completed on March 8, 2022 by Carter Biliato

import pygame
from pygame.locals import *
import time
import random

SIZE = 40  # size of the images 40x40 pixels


class Google:  # class for the icon that is consumed
    def __init__(self, screen):  # method for outputting the icon onto screen
        self.screen = screen
        self.image = pygame.image.load("images/Google.png").convert()  # use this image from folder
        self.x = random.randint(1, 24) * SIZE  # random google spawn location
        self.y = random.randint(1, 19) * SIZE

    def draw(self):  # method to see the image
        self.screen.blit(self.image, (self.x, self.y))  # refresh so the image doesn't have dragging tail
        pygame.display.update()  # updates the game display

    def move(self):  # method of randomizing apple
        self.x = random.randint(1, 24) * SIZE  # random location after initial spawn
        self.y = random.randint(1, 19) * SIZE


class Mark:  # class for the icon that is consuming
    def __init__(self, screen):  # method for outputting the icon onto screen
        self.screen = screen
        self.image = pygame.image.load("images/Mark.png").convert()
        self.direction = 'down'  # start initial direction down or will instantly lose

        self.length = 1  # start with initial length 1
        self.x = [40]  # size of icon
        self.y = [40]

    def move_left(self):  # method for movement in all directions
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def follow(self):  # method updates attributes of the body
        for i in range(self.length - 1, 0, -1):  # for loops to follow the previous block position
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE  # trailing distance
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):  # clear the Google icon when Mark head goes is in the same space
        for i in range(self.length):
            self.screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.update()

    def increase_length(self):  # increases length of Mark
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:  # class for the game
    def __init__(self):  # method for game
        pygame.init()  # initializes the game
        pygame.display.set_caption("Snake Game!")  # name

        self.surface = pygame.display.set_mode((1000, 800))  # size of window
        self.mark = Mark(self.surface)  # Mark appears
        self.mark.draw()
        self.google = Google(self.surface)  # Google appears
        self.google.draw()

    def reset(self):  # reset to original
        self.mark = Mark(self.surface)
        self.google = Google(self.surface)

    @staticmethod
    def eating(x1, y1, x2, y2):  # if a collision occurs with anything
        if x2 <= x1 < x2 + SIZE:  # coordinates of corners of icons, needs to consume full icon
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):  # method for background
        bg = pygame.image.load("images/Background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):  # method for gameplay
        self.render_background()
        self.mark.follow()
        self.google.draw()
        self.display_score()
        pygame.display.flip()

        for i in range(self.mark.length):  # Mark consuming Google
            if self.eating(self.mark.x[i], self.mark.y[i], self.google.x, self.google.y):
                self.mark.increase_length()
                self.google.move()

        for i in range(1, self.mark.length):  # Mark colliding with himself
            if self.eating(self.mark.x[0], self.mark.y[0], self.mark.x[i], self.mark.y[i]):
                raise "Collision"

        if not (0 <= self.mark.x[0] < 1000 and 0 <= self.mark.y[0] < 800):  # colliding with boundaries of the window
            raise "Boundary"

    def display_score(self):  # method for displaying score
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.mark.length}", True, (0, 0, 0))
        self.surface.blit(score, (850, 10))  # position of text

    def show_game_over(self):  # method for endgame
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over! Your score is {self.mark.length}!", True, (0, 0, 0))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Press Enter to play again! Press Exit to escape!", True, (0, 0, 0))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def run(self):  # movement from keyboard
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.mark.move_left()

                        if event.key == K_RIGHT:
                            self.mark.move_right()

                        if event.key == K_UP:
                            self.mark.move_up()

                        if event.key == K_DOWN:
                            self.mark.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.1)


if __name__ == '__main__':  # game operation
    game = Game()
    game.run()
