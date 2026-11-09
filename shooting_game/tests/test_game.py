"""Game: objects working together (integration test)."""
from game import Game
from monster import Monster
from settings import MONSTER_COUNT


def test_starts_with_several_monsters():
    assert len(Game().monsters) == MONSTER_COUNT


def test_three_bolts_kill_a_monster_and_score():
    game = Game()
    for other in list(game.monsters):                   # keep only one known monster
        other.kill()
    monster = Monster(game.player.pos.x, game.player.pos.y - 200, target=game.player)
    monster.speed = 0                                   # keep it still
    game.monsters.add(monster)
    game.all_sprites.add(monster)

    game.player.trigger_pressed = True                  # hold Space...
    for _ in range(120):                                # ...for at most 2 seconds of game
        game.update(1 / 60)
        if not monster.alive():                         # stop as soon as it is defeated, so the
            break                                       # new monster cannot be hit by chance

    assert not monster.alive()
    assert game.player.score == Monster.POINTS
    assert len(game.monsters) == 1                      # a new monster appeared
