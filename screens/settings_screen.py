import pygame
from utils.ui_functions import *
from utils.setting_manager import *
from utils.asset_manager import *

SIZE = WIDTH, HEIGHT = (720, 440)
LINE_HEIGHT = 40
MARGIN_TOP = 70
MARGIN_LEFT = 30
MARGIN_BOTTOM = 30
background_color = (222, 184, 135)
click_times = {}
bgm_playing = False
PATH = "settings.txt"


SETTING_LIMITS = {
    "sound_bgm": (0,10),
    "sound_effect": (0,10),
    "max_depth": (2, 5),
    "search_range": (1, 3),
    "attack_weight": (1, 9),
    "defense_weight": (1,9),
}

setting_btns = []

# 세팅 버튼 리스트 추가가
def append_setting_btn(id, buttens):
    global setting_btns
    setting_btns.append({
        "id": id,
        "btn" : buttens,
    })


#설정 출력
def draw_settings_line(screen, col, line, text, id, only_text = False):
    global click_times
    width = MARGIN_LEFT if col == 1 else WIDTH/2 + MARGIN_LEFT
    height = MARGIN_TOP + line * LINE_HEIGHT
    if only_text:
        draw_text(screen, text, width, height, get_font("Galmuri11-Bold.ttf", 16), True)
        return
    #텍스트 출력
    draw_text(screen, text, width, height, get_font("Galmuri.ttf", 17), True)
    # - 버튼 출력
    btn_pos_width_minus = WIDTH/2 - 70 if col == 1 else WIDTH - 70
    btn_pos_height = height + 10
    minus_btn, click_times = draw_button(screen, "-", btn_pos_width_minus, btn_pos_height, 15, 15, font=get_font("Galmuri.ttf", 15), color_bg=background_color, border_thickness=2, click_delay_ms=150, button_id=id, last_click_time_dict=click_times)
    # + 버튼 출력
    btn_pos_width_plus = btn_pos_width_minus + 50
    plus_btn, click_times = draw_button(screen, "+", btn_pos_width_plus, btn_pos_height, 15, 15, font=get_font("Galmuri.ttf", 15), color_bg=background_color, border_thickness=2, click_delay_ms=150, button_id=id, last_click_time_dict=click_times)
    # 값 출력
    value_text_pos_width = (btn_pos_width_plus + btn_pos_width_minus) / 2 - 5
    draw_text(screen, f"{get_settings_by_id(id)}", value_text_pos_width, height, get_font("Galmuri11-Bold.ttf", 17), True)

    return [plus_btn, minus_btn]

# bgm 소리 업데이트
def update_bgm_sound():
    volume = get_settings_by_id("sound_bgm")
    pygame.mixer.music.set_volume(0.1 * volume)

