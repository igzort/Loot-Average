import pygame
import config as cfg

class UICore:
    def __init__(self):
        # Настройка мобильных шрифтов
        font_size_small = max(13, int(cfg.WIDTH * 0.038))
        font_size_big = max(16, int(cfg.WIDTH * 0.052))
        self.font_small = pygame.font.SysFont("Courier", font_size_small, bold=True)
        self.font_big = pygame.font.SysFont("Courier", font_size_big, bold=True)
        
        w = cfg.WIDTH
        h = cfg.HEIGHT
        
        # Элементы главного экрана
        self.mob_img_rect = pygame.Rect(int(w * 0.30), int(h * 0.10), int(w * 0.40), int(w * 0.40))
        
        macro_y = int(h * 0.43)
        m_btn_w = int(w * 0.28)
        m_btn_h = int(h * 0.05)
        self.btn_macro1_rect = pygame.Rect(int(w * 0.05), macro_y, m_btn_w, m_btn_h)
        self.btn_macro2_rect = pygame.Rect(int(w * 0.36), macro_y, m_btn_w, m_btn_h)
        self.btn_macro3_rect = pygame.Rect(int(w * 0.67), macro_y, m_btn_w, m_btn_h)
        
        self.btn_clean_rect = pygame.Rect(int(w * 0.55), int(h * 0.50), int(w * 0.40), int(h * 0.045))
        self.btn_mobs_menu_rect = pygame.Rect(int(w * 0.05), int(h * 0.89), int(w * 0.90), int(h * 0.06))
        
        # Окно выбора мобов
        self.menu_mobs_bg = pygame.Rect(int(w * 0.05), int(h * 0.20), int(w * 0.90), int(h * 0.50))
        self.btn_close_mobs = pygame.Rect(int(w * 0.75), int(h * 0.21), int(w * 0.18), int(h * 0.04))
        self.row_wolf_rect = pygame.Rect(int(w * 0.08), int(h * 0.28), int(w * 0.55), int(h * 0.06))
        self.drop_wolf_rect = pygame.Rect(int(w * 0.66), int(h * 0.28), int(w * 0.25), int(h * 0.06))
        self.row_ww_rect = pygame.Rect(int(w * 0.08), int(h * 0.36), int(w * 0.55), int(h * 0.06))
        self.drop_ww_rect = pygame.Rect(int(w * 0.66), int(h * 0.36), int(w * 0.25), int(h * 0.06))
        
        # Окно Дроплиста
        self.menu_drop_bg = pygame.Rect(int(w * 0.10), int(h * 0.25), int(w * 0.80), int(h * 0.40))
        self.btn_close_drop = pygame.Rect(int(w * 0.72), int(h * 0.26), int(w * 0.16), int(h * 0.04))
