#! /usr/bin/env python
# -*- coding: utf-8 -*-

# python imports
import os
from shutil import copyfile

# chillin imports
from koala_serializer import generate


ks_rel_dir = 'app/ks'
commands_ksfile = 'commands.ks'
models_ksfile = 'models.ks'

destinations = [
    '../PythonClient/ks',
    '../PythonRandomClient/ks',
    '../CppClient/Game/ks',
    '../JavaClient/src/ks',
    '../CSharpClient/Game/KS',
]

for dest in destinations:
    for ksfile in [commands_ksfile, models_ksfile]:
        path = os.path.join(dest, ksfile)
        if not os.path.exists(os.path.dirname(path)):
            os.mkdir(os.path.dirname(path))
        copyfile(os.path.join(ks_rel_dir, ksfile), path)

all_args = [
    ('python', ks_rel_dir, 'snake_case'),
    ('python', '../PythonClient/ks', 'snake_case'),
    ('python', '../PythonRandomClient/ks', 'snake_case'),
    ('cpp', '../CppClient/Game/ks', 'camelCase'),
    ('java', '../JavaClient/src', 'camelCase'),
    ('cs', '../CSharpClient/Game/KS', 'PascalCase')
]

for args in all_args:
    generate(os.path.join(ks_rel_dir, commands_ksfile), *args)
    generate(os.path.join(ks_rel_dir, models_ksfile), *args)
