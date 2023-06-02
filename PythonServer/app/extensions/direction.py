# -*- coding: utf-8 -*-

# project imports
from ..ks.models import EDirection


def opposite(self):
    opposite_direction_map = {
        EDirection.Up: EDirection.Down,
        EDirection.Down: EDirection.Up,
        EDirection.Right: EDirection.Left,
        EDirection.Left: EDirection.Right
    }
    return opposite_direction_map[self]


EDirection.opposite = opposite
