# -*- coding: utf-8 -*-

# chillin imports
from chillin_server.gui.tools import GuiTools

# project imports
from ....ks.models import Agent, EDirection, Position
from ....gui_events import GuiEventType
from ..utils import create_asset, change_transform, change_material, change_is_active, change_audio


def gui_init(self, world, side):
    self._gui_ref = create_asset(world, '{}Bike'.format(side))
    change_transform(
        world,
        self._gui_ref,
        position = self.position.get_gui_position(),
        y_rotation = self.direction.get_gui_rotation(),
    )
    world.wall_refs[side][(self.position.x, self.position.y)] = {}


def gui_change_direction(self, world, gui_event):
    # GuiEvent(GuiEventType.ChangeDirection, side=side, agent=self)
    change_transform(
        world,
        self._gui_ref,
        y_rotation = self.direction.get_gui_rotation(),
    )


def _gui_move_step(self, world, half=False):
    duration_cycles = 0.5 if half else 1
    position = Position(x=self.position.x, y=self.position.y)
    if half:
        offset_pos = Position.dir_to_pos(self.direction.opposite())
        position.x += offset_pos.x / 2
        position.y += offset_pos.y / 2

    change_transform(
        world,
        self._gui_ref,
        duration_cycles = duration_cycles,
        position = position.get_gui_position(),
    )


def gui_move(self, world):
    if self.crashed:
        return

    self._gui_move_step(world, half=False)


def gui_activate_wall_breaker(self, world, gui_event):
    # GuiEvent(GuiEventType.ActivateWallBreaker, side=side, agent=self)
    self._gui_shield_ref = create_asset(
        world,
        '{}Shield'.format(gui_event.side),
        parent_ref = self._gui_ref,
        parent_child_ref = 'Shield',
    )

    change_audio(world, self._gui_ref, child_ref='AudioSource', clip='Shield', play=True, loop=True, volume=0.5)


def gui_end_wall_breaker(self, world, gui_event):
    # GuiEvent(GuiEventType.EndWallBreaker, side=side, agent=self)
    change_is_active(world, self._gui_shield_ref, False)
    change_audio(world, self._gui_ref, child_ref='AudioSource', play=False)


def gui_reload_wall_breaker(self, world, gui_event):
    # GuiEvent(GuiEventType.ReloadWallBreaker, side=side, agent=self)
    # TODO: Add sound
    pass


def gui_construct_wall(self, world, gui_event):
    # [GuiEvent(GuiEventType.ConstructWall, side=side, agent=self)]

    # Change ground
    ref = world.ground_refs[(self._prev_position.x, self._prev_position.y)]
    change_material(world, ref, '{}Ground'.format(gui_event.side))

    if self.crashed and not self.move_before_crash:
        return

    # Create Walls
    ref = create_asset(world, asset_name='{}CenterWall'.format(gui_event.side))
    world.wall_refs[gui_event.side][(self._prev_position.x, self._prev_position.y)]['center'] = ref
    change_transform(world, ref, position=self._prev_position.get_gui_position())

    ref = create_asset(world, asset_name='{}Wall'.format(gui_event.side))
    world.wall_refs[gui_event.side][(self._prev_position.x, self._prev_position.y)][self.direction] = ref
    change_transform(
        world,
        ref,
        position = self._prev_position.get_gui_position(),
        y_rotation = self.direction.get_gui_rotation(),
    )
    change_transform(world, ref, cycle=0, duration_cycles=0.5, z_scale=world.GUI_CELL_SIZE / 2)

    if self.crashed:
        return

    ref = create_asset(world, asset_name='{}Wall'.format(gui_event.side), cycle=0.5)
    world.wall_refs[gui_event.side][(self.position.x, self.position.y)] = {self.direction.opposite(): ref}
    offset_pos = Position.dir_to_pos(self.direction)
    change_transform(
        world,
        ref,
        cycle = 0.5,
        position = Position(x=self._prev_position.x + offset_pos.x/2, y=self._prev_position.y + offset_pos.y/2).get_gui_position(),
        y_rotation = self.direction.get_gui_rotation(),
    )
    change_transform(world, ref, cycle=0.5, duration_cycles=0.5, z_scale=world.GUI_CELL_SIZE / 2)


