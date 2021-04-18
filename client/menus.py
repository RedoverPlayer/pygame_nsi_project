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

class Menu:
    def __init__(self, screen_width, screen_height):
        self.manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')
        self.clock = pygame.time.Clock()

        self.screen_width = screen_width
        self.screen_height = screen_height

    def centerX(self, elem_width):
        return self.screen_width // 2 - elem_width // 2
    
    def centerY(self, elem_height):
        return self.screen_height // 2 - elem_height // 2

class ConnectionMenu(Menu):
    def __init__(self, screen_width, screen_height):
        Menu.__init__(self, screen_width, screen_height)

        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.centerX(screen_width // 1.2), self.centerY(screen_height // 15)), (screen_width // 1.2, screen_height // 15)),
            text='Connecting to the server',
            manager=self.manager,
            object_id="title"
        )

    def run(self, screen, fps, ui_status):
        running = True
        while running:
            time_delta = self.clock.tick(fps)/1000.0
            screen.fill((50, 50, 50))

            if ui_status[0] == "connecting":
                self.title.set_text("Connecting to the server")
            elif ui_status[0] == "connection_failed":
                self.title.set_text("Connection failed, retrying in 5 seconds")
            elif ui_status[0] not in ("connecting", "connection_failed"):
                running = False

            for event in pygame.event.get():
                self.manager.process_events(event)

                if event.type == pygame.locals.QUIT:
                    running = False
                    ui_status[0] == "quit"
            
            self.manager.update(time_delta)
            self.manager.draw_ui(screen)

            pygame.display.flip()

class MainMenu(Menu):
    def __init__(self, screen_width, screen_height):
        Menu.__init__(self, screen_width, screen_height)
        
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.centerX(screen_width // 1.1), screen_height // 60), (screen_width // 1.1, screen_height // 15)),
            text='Jeu en cours de développement nom sujet à modification',
            manager=self.manager,
            object_id="title"
        )

        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.centerX(screen_width // 6), screen_height - screen_height // 11), (screen_width // 6, screen_height // 15)),
            text='PLAY',
            manager=self.manager,
            object_id="play_button"
        )

    def run(self, screen, fps, ui_status, events, event_lock):
        running = True
        while running:
            time_delta = self.clock.tick(fps)/1000.0
            screen.fill((50, 50, 50))

            for event in pygame.event.get():
                self.manager.process_events(event)
                    
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.play_button:
                            ui_status[0] = "searching_game"
                            running = False

                if event.type == pygame.locals.QUIT:
                    running = False
                    ui_status[0] = "quit"
            
            self.manager.update(time_delta)
            self.manager.draw_ui(screen)

            pygame.display.flip()

class SearchMenu(Menu):
    def __init__(self, screen_width, screen_height):
        Menu.__init__(self, screen_width, screen_height)

        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.centerX(screen_width // 1.2), self.centerY(screen_height // 15)), (screen_width // 1.2, screen_height // 15)),
            text='Searching for a game',
            manager=self.manager,
            object_id="title"
        )

    def run(self, screen, fps, ui_status, events, event_lock, tcp_sock):
        tcp_sock.send('{"type": "game_search", "gamemode": "showdown"}'.encode())

        running = True
        while running:
            time_delta = self.clock.tick(fps)/1000.0
            screen.fill((50, 50, 50))

            event_lock.acquire()
            for event in events:
                if event["type"] == "search_update":
                    self.title.set_text(f"Searching for a game ({event['player_count']}/2)")
                
                elif event["type"] == "search_finished":
                    self.title.set_text(f"Launching game")
                    ui_status[0] = "showdown_game"
                    running = False

            events.clear()
            event_lock.release()

            for event in pygame.event.get():
                self.manager.process_events(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        ui_status[0] = "main_menu"
                        tcp_sock.send('{"type": "stop_search", "gamemode": "showdown"}'.encode())

                elif event.type == pygame.locals.QUIT:
                    running = False
                    ui_status[0] == "quit"
            
            self.manager.update(time_delta)
            self.manager.draw_ui(screen)

            pygame.display.flip()

class EndScreen(Menu):
    def __init__(self, screen_width, screen_height):
        Menu.__init__(self, screen_width, screen_height)

        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.centerX(screen_width // 1.2), self.centerY(screen_height // 15)), (screen_width // 1.2, screen_height // 15)),
            text='Game finished',
            manager=self.manager,
            object_id="title"
        )

    def run(self, screen, fps, ui_status, events, event_lock, tcp_sock):
        tcp_sock.send('{"type": "game_search", "gamemode": "showdown"}'.encode())

        running = True
        while running:
            time_delta = self.clock.tick(fps)/1000.0
            screen.fill((50, 50, 50))

            event_lock.acquire()
            for event in events:
                if event["type"] == "search_update":
                    self.title.set_text(f"Searching for a game ({event['player_count']}/2)")
                
                elif event["type"] == "search_finished":
                    self.title.set_text(f"Launching game")
                    ui_status[0] = "showdown_game"
                    running = False

            events.clear()
            event_lock.release()

            for event in pygame.event.get():
                self.manager.process_events(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        ui_status[0] = "main_menu"

                elif event.type == pygame.locals.QUIT:
                    running = False
                    ui_status[0] == "quit"
            
            self.manager.update(time_delta)
            self.manager.draw_ui(screen)

            pygame.display.flip()