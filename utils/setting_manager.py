import pygame, os, subprocess, platform
from utils.path_manager import *

settings = None
DEFAULT_SETTINGS = {
    "sound_bgm": 5,
    "sound_effect": 5,
    "max_depth": 3,
    "search_range": 1,
    "attack_weight": 3,
    "defense_weight": 7,
}

DEFAULT_TEXT = [
    'sound_bgm = 5',
    'sound_effect = 5'
    'max_depth = 3',
    'search_range = 1',
]

#설정 불러오기
def load_settings_from_file():
    global settings
    if settings is None:
        path = get_resource_path(f"settings.txt")
        settings = {}
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue  # 빈 줄이나 주석 무시
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    # 숫자로 자동 변환
                    if value.isdigit():
                        value = int(value)
                    elif value.replace('.', '', 1).isdigit():
                        value = float(value)
                    settings[key] = value
    return settings

# 설정 업데이트
def update_settings():
    global settings
    settings = load_settings_from_file()

#설정 저장
def save_settings_to_file(settings: dict, filename="settings"):
    path = get_resource_path(f"{filename}.txt")
    with open(path, "w", encoding="utf-8") as file:
        for key, value in settings.items():
            file.write(f"{key} = {value}\n")

#설정 초기화
def init_settings():
    global settings
    save_settings_to_file(DEFAULT_SETTINGS)
    settings = None
    update_settings()
    pygame.mixer.music.set_volume(0.5)

# 설정 가져오기
def get_settings_by_id(id):
    global settings
    if settings is None: settings = load_settings_from_file()
    return settings.get(id, 0)
def get_all_settings():
    global settings
    return settings

####################평가 점수 관련#######################
DEFALUT_SCORES = {
    # 기본 연속 패턴 점수 (단일 발견 시)
    "4_in_a_row_2_open": 100000,     # 즉시 승리 가능
    "4_in_a_row_1_open": 1000,
    "3_in_a_row_2_open": 500,
    "3_in_a_row_1_open": 50,
    "2_in_a_row_2_open": 10,
    "2_in_a_row_1_open": 1,

    # 복합 패턴 보너스 (중복 조건 발견 시 추가 점수)
    "bonus_3x2open_double": 20000,        # 삼삼
    "bonus_3x2open_4x1open": 10000,       # 삼삼 + 막힌 사
    "bonus_4x1open_double": 100000,         # 막힌 사 두 개
}


score_settings=None
#설정 불러오기
def load_scores_from_file():
    global score_settings
    if score_settings is None:
        path = get_resource_path(f"pattern_scores.txt")
        score_settings = {}
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue  # 빈 줄이나 주석 무시
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    # 숫자로 자동 변환
                    if value.isdigit():
                        value = int(value)
                    elif value.replace('.', '', 1).isdigit():
                        value = float(value)
                    score_settings[key] = value

    return score_settings

def update_score_settings():
    global score_settings
    score_settings = None

def get_score_settings():
    global score_settings
    if score_settings is None: score_settings = load_scores_from_file()
    return score_settings

def reset_score_settings():
    save_settings_to_file(DEFALUT_SCORES, "pattern_scores")

def open_txt_file(filename):
    # 파일이 없으면 생성
    with open(filename, 'a'):
        pass
    system_name = platform.system()

    if system_name == "Windows":
        subprocess.Popen(["notepad", filename])
    elif system_name == "Darwin":  # macOS
        subprocess.Popen(["open", filename])
