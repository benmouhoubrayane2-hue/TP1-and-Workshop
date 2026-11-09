"""GameBoard: play area, limits and spawn positions."""
from settings import WIDTH, HEIGHT, BOARD_MARGIN


def test_play_area_leaves_a_margin(board):
    assert board.rect.topleft == (BOARD_MARGIN, BOARD_MARGIN)
    assert board.rect.bottomright == (WIDTH - BOARD_MARGIN, HEIGHT - BOARD_MARGIN)


def test_player_start_is_inside(board):
    assert board.rect.collidepoint(board.player_start)


def test_random_top_position_is_inside(board):
    for _ in range(50):
        assert board.rect.collidepoint(board.random_top_position(margin=40))


def test_keep_inside_pulls_object_back(board, player):
    player.pos.update(-500, 5000)           # far outside, bottom-left
    board.keep_inside(player)
    assert board.rect.contains(player.rect)


def test_is_outside(board, player):
    assert not board.is_outside(player)
    player.pos.update(-1000, -1000)
    player.sync_rect()
    assert board.is_outside(player)
