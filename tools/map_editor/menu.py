import pygame
from pygame.surfarray import map_array
import pygame_gui
import tkinter as tk
from tkinter.filedialog import askopenfile
import json

class Menu:
    def __init__(self, screen_width, screen_height, margin_left, window_height, map_data):
        self.manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')

        self.buildFromSize(screen_width, screen_height, margin_left, window_height, map_data)

    def update(self, screen, tick_time, margin_left, window_height):
        self.manager.update(tick_time/1000.0)
        self.manager.draw_ui(screen)

        pygame.display.flip()

    def procesEvents(self, event):
        self.manager.process_events(event)

    def buildFromSize(self, screen_width, screen_height, margin_left, window_height, map_data):
        with open("theme.json", "r") as f:
            theme = json.load(f)

        theme["label"]["font"]["size"] = str(int(margin_left * 0.05))
        theme["button"]["font"]["size"] = str(int(margin_left * 0.04))
        theme["map_data"]["font"]["size"] = str(int(margin_left * 0.07))

        with open("theme.json", "w") as f:
            json.dump(theme, f, indent=4)

        self.manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')
        orig = margin_left * 0.05
        width = margin_left * 0.90

        elem_height = window_height * 0.05

        self.map_name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((orig, orig), (width, elem_height)),
            text=map_data["map_name"],
            manager=self.manager,
        )

        self.map_max_players = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((orig, orig + elem_height), (width, elem_height)),
            text="Max players : " + str(map_data["max_players"]),
            manager=self.manager,
            object_id="map_data"
        )

        self.map_gamemode = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((orig, orig + 2 * elem_height), (width, elem_height)),
            text="Gamemode : " + map_data["gamemode"],
            manager=self.manager,
            object_id="map_data"
        )

        self.file_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((orig, orig + 3 * elem_height), (width, elem_height)),
            text='Load a map',
            manager=self.manager,
        )
    
        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((orig, orig + 4 * elem_height), (width, elem_height)),
            text='Save current map',
            manager=self.manager,
        )

        self.map_name_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((orig, orig + 5 * elem_height), (width, elem_height)),
            text='Change map name',
            manager=self.manager,
        )

        self.player_count_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((orig, orig + 6 * elem_height), (width, elem_height)),
            text='Change max players',
            manager=self.manager,
        )

        self.toggle_spawn_mode_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((orig, orig + 7 * elem_height), (width, elem_height)),
            text='Toggle spawn mode',
            manager=self.manager,
        )

    def askForMap(self):
        root = tk.Tk()
        root.withdraw()
        map_path = askopenfile(mode="r", initialdir="./maps", title="Select a map file", filetypes=[('JSON map file', '*.json')])
        
        if map_path != None:
            return map_path.name
        else:
            return None

    def askForText(self, window_title, prompt_text, text_return, text_return_lock):
        self.popup = tk.Tk()
        self.popup.wm_title(window_title)
        self.popup.geometry("340x150")
        self.entries = {}

        self.entries["text_label"] = tk.Label(self.popup, text=prompt_text)
        self.entries["text_var"] = tk.StringVar(self.popup)
        self.entries["text_entry"] = tk.Entry(self.popup, width = 40, textvariable = self.entries["text_var"])

        self.entries["text_label"].grid(column=0, row=0, padx=5)
        self.entries["text_entry"].grid(column=0, row=1, padx=5)

        confirm = tk.Button(self.popup, text="Confirm", command = self.textReturn)
        confirm.grid(column=0, row=2, pady=(5,5))

        self.popup.mainloop()

        text_return_lock.acquire()
        text_return[0] = self.entries["text_var"].get()
        text_return[1] = self.entries["text_var"].get()
        text_return_lock.release()

    def textReturn(self):
        self.popup.destroy()