# coding: utf-8

import os
import sys
import json
import math


def load_instance(target):
    global data, optimum

    file = open(os.path.join(os.path.dirname(__file__), '../instances.json'), "r")
    data = json.load(file)
    instance = [inst for inst in data if inst['name'] == target]
    if len(instance) == 0:
        raise Exception("There is no instance named %s" % target)
    instance = instance[0]
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../%s" % instance['path']))
    optimum = instance['optimum']
    if optimum is None:
        if instance['bounds'] is None:
            optimum = "nan"
        else:
            optimum = instance['bounds']['lower']

    return path, optimum
