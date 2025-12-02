"""Pause menu scene - overlay during gameplay."""
import pygame
import pygame_gui
from ..game_state import GameScene


class PauseScene:
    """Pause menu overlay with semi-transparent background."""
    
    def __init__(self, game):
        self.game = game
        self.resume_button = None
        self.restart_button = None
        self.settings_button = None
        self.menu_button = None
        self.quit_button = None
        self.overlay_surface = None
        self.pulse_timer = 0
        self.scan_line_y = 0
    
    def setup(self):
        """Initialize the pause scene."""
        # Cleanup old elements
        if self.resume_button is not None:
            self.resume_button.kill()
        if self.restart_button is not None:
            self.restart_button.kill()
        if self.settings_button is not None:
            self.settings_button.kill()
        if self.menu_button is not None:
            self.menu_button.kill()
        if self.quit_button is not None:
            self.quit_button.kill()
        
        # Create semi-transparent overlay
        self.overlay_surface = pygame.Surface((self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT))
        self.overlay_surface.set_alpha(200)
        self.overlay_surface.fill((0, 0, 0))
        
        # Button dimensions
        button_width = 300
        button_height = 50
        spacing = 20
        x = (self.game.SCREEN_WIDTH - button_width) // 2
        start_y = self.game.SCREEN_HEIGHT // 2 - 150
        
        # Create buttons
        self.resume_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, start_y), (button_width, button_height)),
            text='[RESUME]',
            manager=self.game.ui_manager
        )
        
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, start_y + (button_height + spacing)), (button_width, button_height)),
            text='RESTART LEVEL',
            manager=self.game.ui_manager
        )
        
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, start_y + 2 * (button_height + spacing)), (button_width, button_height)),
            text='SETTINGS',
            manager=self.game.ui_manager
        )
        
        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, start_y + 3 * (button_height + spacing)), (button_width, button_height)),
            text='BACK TO MENU',
            manager=self.game.ui_manager
        )
        
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, start_y + 4 * (button_height + spacing)), (button_width, button_height)),
            text='QUIT GAME',
            manager=self.game.ui_manager
        )
    
    def handle_event(self, event):
        """Handle events for pause scene."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Resume game
                self.game.game_state.resume_timer()
                self.game.change_scene(GameScene.GAMEPLAY)
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.resume_button:
                self.game.game_state.resume_timer()
                self.game.change_scene(GameScene.GAMEPLAY)
            elif event.ui_element == self.restart_button:
                # Restart current level
                level = self.game.game_state.get_current_level()
                if level:
                    self.game.game_state.user_code = level.starter_code
                    self.game.game_state.current_hint_index = 0
                    self.game.game_state.show_solution = False
                    self.game.game_state.start_level_timer()
                self.game.change_scene(GameScene.GAMEPLAY)
            elif event.ui_element == self.settings_button:
                self.game.change_scene(GameScene.SETTINGS)
            elif event.ui_element == self.menu_button:
                self.game.game_state.stop_timer()
                self.game.change_scene(GameScene.LEVEL_SELECT)
            elif event.ui_element == self.quit_button:
                self.game.running = False
    
    def update(self, dt):
        """Update pause scene."""
        self.pulse_timer += dt * 2
        self.scan_line_y += 300 * dt
        if self.scan_line_y > self.game.SCREEN_HEIGHT:
            self.scan_line_y = 0
    
    def draw(self, screen):
        """Draw pause scene."""
        import math
        
        # Draw semi-transparent overlay
        screen.blit(self.overlay_surface, (0, 0))
        
        # Draw scan line effect
        if int(self.scan_line_y) % 4 == 0:
            pygame.draw.line(screen, self.game.DARK_GREEN, (0, int(self.scan_line_y)), (self.game.SCREEN_WIDTH, int(self.scan_line_y)), 2)
        
        # Draw glowing pulsing PAUSED title
        pulse = math.sin(self.pulse_timer)
        pulse_size = int(2 + pulse)
        self.game.draw_glow_text(
            screen,
            "PAUSED",
            (self.game.SCREEN_WIDTH // 2, 150),
            self.game.title_font,
            self.game.BRIGHT_GREEN,
            glow_size=pulse_size
        )
        
        # Draw border box around title
        box_width = 400
        box_height = 100
        box_x = (self.game.SCREEN_WIDTH - box_width) // 2
        box_y = 120
        pygame.draw.rect(screen, self.game.DARK_GREEN, (box_x, box_y, box_width, box_height), 2)
        pygame.draw.rect(screen, self.game.GREEN, (box_x + 3, box_y + 3, box_width - 6, box_height - 6), 1)
        
        # Draw corner brackets
        corner_size = 15
        corners = [
            (box_x, box_y),
            (box_x + box_width, box_y),
            (box_x, box_y + box_height),
            (box_x + box_width, box_y + box_height)
        ]
        for cx, cy in corners:
            # Horizontal lines
            if cx == box_x:
                pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx, cy), (cx + corner_size, cy), 2)
            else:
                pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx, cy), (cx - corner_size, cy), 2)
            
            # Vertical lines
            if cy == box_y:
                pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx, cy), (cx, cy + corner_size), 2)
            else:
                pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx, cy), (cx, cy - corner_size), 2)
        
        # Draw instructions with glow
        self.game.draw_glow_text(
            screen,
            "Press ESC to resume",
            (self.game.SCREEN_WIDTH // 2, 200),
            self.game.text_font,
            self.game.GREEN,
            glow_size=1
        )
