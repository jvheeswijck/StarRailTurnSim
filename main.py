from builder import CharacterManager
from sim import Sim

bronya_target = "Serval"

selector = CharacterManager()
selector("Bronya").setSkillTarget(selector(bronya_target))
selector("Bronya").setActionSeq(["basic", "skill"])
sim1 = Sim(selector.get("Bronya", "Sushang", "Serval"))

sim1.run(750)
sim1.plot().get_figure().savefig("test.png")


v = sim1.run_speed_comparison("Serval", 100, 200)
sim1.plot_speed_comparison().get_figure().savefig("speed.png")
