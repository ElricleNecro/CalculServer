#!/usr/bin/env python
# encoding: utf-8

class Ordonanceur(object):
    def __init__(self, nb_proc=4):
        self._nb_proc = nb_proc
        self._already_running = list()
        self._waiting = list()
        self._over = list()

    def __add__(self, cmd):
        if not isinstance(cmd, Ordonanceur):
            self.add(cmd)
            return self
        else:
            raise TypeError("Cannot add an Ordonanceur object to another.")

    def add(self, cmd):
        if len(self._already_running) <= self._nb_proc:
            self._already_running.append(cmd)
            cmd.launch(self)
        else:
            self._waiting.append(cmd)

    def end(self, obj):
        i = 0
        while id(obj) != id(self._already_running[i]):
            i += 1

        self._over.append(self._already_running[i])
        del self._already_running[i]

        if len(self._waiting) > 0:
            self._already_running.append(self._waiting[0])
            del self._waiting[0]
