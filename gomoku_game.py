import pygame
import os
from screens.main_screen import main_screen
from screens.game_screen import game_screen
from screens.settings_screen import settings_screen
from utils.setting_manager import *
from game_functions import *
from utils.asset_manager import *

SIZE = WIDTH, HEIGHT = (720, 540)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#셋업
pygame.init()
pygame.display.set_icon(get_icon())
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("GOMOKU AI   by.soohwan")
clock = pygame.time.Clock()
running = True
current_screen = "init"
just_switched_screen = False
frame = 0
mouse_pressed = False


#스크린 변경
def switch_screen(screen):
    global current_screen
    global just_switched_screen
    current_screen = screen
    if screen == "game" or screen == "game-ai":
        just_switched_screen = True



while running:
    mouse_pos = pygame.mouse.get_pos()

    if current_screen == "init":
        update_bgm_sound()
        current_screen = "main"
    elif current_screen == "main":
        main_screen(screen=screen, frame=frame, mouse_pressed=mouse_pressed, switch_screen_func=switch_screen)
    elif current_screen == "game":
        game_screen(frame, "player_vs_ai", screen, mouse_pos=mouse_pos, mouse_clicked=mouse_pressed, just_switched_screen=just_switched_screen, switch_screen_func=switch_screen)
    elif current_screen == "game-ai":
        game_screen(frame, "ai_vs_ai", screen, mouse_pos=mouse_pos, mouse_clicked=mouse_pressed, just_switched_screen=just_switched_screen, switch_screen_func=switch_screen)
    elif current_screen == "settings":
        settings_screen(screen, mouse_pressed=mouse_pressed, switch_screen_func=switch_screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 1 = 왼쪽 버튼
                if just_switched_screen:
                    just_switched_screen = False
                else:
                    mouse_pressed = True
            else:
                mouse_pressed = False
        else:
            mouse_pressed = False    
                    
    pygame.display.flip()

    frame += 1
    clock.tick(60)

pygame.quit()
