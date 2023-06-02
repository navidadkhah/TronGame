# -*- coding: utf-8 -*-

# project imports
from ..ks.models import ECell


@staticmethod
def get_wall_type(side):
    cell_name = side + "Wall"
    return ECell[cell_name]


ECell.get_wall_type = get_wall_type
