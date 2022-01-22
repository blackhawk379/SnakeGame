# Add background image and music

import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)
X_END, Y_END = 960, 680


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.png").convert()
        self.x = 0
        self.y = 40

    def draw(self):
        image = pygame.transform.scale(self.image, (SIZE, SIZE))
        self.parent_screen.blit(image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(2, 22) * SIZE
        self.y = random.randint(2, 15) * SIZE


class Rock:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/rock.jpg").convert()
        self.x = [X_END - 40, X_END - 40, 800]
        self.y = [Y_END - 40, 0, 600]

    def draw(self):
        image = pygame.transform.scale(self.image, (SIZE, SIZE))
        for i in range(len(self.x)):
            self.parent_screen.blit(image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move(self):
        self.x.pop(0)
        self.y.pop(0)
        self.x.append(random.randint(2, 22) * SIZE)
        self.y.append(random.randint(2, 15) * SIZE)


class Snake:
    def __init__(self, parent_screen, isWall):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/head.png").convert()
        self.direction = 'down'
        self.degree = 0
        self.degree_end = 0
        self.turn = []
        self.count = 0
        self.isWall = isWall

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        if self.direction in ['down', 'up']:
            while self.y[0] % 40 != 0:
                self.walk()
                time.sleep(0.001)
            self.degree = 270
            self.direction = 'left'
            if self.length > 1:
                self.turn.append([self.x[0], self.y[0], 270])

    def move_right(self):
        if self.direction in ['down', 'up']:
            while self.y[0] % 40 != 0:
                self.walk()
                time.sleep(0.001)
            self.degree = 90
            self.direction = 'right'
            if self.length > 1:
                self.turn.append([self.x[0], self.y[0], 90])

    def move_up(self):
        if self.direction in ['left', 'right']:
            while self.x[0] % 40 != 0:
                self.walk()
                time.sleep(0.001)
            self.degree = 180
            self.direction = 'up'
            if self.length > 1:
                self.turn.append([self.x[0], self.y[0], 180])

    def move_down(self):
        if self.direction in ['left', 'right']:
            while self.x[0] % 40 != 0:
                self.walk()
                time.sleep(0.001)
            self.degree = 0
            self.direction = 'down'
            if self.length > 1:
                self.turn.append([self.x[0], self.y[0], 0])

    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        update = SIZE - 30
        if self.direction == 'left':
            if self.x[0] == 0:
                if self.isWall:
                    self.crash()
                else:
                    self.x[0] = X_END - 40
            else:
                self.x[0] -= update
        if self.direction == 'right':
            if self.x[0] == X_END - 40:
                if self.isWall:
                    self.crash()
                else:
                    self.x[0] = 0
            else:
                self.x[0] += update
        if self.direction == 'up':
            if self.y[0] == 0:
                if self.isWall:
                    self.crash()
                else:
                    self.y[0] = Y_END - 40
            else:
                self.y[0] -= update
        if self.direction == 'down':
            if self.y[0] == Y_END - 40:
                if self.isWall:
                    self.crash()
                else:
                    self.y[0] = 0
            else:
                self.y[0] += update
        self.draw()

    def draw(self):
        head = pygame.image.load("resources/head.png").convert()
        tail = pygame.image.load("resources/tail.jpg").convert()
        head = pygame.transform.scale(head, (SIZE, SIZE))
        head = pygame.transform.rotate(head, self.degree)
        if self.length > 1:
            for i in range(1, self.length - 1):
                image = pygame.transform.scale(self.image, (SIZE, SIZE))
                self.parent_screen.blit(image, (self.x[i], self.y[i]))

            if self.count < len(self.turn):
                if [self.x[-1], self.y[-1]] == self.turn[self.count][:2]:
                    self.degree_end = self.turn[self.count][-1]
                    self.count += 1
            tail = pygame.transform.scale(tail, (SIZE, SIZE))
            tail = pygame.transform.rotate(tail, self.degree_end)
            self.parent_screen.blit(tail, (self.x[-1], self.y[-1]))
        self.parent_screen.blit(head, (self.x[0], self.y[0]))

        pygame.display.flip()

    def crash(self):
        sound = pygame.mixer.Sound("resources/crash.wav")
        pygame.mixer.Sound.play(sound)
        img = pygame.image.load("resources/crash.jpg").convert()
        img = pygame.transform.scale(img, (SIZE, SIZE))
        self.parent_screen.blit(img, (self.x[0], self.y[0]))
        pygame.display.flip()

        raise "Collision Occurred"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self, mode, isWall):
        pygame.init()
        pygame.display.set_caption("Snakes, Apple, Rock and Wall")

        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((X_END, Y_END))
        self.snake = Snake(self.surface, isWall)
        self.apple = Apple(self.surface)
        self.rock = Rock(self.surface)
        self.surface.blit(pygame.image.load("resources/block1.png").convert(), (40, 40))
        self.apple.draw()
        self.rock.draw()
        self.high_score = 0
        self.mode = mode
        self.isWall = isWall

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()

    def reset(self):
        self.mode = set_mode()
        self.isWall = is_wall()
        self.high_score = max(self.high_score, self.snake.length-1)
        self.snake = Snake(self.surface, self.isWall)
        self.apple = Apple(self.surface)

    def render_background(self):
        if self.isWall:
            bg = pygame.image.load("resources/background.png")
        else:
            bg = pygame.image.load("resources/background.jpg")
        bg = pygame.transform.scale(bg, (X_END, Y_END))
        self.surface.blit(bg, (0, 0))
        self.show_mode()
        self.show_high_score()
        self.show_score()

    def show_mode(self):
        font = pygame.font.SysFont('arial', 30)
        if self.mode == 1:
            x = "Beginner"
        elif self.mode == 2:
            x = "Intermediate"
        else:
            x = "Expert"
        self.surface.blit(font.render(f"{x} Mode", True, (200, 200, 200)), (400, 10))

    def show_high_score(self):
        font = pygame.font.SysFont('arial', 30)
        high = font.render(f"High Score: {max(self.high_score, self.snake.length-1)}", True, (200, 200, 200))
        self.surface.blit(high, (790, 10))

    def show_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length-1}", True, (200, 200, 200))
        self.surface.blit(score, (850, 60))

    def play(self):
        self.render_background()  # Definition Above
        self.snake.walk()
        self.apple.draw()

        # if random position of apple and any rock are the same
        i = 0
        while i < 3:
            if [self.apple.x, self.apple.y] == [self.rock.x[i], self.rock.y[i]]:
                self.rock.x.pop(i)
                self.rock.y.pop(i)
                self.rock.x.append(random.randint(1, 23) * SIZE)
                self.rock.y.append(random.randint(1, 16) * SIZE)
                i -= 1
            i += 1
        self.rock.draw()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            for _ in range(self.mode * 2):
                self.snake.increase_length()
            self.apple.move()
            self.rock.move()

        # snake colliding with rock
        for i in range(len(self.rock.x)):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.rock.x[i], self.rock.y[i]):
                self.crash((self.rock.x[i], self.rock.y[i]))

        # snake colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.crash((self.snake.x[i], self.snake.y[i]))

    def is_collision(self, x1, y1, x2, y2):
        if [x2, y2] == [x1, y1]:
            return True
        if self.snake.direction == 'up':
            return x1 == x2 and y1 - SIZE < y2 < y1
        if self.snake.direction == 'down':
            return x1 == x2 and y1 < y2 < y1 + SIZE
        if self.snake.direction == 'right':
            return y1 == y2 and x1 < x2 < x1 + SIZE
        if self.snake.direction == 'left':
            return y1 == y2 and x1 - SIZE < x2 < x1

    def crash(self, position):
        self.play_sound('crash')
        img = pygame.image.load("resources/crash.jpg").convert()
        img = pygame.transform.scale(img, (SIZE, SIZE))
        self.surface.blit(img, position)
        pygame.display.flip()

        raise "Collision Occurred"

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.wav")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/eat.wav")
        pygame.mixer.Sound.play(sound)

    def show_game_over(self):
        pygame.mixer.music.pause()
        time.sleep(1)
        self.render_background()
        font = pygame.font.SysFont('comicsansms', 50)
        line1 = font.render(f"GAME OVER!", True, (255, 255, 255))
        line2 = font.render(f"Your Score: {self.snake.length}", True, (255, 255, 255))
        line3 = font.render(f"High Score: {max(self.high_score, self.snake.length)}", True, (255, 255, 255))
        self.surface.blit(line1, (325, 100))
        self.surface.blit(line2, (325, 200))
        self.surface.blit(line3, (325, 300))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT or event.key == K_a:
                            self.snake.move_left()

                        if event.key == K_RIGHT or event.key == K_d:
                            self.snake.move_right()

                        if event.key == K_UP or event.key == K_w:
                            self.snake.move_up()

                        if event.key == K_DOWN or event.key == K_s:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            if self.mode == 1:
                time.sleep(0.005)
            elif self.mode == 2:
                time.sleep(0.001)
            elif self.mode == 3:
                time.sleep(0.0001)


