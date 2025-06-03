import pygame
from utils.path_manager import *
from utils.setting_manager import load_settings_from_file

#bgm 출력
def play_bgm(bgm, is_bgm=True):
    music_path = get_resource_path("sounds", bgm)
    pygame.mixer.init()
    if is_bgm:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
    else:
        settings = load_settings_from_file()
        sound = pygame.mixer.Sound(music_path)
        volume = settings.get("sound_effect")
        sound.set_volume(0.1 * volume)
        sound.play()

#폰트 가져오기기
def get_font(font,size):
    font_path = get_resource_path('fonts', font)
    return pygame.font.Font(font_path, size)

def get_icon():
    icon_path = get_resource_path('images', 'logo.png')
    icon = pygame.image.load(icon_path)
    return icon