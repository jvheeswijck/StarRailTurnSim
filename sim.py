import pandas as pd

from dataclasses import dataclass

from character_base import Character
from builder import charactersDB


def flatten(xss):
    return [x for xs in xss for x in xs]


@dataclass
class CombatState:
    av: int
    sp: int
    turnQueue: list


class Sim:
    def __init__(self, characters: dict[str:Character] = None):
        self.elapsedAV = 0
        self.actionPoints = 3
        if characters is not None:
            self.characters = characters
            self.char_list: list[Character] = list(characters.values())
            self.entity_list: list[Character] = list(characters.values())

        self.timeFrame = 750
        self.turnCounts = {}
        self.data = None

        for c in charactersDB:
            c.setEnvironment(self)

        # self.characters = characters
        # self.char_list: list[Character] = list(characters.values())
        # self.units = 750
        # self.turnCounts = {}
        # self.data = None

    def set_sp(self, sp):
        self._sp = sp

    def set_chars(self, characters: dict[str:Character]):
        self.characters = characters
        self.char_list: list[Character] = list(characters.values())
        self.entity_list: list[Character] = list(characters.values())
        self.timeFrame = 750
        self.turnCounts = {}
        self.data = None

    # def tick(self):
    #     # for c in sorted(self.char_list, key=lambda x: x.actionGauge):
    #     for c in self.char_list:
    #         c.tick()

    #     # Move action

    def advance_time(self):
        # try:
        #     lowest_av = self.entity_list[0].av
        #     for i, entity in enumerate(self.entity_list[1:]):
        #         if entity.av < lowest_av:
        #             lowest_av = entity.av

        #     for entity in self.entity_list:
        #         entity.actionGauge -= lowest_av * entity.currentSpeed
        #         entity.elapsedAV += lowest_av

        #     self.elapsedAV += lowest_av
        # except Exception as e:
        #     print(e)

        try:
            lowest_av = self.entity_list[0].av
            for i in range(1, len(self.entity_list)):
                if self.entity_list[i].av < lowest_av:
                    lowest_av = self.entity_list[i].av

            for i in range(len(self.entity_list)):
                self.entity_list[i].actionGauge -= (
                    lowest_av * self.entity_list[i].currentSpeed
                )
                self.entity_list[i].elapsedAV += lowest_av

            self.elapsedAV += lowest_av
        except Exception as e:
            print(e)

    def excTurn(self):
        # Create turn queue, advance forwards go to the top of the queue
        pass

    def tick(self):
        active = False
        for entity in self.entity_list:
            if entity.av == 0 or entity.actionGauge <= 0:
                active = True
                break
        if not active:
            # print("Advancing")
            self.advance_time()

        for c in self.entity_list:
            c.tick()
            if c.actionGauge <= 0:
                c.actionGauge += 10_000
            for c in self.entity_list:
                c.log_history()

    def reset(self):
        for c in self.char_list:
            c.reset()
            c.log_history()
        self.data = None
        self.elapsedAV = 0

    def run(self, units=None, turns=0):
        if units:
            self.timeFrame = units
        while True:
            self.tick()
            if self.elapsedAV > self.timeFrame:
                break

    def run_speed_comparison(
        self, target: Character | str, start=100, end=160, units=750
    ):
        if isinstance(target) is str:
            target = self.characters[target]

        self.turnCounts = {target.name: []}
        self.timeFrame = units

        for speed in range(start, end, 1):
            self.reset()
            target.setSpeed(speed)
            self.run(units)
            self.turnCounts[target.name].append((speed, target._turnCount))
        return self.turnCounts[target.name]

    def plot_speed_comparison(self):
        name = list(self.turnCounts.keys())[0]
        x = [x for x, y in self.turnCounts[name]]
        y = [y for x, y in self.turnCounts[name]]
        df2 = pd.DataFrame(
            {
                "speed": x,
                "turns": y,
            }
        )
        return df2.plot.line(
            "speed",
            "turns",
            title=f"Actions for {name} in {self.timeFrame / 75} cycles. Bronya 105 speed, skill+basic rotation",
        )

    def plot(self, *chars):
        if not len(chars):
            data = {name: c.history for name, c in self.characters.items()}
        else:
            data = {name: self.characters[name].history for name in chars}
        df = pd.DataFrame(data)
        return df.plot.line(figsize=(15, 2))

    def build_dataframe(self):
        # Redo this to include elapsedAV
        # data = list(
        #     chain(
        #         *[
        #             [
        #                 (i, name, av, tc)
        #                 for i, (av, tc) in enumerate(
        #                     zip(char.history, char.turn_history)
        #                 )
        #             ]
        #             for name, char in self.characters.items()
        #         ]
        #     )
        # )

        # data = list(
        #     chain(
        #         *[
        #             [
        #                 (name, elapsedAV, actionGauge, turnCount, avValue)
        #                 for elapsedAV, actionGauge, turnCount, avValue in char.history
        #             ]
        #             for name, char in self.characters.items()
        #         ]
        #     )
        # )
        # df = pd.DataFrame(
        #     data, columns=["Character", "Elapsed Action Value", "Action Gauge", "Turns", "AV Value"]
        # )
        # df["Cycles"] = df["Elapsed Action Value"] / 75
        # return df

        # data = list(
        #     chain(*[char.history for _, char in self.characters.items()]))

        data = flatten([char.history for _, char in self.characters.items()])

        df = pd.DataFrame(data)
        # print("===========================================================")
        # print(df.head())
        df = df.rename(
            columns={
                "name": "Character",
                "elapsedAV": "Elapsed Action Value",
                "actionGauge": "Action Gauge",
                "turnCount": "Turns",
                "av": "AV Value",
                "speed": "Speed",
            }
        )

        df["Cycles"] = df["Elapsed Action Value"] / 75

        return df
        # Calculate turns for every row

    def sort(self, order: list[Character]):
        self.char_list = sorted(self.char_list, key=lambda x: order.index(x.name))
