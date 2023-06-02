# -*- coding: utf-8 -*-

# python imports
from enum import Enum


class GuiEventType(Enum):
    ChangeDirection = 0
    ActivateWallBreaker = 1
    EndWallBreaker = 2
    ReloadWallBreaker = 3
    ConstructWall = 4
    DestructWall = 5
    CrashAreaWall = 6
    CrashMyWall = 7
    CrashEnemyWall = 8
    CrashEnemyAgent = 9
    DecreaseHealth = 10


class GuiEvent(object):

    def __init__(self, type, **kwargs):
        self.type = type
        self.__dict__.update(kwargs)
