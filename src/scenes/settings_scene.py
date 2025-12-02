"""Settings menu scene."""
import pygame
import pygame_gui
from ..game_state import GameScene


class SettingsScene:
    """Settings menu for game configuration."""
    
    def __init__(self, game):
        self.game = game
        self.fullscreen_button = None
        self.back_button = None
        self.is_fullscreen = False
        self.previous_scene = GameScene.TITLE
    
    def setup(self, previous_scene=GameScene.TITLE):
        """Initialize the settings scene."""
        self.previous_scene = previous_scene
        
        # Cleanup old elements
        if self.fullscreen_button is not None:
            self.fullscreen_button.kill()
        if self.back_button is not None:
            self.back_button.kill()
        
        # Button dimensions
        button_width = 350
        button_height = 50
        x = (self.game.SCREEN_WIDTH - button_width) // 2
        start_y = 250
        spacing = 20
        
        # Fullscreen toggle button
        fullscreen_text = "FULLSCREEN: ON" if self.is_fullscreen else "FULLSCREEN: OFF"
        self.fullscreen_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, start_y), (button_width, button_height)),
            text=fullscreen_text,
            manager=self.game.ui_manager
        )
        
        # Back button
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, start_y + 2 * (button_height + spacing)), (button_width, button_height)),
            text='BACK',
            manager=self.game.ui_manager
        )
    
    def handle_event(self, event):
        """Handle events for settings scene."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.fullscreen_button:
                # Toggle fullscreen
                self.is_fullscreen = not self.is_fullscreen
                if self.is_fullscreen:
                    self.game.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    self.fullscreen_button.set_text("FULLSCREEN: ON")
                else:
                    self.game.screen = pygame.display.set_mode(
                        (1280, 720),
                        pygame.RESIZABLE
                    )
                    self.fullscreen_button.set_text("FULLSCREEN: OFF")
                # Update dimensions
                self.game.SCREEN_WIDTH = self.game.screen.get_width()
                self.game.SCREEN_HEIGHT = self.game.screen.get_height()
                self.game.ui_manager.set_window_resolution((self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT))
            elif event.ui_element == self.back_button:
                self.game.change_scene(self.previous_scene)
    
    def update(self, dt):
        """Update settings scene."""
        pass
    
    def draw(self, screen):
        """Draw settings scene."""
        # Draw title
        title_text = self.game.heading_font.render("SETTINGS", True, self.game.GREEN)
        title_rect = title_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Draw info text
        info_text = self.game.text_font.render(
            "Configure game settings below",
            True,
            self.game.DARK_GREEN
        )
        info_rect = info_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 190))
        screen.blit(info_text, info_rect)
