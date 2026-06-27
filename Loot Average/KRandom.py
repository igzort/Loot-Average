# KRandom.py
import sys
import pygame
import config as cfg
from logic import GameLogic
from renderer import GameRenderer

def main():
    pygame.init()
    # Принудительно заставляем Android растянуть 450х800 на весь экран смартфона
    screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT), pygame.FULLSCREEN | pygame.SCALED)

    pygame.display.set_caption("L2 Korean Random Mobile")
    clock = pygame.time.Clock()

    logic = GameLogic()
    renderer = GameRenderer(screen)

    running = True
    while running:
        logic.update_macros()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # 1. Клики по окну дропа
                    if logic.show_droplist_for is not None:
                        if renderer.btn_close_drop.collidepoint(mouse_pos):
                            logic.show_droplist_for = None
                        continue 
                        
                    # 2. Клики по меню мобов
                    if logic.show_mobs_menu:
                        if renderer.btn_close_mobs.collidepoint(mouse_pos):
                            logic.show_mobs_menu = False
                        elif renderer.row_wolf_rect.collidepoint(mouse_pos):
                            logic.change_mob("Wolf")
                        elif renderer.row_ww_rect.collidepoint(mouse_pos):
                            logic.change_mob("Werewolf")
                        elif hasattr(renderer, 'row_orc_rect') and renderer.row_orc_rect.collidepoint(mouse_pos):
                            logic.change_mob("Orc Grunt")
                            
                        elif renderer.drop_wolf_rect.collidepoint(mouse_pos):
                            logic.show_droplist_for = "Wolf"
                        elif renderer.drop_ww_rect.collidepoint(mouse_pos):
                            logic.show_droplist_for = "Werewolf"
                        elif hasattr(renderer, 'drop_orc_rect') and renderer.drop_orc_rect.collidepoint(mouse_pos):
                            logic.show_droplist_for = "Orc Grunt"
                        continue 
                        
                      # 3. Клики по инвентарю (Скроллбар и очистка)
                    if renderer.inv_renderer.scrollbar_rect.collidepoint(mouse_pos):
                        renderer.inv_renderer.handle_scroll_click(mouse_pos)
                        continue
                    elif renderer.inv_renderer.btn_clean_mini.collidepoint(mouse_pos):
                        logic.clean_inventory()
                        continue

                    # 4. Основной игровой экран
                    if renderer.btn_mobs_menu_rect.collidepoint(mouse_pos):
                        logic.show_mobs_menu = True
                    elif renderer.btn_macro1_rect.collidepoint(mouse_pos):
                        logic.toggle_macro(1)
                    elif renderer.btn_macro2_rect.collidepoint(mouse_pos):
                        logic.toggle_macro(2)
                    elif renderer.btn_macro3_rect.collidepoint(mouse_pos):
                        logic.toggle_macro(3)
                    elif renderer.mob_img_rect.collidepoint(mouse_pos):
                        logic.hit_mob()
                    # 4. Основной игровой экран
                    if hasattr(renderer, 'btn_change_time_rect') and renderer.btn_change_time_rect.collidepoint(mouse_pos):
                        logic.toggle_time_per_kill()
                    elif renderer.btn_mobs_menu_rect.collidepoint(mouse_pos):
                        logic.show_mobs_menu = True


        renderer.draw(logic)
        pygame.display.flip()
        clock.tick(cfg.FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