def gui_destruct_wall(self, world, gui_event):
    # GuiEvent(GuiEventType.DestructWall, side=side, agent=self, wall_side=wall_side)

    def destruct_wall(wall_ref, cycle):
        change_is_active(world, wall_ref, False, child_ref='Cube', cycle=cycle)
        explosion_ref = create_asset(
            world,
            '{}WallExplosion'.format(gui_event.wall_side),
            parent_ref = wall_ref,
            parent_child_ref = 'Explosion',
            cycle = cycle,
        )
        change_is_active(world, wall_ref, False, cycle=cycle+GuiTools.time_to_cycle(1))

        change_audio(world, wall_ref, child_ref='AudioSource', clip='WallDestruction', play=True, cycle=cycle)
        change_audio(world, wall_ref, child_ref='AudioSource', play=False, cycle=cycle+GuiTools.time_to_cycle(1))

    # Change ground
    ref = world.ground_refs[(self.position.x, self.position.y)]
    change_material(world, ref, 'EmptyGround')

    # Destruct walls
    for direction, wall_ref in world.wall_refs[gui_event.wall_side][(self.position.x, self.position.y)].items():
        if direction == 'center':
            change_is_active(world, wall_ref, False, cycle=0.5)
        elif direction == self.direction.opposite():
            destruct_wall(wall_ref, 0)
        else:
            destruct_wall(wall_ref, 0.5)

    world.wall_refs[gui_event.wall_side][(self.position.x, self.position.y)] = {}


def _gui_handle_crash(self, world, gui_event):
    if self.move_before_crash:
        self._gui_move_step(world, half=True)

    cycle = 0.5 if self.move_before_crash else 0

    change_is_active(world, self._gui_ref, False, child_ref='Bike', cycle=cycle)
    change_is_active(world, self._gui_ref, False, child_ref='Shield', cycle=cycle)
    explosion_ref = create_asset(
        world,
        '{}BikeExplosion'.format(gui_event.side),
        parent_ref = self._gui_ref,
        parent_child_ref = 'Explosion',
        cycle = cycle,
    )
    change_is_active(world, self._gui_ref, False, cycle=cycle+GuiTools.time_to_cycle(1))

    change_audio(world, self._gui_ref, child_ref='AudioSource', clip='BikeCrash', play=True, cycle=cycle, volume=1)
    change_audio(world, self._gui_ref, child_ref='AudioSource', play=False, cycle=cycle+GuiTools.time_to_cycle(1))


def gui_crash_area_wall(self, world, gui_event):
    # GuiEvent(GuiEventType.CrashAreaWall, side=side, agent=self)
    self._gui_handle_crash(world, gui_event)


def gui_crash_my_wall(self, world, gui_event):
    # GuiEvent(GuiEventType.CrashMyWall, side=side, agent=self)
    self._gui_handle_crash(world, gui_event)


def gui_crash_enemy_wall(self, world, gui_event):
    # GuiEvent(GuiEventType.CrashEnemyWall, side=side, agent=self)
    self._gui_handle_crash(world, gui_event)


def gui_crash_enemy_agent(self, world, gui_event):
    # GuiEvent(GuiEventType.CrashEnemyAgent, side=side, agent=self)
    self._gui_handle_crash(world, gui_event)


Agent.gui_init = gui_init
Agent._gui_move_step = _gui_move_step
Agent.gui_move = gui_move
Agent.gui_change_direction = gui_change_direction
Agent.gui_activate_wall_breaker = gui_activate_wall_breaker
Agent.gui_end_wall_breaker = gui_end_wall_breaker
Agent.gui_reload_wall_breaker = gui_reload_wall_breaker
Agent.gui_construct_wall = gui_construct_wall
Agent.gui_destruct_wall = gui_destruct_wall
Agent._gui_handle_crash = _gui_handle_crash
Agent.gui_crash_area_wall = gui_crash_area_wall
Agent.gui_crash_my_wall = gui_crash_my_wall
Agent.gui_crash_enemy_wall = gui_crash_enemy_wall
Agent.gui_crash_enemy_agent = gui_crash_enemy_agent
