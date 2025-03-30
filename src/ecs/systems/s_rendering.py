import pygame
import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface


def system_rendering(world:esper.World, screen:pygame.Surface):
    componentes = world.get_components(CTransform, CSurface)

    c_s:CSurface
    c_t:CTransform
    for entity, (c_t, c_s) in componentes:
        screen.blit(c_s.surf, c_t.pos)
