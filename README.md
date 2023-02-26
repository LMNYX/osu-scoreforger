# osu! Score Forger

A tool to create scores on lazer in osu!

> ⚠ **Warning:** Anything you do is your own responsibility, using it is considered cheating. Please use it only for educational purposes.

## Installation

> ⚠ You need to have lazer installed on your PC and updated to the latest version for the best output.

1. Clone the repository
2. Install dependencies: `pip3 install -r requirements.txt`
3. Edit the `run.py` and `.env` to your needs
4. Run `python3 run.py`


## Best practices

1. Keep accuracy limited to `1` (100%), otherwise you'll break your pp and possibly leaderboard submissions (idk if they still break). Other than that accuracy is not limited, even by computing limits
2. Keep score limited to `1000000` (lazer maximum with no mods)
3. You'll be eventually banned if you submit obvious fake scores, they care about lazer scores as much as stable
4. Do not submit scores on mode maps on standard and vice versa

## Limits

* Score is limited to 32 bit integer limit;
* Combo, greats, okays and misses are limited to 16 bit integer limit;
* Tick hits, bonuses, misses are limited to 16 bit integer limit;
* Accuracy is unlimited;

## Definition book

Rulesets:
```python
ScoreForger.RuleSets.STANDARD
ScoreForger.RuleSets.TAIKO
ScoreForger.RuleSets.CATCH
ScoreForger.RuleSets.MANIA
```

Passstates:
```python 
ScoreForger.PassState.FAIL
ScoreForger.PassState.PASS
```

Ranks:
```python
ScoreForger.Ranks.SS
ScoreForger.Ranks.SSH
ScoreForger.Ranks.SH
ScoreForger.Ranks.S
ScoreForger.Ranks.A
ScoreForger.Ranks.B
ScoreForger.Ranks.C
ScoreForger.Ranks.D
ScoreForger.Ranks.F
```

Building mods array:
```python
ScoreForger.BuildModsArray("HD", "DT", "NF", ...)
```

Computing limits:
```python
ScoreForger.bit32limit # 2147483647 (score)
ScoreForger.bit16limit # 65535 (combo, greats, oks, misses, hits)
ScoreForger.bit8limit  # 255
ScoreForger.bit4limit  # 15
ScoreForger.bit2limit  # 3
ScoreForger.bit1limit  # 1
```