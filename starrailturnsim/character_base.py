from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from effects import Basic, Buff, SpeedBuff


# @dataclass(frozen=True, slots=True)
# class AVPoint:
#     name : float
#     elapsedAV : float 
#     actionGauge : float
#     turnCount : int
#     av : float
#     speed : float

@dataclass
class Character:
    """Character object"""

    name: str
    baseSpeed: float
    maxEnergy: int
    energyRegen : float
    
    energy: float
    
    _currentSpeed: float = 98
    _actionGauge: int = 10_000
    elapsedAV: int = 0
    av: int = 0
    
    history : list[tuple] = field(default_factory=list)
    
    def __post_init__(self):
        self._currentSpeed = self.baseSpeed
        
        self.buffs: dict = {}
        self.basic = None
        self.skill = None
        self.ultimate = None

        self.auto = True
        self.basicTarget = self
        self.skillTarget: Character = None
        self.agent = []
        self.agentCount = 0
        self._turnCount = 0
        self.av = 10_000 / self.currentSpeed
        
        self.battleHandler = None
        

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
        
    @property
    def currentSpeed(self):
        return self._currentSpeed
    
    @currentSpeed.setter
    def currentSpeed(self, speed):
        self._currentSpeed = speed
        self.av = self.actionGauge / self._currentSpeed
        
    @property
    def actionGauge(self):
        return self._actionGauge
    
    @actionGauge.setter
    def actionGauge(self, val):
        self._actionGauge = max(val, 0)
        self.av = self.actionGauge / self.currentSpeed

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
        self.buffs = {}
        self._turnCount = 0
        self.elapsedAV = 0
        
    @property
    def turnCount(self):
        # TODO: This produces absurdly high values occasionally
        try:
            idx = 0
            for i, entry in enumerate(self.history):
                if entry.elapsedAV > 750:
                    idx = i-1
                    break
            last_log = self.history[idx]
            # remaining_av = 750 - last_log.
            # return round(self._turnCount + (remaining_av / self.av), 2)
            return last_log.turnCount
        
        except Exception as e:
            print("error when calculating turnCount")
            print(e)
            return 0
        
    
    @property
    def baseAV(self):
        return round(10_000 / self.currentSpeed,2)
        
    @property
    def avgAV(self):
        return round(self.elapsedAV / self.turnCount, 2)
    
    def tick(self):
        # self.elapsedAV += 1
        
        # During Turn
        if self.actionGauge <= 0:
            self.actionGauge = max(self.actionGauge, 0)
            
            self._turnCount += 1
            self.log_history()
            
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
            # self.actionGauge += 10_000
            # self.history.append(self.actionGauge)

        else:
            # self.history.append(self.actionGauge)
            # self.turn_history.append(self._turnCount)
            pass
        
        # Include elapsedAV for history
        
        
    def log_history(self):
        # SP points in main sim?
        # Log current energy
        entry = (self.name, self.elapsedAV, self.actionGauge, self._turnCount, self.av, self.currentSpeed)
        self.history.append(entry)
        
    def setEnvironment(self, sim):
        self.battleHandler = sim