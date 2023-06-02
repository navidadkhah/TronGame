# -*- coding: utf-8 -*-

# project imports
from ....ks.models import World, Position, ECell, EDirection
from ....gui_events import GuiEventType
from ..utils import (create_asset, change_transform, end_cycle, create_main_light, change_material,
                     init_main_camera, change_text, change_slider, change_scale, change_audio)


def _configure(self):
    self.ground_refs = {}
    self.wall_refs = {side: {} for side in self.agents.keys()}

    self.GUI_CELL_SIZE = 2
    self.GUI_X_OFFSET = -(len(self.board[0]) - 1) * self.GUI_CELL_SIZE / 2
    self.GUI_Z_OFFSET = -(len(self.board) - 1) * self.GUI_CELL_SIZE / 2

    Position.GUI_CELL_SIZE = self.GUI_CELL_SIZE
    Position.GUI_X_OFFSET = self.GUI_X_OFFSET
    Position.GUI_Z_OFFSET = self.GUI_Z_OFFSET


def _init_objects(self):
    # Create Board
    base_ground_ref = create_asset(self, 'BaseGround')
    change_scale(
        self,
        base_ground_ref,
        x_scale = (len(self.board[0])) * self.GUI_CELL_SIZE / 10,
        z_scale = (len(self.board)) * self.GUI_CELL_SIZE / 10,
    )

    area_walls = {}

    for y in range(len(self.board)):
        for x in range(len(self.board[y])):
            ref = create_asset(self, 'Ground')
            change_transform(self, ref, position=Position(x=x, y=y).get_gui_position())
            self.ground_refs[(x, y)] = ref

            if self.board[y][x] == ECell.AreaWall:
                change_material(self, ref, 'AreaWallGround')
            
            if self.board[y][x] == ECell.Empty:
                neighbors = Position(x=x, y=y).get_8neighbors(self, ECell.AreaWall)

                for neighbor_dirs, neighbor_pos in neighbors.items():
                    if (neighbor_pos.x, neighbor_pos.y) not in area_walls:
                        area_walls[(neighbor_pos.x, neighbor_pos.y)] = {}

                    if 'center' not in area_walls[(neighbor_pos.x, neighbor_pos.y)]:
                        area_walls[(neighbor_pos.x, neighbor_pos.y)]['center'] = True
                        ref = create_asset(self, 'AreaWallCenter')
                        change_transform(self, ref, position=neighbor_pos.get_gui_position())

                    if len(neighbor_dirs) == 1:
                        dirs = [d for d in EDirection if d != neighbor_dirs[0] and d != neighbor_dirs[0].opposite()]
                    else:
                        dirs = [d.opposite() for d in neighbor_dirs]
                    neighbor_walls = neighbor_pos.get_neighbors(self, ECell.AreaWall)

                    for d in dirs:
                        if d in neighbor_walls and d not in area_walls[(neighbor_pos.x, neighbor_pos.y)]:
                            area_walls[(neighbor_pos.x, neighbor_pos.y)][d] = True
                            ref = create_asset(self, 'AreaWall')
                            change_transform(
                                self,
                                ref,
                                position = neighbor_pos.get_gui_position(),
                                y_rotation = d.get_gui_rotation(),
                            )

    # Create Agents
    for side, agent in self.agents.items():
        agent.gui_init(self, side)

    # Create top status
    self._top_status_ref = create_asset(self, 'TopStatus', is_ui=True)
    change_text(self, self._top_status_ref, child_ref='Cycle/Max', text=str(self.constants.max_cycles))
    for side, agent in self.agents.items():
        change_text(self, self._top_status_ref, child_ref='{}TeamName'.format(side), text=self._team_nicknames[side])
        change_text(self, self._top_status_ref, child_ref='{}Health'.format(side), text=str(agent.health))
    self._update_top_status(0)


def _init_light(self):
    create_main_light(self)


def _init_camera(self):
    init_main_camera(self)


def _init_sounds(self):
    ref = create_asset(self, 'BackgroundAudioSource')
    change_audio(self, ref, clip='BackgroundMusic', play=True, time=0)


