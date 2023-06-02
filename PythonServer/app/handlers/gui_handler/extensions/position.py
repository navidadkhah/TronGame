# -*- coding: utf-8 -*-

# chillin imports
from chillin_server.gui.scene_actions import Vector3

# project imports
from ....ks.models import Position, EDirection


def get_gui_position(self):
    return Vector3(
        x = self.x * Position.GUI_CELL_SIZE + Position.GUI_X_OFFSET,
        z = -self.y * Position.GUI_CELL_SIZE - Position.GUI_Z_OFFSET,
    )


Position.get_gui_position = get_gui_position
