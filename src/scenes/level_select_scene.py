"""Level select scene."""
import pygame
import pygame_gui
from ..game_state import GameScene


class LevelSelectScene:
    """Scene for selecting levels."""
    
    def __init__(self, game):
        self.game = game
        self.level_buttons = []
        self.back_button = None
        self.quit_button = None
        self.hover_pulse = 0
        self.progress_pulse = 0
    
    def setup(self):
        """Initialize the level select scene."""
        # Cleanup old buttons
        for button in self.level_buttons:
            button.kill()
        self.level_buttons = []
        
        if self.back_button is not None:
            self.back_button.kill()
        if self.quit_button is not None:
            self.quit_button.kill()
        
        # Create level buttons in a grid
        levels = self.game.game_state.get_all_levels()
        
        cols = 5
        rows = (len(levels) + cols - 1) // cols
        
        button_width = 150
        button_height = 80
        spacing = 20
        start_x = (self.game.SCREEN_WIDTH - (cols * (button_width + spacing))) // 2
        start_y = 150
        
        for i, level in enumerate(levels):
            row = i // cols
            col = i % cols
            
            x = start_x + col * (button_width + spacing)
            y = start_y + row * (button_height + spacing)
            
            # Check if level is completed
            is_completed = self.game.game_state.is_level_completed(level.id)
            
            # Create button
            button_text = f"Level {i+1}"
            if is_completed:
                button_text += " [DONE]"
            
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((x, y), (button_width, button_height)),
                text=button_text,
                manager=self.game.ui_manager
            )
            button.level_id = level.id
            self.level_buttons.append(button)
        
        # Add back and quit buttons at the bottom
        button_width_bottom = 200
        button_height_bottom = 50
        spacing_bottom = 20
        bottom_y = self.game.SCREEN_HEIGHT - 100
        
        # Calculate positions for centered buttons
        total_width = (button_width_bottom * 2) + spacing_bottom
        start_x = (self.game.SCREEN_WIDTH - total_width) // 2
        
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((start_x, bottom_y), (button_width_bottom, button_height_bottom)),
            text='<< BACK TO MENU',
            manager=self.game.ui_manager
        )
        
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((start_x + button_width_bottom + spacing_bottom, bottom_y), (button_width_bottom, button_height_bottom)),
            text='QUIT GAME',
            manager=self.game.ui_manager
        )
    
    def handle_event(self, event):
        """Handle events for level select scene."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                self.game.change_scene(GameScene.TITLE)
            elif event.ui_element == self.quit_button:
                self.game.running = False
            else:
                for button in self.level_buttons:
                    if event.ui_element == button:
                        self.game.game_state.current_level_id = button.level_id
                        self.game.game_state.user_code = ""
                        self.game.game_state.current_hint_index = 0
                        self.game.game_state.show_solution = False
                        self.game.game_state.reset_attempts()
                        self.game.change_scene(GameScene.GAMEPLAY)
                        break
    
    def update(self, dt):
        """Update level select scene."""
        self.hover_pulse += dt * 3
        self.progress_pulse += dt * 2
    
    def draw(self, screen):
        """Draw level select scene."""
        import math
        
        # Draw glowing header
        header_x = self.game.SCREEN_WIDTH // 2
        self.game.draw_glow_text(
            screen,
            f"SELECT MISSION - Agent: {self.game.game_state.player_name}",
            (header_x, 80),
            self.game.heading_font,
            self.game.BRIGHT_GREEN,
            glow_size=2
        )
        
        # Draw progress with glow
        total_levels = self.game.game_state.level_loader.get_level_count()
        completed = len(self.game.game_state.completed_levels)
        self.game.draw_glow_text(
            screen,
            f"Progress: {completed}/{total_levels} | Total Score: {self.game.game_state.total_score}",
            (self.game.SCREEN_WIDTH // 2, 110),
            self.game.text_font,
            self.game.GREEN,
            glow_size=1
        )
        
        # Draw enhanced progress bar
        bar_width = 400
        bar_height = 20
        bar_x = (self.game.SCREEN_WIDTH - bar_width) // 2
        bar_y = 130
        
        # Draw outer glow
        glow_alpha = int(50 + 20 * math.sin(self.progress_pulse))
        glow_surface = pygame.Surface((bar_width + 10, bar_height + 10))
        glow_surface.set_alpha(glow_alpha)
        glow_surface.fill(self.game.DARK_GREEN)
        screen.blit(glow_surface, (bar_x - 5, bar_y - 5))
        
        # Draw double border
        pygame.draw.rect(screen, self.game.DARK_GREEN, (bar_x, bar_y, bar_width, bar_height), 2)
        pygame.draw.rect(screen, self.game.GREEN, (bar_x + 2, bar_y + 2, bar_width - 4, bar_height - 4), 1)
        
        # Draw progress fill with pulse
        fill_width = int((completed / total_levels) * (bar_width - 8)) if total_levels > 0 else 0
        if fill_width > 0:
            # Pulsing fill
            pulse_brightness = int(200 + 55 * math.sin(self.progress_pulse))
            fill_color = (0, pulse_brightness, 0)
            pygame.draw.rect(screen, fill_color, (bar_x + 4, bar_y + 4, fill_width, bar_height - 8))
            
            # Draw corner accents on progress bar
            corner_size = 5
            pygame.draw.line(screen, self.game.BRIGHT_GREEN, (bar_x, bar_y), (bar_x + corner_size, bar_y), 2)
            pygame.draw.line(screen, self.game.BRIGHT_GREEN, (bar_x, bar_y), (bar_x, bar_y + corner_size), 2)
            pygame.draw.line(screen, self.game.BRIGHT_GREEN, (bar_x + bar_width, bar_y), (bar_x + bar_width - corner_size, bar_y), 2)
            pygame.draw.line(screen, self.game.BRIGHT_GREEN, (bar_x + bar_width, bar_y), (bar_x + bar_width, bar_y + corner_size), 2)
