#! /usr/bin/env python
# -*- coding: utf-8 -*-

# python imports
import os
import sys

# chillin imports
from chillin_server import GameServer, Config

# project imports
from app.game_manager import GameManager


config_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "gamecfg.json"
)
if len(sys.argv) > 1:
    config_path = sys.argv[1]

app = GameServer(config_path)
app.register_game_handler(GameManager(Config.config))
app.run()
