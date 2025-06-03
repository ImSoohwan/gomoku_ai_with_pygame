import pygame, math
from utils.ui_functions import *
from utils.setting_manager import *
from utils.asset_manager import *


SIZE = WIDTH, HEIGHT = (720, 440)
background_color = (222, 184, 135)
# background_color = (255,255,255)
title_shadow_color = (209, 207, 207)
btn_width, btn_height = (150, 50)
btn_font_size = 20
bgm_playing = False
settings = None

#폰트
def gamluri_bold(size):
    return get_font("Galmuri11-Bold.ttf", size)


def draw_title(screen, frame):
    offset = math.sin(frame * 0.04) * 5
    #제목 그림자
    shadow_offset = (4,4)
    Title_font = gamluri_bold(int(HEIGHT/11))
    title_text = Title_font.render("Gomoku 에이아이!!", True, title_shadow_color)
    title_text_area = title_text.get_rect()
    title_text_area.center = (WIDTH/2+shadow_offset[0], HEIGHT*(1/4)+offset+shadow_offset[1])
    screen.blit(title_text, title_text_area)
    #제목 텍스트
    Title_font = gamluri_bold(int(HEIGHT/11))
    title_text = Title_font.render("Gomoku 에이아이!!", True, 'black')
    title_text_area = title_text.get_rect()
    title_text_area.center = (WIDTH/2, HEIGHT*(1/4)+offset)
    screen.blit(title_text, title_text_area)
    #by soohwan
    Title_font = gamluri_bold(int(HEIGHT/26))
    title_text = Title_font.render("by, soohwan", True, 'black')
    title_text_area = title_text.get_rect()
    title_text_area.center = (WIDTH* (4/5), HEIGHT*(1/4) + 50)
    screen.blit(title_text, title_text_area)


def main_screen(screen, frame, mouse_pressed, switch_screen_func):
    global settings
    if settings is None: update_settings()

    #bgm
    global bgm_playing
    if not bgm_playing:
        play_bgm("main_screen_bgm.mp3")
        bgm_playing = True
    
    if screen.get_size() != SIZE: pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Gomoku AI!!")
    screen_clear(screen, background_color)
    draw_title(screen, frame)
    player_vs_ai_btn = draw_button(screen, "Player vs AI", WIDTH*(1/6),HEIGHT*(2/3),btn_width,btn_height,gamluri_bold(btn_font_size),background_color, border_thickness=6,frame=frame, animation_speed=6, button_id="pl_vs_ai")
    ai_vs_ai_btn = draw_button(screen, "AI vs AI", WIDTH*(3/6),HEIGHT*(2/3),btn_width,btn_height,gamluri_bold(btn_font_size),background_color, border_thickness=6,frame=frame, animation_speed=6, button_id="ai_vs_ai")
    settings_btn = draw_button(screen, "Settings", WIDTH*(5/6),HEIGHT*(2/3),btn_width,btn_height,gamluri_bold(btn_font_size),background_color, border_thickness=6,frame=frame, animation_speed=6, button_id="settings")

    if player_vs_ai_btn:
        bgm_playing = False
        pygame.mixer.music.stop()
        play_bgm("butten_click.mp3", False)
        switch_screen_func("game")
    elif ai_vs_ai_btn:
        bgm_playing = False
        pygame.mixer.music.stop()
        play_bgm("butten_click.mp3", False)
        switch_screen_func("game-ai")
    elif settings_btn:
        settings = False
        play_bgm("butten_click.mp3", False)
        pygame.mixer.music.stop()
        switch_screen_func("settings")


    
