#!/usr/bin/env python3

DEBUGGING = False

def dprint(*args, **kwargs):
    if DEBUGGING:
        print(*args, **kwargs)
