import pygame

# game_logicの主要関数に対する単体テスト

from constants import GRID_HEIGHT, GRID_WIDTH, SCORE_PER_LINE
from game_logic import (
    clear_rows,
    check_lost,
    create_grid,
    keyOperation,
    lock_mino,
    valid_space,
)
from helpers import get_mino_positions
from shapes import I, O


class DummyMino:
    # テスト用の簡易ミノ（game_logicが参照する属性のみ持たせる）
    def __init__(self, x, y, shape, color=(255, 0, 0), rotation=0):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.rotation = rotation


def empty_grid():
    # 盤面を空状態で初期化するヘルパー
    return [[(0, 0, 0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def test_clear_rows_updates_score_and_shifts():
    # 1行が埋まったらスコア加算＆上段の行が落ちることを確認
    locked = empty_grid()
    full_row = [(255, 0, 0) for _ in range(GRID_WIDTH)]
    shifted_row = [(0, 0, 0) for _ in range(GRID_WIDTH)]
    shifted_row[0] = (0, 255, 0)

    locked[GRID_HEIGHT - 1] = full_row
    locked[GRID_HEIGHT - 2] = list(shifted_row)

    score = clear_rows(locked, 0)

    assert score == SCORE_PER_LINE
    assert locked[GRID_HEIGHT - 1] == shifted_row


def test_check_lost_detects_block_in_top_row():
    # 最上段にブロックがあるとゲームオーバーになることを確認
    locked = empty_grid()
    assert check_lost(locked) is False

    locked[0][0] = (255, 255, 255)
    assert check_lost(locked) is True


def test_valid_space_allows_empty_and_rejects_collisions_or_bounds():
    # 空きマスでは配置可能、衝突・枠外は不可であることを確認
    locked = empty_grid()
    grid = create_grid(locked)
    mino = DummyMino(0, 0, O)

    assert valid_space(grid, mino) is True

    collision_pos = get_mino_positions(mino)[0]
    grid[collision_pos[1]][collision_pos[0]] = (255, 0, 0)
    assert valid_space(grid, mino) is False

    edge_mino = DummyMino(GRID_WIDTH - 2, 0, O)
    assert valid_space(create_grid(locked), edge_mino) is False


def test_lock_mino_marks_cells():
    # ミノ固定時に色が正しく書き込まれることを確認
    locked = empty_grid()
    mino = DummyMino(2, 1, O, color=(10, 20, 30))

    lock_mino(locked, mino)

    for x, y in get_mino_positions(mino):
        assert locked[y][x] == (10, 20, 30)


def test_create_grid_returns_deep_copy():
    # create_gridが深いコピーを返すことを確認
    locked = empty_grid()
    grid = create_grid(locked)

    grid[0][0] = (1, 1, 1)

    assert locked[0][0] == (0, 0, 0)


def test_keyOperation_left_key():
    """左キー: 正常な移動 + 左端での制限"""
    locked = empty_grid()
    grid = create_grid(locked)

    # 正常な移動: 左に移動できることを確認
    mino = DummyMino(5, 5, O)
    _, moved_mino = keyOperation(True, pygame.K_LEFT, grid, mino)
    assert moved_mino.x == 4

    # 左端制限: 左端では移動できないことを確認
    # Oミノは相対位置(2,1)から始まるので、x=-1が実質的な左端
    left_edge_mino = DummyMino(-1, 5, O)
    _, edge_mino = keyOperation(True, pygame.K_LEFT, grid, left_edge_mino)
    assert edge_mino.x == -1  # 移動できず、x=-1のまま


def test_keyOperation_right_key():
    """右キー: 正常な移動 + 右端での制限"""
    locked = empty_grid()
    grid = create_grid(locked)

    # 正常な移動: 右に移動できることを確認
    mino = DummyMino(3, 5, O)
    _, moved_mino = keyOperation(True, pygame.K_RIGHT, grid, mino)
    assert moved_mino.x == 4

    # 右端制限: 右端では移動できないことを確認
    # Oミノは相対位置(2,1)から(2,2)まで占有するので、x=GRID_WIDTH-2が実質的な右端
    right_edge_mino = DummyMino(GRID_WIDTH - 2, 5, O)
    _, edge_mino = keyOperation(True, pygame.K_RIGHT, grid, right_edge_mino)
    assert edge_mino.x == GRID_WIDTH - 2  # 移動できず、そのまま


def test_keyOperation_down_key():
    """下キー: 正常な移動 + 衝突時の制限"""
    locked = empty_grid()
    grid = create_grid(locked)

    # 正常な移動: 下に移動できることを確認
    mino = DummyMino(5, 5, O)
    _, moved_mino = keyOperation(True, pygame.K_DOWN, grid, mino)
    assert moved_mino.y == 6

    # 衝突時の制限: 下に障害物がある場合は移動できないことを確認
    # Oミノはx=5,y=5の時、実際には(6,7),(7,7),(6,8),(7,8)を占有
    # 下に移動すると(6,8),(7,8),(6,9),(7,9)を占有する
    # y=9の位置に障害物を配置して移動を防ぐ
    locked_with_obstacle = empty_grid()
    locked_with_obstacle[9][6] = (255, 0, 0)
    locked_with_obstacle[9][7] = (255, 0, 0)
    grid_with_obstacle = create_grid(locked_with_obstacle)

    blocked_mino = DummyMino(5, 5, O)
    _, result_mino = keyOperation(True, pygame.K_DOWN, grid_with_obstacle, blocked_mino)
    assert result_mino.y == 5  # 移動できず、y=5のまま


def test_keyOperation_rotation():
    """回転キー: 正常な回転 + 衝突時の復帰"""
    locked = empty_grid()
    grid = create_grid(locked)

    # 正常な回転: 回転できることを確認
    mino = DummyMino(5, 5, I, rotation=0)
    _, rotated_mino = keyOperation(True, pygame.K_UP, grid, mino)
    assert rotated_mino.rotation == 1

    # 衝突時の復帰: 回転が衝突する場合に元の回転へ戻ることを確認
    locked_with_obstacle = empty_grid()
    blocking_x, blocking_y = 4, 2
    locked_with_obstacle[blocking_y][blocking_x] = (255, 0, 0)
    grid_with_obstacle = create_grid(locked_with_obstacle)

    blocked_mino = DummyMino(3, 0, I, rotation=0)
    _, result_mino = keyOperation(True, pygame.K_UP, grid_with_obstacle, blocked_mino)
    assert result_mino.rotation == 0  # 回転できず、元の回転状態のまま


def test_keyOperation_hard_drop():
    """ハードドロップ: 最下部まで落下"""
    locked = empty_grid()
    grid = create_grid(locked)

    # ハードドロップの動作: 一番下まで落下することを確認
    drop_mino = DummyMino(0, 0, O)
    _, dropped = keyOperation(True, pygame.K_RSHIFT, grid, drop_mino)
    assert dropped.y == GRID_HEIGHT - 4  # Oミノは4マスの高さなので、GRID_HEIGHT-4が最下部
