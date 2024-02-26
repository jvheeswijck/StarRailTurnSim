from character_base import Character

from typing import Callable


class Buff(object):
    def __init__(self, host: Character, turns: int):
        self.host = host
        self.turns = turns

    def apply(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError


class SpeedBuff(Buff):
    def __init__(self, host: Character, turns, flatValue=None, percentValue=None):
        super.__init__(host, turns)
        if flatValue:
            self.flatValue = flatValue
        else:
            self.flatValue = None
        if percentValue:
            self.percFlatValue = self.host.baseSpeed * (1 + percentValue / 100)
        else:
            self.perFlatvalue = None
        self.turns = turns
        self.host = host

    def apply(self):
        if self.percFlatValue is not None:
            self.host.currentSpeed += self.percFlatValue
        if self.flatValue is not None:
            self.host.currentSpeed += self.flatValue

    def remove(self):
        if self.percent is not None:
            self.host.currentSpeed -= self.percFlatValue
        elif self.flatValue is not None:
            self.host.currentSpeed -= self.flatValue


class Basic(object):
    def __init__(self, energy):
        self.energy = energy


class Skill(object):
    def __init__(
        self, target: Character = None, effect: Callable = None, energy: int = 30
    ):
        self.target = target
        self.effect = effect
        self.energy = energy

    def setTarget(self, target: Character):
        self.target = target

    def activate(self):
        self.effect(self.target)
