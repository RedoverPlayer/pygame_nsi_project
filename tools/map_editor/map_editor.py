import json
import pygame
from pygame import mouse
from pygame.locals import (MOUSEWHEEL, QUIT)
import tkinter as tk
import pygame_gui
import threading

import map
import menu

# INFO
# To use the map editor, place tha map (named map1.json) into this folder and start this program. To add a tile, click left, to remove a tile (place terrain) click right.
# To pick the type of the tile the mouse cursor is in, click on the mouse wheel. To change tool, scroll.

# ---- Config ----

window_size = (1120, 840) # Note that the window should be preferably divisible by 60 in height to fit the size of the map and that you can resize the window once opened.
frames_per_second = 144

# ----------------

def loadMap(map_path):
    with open(map_path, "r") as f:
        map_data = json.load(f)
    current_map = map.Map(map_path, min(window_size) // 60, 60, SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.display.set_caption("NSI project - Map Editor - Editing " + map_data["map_name"])
    
    width, height = pygame.display.get_surface().get_size()
    margin_left = width // 4
    window_height = height

    current_map.tile_size = height // 60
    for tile in current_map.tiles:
        tile.changeSize(height // 60)

    return map_data, current_map

def saveMap(current_map, map_data, map_path):
    print("Saving map...")
    spawn_points = []
    map_list = [[0 for _ in range(60)] for _ in range(60)]
    x = 0
    y = 0
    for tile in current_map.tiles:
        if tile.is_spawn:
            spawn_points.append((x, y))
        map_list[y][x] = map.Map.tile_to_id[tile.type]
        x += 1
        if x > 59:
            x = 0
            y += 1
        if y >= 60:
            break

    map_data["spawn_points"] = spawn_points
    map_data["tiles"] = map_list

    with open(map_path, "w") as f:
        f.write(json.dumps(map_data))

    print("Saved")

SCREEN_WIDTH = window_size[0]
SCREEN_HEIGHT = window_size[1]

pygame.init()
pygame.font.init()

# window title
pygame.display.set_caption("NSI project - Map Editor")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
screen.fill((50, 50, 50))

# loading map
map_path = "./maps/map1.json"
map_data, current_map = loadMap("./maps/map1.json")

running = True

clock = pygame.time.Clock()

tools = ["wall", "water", "bush", "cactus", "barrel", "crate"]
tool = 0
margin_left = window_size[0] // 4
window_height = window_size[1]
main_menu = menu.Menu(SCREEN_WIDTH, SCREEN_HEIGHT, margin_left, window_height, map_data)

width, height = window_size

text_return = [""]
text_return_lock = threading.Lock()

spawn_mode = [False]

# main loop
while running:
    tick_time = clock.tick(frames_per_second)

    if spawn_mode[0]:
        tool = "spawn"
    mouse_button_pos = None

    text_return_lock.acquire()
    if text_return[0] != "":
        map_data["map_name"] = text_return[0]
        text_return[0] = ""
        pygame.display.set_caption("NSI project - Map Editor - Editing " + map_data["map_name"])
        main_menu.buildFromSize(width, height, margin_left, window_height, map_data)
    text_return_lock.release()

    for event in pygame.event.get():
        main_menu.procesEvents(event)
                    
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == main_menu.file_button:
                    map_path = main_menu.askForMap()

                    if map_path != None:
                        map_data, current_map = loadMap(map_path)
                        print(map_data["map_name"])
                        main_menu.buildFromSize(width, height, margin_left, window_height, map_data)

                elif event.ui_element == main_menu.save_button:
                    saveMap(current_map, map_data, map_path)
                
                elif event.ui_element == main_menu.map_name_button:
                    thread_1 = threading.Thread(target=main_menu.askForText, args=["Change map name", "Enter the new name", text_return, text_return_lock])
                    thread_1.start()

                elif event.ui_element == main_menu.toggle_spawn_mode_button:
                    spawn_mode[0] = not spawn_mode[0]
                    if spawn_mode[0] == False:
                        tool = 0

        if event.type == pygame.VIDEORESIZE:
            width, height = pygame.display.get_surface().get_size()
            margin_left = width // 4
            window_height = height
            
            current_map.tile_size = height // 60
            for tile in current_map.tiles:
                tile.changeSize(height // 60)

            screen.fill((50, 50, 50))

            main_menu.buildFromSize(width, height, margin_left, window_height, map_data)

        elif event.type == QUIT:
            running = False

        elif event.type == MOUSEWHEEL and not spawn_mode[0]:
            if event.y == -1:
                if tool == 0:
                    tool = len(tools) - 1
                else:
                    tool -= 1
            elif event.y == 1:
                if tool == len(tools) - 1:
                    tool = 0
                else:
                    tool += 1

    # render menu
    main_menu.update(screen, tick_time, margin_left, window_height)

    # adding map tiles to the screen
    if not spawn_mode[0]:
        tiles_rendered = [elem for elem in current_map.update(screen, pygame.mouse.get_pos(), tools[tool], pygame.mouse.get_pressed(), margin_left, spawn_mode) if elem != None]
    else:
        tiles_rendered = [elem for elem in current_map.update(screen, pygame.mouse.get_pos(), "spawn", pygame.mouse.get_pressed(), margin_left, spawn_mode) if elem != None]
    if len(tiles_rendered) > 0:
        if tiles_rendered[0] != "terrain":
            tool = tools.index(tiles_rendered[0])

    # render elements to the screen
    pygame.display.flip()