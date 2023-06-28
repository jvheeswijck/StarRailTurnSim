from base import Character

from typing import Callable


class Buff(object):
    def __init__(self, target: Character, turns: int):
        self.target = target
        self.turns = turns

    def apply(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError


class SpeedBuff(Buff):
    def __init__(self, target: Character, turns, flat=None, percent=None):
        super.__init__(target, turns)
        self.flat = flat
        self.percent_flat = self.target.base_speed * (1 + percent / 100)
        self.turns = turns
        self.target = target

    def apply(self):
        if self.percent is not None:
            self.target.current_speed += self.percent_flat
        if self.flat is not None:
            self.target.current_speed += self.flat

    def remove(self):
        if self.percent is not None:
            self.target.current_speed -= self.percent_flat
        elif self.flat is not None:
            self.target.current_speed -= self.flat


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
