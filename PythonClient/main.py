#! /usr/bin/env python
# -*- coding: utf-8 -*-

# python imports
import os
import sys

# chillin imports
from chillin_client import GameClient

# project imports
from ai import AI
from ks.models import World


config_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "gamecfg.json"
)
if len(sys.argv) > 1:
    config_path = sys.argv[1]


ai = AI(World())

app = GameClient(config_path)
app.register_ai(ai)
app.run()
