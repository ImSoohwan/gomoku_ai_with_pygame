import pygame, math, threading, copy
from game_functions import create_board, apply_move, check_winner, is_full
from minimax import get_optimal_move
from utils.setting_manager import *
from utils.asset_manager import *
from utils.ui_functions import *


SIZE = WIDTH, HEIGHT = (525, 560)
GRID_SIZE = 15
CELL_SIZE = 33
MARGIN = 30
SCREEN_SIZE = GRID_SIZE * CELL_SIZE + MARGIN * 2
STONE_RADIUS = 14
current_player = "O"
board = create_board(15)
ai_last_move = None
ai_first_move = False
ai_move_result = None
ai_thinking = None
bgm_playing = False
is_error = False
need_wait = True

# 색상 정의
COLOR_BG = (240, 220, 180)
COLOR_GRID = (0, 0, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255,255,255)

def start_ai_thread(board, current, opponent):
    settings = load_settings_from_file()
    global ai_move_result, ai_thinking
    ai_thinking = True

    def worker():
        global ai_move_result, ai_thinking, current_player
        ai_move_result = get_optimal_move(board, current, opponent, True, 1, max_depth=settings.get("max_depth", 3), search_range=settings.get("search_range", 1))
        # current_player = "O" if current_player == "X" else "X"
        # ai_thinking = False

    threading.Thread(target=worker, daemon=True).start()

def init_board():
    global board, current_player, ai_first_move, ai_thinking, ai_move_result, is_error
    board = create_board(15)
    current_player = "O"
    ai_first_move = False
    ai_thinking = False
    ai_move_result = None
    is_error = False

def draw_grid(screen):
    for i in range(GRID_SIZE):
        pygame.draw.line(
            screen, COLOR_GRID,
            (MARGIN, MARGIN + i * CELL_SIZE),
            (SCREEN_SIZE - MARGIN - CELL_SIZE, MARGIN + i * CELL_SIZE), 1)
        pygame.draw.line(
            screen, COLOR_GRID,
            (MARGIN + i * CELL_SIZE, MARGIN),
            (MARGIN + i * CELL_SIZE, SCREEN_SIZE - MARGIN - CELL_SIZE), 1)

def draw_stones(screen):
    global board
    global ai_last_move
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] != " ":
                center = (MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE)
                color = COLOR_BLACK if board[y][x] == 'O' else COLOR_WHITE
                pygame.draw.circle(
                    screen,
                    color,
                    center,
                    STONE_RADIUS)
                if ai_last_move == (y, x):
                    font = get_font("Galmuri11-Bold.ttf", 10)
                    text_surface = font.render("L", True, 'black' if board[y][x] == "X" else 'white')
                    text_rect = text_surface.get_rect(center=center)
                    screen.blit(text_surface, text_rect)

def player_vs_ai(frame, screen, mouse_pos, mouse_clicked, just_switched_screen, switch_screen_func):
    pygame.display.set_caption("Player vs AI")
    global is_error, current_player, board, ai_last_move, ai_thinking, ai_move_result, bgm_playing
    if just_switched_screen: init_board()

    # 1. 이벤트 처리 (마우스 클릭으로 돌 놓기)
    winner = check_winner(board)
    if is_error:
        draw_text(screen, "알 수 없는 오류 발생...", WIDTH/2, 530, get_font("Galmuri11-Bold.ttf", 20), center=True)
    elif is_full(board):
        draw_text(screen, "무승부..!!", WIDTH/2, 530, get_font("Galmuri11-Bold.ttf", 20), center=True)
    elif winner is None:
        if ai_move_result is not None:
            newBoard = apply_move(board, ai_move_result[1], 'X')
            if newBoard is not False:
                board = newBoard
                ai_last_move = ai_move_result[1]
                current_player = "O"
                ai_thinking = False
                ai_move_result = None
                play_bgm("stone.mp3", False)
            else:
                print(f"[Error Log] {ai_move_result} {ai_thinking}")
                is_error = True #먼가 이부분에 심각한 문제가 있음==================

        if not just_switched_screen:
            offset = abs(int(math.sin(frame * 0.04) * 6))
            ai_text = "AI가 고민중" + ("." * offset)
            draw_text(screen, "나의 차례!" if current_player == "O" else ai_text, WIDTH/2, 530, get_font("Galmuri11-Bold.ttf", 20), center=True)
            if mouse_clicked:
                if current_player == "O" and ai_move_result is None:
                    mx, my = mouse_pos
                    gx = round((mx - MARGIN) / CELL_SIZE)
                    gy = round((my - MARGIN) / CELL_SIZE)
                    if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
                        newBoard = apply_move(board, (gy, gx), current_player)
                        if newBoard != False:
                            board = newBoard
                            play_bgm("stone.mp3", False)
                            current_player = 'O' if current_player == 'X' else 'X'
                elif current_player == "X" and not ai_thinking:
                    newBoard = copy.deepcopy(board)
                    start_ai_thread(newBoard, 'X', 'O')
    else:
        winner_text = "Player 승리!! 대단해요!" if winner == "O" else "AI 승리!!"
        draw_text(screen, winner_text, WIDTH/2, 530, get_font("Galmuri11-Bold.ttf", 20), center=True)
        

    # 2. 격자 그리기
    draw_grid(screen)
    # 3. 돌 그리기
    draw_stones(screen)
    # 4. 홈버튼 그리기기
    restart_btn = draw_button(screen, "메인으로", 465, 530, 70, 30, get_font("Galmuri11-Bold.ttf", 15), (222, 184, 135), color_border=(0,0,0))
    if restart_btn:
        init_board()
        pygame.mixer.music.stop()
        bgm_playing = False
        switch_screen_func("main")

