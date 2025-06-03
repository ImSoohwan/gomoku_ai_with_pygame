from minimax import get_optimal_move
from game_functions import *
import os

def clear():
    os.system('cls')
    os.system('clear')

def get_int_input(num_range = None):
    while(True):
        try:
            num = int(input(">>> "))
            if num_range is not None:
                min, max = num_range
                if num >= min and num <= max:
                    return num
                else:
                    raise ValueError
            return num
        except:
            print("[*] 올바른 숫자를 입력하세요.")
            continue

def end_game(winner, board):
    print("=======================================")
    if winner == "Draw": print("무승부 입니다!!!!!")
    else: print(f"Winner is {winner}!!!")
    print()
    print_board(board)
    print()
    print("다시 게임을 플레이 하시겠습니까?")
    print("1: 다시 플레이,  2: 게임 종료")
    print("=======================================")
    
    choice = get_int_input(num_range=(1,2))
    if choice == 1: select_mode()
    else: SystemExit()
    
def print_board_console(board):
    print("=======================================")
    print_board(board, number=True,)
    print("=======================================")

def print_error_message():
    clear()
    print("========================================================")
    print("[*] 올바른 형식의 좌표를 입력해주세요.")
    print("[*] 좌표는 '2 4' 과 같이 가로열과 세로열이 공백으로 구분된 형태여야 하며")
    print("[*] 현재 돌을 두는 것이 가능한 위치여야 합니다.")
    print("========================================================")
    print("Press any key to continue...")
    input()


def player_vs_ai(size):
    alphabet_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    board = create_board(size)
    aiMove = [0, (0,0)]
    while(True):
        clear()
        print(f"AI의 이전 수: {aiMove[1][0], alphabet_list[aiMove[1][1]]}")
        
        winner = check_winner(board)
        if winner is not None:
            end_game(winner, board)
            break
        elif is_full(board):
            end_game("Draw", board)
            break

        print_board_console(board)
        try:
            playerInput = input('좌표를 입력하세요: ').strip().split()
            if len(playerInput) != 2: raise KeyError
            newBoard = apply_move(board, playerInput, 'O')
        except:
            print_error_message()
            continue

        if newBoard == False:
            print_error_message()
            continue

        board = newBoard
        aiMove= get_optimal_move(board, 'X', 'O', True, 1, 3)
        board = apply_move(board, aiMove[1], 'X')

def input_ai_first_move(size):
    clear()
    board = create_board(size)
    while(True):
        print_board_console(board)
        try:
            playerInput = tuple(map(int,input('AI첫번째 수의 좌표를 입력하세요: ').strip().split()))
            newBoard = apply_move(board, playerInput, 'O')
            if newBoard != False:
                break
            else:
                raise KeyError
        except:
            print_error_message()
            continue
    return newBoard

def ai_vs_ai(size):
    board = input_ai_first_move(size)
    current_ai = "X"
    opponent_ai = "O"
    while(True):
        clear()
        print("ai vs ai 진행중...")
        winner = check_winner(board)
        if winner is not None:
            end_game(winner, board)
            break
        elif is_full(board):
            end_game("Draw", board)
            break

        print_board_console(board)

        aiMove= get_optimal_move(board, current_ai, opponent_ai, True, 1, 3)
        board = apply_move(board, aiMove[1], current_ai)

        temp = current_ai
        current_ai = opponent_ai
        opponent_ai = temp


def select_mode():
    clear()
    print("=======================================")
    print("오모쿠 AI에 오신것을 환영합니다!")
    print("본 게임은 player vs ai 와 ai vs ai 모드를 지원합니다.")
    print("메뉴를 보고 원하는 모드의 숫자를 입력해주세요!")
    print("1. player vs ai")
    print("2. ai vs ai")
    print("=======================================")
    choice = get_int_input((1, 2))
    if choice == 1:
        player_vs_ai(15)
    elif choice == 2:
        ai_vs_ai(15)

#게임 시작
if __name__ == "__main__":
    select_mode()