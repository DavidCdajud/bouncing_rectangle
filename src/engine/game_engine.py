import pygame
import esper

from src.create.prefab_creator import crear_cuadrado
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_Velocity import CVelocity
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce

class GameEngine:
    def __init__(self) -> None:
        self.is_running = False
        pygame.init()
        self.screen = pygame.display.set_mode((640, 360), pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.frame_rate = 60
        self.delta_time = 0

        self.ecs_world = esper.World()


    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        crear_cuadrado (self.ecs_world, 
                       pygame.Vector2(50, 50), 
                       pygame.Vector2(100, 100),
                         pygame.Vector2(200, 200), 
                         pygame.Color(255, 0, 0))

    def _calculate_time(self):
        self.clock.tick(self.frame_rate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)


    def _draw(self):
        self.screen.fill((64,64,64))


        system_rendering(self.ecs_world, self.screen)


        pygame.display.flip()

    def _clean(self):
        pygame.quit()
        self.is_running = False
