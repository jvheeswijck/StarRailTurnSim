from __future__ import annotations

import logging

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from effects import Basic, Buff, SpeedBuff
    from sim import Sim


# @dataclass(frozen=True, slots=True)
# class AVPoint:
#     name : float
#     elapsedAV : float
#     actionGauge : float
#     turnCount : int
#     av : float
#     speed : float

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass(slots=True)
class CharacterStats:
    baseSpeed: float
    maxEnergy: int
    energyRegen: float


class CharacterAction:
    def __init__(self): ...


@dataclass
class Character:
    """Character object"""

    name: str
    baseSpeed: float
    maxEnergy: int
    energyRegen: float

    energy: float

    _currentSpeed: float = 98
    _actionGauge: int = 10_000
    elapsedAV: int = 0
    av: int = 0

    history: list[tuple] = field(default_factory=list)

    def __post_init__(self):
        self._currentSpeed = self.baseSpeed

        self.buffs: dict[str,] = {}
        self.basic: callable = None
        self.skill: callable = None
        self.ultimate: callable = None

        self.auto: bool = True
        self.basicTarget: Character = self
        self.skillTarget: Character = None
        self.agent: list[str] = []
        self.agentCount: int = 0
        self._turnCount: int = 0
        self.av: float = 10_000 / self.currentSpeed

        self.battleHandler : Sim = None

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
        self._actionGauge = val
        self.av = self.actionGauge / self.currentSpeed

    def advance(self, percent):
        self.log_history()
        self.actionGauge -= (percent / 100) * 10_000

    def delay(self, percent):
        self.log_history()
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
    def totalTurnCount(self):  # Rename this to totalTurnCount
        # TODO: This produces absurdly high values occasionally
        try:
            idx = 0
            for i, entry in enumerate(reversed(self.history)):
                if int(entry[1]) < self.battleHandler.timeFrame:
                    idx = i
                    break
            last_log = list(reversed(self.history))[idx]
            # remaining_av = 750 - last_log.
            # return round(self._turnCount + (remaining_av / self.av), 2)
            return last_log[3]

        except Exception:
            logger.error("Could not determine total turn count")
            return -1

    @property
    def baseAV(self):
        return round(10_000 / self.currentSpeed, 2)

    @property
    def avgAV(self):
        if self.totalTurnCount != 0:
            return round(self.elapsedAV / self.totalTurnCount, 2)
        else:
            return "N/A"

    def tick(self):
        # During Turn
        if self.actionGauge <= 0:
            self.actionGauge = max(self.actionGauge, 0.0)

            self._turnCount += 1
            self.log_history()

            if self.buffs:
                for k, b in self.buffs.items():
                    b.onTurnStart()

            if self.auto:
                self.skill(self.skillTarget)
            else:
                if self.agent[self.agentCount] == "basic":
                    logger.debug("Basic targeting %s", self.basicTarget.name)
                    self.basic(self.basicTarget)
                elif self.agent[self.agentCount] == "skill":
                    logger.debug("Skill targeting %s", self.skillTarget.name)
                    self.skill(self.skillTarget)
                self.agentCount = (self.agentCount + 1) % len(self.agent)

            if self.buffs:
                for k in list(self.buffs.keys()):
                    if self.buffs[k].turns == 0:
                        del self.buffs[k]
            self.battleHandler.turnHistory.append((self.name, round(self.battleHandler.elapsedAV, 1)))

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

        entry = (
            self.name,
            round(self.elapsedAV, 1),
            round(max(self.actionGauge, 0), 1),
            self._turnCount,
            round(max(self.av, 0), 1),
            self.currentSpeed,
        )
        self.history.append(entry)

    def setEnvironment(self, sim):
        self.battleHandler = sim
