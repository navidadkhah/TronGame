# -*- coding: utf-8 -*-

# project imports
from ..ks.models import Agent, Position, ECell
from ..gui_events import GuiEvent, GuiEventType


def change_direction(self, world, side, direction):
    if self.direction in [direction, direction.opposite()]:
        return []

    self.direction = direction
    return [GuiEvent(GuiEventType.ChangeDirection, side=side, agent=self)]


def activate_wall_breaker(self, world, side):
    if self.wall_breaker_cooldown > 0:
        return []

    self.wall_breaker_cooldown = world.constants.wall_breaker_cooldown
    self.wall_breaker_rem_time = world.constants.wall_breaker_duration + 1
    return [GuiEvent(GuiEventType.ActivateWallBreaker, side=side, agent=self)]


def tick_wall_breaker(self, world, side):
    gui_events = []

    if self.wall_breaker_cooldown > 0:
        self.wall_breaker_cooldown -= 1

        if self.wall_breaker_cooldown == 0:
            gui_events.append(GuiEvent(GuiEventType.ReloadWallBreaker, side=side, agent=self))

    if self.wall_breaker_rem_time > 0:
        self.wall_breaker_rem_time -= 1

        if self.wall_breaker_rem_time == 0:
            gui_events.append(GuiEvent(GuiEventType.EndWallBreaker, side=side, agent=self))

    return gui_events


def construct_wall(self, world, side):
    my_cell_name = side + "Wall"
    my_cell_type = ECell[my_cell_name]
    world.board[self.position.y][self.position.x] = my_cell_type
    world.scores[side] += world.constants.wall_score_coefficient
    return [GuiEvent(GuiEventType.ConstructWall, side=side, agent=self)]


def move(self, world, side):
    self._prev_position = self.position
    self.position += Position.dir_to_pos(self.direction)
    return []


def check_crash_wall(self, world, side):
    return (world.board[self.position.y][self.position.x] == ECell.AreaWall or \
            world.board[self.position.y][self.position.x] != ECell.Empty and self.health == 0)


def check_crash_agent(self, world, side):
    agents = list(world.agents.values())

    if (agents[0]._prev_position == agents[1].position and
        agents[1]._prev_position == agents[0].position):
        return True

    return agents[0].position == agents[1].position


def handle_collision(self, world, side):
    enemy_side = [s for s in world.agents.keys() if s != side][0]

    # CrashEnemyAgent
    if self.check_crash_agent(world, side):
        self.crashed = True
        self.move_before_crash = world.agents[side].position == world.agents[enemy_side].position
        return [GuiEvent(GuiEventType.CrashEnemyAgent, side=side, agent=self)]

    # CrashAreaWall
    if world.board[self.position.y][self.position.x] == ECell.AreaWall:
        self.crashed = True
        self.move_before_crash = True
        world.scores[side] += world.constants.area_wall_crash_score
        return [GuiEvent(GuiEventType.CrashAreaWall, side=side, agent=self)]

    # WallBreaker
    my_cell_type = ECell.get_wall_type(side)
    enemy_cell_type = ECell.get_wall_type(enemy_side)

    if (self.wall_breaker_rem_time > 0 and \
        world.board[self.position.y][self.position.x] in [my_cell_type, enemy_cell_type]):
        return self._destruct_wall(world, side)

    # CrashMyWall
    if world.board[self.position.y][self.position.x] == my_cell_type:
        gui_events = self._decrease_health(world, side)
        if self.health == 0:
            self.crashed = True
            my_wall_refs = world.wall_refs[side][(self.position.x, self.position.y)]
            self.move_before_crash = self.direction.opposite() not in my_wall_refs.keys()
            world.scores[side] += world.constants.my_wall_crash_score
            gui_events += [GuiEvent(GuiEventType.CrashMyWall, side=side, agent=self)]
        else:
            gui_events += self._destruct_wall(world, side)

        return gui_events

    # CrashEnemyWall
    if world.board[self.position.y][self.position.x] == enemy_cell_type:
        gui_events = self._decrease_health(world, side)
        if self.health == 0:
            self.crashed = True
            enemy_wall_refs = world.wall_refs[enemy_side][(self.position.x, self.position.y)]
            self.move_before_crash = self.direction.opposite() not in enemy_wall_refs.keys()
            world.scores[side] += world.constants.enemy_wall_crash_score
            gui_events += [GuiEvent(GuiEventType.CrashEnemyWall, side=side, agent=self)]
        else:
            gui_events += self._destruct_wall(world, side)

        return gui_events

    return []


def _decrease_health(self, world, side):
    self.health -= 1
    return [GuiEvent(GuiEventType.DecreaseHealth, side=side, agent=self)]


def _destruct_wall(self, world, side):
    enemy_side = [s for s in world.agents.keys() if s != side][0]
    my_cell_type = ECell.get_wall_type(side)
    enemy_cell_type = ECell.get_wall_type(enemy_side)

    wall_side = side if world.board[self.position.y][self.position.x] == my_cell_type else enemy_side
    world.board[self.position.y][self.position.x] = ECell.Empty
    world.scores[wall_side] -= world.constants.wall_score_coefficient
    return [GuiEvent(GuiEventType.DestructWall, side=side, agent=self, wall_side=wall_side)]


Agent.change_direction = change_direction
Agent.activate_wall_breaker = activate_wall_breaker
Agent.tick_wall_breaker = tick_wall_breaker
Agent.construct_wall = construct_wall
Agent.move = move
Agent.check_crash_wall = check_crash_wall
Agent.check_crash_agent = check_crash_agent
Agent.handle_collision = handle_collision
Agent._decrease_health = _decrease_health
Agent._destruct_wall = _destruct_wall
