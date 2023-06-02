# -*- coding: utf-8 -*-

# project imports
from ....ks.models import EDirection


def get_gui_rotation(self):
    dir_to_rotation = {
        EDirection.Up: 0,
        EDirection.Right: 90,
        EDirection.Down: 180,
        EDirection.Left: -90,
    }

    return dir_to_rotation[self]


EDirection.get_gui_rotation = get_gui_rotation
