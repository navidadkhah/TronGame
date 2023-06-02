# -*- coding: utf-8 -*-

# project imports
from ..ks.models import World
from ..gui_events import GuiEvent, GuiEventType
from ..ks.commands import ChangeDirection, ActivateWallBreaker


def apply_commands(self, commands):
    gui_events = []

    for side, last_commands in commands.items():
        for command in last_commands.values():
            if command.name() == ChangeDirection.name():
                gui_events += self.agents[side].change_direction(self, side, command.direction)
            elif command.name() == ActivateWallBreaker.name():
                gui_events += self.agents[side].activate_wall_breaker(self, side)

    return gui_events


def tick(self):
    gui_events = []

    for side, agent in self.agents.items():
        gui_events += agent.tick_wall_breaker(self, side)

    for side, agent in self.agents.items():
        gui_events += agent.construct_wall(self, side)

    for side, agent in self.agents.items():
        gui_events += agent.move(self, side)

    for side, agent in self.agents.items():
        gui_events += agent.handle_collision(self, side)

    return gui_events


def check_end_game(self, current_cycle):
    if current_cycle >= self.constants.max_cycles - 1:
        return True

    for side, agent in self.agents.items():
        if agent.check_crash_wall(self, side) or agent.check_crash_agent(self, side):
            return True

    return False


def get_winner(self):
    # Check if scores are equal
    if len(set(self.scores.values())) == 1:
        return None
    # Find side with maximum score
    return max(self.scores.keys(), key=(lambda key: self.scores[key]))


World.apply_commands = apply_commands
World.tick = tick
World.check_end_game = check_end_game
World.get_winner = get_winner