def settings_screen(screen, mouse_pressed, switch_screen_func):
    global click_times, bgm_playing
    #bgm
    if not bgm_playing:
        play_bgm("main_screen_bgm.mp3")
        bgm_playing = True

    if screen.get_size() != SIZE: pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Settings")
    screen_clear(screen, background_color)

    #홈으로 돌아가기 버튼
    restart_btn = draw_button(screen, "메인으로", 45, 25, 70, 30, get_font("Galmuri11-Bold.ttf", 15), (222, 184, 135), color_border=(0,0,0))
    if restart_btn:
        bgm_playing = False
        play_bgm("butten_click.mp3", False)
        switch_screen_func("main")
        update_settings()

    #설정 초기화 버튼
    reset_btn, click_times = draw_button(screen, "초기화", 720-45, 25, 70, 30, get_font("Galmuri11-Bold.ttf", 16), (222, 184, 135), color_border=(0,0,0), click_delay_ms=300, button_id="setting_reset", last_click_time_dict=click_times)
    if reset_btn:
        init_settings()
        play_bgm("butten_click.mp3", False)
        return

    #가운데 구분선
    pygame.draw.line(screen, (189, 161, 125), (WIDTH/2, MARGIN_TOP-10), (WIDTH/2, HEIGHT-MARGIN_BOTTOM), 1)

    #점수 설정 안내 텍스트
    draw_text(screen, "휴리스틱 함수 패턴 평가 점수 설정", MARGIN_LEFT, HEIGHT-150, get_font("Galmuri11-Bold.ttf", 16))
    draw_text(screen, "*점수 설정은 '설정 적용'을 눌러야 게임에 적용됩니다", MARGIN_LEFT, HEIGHT-45, get_font("Galmuri.ttf", 13))
    draw_text(screen, "*비정상적인 점수 입력시 게임이 강제종료될 수 있습니다.", MARGIN_LEFT, HEIGHT-25, get_font("Galmuri.ttf", 13))

    #점수 설정 버튼
    open_txt_file_btn, click_times = draw_button(screen, "oepn pattern_settings.txt", MARGIN_LEFT+140, HEIGHT-100, 280, 25, get_font("Galmuri11-Bold.ttf", 13), (222, 184, 135), color_border=(0,0,0), click_delay_ms=300, button_id="open_txt_file_btn", last_click_time_dict=click_times)
    if open_txt_file_btn:
        play_bgm("butten_click.mp3", False)
        open_txt_file("pattern_scores.txt")
    score_update_btn, click_times = draw_button(screen, "설정 적용", MARGIN_LEFT+35, HEIGHT-65, 70, 25, get_font("Galmuri11-Bold.ttf", 13), (222, 184, 135), color_border=(0,0,0), click_delay_ms=300, button_id="score_update_btn", last_click_time_dict=click_times)
    if score_update_btn:
        play_bgm("butten_click.mp3", False)
        update_score_settings()
    score_reset_btn, click_times = draw_button(screen, "점수 초기화", MARGIN_LEFT+130, HEIGHT-65, 100, 25, get_font("Galmuri11-Bold.ttf", 13), (222, 184, 135), color_border=(0,0,0), click_delay_ms=300, button_id="score_reset_btn", last_click_time_dict=click_times)
    if score_reset_btn:
        play_bgm("butten_click.mp3", False)
        reset_score_settings()

    #설정 출력
    global setting_btns
    setting_btns = []
    draw_settings_line(screen, 1, 0, "소리 설정", id="sound_setting_text", only_text=True)
    append_setting_btn("sound_bgm", draw_settings_line(screen, 1, 1, "배경음악 음량", id="sound_bgm"))
    append_setting_btn("sound_effect", draw_settings_line(screen, 1, 2, "효과음 음량", id = "sound_effect"))

    draw_settings_line(screen, 2, 0, "AI 설정", id="ai_setting_text", only_text=True)
    append_setting_btn("max_depth", draw_settings_line(screen, 2, 1, "탐색 깊이 제한", id = "max_depth")) 
    append_setting_btn("search_range", draw_settings_line(screen, 2, 2, "탐색 범위 (칸)", id="search_range")) 
    append_setting_btn("attack_weight", draw_settings_line(screen, 2, 3, "AI공격성 - 낮은(1)~높은(9)", id="attack_weight"))
    append_setting_btn("defense_weight", draw_settings_line(screen, 2, 4, "AI수비성 - 낮은(1)~높은(9)", id="defense_weight")) 

    for setting_btn in setting_btns:
        id = setting_btn["id"]
        btns = setting_btn["btn"]
        current_settings = get_all_settings()
        if id in current_settings:
            if btns[0]:
                if current_settings[id] < SETTING_LIMITS[id][1]:
                    current_settings[id] += 1
                    save_settings_to_file(current_settings)
                    play_bgm("butten_click.mp3", False)
                    update_bgm_sound()
            elif btns[1]:
                if current_settings[id] > SETTING_LIMITS[id][0]:
                    current_settings[id] -= 1
                    save_settings_to_file(current_settings)
                    play_bgm("butten_click.mp3", False)
                    update_bgm_sound()