def set_mode():
    pygame.init()
    pygame.font.init()
    bg = pygame.image.load("resources/background_intro.jpg")
    surface = pygame.display.set_mode((X_END, Y_END))
    surface.blit(bg, (0, 0))
    font = pygame.font.SysFont('comicsansms', 20)
    line = font.render("CHOOSE MODE", True, (255, 255, 255))
    line1 = font.render("Press 'b' to enter game in beginner mode", True, (255, 255, 255))
    line2 = font.render("Press 'm' to enter game in intermediate mode", True, (255, 255, 255))
    line3 = font.render("Press 'h' to enter game in expert mode", True, (255, 255, 255))
    surface.blit(line, (325, 100))
    surface.blit(line1, (325, 200))
    surface.blit(line2, (325, 300))
    surface.blit(line3, (325, 400))
    pygame.display.flip()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

                if event.key == K_b:
                    return 1

                if event.key == K_m:
                    return 2

                if event.key == K_h:
                    return 3

                else:
                    continue

            elif event.type == QUIT:
                running = False


def is_wall():
    pygame.init()
    pygame.font.init()
    bg = pygame.image.load("resources/background_intro.jpg")
    surface = pygame.display.set_mode((X_END, Y_END))
    surface.blit(bg, (0, 0))
    font = pygame.font.SysFont('comicsansms', 20)
    line = font.render("CHOOSE WALL OR NO WALL", True, (255, 255, 255))
    line1 = font.render("Press 'w' for walls", True, (255, 255, 255))
    line2 = font.render("Press 'n' no walls", True, (255, 255, 255))
    emergency = font.render("Press enter if not working", True, (255, 255, 255))
    surface.blit(line, (325, 100))
    surface.blit(line1, (325, 200))
    surface.blit(line2, (325, 300))
    surface.blit(emergency, (325, 590))
    pygame.display.flip()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

                if event.key == K_w:
                    return True

                if event.key == K_n:
                    return False

                else:
                    continue

            elif event.type == QUIT:
                running = False


if __name__ == '__main__':
    mode = set_mode()
    wall = is_wall()
    game = Game(mode, wall)
    game.run()
