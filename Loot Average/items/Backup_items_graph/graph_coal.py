import pygame
import os

def get_texture(size):
    # Путь к файлу картинки
    path = os.path.join("assets", "items", "coal.png")
    
    # 1. Загружаем реальную картинку
    img = pygame.image.load(path).convert_alpha()
    
    # 2. Сжимаем до 16х16 (это создаст пиксельный эффект)
    pixel_img = pygame.transform.scale(img, (16, 16))
    
    # 3. Растягиваем до размера ячейки инвентаря
    return pygame.transform.scale(pixel_img, (size, size))
