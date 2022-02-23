import pygame
import time
from models import Spaceship,Asteroid
from pygame.constants import K_DOLLAR, K_DOWN, K_ESCAPE
from utils import load_sprite,print_upper_left_text,get_random_position,print_text,print_lower_left_text,print_upper_middle_text


class SpaceRocks:

    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space",False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None,64)
        self.pause = False
        self.invisible = 3
        self.invisible_yo = False
        self.x = 0
        self.message = ""
        self.message_upper = ""
        self.message_middle = ""
        self.message_lower = ""
        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400,300) , self.bullets.append)
        # self.rock = self.load_sound("Rock_destroy")

        for _ in  range(7):
            while True:
                position = get_random_position(self.screen)
                if (position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE):
                    break
            self.asteroids.append(Asteroid(position , self.asteroids.append))
        
    def _get_game_objects(self):
        game_objects = [*self.asteroids,*self.bullets]
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks By Neel Patel")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
                
            elif not self.pause and event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.pause = True
                self.message = '''Pause'''
                self.message_lower = "Press P to continue"

            elif self.pause and event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.pause = False
                self.message = ""
                self.message_lower = ""
            
            elif (self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.spaceship.shoot()


        is_key_pressed = pygame.key.get_pressed()
        
        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            elif is_key_pressed[pygame.K_DOWN]:
                self.spaceship.raccelerate()
            if is_key_pressed[pygame.K_i]:
                self.x = time.time()
                if self.invisible >0 and self.invisible_yo == False:
                    self.message_upper = "Invisible"
                    self.spaceship.NopToP(True)
                    self.invisible_yo = True
                    self.invisible = self.invisible - 1
                elif self.invisible <= 0 and self.invisible_yo == False:
                    self.invisible_yo = False

            if time.time() - self.x > 10:
                self.invisible_yo = False
                self.spaceship.NopToP(False)
                self.message_upper = ""
                self.message_lower = ""
            

    def _process_game_logic(self):
        if not self.pause:
            for game_object in self._get_game_objects():
                game_object.move(self.screen)
            if self.spaceship:
                self.message_lower = f"Invisible Left : {self.invisible}"
                for asteroid in self.asteroids:
                    if asteroid.collides_with(self.spaceship):
                        if self.invisible_yo:
                            continue
                        else:
                            self.spaceship = None
                            self.message = "You lost!"
                            break
            
            for bullet in self.bullets[:]:
                for asteroid in self.asteroids[:]:
                    if asteroid.collides_with(bullet):
                        self.asteroids.remove(asteroid)
                        self.bullets.remove(bullet)
                        asteroid.split()
                        break
            
            for bullet in self.bullets[:]:
                if not self.screen.get_rect().collidepoint(bullet.position):
                    self.bullets.remove(bullet)
            
            if not self.asteroids and self.spaceship:
                self.message = "You won!"
        
    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        
        if self.message:
            print_text(self.screen, self.message,self.font)

        if self.message_upper:
            print_upper_left_text(self.screen, self.message_upper , self.font)

        if self.message_lower:
            self.ffont = pygame.font.Font(None,30)
            print_lower_left_text(self.screen, self.message_lower , self.ffont)

        if self.message_middle:
            self.ffont = pygame.font.Font(None,27)
            print_upper_middle_text(self.screen,self.message_middle,self.ffont)

        pygame.display.flip()
        self.clock.tick(60)
