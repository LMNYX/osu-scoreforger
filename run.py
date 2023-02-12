import os
import ScoreForger

verhash = ScoreForger.md5(f"{ScoreForger.get_osu_runtime_dir()}/osu.Game.dll")

print("Using verhash: " + verhash)

sc = ScoreForger.ScoreForger(
    os.environ['OSU_USERNAME'], os.environ['OSU_PASSWORD'], verhash)

scoredata = ScoreForger.ScoreData(
    ScoreForger.RuleSets.STANDARD,
    ScoreForger.PassState.PASS,
    ScoreForger.bit32limit-ScoreForger.random_between(1, 10000),
    "1.0",
    ScoreForger.bit16limit,
    ScoreForger.Ranks.SSH,
    ScoreForger.BuildModsArray("HD", "DT", "HR", "FL"),
    {
        "miss": 0,
        "ok": 0,
        "great": ScoreForger.bit16limit,
        "small_tick_miss": 0,
        "small_tick_hit": 0,
        "large_tick_hit": 0,
        "small_bonus": 0,
        "large_bonus": 0,
        "ignore_miss": 1000,
        "ignore_hit": 0
    },
    {
        "great": ScoreForger.bit16limit,
        "small_tick_hit": 0,
        "large_tick_hit": 0,
        "small_bonus": 0,
        "large_bonus": 1000,
        "ignore_hit": 0
    }
)

score = sc.create_score(1, ScoreForger.RuleSets.STANDARD)
res = sc.submit_score(score, scoredata)
print("Successfully forged a score!")
