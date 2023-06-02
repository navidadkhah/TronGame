# -*- coding: utf-8 -*-

# python imports
import os
import json

# project imports
from ..ks.models import *


class MapHandler:

    def __init__(self, sides):
        self._sides = sides


    def _fill_board(self, world, board_info):
        width = len(board_info[0])
        height = len(board_info)

        world.board = [
            [
                ECell.AreaWall if board_info[y][x] == 'W' else ECell.Empty 
                for x in range(width)
            ]
            for y in range(height)
        ]


    def _fill_constants(self, world, constants_info):
        world.constants = Constants(
            max_cycles = constants_info['max_cycles'],
            init_health = constants_info['init_health'],
            wall_breaker_cooldown = constants_info['wall_breaker_cooldown'],
            wall_breaker_duration = constants_info['wall_breaker_duration'],
            wall_score_coefficient = constants_info['wall_score_coefficient'],
            area_wall_crash_score = constants_info['area_wall_crash_score'],
            my_wall_crash_score = constants_info['my_wall_crash_score'],
            enemy_wall_crash_score = constants_info['enemy_wall_crash_score'],
        )


    def _fill_agents(self, world, agents_info):
        world.agents = {}
        for side, agent_info in agents_info.items():
            agent = Agent(
                health = world.constants.init_health,
                position = Position(agent_info['position']['x'], agent_info['position']['y']),
                direction = EDirection[agent_info['direction']],
                wall_breaker_cooldown = 0,
                wall_breaker_rem_time = 0,
            )
            agent.crashed = False
            agent.move_before_crash = False
            world.agents[side] = agent


    def load_map(self, config):
        with open((config['map_path']), 'r') as map_file:
            map_info = json.loads(map_file.read())

        world = World()
        world.scores = {side: 0 for side in self._sides}

        self._fill_board(world, map_info['board'])
        self._fill_constants(world, map_info['constants'])
        self._fill_agents(world, map_info['agents'])

        return world
