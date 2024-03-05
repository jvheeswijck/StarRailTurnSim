import polars as pl
import logging

from pprint import pprint

from dataclasses import dataclass

from character_base import Character
from builder import charactersDB

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def flatten(xss):
    return [x for xs in xss for x in xs]


# Divide each turn into parts, start of turn, end of turn, action phase, ultimate phase, extra turn phase
# Current turn queue

@dataclass
class CombatState:
    turnQueue: list
    av: int = 0
    sp: int = 3
    

class Sim:
    def __init__(self, characters: dict[str:Character] = None):
        self.battleState = CombatState
        self.battleState.turnQueue = []
        
        self.elapsedAV = 0
        self.actionPoints = 3
        if characters is not None:
            self.characters = characters
            self.char_list: list[Character] = list(characters.values())
            self.entity_list: list[Character] = list(characters.values())
            self.character_names = [x.name for x in self.char_list]

        self.timeFrame = 450
        self.turnCounts = {}
        self.data = None
        self.speed_turn_data = {}
        self.turnHistory = []

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
        self.characters : dict[str:Character] = characters
        self.char_list: list[Character] = list(characters.values())
        self.entity_list: list[Character] = list(characters.values())
        self.character_names = [x.name for x in self.char_list]
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
            for char in self.entity_list[1:]:
                lowest_av = min(lowest_av, char.av)
                
            # for i in range(1, len(self.entity_list)):
            #     if self.entity_list[i].av < lowest_av:
            #         lowest_av = self.entity_list[i].av

            # Will there be rounding problems here?
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
        # Sooomewhere here?
        active = False
        for entity in self.entity_list:
            if entity.av <= 0 or entity.actionGauge <= 0:
                active = True
                break
        if not active:
            self.advance_time()
        else:
            logging.debug('No need to advance time')

        for c in self.entity_list:
            c.tick()        
            if c.actionGauge <= 0:
                c.actionGauge += 10_000.0
            for c in self.entity_list:
                c.log_history()

    def reset(self):
        for char in self.char_list:
            char.reset()
            char.log_history()
        self.data = None
        self.elapsedAV = 0
        self.turnHistory = []
    

    def run(self, units=None, turns=0):
        failsafe_counter = 0
        if units:
            self.timeFrame = units
        while True:
            failsafe_counter += 1
            self.tick()
            if self.elapsedAV > self.timeFrame:
                break


    def run_speed_compare(
        self, 
        target: Character | str,
        duration : int = None,
        start_speed : int = 95, 
        end_speed : int = 174,
    ):
        if isinstance(target, str):
            target = self.characters[target]
            
        if target is None:
            print('No character selected')
            return None, None
            
        logger.info('Simulating speed for %s', target.name)
        
        data = {name:{'x_speed':[], 'y_turns':[]} for name in self.character_names}
    
        if duration is None:
            duration = self.timeFrame

        # THe problem is not here since the speed was only printed once.. the history seems to be repeating
        original_speed = target.currentSpeed
        for speed in range(start_speed, end_speed, 1):
            target.setSpeed(speed)
                        
            self.reset()
            self.run(duration)
            
            # time.sleep(0.05)
            
            # A TIMING ISSUE?
            
            # IF I COMMENT THIS OUT, THE THING BREAKS
            
            # cols = ['name', 'elapsedav', 'actiongauage', 'turncount', 'av', 'speed']

            # df = pl.from_records(target.history, schema=['Character', 'Elapsed Action Value', 'Action Gauge', 'Turns', 'AV Value', 'Speed'])
            # df.write_parquet(f'../test_data/{speed}.parquet')
            for char in self.char_list:
                data[char.name]['x_speed'].append(speed)
                data[char.name]['y_turns'].append(char.totalTurnCount)
            
            # Check why there are speeds where turnCount is 0
            # if target.totalTurnCount == 0:
            #     print(target.history)
                
        # dfr = pl.DataFrame({
        #     'speed':x_speed,
        #     'turns':y_turns
        # })
        # dfr.write_parquet('../test_data/result.parquet')
        # Temporary solution, make sure orignal graph/values are unchanged. 
        target.setSpeed(original_speed)
        self.reset()
        self.run(duration)
        self.speed_turn_data = data
        return data

    # def plot_speed_comparison(self):
    #     name = list(self.turnCounts.keys())[0]
    #     x = [x for x, y in self.turnCounts[name]]
    #     y = [y for x, y in self.turnCounts[name]]
    #     df2 = pd.DataFrame(
    #         {
    #             "speed": x,
    #             "turns": y,
    #         }
    #     )
    #     return df2.plot.line(
    #         "speed",
    #         "turns",
    #         title=f"Actions for {name} in {self.timeFrame / 75} cycles. Bronya 105 speed, skill+basic rotation",
    #     )

    # def plot(self, *chars):
    #     if not len(chars):
    #         data = {name: c.history for name, c in self.characters.items()}
    #     else:
    #         data = {name: self.characters[name].history for name in chars}
    #     df = pd.DataFrame(data)
    #     return df.plot.line(figsize=(15, 2))

    def build_dataframe(self):
        data = flatten([char.history for _, char in self.characters.items()])

        # df = pd.DataFrame(data)
        # df = df.rename(
        #     columns={
        #         "name": "Character",
        #         "elapsedAV": "Elapsed Action Value",
        #         "actionGauge": "Action Gauge",
        #         "turnCount": "Turns",
        #         "av": "AV Value",
        #         "speed": "Speed",
        #     }
        # )

        # df["Cycles"] = df["Elapsed Action Value"] / 75
        # print(data)
        # df = df.rename(
        #     {
        #         "name": "Character",
        #         "elapsedAV": "Elapsed Action Value",
        #         "actionGauge": "Action Gauge",
        #         "turnCount": "Turns",
        #         "av": "AV Value",
        #         "speed": "Speed",
        #     }
        # )
        
        df = pl.from_records(data, schema=['Character', 'Elapsed Action Value', 'Action Gauge', 'Turns', 'AV Value', 'Speed'])
        df = df.with_columns((pl.col("Elapsed Action Value") / 75).alias("Cycles"))

        return df

    def sort(self, order: list[Character]):
        self.char_list = sorted(self.char_list, key=lambda x: order.index(x.name))
