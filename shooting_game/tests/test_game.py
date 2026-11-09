"""Game: objects working together (integration test)."""
from game import Game


def test_three_bolts_kill_a_monster_and_score():
    game = Game()
    monster = next(iter(game.monsters))
    monster.speed = 0                                   # keep it still
    monster.pos.update(game.player.pos.x, game.player.pos.y - 200)
    monster.sync_rect()

    game.player.trigger_pressed = True                  # hold Space
    for _ in range(120):                                # 2 seconds of game
        game.update(1 / 60)

    assert not monster.alive()
    assert game.player.score == 1
    assert len(game.monsters) == 1                      # a new monster appeared
