import pygame, math

def screen_clear(screen, color = (255,255,255)):
    screen.fill(color)

def draw_button(screen, text, x, y, width, height, font,
                            color_bg=(200, 200, 200), color_text=(0, 0, 0),
                            color_border=(50, 50, 50), border_thickness=4,
                            border_radius=5, frame=None, animation_speed = 5,
                            click_delay_ms=0, last_click_time_dict=None, 
                            button_id="default",):
    """버튼을 그리면서, 클릭되었는지 여부를 리턴한다."""
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    now = pygame.time.get_ticks()

    # 클릭 가능 여부 체크 (버튼별로 딜레이 따로 적용)
    if last_click_time_dict is None:
        last_click_time_dict = {}
        
    last_time = last_click_time_dict.get(button_id)
    if last_time is None:
        can_click = True
    else:
        can_click = now - last_time >= click_delay_ms

    #애니메이션
    if frame is not None:
        offset = offset = math.sin(frame * 0.01 * animation_speed) * 4
        width = width + offset
        height = height + offset
    
    # 버튼 사각형
    rect = pygame.Rect(x-width/2, y-height/2, width, height)

    # 테두리
    rect_outer = pygame.Rect(x-(width+border_thickness)/2, y-(height+border_thickness)/2, width+border_thickness, height+border_thickness)
    pygame.draw.rect(screen, color_border, rect_outer, border_radius=border_radius)

    # 마우스가 버튼 위에 있는가?
    hovered = rect.collidepoint(mouse_pos)

    # 클릭 여부 판단
    clicked = False
    if hovered and click[0]:
        if can_click:
            clicked = True
            last_click_time_dict[button_id] = now

    # 배경 색상 변경 (호버 시 약간 어둡게)
    color_final = tuple(c - 20 if hovered else c for c in color_bg)

    # 버튼 배경
    pygame.draw.rect(screen, color_final, rect, border_radius=border_radius)

    # 텍스트
    text_surface = font.render(text, True, color_text)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    if click_delay_ms == 0:
        return clicked
    else:
        return clicked, last_click_time_dict


def draw_text(surface, text, x, y, font, color=(0, 0, 0), center=False):
    """지정한 위치에 텍스트를 그리는 함수.
    
    - surface: 텍스트를 그릴 대상 (예: screen)
    - text: 표시할 문자열
    - x, y: 위치 (center=True이면 중심 좌표, 아니면 왼쪽 상단)
    - font: pygame.font.Font 객체
    - color: 텍스트 색상
    - center: 중심 정렬 여부
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)

    surface.blit(text_surface, text_rect)
