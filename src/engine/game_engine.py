""""Modulo del motor de juego"""

import json
import pygame
import esper

from src.create.prefab_creator import create_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner

class GameEngine:

    # Inicializar el motor de juego
    def __init__(self) -> None: 

        self._load_json()
        pygame.init()

        pygame.display.set_caption(self.window_data["title"])
        self.screen = pygame.display.set_mode( (self.window_data["size"]["w"], 
                                               self.window_data["size"]["h"]),
                                               pygame.SCALED)
        
        self.clock = pygame.time.Clock()
        self.bg_color = pygame.Color(self.window_data["bg_color"]["r"],
                                     self.window_data["bg_color"]["g"],
                                     self.window_data["bg_color"]["b"])
        self.is_running = False
        self.framerate = self.window_data["framerate"]
        self.deltatime = 0
        
        self.ecs_world = esper.World()


    # Iniciar el motor de juego
    def run(self) -> None: 

        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    # Crear el motor de juego
    def _create(self): 
        create_enemy_spawner(self.ecs_world, self.level_data)
        
    # Calcular el tiempo
    def _calculate_time(self): 
        self.clock.tick(self.framerate)
        self.deltatime = self.clock.get_time() / 1000.0

    # Procesar eventos
    def _process_events(self): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
    
     # Actualizar el motor de juego
    def _update(self):
        system_enemy_spawner(self.ecs_world, self.enemies_data, self.deltatime)
        system_movement(self.ecs_world,self.deltatime)
        system_screen_bounce(self.ecs_world,self.screen)


    # Renderizar la pantalla
    def _draw(self): 
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

     # Limpiar el motor de juego
    def _clean(self):
        pygame.quit()

     # Cargar archivos JSON
    def _load_json(self):
        with open("./assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_data = json.load(window_file)
        with open("./assets/cfg/enemies.json") as enemies_file:
            self.enemies_data = json.load(enemies_file)
        with open("./assets/cfg/level_01.json") as level_01_file:
            self.level_data = json.load(level_01_file)
