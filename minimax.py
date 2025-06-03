from game_functions import *
from utils.setting_manager import *
from utils.asset_manager import *

def any_stone_nearby(board, px, py, search_range=1):
    size = len(board)
    for i in range(px-search_range, px+search_range+1):
        for j in range(py-search_range, py+search_range+1):
            if (not is_valid_move(board, (i, j))) and (not is_out_of_board(board, (i, j))):
                return True
    return False

def get_possible_moves(board, search_range=1):
    size = len(board)
    possible_moves = []
    for px in range(size):
        for py in range(size):
            if any_stone_nearby(board, px, py, search_range) and is_valid_move(board, (px, py)):
                possible_moves.append((px, py))
    return possible_moves


def is_n_in_a_row(board, player, pos, dir, n):
    """
    해당 좌표부터 특정 방향으로 총 n개의 돌이 연속으로 놓여져 있는지 확인

    매개변수:
        board: 현재 보드 상태
        player: 검사할 돌의 종류
        pos: 검사 시작 좌표
        dir: 검사 방향
        n: 검사 개수
    
    반환값:
        True if n개의 돌이 연속되어 놓여져 있으면 else False
    """
    x_dir, y_dir = dir
    px, py = pos
    for i in range(n):
        x_pos, y_pos = (px + i*x_dir, py + i*y_dir)
        if not is_out_of_board(board, (x_pos, y_pos)):
            stone = board[x_pos][y_pos]
            if stone != player:
                return False
        else:
            return False
    return True


def check_both_ends(board, pos, dir, n):
    """
    찾은 연속된 돌 행렬의 양 끝이 열려 있는지 확인

    반환값:
        양 쪽 모두가 열려있으면 2, 하나만 열려있으면 1, 전부 막혀있으면 0 반환환
    """
    px, py = pos
    count = 0
    before_start_pos = (px - dir[0], py - dir[1])
    after_end_pos = (px + dir[0] * n, py + dir[1] * n)
    if is_valid_move(board, before_start_pos):
        count += 1
    if is_valid_move(board, after_end_pos):
        count += 1
    return count


def stones_in_a_row(board, player, num, exception):
    """
    n개의 돌이 연속으로 있는지 검사하는 함수

    매개변수:
        board: 현재 보드 상태
        player: 검사할 돌의 종류
        num: 연속된 몇개의 돌을 검사할 것인지
        exception: 검사에서 제외할 (시작좌표, 방향) 튜플플
    
    반환값:
        다음 튜플의 리스트
        tuple: 연속된 돌을 찾았는지, 열린 방향 수 (0~2)

    """
    directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]
    size = len(board)
    found_rows = []
    for px in range(size):
        for py in range(size):
            if board[px][py] == player:
                for dir in directions:
                    if ((px, py), dir) in exception: continue
                    if(is_n_in_a_row(board, player, (px,py), dir, num)):
                        both_ends = check_both_ends(board, (px, py), dir, num)
                        new_exceptions = set()
                        for i in range(num):
                            new_exceptions.add(((px+dir[0]*i, py+dir[1]*i), dir))
                        found_rows.append((True, both_ends, new_exceptions))
    return found_rows

def evaluate_board(board, ai):
    pattern_score = get_score_settings()
    score = 0
    exception = set()
    pattern_counter = [[0 for j in range(6)] for i in range(6)]
    for num in [4,3,2]:
        found_rows = stones_in_a_row(board, ai, num, exception)
        for found in found_rows:
            _, opens, new_exceptions = found
            exception = exception.union(new_exceptions)
            if opens == 2 or opens == 1:
                score += pattern_score.get(f"{num}_in_a_row_{opens}_open", 0)
                pattern_counter[num][opens] += 1
    
    #보너스 점수 계산
    if pattern_counter[3][2] >= 2: 
        score += pattern_score.get("bonus_3x2open_double", 0) #삼삼
    if pattern_counter[3][2] >= 1 and pattern_counter[4][1] >= 1: 
        score += pattern_score.get("bonus_3x2open_4x1open", 0) #삼삼 + 막힌 사
    if pattern_counter[4][1] >= 2: 
        score += pattern_score.get("bonus_4x1open_double", 0) #막힌 사 두 개
    
    return score

def calculate_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distence = ((x2-x1)**2 + (y2-y1)**2)**(1/2)
    return distence

def sort_by_previous_move(possible_moves, previous_move):
    distance = []
    for move in possible_moves:
        distance.append(calculate_distance(move, previous_move))
    possible_moves_sorted = [x for x, _ in sorted(zip(possible_moves, distance), key=lambda pair: pair[1], reverse=False)]
    return possible_moves_sorted

def get_optimal_move(board, ai, opponent, isMaximizing, current_depth, max_depth=3, search_range = 1, alpha = float("-inf"), beta = float("inf"), previous_move=None):
    winner = check_winner(board)
    if winner is not None: return 10000000 if winner == ai else -10000000
    elif current_depth >= max_depth:
        attack_weight = 1 + (get_settings_by_id("attack_weight") - 5) * 0.15
        defense_weight = 1 + (get_settings_by_id("defense_weight") - 5) * 0.15
        return attack_weight * evaluate_board(board, ai) - defense_weight * evaluate_board(board, opponent)

    possible_moves = get_possible_moves(board, search_range=search_range)
    if previous_move is not None: possible_moves = sort_by_previous_move(possible_moves, previous_move)

    score = float("-inf") if isMaximizing else float("inf")
    optimal_move = None 
    for move in possible_moves:
        newboard = apply_move(board, move, ai if isMaximizing else opponent)
        if not newboard: continue

        newScore = get_optimal_move(newboard, ai, opponent, not isMaximizing, current_depth+1, max_depth, search_range, alpha, beta, move)

        #알파 베타 값 설정
        if isMaximizing: alpha = max(alpha, newScore)
        else: beta = min(beta, newScore)

        if (isMaximizing and newScore > score) or (not isMaximizing and newScore < score):
            score = newScore
            optimal_move = move
        
        #가지치기
        if alpha >= beta: break

    if current_depth == 1:
        return (score, optimal_move)
    return score

    





