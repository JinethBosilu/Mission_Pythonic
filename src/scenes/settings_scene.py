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
        self.pulse_timer = 0
    
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
        self.pulse_timer += dt * 2
    
    def draw(self, screen):
        """Draw settings scene."""
        import math
        
        # Draw glowing pulsing title
        pulse = math.sin(self.pulse_timer)
        pulse_size = int(2 + pulse)
        self.game.draw_glow_text(
            screen,
            "SETTINGS",
            (self.game.SCREEN_WIDTH // 2, 150),
            self.game.heading_font,
            self.game.BRIGHT_GREEN,
            glow_size=pulse_size
        )
        
        # Draw border box around title
        box_width = 350
        box_height = 80
        box_x = (self.game.SCREEN_WIDTH - box_width) // 2
        box_y = 120
        pygame.draw.rect(screen, self.game.DARK_GREEN, (box_x, box_y, box_width, box_height), 2)
        pygame.draw.rect(screen, self.game.GREEN, (box_x + 3, box_y + 3, box_width - 6, box_height - 6), 1)
        
        # Draw corner brackets
        corner_size = 12
        corners = [
            (box_x, box_y),
            (box_x + box_width, box_y),
            (box_x, box_y + box_height),
            (box_x + box_width, box_y + box_height)
        ]
        for cx, cy in corners:
            if cx == box_x:
                pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx, cy), (cx + corner_size, cy), 2)
            else:
                pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx, cy), (cx - corner_size, cy), 2)
            
            if cy == box_y:
                pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx, cy), (cx, cy + corner_size), 2)
            else:
                pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx, cy), (cx, cy - corner_size), 2)
        
        # Draw info text
        info_text = self.game.text_font.render(
            "Configure game settings below",
            True,
            self.game.DARK_GREEN
        )
        info_rect = info_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 190))
        screen.blit(info_text, info_rect)