def ai_vs_ai(frame, screen, mouse_pos, mouse_clicked, just_switched_screen, switch_screen_func):
    global is_error,ai_last_move, ai_first_move, board, current_player, ai_move_result, ai_first_move, bgm_playing, ai_thinking
    pygame.display.set_caption("AI vs AI")
    draw_grid(screen)
    draw_stones(screen)

    if ai_first_move is False:
        draw_text(screen, "AI 첫 수의 위치를 클릭해주세요", WIDTH/2, 530, get_font("Galmuri11-Bold.ttf", 20), center=True)
        if not just_switched_screen:
            if mouse_clicked:
                mx, my = mouse_pos
                gx = round((mx - MARGIN) / CELL_SIZE)
                gy = round((my - MARGIN) / CELL_SIZE)
                if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
                    newBoard = apply_move(board, (gy, gx), current_player)
                    if newBoard != False:
                        board = newBoard
                        current_player = "X"
                        ai_last_move = (gy, gx)
                        ai_first_move = True
                        play_bgm("stone.mp3", False)
    else:
        winner = check_winner(board)
        if is_error:
            draw_text(screen, "알 수 없는 오류 발생...", WIDTH/2, 530, get_font("Galmuri11-Bold.ttf", 20), center=True)
        elif is_full(board):
            draw_text(screen, "무승부..!!", WIDTH/2, 530, get_font("Galmuri11-Bold.ttf", 20), center=True)
        elif winner is None:
            offset = abs(int(math.sin(frame * 0.04) * 6))
            ai_text = "AI vs AI 진행중" + ("." * offset)
            draw_text(screen, ai_text, WIDTH/2, 530, get_font("Galmuri11-Bold.ttf", 20), center=True)

            if ai_move_result is not None:
                newBoard = apply_move(board, ai_move_result[1], current_player)
                if newBoard is not False:
                    board = newBoard
                    ai_last_move = ai_move_result[1]
                    ai_move_result = None
                    current_player = "O" if current_player == "X" else "X"
                    ai_thinking = False
                    play_bgm("stone.mp3", False)
                else:
                    print(f"[Error Log] {ai_move_result} {ai_thinking}")
                    is_error = True #이부분에도 심각한 문제==================

            if not ai_thinking:
                newBoard = copy.deepcopy(board)
                start_ai_thread(newBoard, current_player, 'O' if current_player == 'X' else 'X')
        else:
            winner_text = "흑" if winner == "O" else "백"
            draw_text(screen, f"[{winner_text}] 승!!", WIDTH/2, 530, get_font("Galmuri11-Bold.ttf", 20), center=True)

    #홈버튼 그리기기
    restart_btn = draw_button(screen, "메인으로", 465, 530, 70, 30, get_font("Galmuri11-Bold.ttf", 15), (222, 184, 135), color_border=(0,0,0))
    if restart_btn:
        init_board()
        pygame.mixer.music.stop()
        bgm_playing = False
        switch_screen_func("main")



def game_screen(frame, game_mode, screen, mouse_pos, mouse_clicked, just_switched_screen, switch_screen_func):
    #bgm
    global bgm_playing
    if not bgm_playing:
        play_bgm("game_screen_bgm.mp3")
        init_board()
        bgm_playing = True

    screen_clear(screen, (222, 184, 135))
    if screen.get_size() != SIZE: pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    
    if game_mode == "player_vs_ai":
        player_vs_ai(frame, screen, mouse_pos=mouse_pos, mouse_clicked=mouse_clicked, just_switched_screen=just_switched_screen, switch_screen_func=switch_screen_func)
    else:
        ai_vs_ai(frame, screen, mouse_pos=mouse_pos, mouse_clicked=mouse_clicked, just_switched_screen=just_switched_screen, switch_screen_func=switch_screen_func)