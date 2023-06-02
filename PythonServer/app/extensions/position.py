# -*- coding: utf-8 -*-

# project imports
from ..ks.models import Position, EDirection


@staticmethod
def dir_to_pos(direction):
    dir_to_pos_map = {
        EDirection.Up: Position(0, -1),
        EDirection.Down: Position(0, +1),
        EDirection.Right: Position(+1, 0),
        EDirection.Left: Position(-1, 0)
    }
    return dir_to_pos_map[direction]


def is_valid(self, world):
    return 0 <= self.x < len(world.board[0]) and 0 <= self.y < len(world.board)


def get_neighbors(self, world, neighbor_type=None):
    neighbors = {}

    for direction in EDirection:
        neighbor_pos = self + Position.dir_to_pos(direction)
        if (neighbor_pos.is_valid(world) and \
            (neighbor_type is None or world.board[neighbor_pos.y][neighbor_pos.x] == neighbor_type)):
            neighbors[direction] = neighbor_pos

    return neighbors


def get_8neighbors(self, world, neighbor_type=None):
    neighbors = self.get_neighbors(world, neighbor_type=neighbor_type)
    for direction, position in list(neighbors.items()):
        neighbors[(direction,)] = position
        del neighbors[direction]

    for dir1 in EDirection:
        for dir2 in EDirection:
            if dir1 == dir2 or dir1 == dir2.opposite():
                continue

            neighbor_pos = self + Position.dir_to_pos(dir1) + Position.dir_to_pos(dir2)
            if (neighbor_pos.is_valid(world) and \
                (neighbor_type is None or world.board[neighbor_pos.y][neighbor_pos.x] == neighbor_type)):
                neighbors[(dir1, dir2)] = neighbor_pos

    return neighbors


def __eq__(self, other):
    if isinstance(other, Position):
        return self.x == other.x and self.y == other.y
    return NotImplemented


def __ne__(self, other):
    r = self.__eq__(other)
    if r is not NotImplemented:
        return not r
    return NotImplemented


def __hash__(self):
    return hash(tuple(sorted(self.__dict__.items())))


def __add__(self, other):
    if isinstance(other, Position):
        return Position(self.x + other.x, self.y + other.y)
    return NotImplemented


def __sub__(self, other):
    if isinstance(other, Position):
        return Position(self.x - other.x, self.y - other.y)
    return NotImplemented


def __repr__(self):
    return "<x: %s, y: %s>" % (self.x, self.y)


Position.dir_to_pos = dir_to_pos
Position.is_valid = is_valid
Position.get_neighbors = get_neighbors
Position.get_8neighbors = get_8neighbors
Position.__eq__ = __eq__
Position.__ne__ = __ne__
Position.__hash__ = __hash__
Position.__add__ = __add__
Position.__sub__ = __sub__
Position.__repr__ = __repr__
