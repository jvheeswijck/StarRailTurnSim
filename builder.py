import yaml
from functools import partial
from character_base import Character


class CharacterManager:
    def __init__(self):
        char_path = "configs/characters.yml"
        skills_path = "configs/skills.yml"
        self.characters = {}

        with open(char_path, "r") as f:
            self.char_config = yaml.safe_load(f)

        with open(skills_path, "r") as f:
            self.skill_config = yaml.safe_load(f)

        for c, config in self.char_config.items():
            character_obj = Character(name=c, **config)

            try:
                character_obj.basic = make_basic(self.skill_config[c]["basic"])
                character_obj.skill = make_skill(self.skill_config[c]["skill"])
            except KeyError:
                print("Skills not found")
                continue
            self.characters[c] = character_obj
            
    def reset(self, name):
        character_obj = Character(name=name, **self.char_config[name])
        character_obj.basic = make_basic(self.skill_config[name]["basic"])
        character_obj.skill = make_skill(self.skill_config[name]["skill"])
        self.characters[name] = character_obj

    def get(self, *names) -> dict:
        return {
            name: self.characters[name]
            for name in names
            if self.characters.get(name, None) is not None
        }

    def get_names(self):
        return sorted(list(self.characters.keys()))

    def __call__(self, name: str) -> Character:
        return self.characters[name]


def make_basic(d: dict):
    if d["effect"]:
        for name, amount in d["effect"].items():
            if name == "advance":
                return partial(advance, percent=amount)
    else:
        return lambda x: None


def make_skill(d: dict):
    if d["effect"]:
        for name, amount in d["effect"].items():
            if name == "advance":
                return partial(advance, percent=amount)
    else:
        return lambda x: None


def make_speed_buff():
    pass


def advance(target: Character, percent: float):
    return target.advance(percent)


def delay(target: Character, percent: float):
    return lambda: target.delay(percent)
