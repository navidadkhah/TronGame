# -*- coding: utf-8 -*-

# project imports
from ..ks.models import World
from ..ks.commands import ChangeDirection


class LogicHandler:

    def __init__ (self, world, sides):
        self._sides = sides
        self.world = world


    def initialize(self):
        self.clear_commands()


    def store_command(self, side_name, command):
        ### This method should be removed after adding 'import' feature to the koala-serializer ###
        def convert_command(command):
            from ..ks.models import EDirection
            command.direction = EDirection(command.direction.value)

        if command.name() == ChangeDirection.name():
            convert_command(command)
        self._last_cycle_commands[side_name][command.name()] = command


    def clear_commands(self):
        self._last_cycle_commands = {side: {} for side in self._sides}


    def process(self, current_cycle):
        gui_events = []
        gui_events.extend(self.world.apply_commands(self._last_cycle_commands))
        gui_events.extend(self.world.tick())
        return gui_events


    def get_client_world(self, side_name):
        return self.world


    def check_end_game(self, current_cycle):
        end_game = self.world.check_end_game(current_cycle)

        if end_game:
            winner = self.world.get_winner()
            details = {
                'Scores': {
                    side: str(score) for side, score in self.world.scores.items()
                }
            }
            return end_game, winner, details

        return end_game, None, None
