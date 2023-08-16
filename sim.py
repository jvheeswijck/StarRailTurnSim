import pandas as pd

from itertools import chain
from character_base import Character


class Sim:
    def __init__(self, characters: dict[str:Character]=None):
        pass
        # self.characters = characters
        # self.char_list: list[Character] = list(characters.values())
        # self.units = 750
        # self.turnCounts = {}
        # self.data = None
        
    def set_chars(self, characters: dict[str:Character]):
        self.characters = characters
        self.char_list: list[Character] = list(characters.values())
        self.units = 750
        self.turnCounts = {}
        self.data = None        

    def tick(self):
        for c in sorted(self.char_list, key=lambda x: x.actionGauge):
            c.tick()

    def reset(self):
        for c in self.char_list:
            c.reset()
        self.data = None

    def run(self, units, turns=0):
        for i in range(units):
            self.tick()

    def run_speed_comparison(
        self, target: Character | str, start=100, end=160, units=750
    ):
        if type(target) is str:
            target = self.characters[target]

        self.turnCounts = {target.name: []}
        self.units = units

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
            title=f"Actions for {name} in {self.units / 75} cycles. Bronya 105 speed, skill+basic rotation",
        )

    def plot(self, *chars):
        if not len(chars):
            data = {name: c.history for name, c in self.characters.items()}
        else:
            data = {name: self.characters[name].history for name in chars}
        df = pd.DataFrame(data)
        return df.plot.line(figsize=(15, 2))

    def build_dataframe(self):
        data = list(
            chain(
                *[
                    [
                        (i, name, av, tc)
                        for i, (av, tc) in enumerate(
                            zip(char.history, char.turn_history)
                        )
                    ]
                    for name, char in self.characters.items()
                ]
            )
        )
        df = pd.DataFrame.from_records(
            data, columns=["Action Value", "Character", "Action Gauge", "Turns"]
        )
        df["Cycles"] = df["Action Value"] / 75
        return df
        # Calculate turns for every row
