# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

# python imports
from __future__ import division
import math

# chillin imports
from chillin_server.gui import GuiTools, scene_actions
from chillin_server.gui.reference_manager import default_reference_manager as drm

# project imports
from ...gui_events import GuiEventType


class GuiHandler:

    def __init__(self, config, world, scene, team_nicknames):
        self._config = config
        self._world = world
        self._scene = scene
        self._team_nicknames = team_nicknames


    def initialize(self):
        self._world.gui_init(self._scene, self._team_nicknames)


    def update(self, current_cycle, events):
        self._world.gui_update(current_cycle, events)
