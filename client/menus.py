import pygame
import pygame_gui
import json

def updateThemeJson(screen_width, screen_height):
    with open("theme.json", "r") as f:
        theme = json.loads(f.read())
    
    theme["label"]["font"]["size"] = str(screen_width // 80)
    theme["title"]["font"]["size"] = str(screen_width // 60)
    theme["play_button"]["font"]["size"] = str(screen_width // 48)
    theme["play_button_text"]["font"]["size"] = str(screen_width // 48)

    with open("theme.json", "w") as f:
        f.write(json.dumps(theme, indent=4))

def mainMenu(screen_width, screen_height, manager):
    def centerX(elem_width, w=screen_width):
        return w // 2 - elem_width // 2

    def centerY(elem_height, h=screen_height):
        return h // 2 - elem_height // 2

    title = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((centerX(screen_width // 1.1), screen_height // 60), (screen_width // 1.1, screen_height // 15)),
        text='Jeu en cours de développement nom sujet à modification',
        manager=manager,
        object_id="title"
    )

    play_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((centerX(screen_width // 6), screen_height - screen_height // 11), (screen_width // 6, screen_height // 15)),
        text='',
        manager=manager,
        object_id="play_button"
    )

    play_button_text = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((centerX(screen_width // 6), screen_height - screen_height // 11), (screen_width // 6, screen_height // 15)),
        text='PLAY',
        manager=manager,
        object_id="play_button_text"
    )

    return title, play_button