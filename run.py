import os
import ScoreForger

verhash = ScoreForger.md5(f"{ScoreForger.get_osu_runtime_dir()}/osu.Game.dll")

print("Using verhash: " + verhash)

sc = ScoreForger.ScoreForger(
    os.environ['OSU_USERNAME'], os.environ['OSU_PASSWORD'], verhash)

scoredata = ScoreForger.CreateScoreData(
    ruleset = ScoreForger.RuleSets.STANDARD,
    passstate = ScoreForger.PassState.PASS,
    total_score = 1000000,
    accuracy = "1",
    max_combo = 1000,
    rank = ScoreForger.Ranks.SS,
    mods = ScoreForger.BuildModsArray("HD", "DT"),
    statistics = {
        "miss": 0,
        "ok": 0,
        "great": 123,
        "small_tick_miss": 0,
        "small_tick_hit": 0,
        "large_tick_hit": 0,
        "small_bonus": 0,
        "large_bonus": 0,
        "ignore_miss": 0,
        "ignore_hit": 0
    }
)

score = sc.create_score(1, ScoreForger.RuleSets.STANDARD)
res = sc.submit_score(score, scoredata)
print("Successfully forged a score!")