def gui_init(self, scene, team_nicknames):
    self.scene = scene
    self._team_nicknames = team_nicknames

    self._configure()
    self._init_objects()
    self._init_light()
    self._init_camera()
    self._init_sounds()

    end_cycle(self)


def _update_top_status(self, current_cycle):
    # Set cycle
    change_text(self, self._top_status_ref, child_ref='Cycle/Current', text=str(current_cycle))

    # Set scores slider
    slider_value = 0.5
    if len(set(self.scores.values())) != 1:
        scores = {side: score for side, score in self.scores.items()}

        min_score = min(scores.values())
        if min_score < 0:
            for side in scores.keys():
                scores[side] -= min_score

        slider_value = scores['Blue'] / sum(scores.values())

    change_slider(self, self._top_status_ref, 'ScoresSlider', slider_value, 0.5)

    for side, agent in self.agents.items():
        # Set score
        change_text(self, self._top_status_ref, child_ref='{}Score'.format(side), text=str(self.scores[side]))

        # Set position
        change_text(
            self,
            self._top_status_ref,
            child_ref = '{}Position'.format(side),
            text = '{}, {}'.format(agent.position.x, agent.position.y),
        )

        # Set wall breaker status
        if agent.wall_breaker_rem_time > 0:
            text = agent.wall_breaker_rem_time
            color = 'FF0000'
        else:
            text = agent.wall_breaker_cooldown
            color = '00FFFF' if side == 'Blue' else 'FFFF00'

        shield_child_ref = '{}Shield'.format(side)
        change_text(self, self._top_status_ref, child_ref=shield_child_ref, text='<color=#{}>{}'.format(color, text))


def _gui_update_health(self, gui_event):
    # GuiEvent(GuiEventType.DecreaseHealth, side=side, agent=self)
    change_text(
        self,
        self._top_status_ref,
        child_ref = '{}Health'.format(gui_event.side),
        text = str(gui_event.agent.health),
    )


def gui_update(self, current_cycle, events):
    # Manage events
    destruct_own_events = []
    destruct_events = []
    construct_events = []

    for event in events:
        if event.type == GuiEventType.ChangeDirection:
            event.agent.gui_change_direction(self, event)

        elif event.type == GuiEventType.ActivateWallBreaker:
            event.agent.gui_activate_wall_breaker(self, event)

        elif event.type == GuiEventType.EndWallBreaker:
            event.agent.gui_end_wall_breaker(self, event)

        elif event.type == GuiEventType.ReloadWallBreaker:
            event.agent.gui_reload_wall_breaker(self, event)

        elif event.type == GuiEventType.ConstructWall:
            construct_events.append(event)

        elif event.type == GuiEventType.DestructWall:
            if event.side == event.wall_side:
                destruct_own_events.append(event)
            else:
                destruct_events.append(event)

        elif event.type == GuiEventType.CrashAreaWall:
            event.agent.gui_crash_area_wall(self, event)

        elif event.type == GuiEventType.CrashMyWall:
            event.agent.gui_crash_my_wall(self, event)

        elif event.type == GuiEventType.CrashEnemyWall:
            event.agent.gui_crash_enemy_wall(self, event)

        elif event.type == GuiEventType.CrashEnemyAgent:
            event.agent.gui_crash_enemy_agent(self, event)

        elif event.type == GuiEventType.DecreaseHealth:
            self._gui_update_health(event)

    for event in destruct_own_events:
        event.agent.gui_destruct_wall(self, event)

    for event in construct_events:
        event.agent.gui_construct_wall(self, event)

    for event in destruct_events:
        event.agent.gui_destruct_wall(self, event)

    for agent in self.agents.values():
        agent.gui_move(self)

    self._update_top_status(current_cycle)

    end_cycle(self)


World._configure = _configure
World._init_objects = _init_objects
World._init_light = _init_light
World._init_camera = _init_camera
World._init_sounds = _init_sounds
World.gui_init = gui_init
World._update_top_status = _update_top_status
World._gui_update_health = _gui_update_health
World.gui_update = gui_update
