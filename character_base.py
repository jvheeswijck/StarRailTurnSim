from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from effects import Basic, Buff, SpeedBuff


@dataclass
class Character:
    """Character object"""

    name: str
    baseSpeed: float
    currentSpeed: float
    maxEnergy: int
    energy: float
    actionGauge: int = 10_000
    
    def __post_init__(self):
        self.currentSpeed = self.baseSpeed
        self.history = []
        self.turn_history = []
        self.buffs: dict = {}
        self.basic = None
        self.skill = None
        self.ultimate = None

        self.auto = True
        self.basicTarget = self
        self.skillTarget: Character = None
        self.agent = []
        self.agentCount = 0
        self.turnCount = 0

    def setActionSeq(self, seq: list[str]):
        self.auto = False
        self.agent = seq

    def setSkillTarget(self, target: Character):
        self.skillTarget = target

    def setBasicTarget(self, target: Character):
        self.basicTarget = target

    def setUltimateTarget(self, target: Character | list[Character]):
        pass

    def setSpeed(self, speed):
        self.baseSpeed = speed
        self.currentSpeed = speed

        # Recalculate speed buffs

    def advance(self, percent):
        self.actionGauge -= (percent / 100) * 10_000

    def delay(self, percent):
        self.actionGauge += (percent / 100) * 10_000

    # def add_buff(self, buff: Buff):
    #     buff.apply()
    #     self.buffs.append(buff)

    def reset(self):
        self.actionGauge = 10_000
        self.agentCount = 0
        self.history = []
        self.turn_history = []
        self.buffs = {}
        self.turnCount = 0

    def tick(self):
        self.actionGauge = max(self.actionGauge - self.currentSpeed, 0)
        
        # During Turn
        if self.actionGauge <= 0:
            self.history.append(0)
            self.turnCount += 1
            self.turn_history.append(self.turnCount)

            if self.buffs:
                for k, b in self.buffs.items():
                    b.turns -= 1

            if self.auto:
                self.skill(self.skillTarget)
            else:
                if self.agent[self.agentCount] == "basic":
                    self.basic(self.basicTarget)
                elif self.agent[self.agentCount] == "skill":
                    self.skill(self.skillTarget)
                self.agentCount = (self.agentCount + 1) % len(self.agent)
                
            if self.buffs:
                for k in list(self.buffs.keys()):
                    if self.buffs[k].turns == 0:
                        del self.buffs[k]
                    
            # Reset Action Gauage
            self.actionGauge = 10_000

        else:
            self.history.append(self.actionGauge)
            self.turn_history.append(self.turnCount)
            

            