import uuid
import logging

from typing import Callable

from character_base import Character


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)




class Buff(object):
    def __init__(self, host: Character):
        self.host = host
        self.id = uuid.uuid4()

    def apply(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    def onTurnStart(self):
        raise NotImplementedError

    def onTurnEnd(self):
        raise NotImplementedError

    def onActionEnd(self):
        raise NotImplementedError
    
class StackBuff(Buff):
    def __init__(self, host: Character):
        super.__init__(host)
        self.stacks : int = 0
    

class SpeedBuff(Buff):
    def __init__(self, host: Character, duration, flatValue=None, percentValue=None):
        super.__init__(host)
        if flatValue:
            self.flatValue = flatValue
        else:
            self.flatValue = None
        if percentValue:
            self.percFlatValue = self.host.baseSpeed * (1 + percentValue / 100)
        else:
            self.perFlatvalue = None
        self.turns = duration
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
