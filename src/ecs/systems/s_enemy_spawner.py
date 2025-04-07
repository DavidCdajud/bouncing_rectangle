import esper

from src.create.prefab_creator import create_enemy_cuadrado
from src.ecs.components.c_enemy_spawn import CEnemySpawn, SpawnEventData



def system_enemy_spawner(world:esper.World, enemies_data:dict, deltatime:float):
    components = world.get_component(CEnemySpawn)
    c_spw:CEnemySpawn
    for _,  c_spw in components:
        c_spw.actual_time += deltatime
        spw_evt:SpawnEventData
        for spw_evt in c_spw.spawn_event_data:
            if c_spw.actual_time >= spw_evt.time and not spw_evt.procesado:
                spw_evt.procesado = True
                print('Cuadro: ' + spw_evt.enemy_type + ' tiempo: ' + str(c_spw.actual_time) )
                create_enemy_cuadrado(world,
                              spw_evt.pos,
                              enemies_data[spw_evt.enemy_type])