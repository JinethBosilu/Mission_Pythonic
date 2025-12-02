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
        pass
    
    def draw(self, screen):
        """Draw level select scene."""
        # Draw header
        header_text = self.game.heading_font.render(
            f"SELECT MISSION - Agent: {self.game.game_state.player_name}", 
            True, 
            self.game.GREEN
        )
        header_rect = header_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 80))
        screen.blit(header_text, header_rect)
        
        # Draw progress
        total_levels = self.game.game_state.level_loader.get_level_count()
        completed = len(self.game.game_state.completed_levels)
        progress_text = self.game.text_font.render(
            f"Progress: {completed}/{total_levels} | Total Score: {self.game.game_state.total_score}", 
            True, 
            self.game.DARK_GREEN
        )
        progress_rect = progress_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 110))
        screen.blit(progress_text, progress_rect)
        
        # Draw progress bar
        bar_width = 400
        bar_height = 20
        bar_x = (self.game.SCREEN_WIDTH - bar_width) // 2
        bar_y = 130
        
        # Draw background
        pygame.draw.rect(screen, self.game.GRAY, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw progress fill
        fill_width = int((completed / total_levels) * bar_width) if total_levels > 0 else 0
        if fill_width > 0:
            pygame.draw.rect(screen, self.game.GREEN, (bar_x + 2, bar_y + 2, fill_width - 4, bar_height - 4))
