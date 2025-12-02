"""Level select scene."""
import pygame
import pygame_gui
from ..game_state import GameScene


class LevelSelectScene:
    """Scene for selecting levels."""
    
    def __init__(self, game):
        self.game = game
        self.level_buttons = []
    
    def setup(self):
        """Initialize the level select scene."""
        self.level_buttons = []
        
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
    
    def handle_event(self, event):
        """Handle events for level select scene."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for button in self.level_buttons:
                if event.ui_element == button:
                    self.game.game_state.current_level_id = button.level_id
                    self.game.game_state.user_code = ""
                    self.game.game_state.current_hint_index = 0
                    self.game.game_state.show_solution = False
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
        
        # Draw score
        score_text = self.game.text_font.render(
            f"Total Score: {self.game.game_state.total_score}", 
            True, 
            self.game.DARK_GREEN
        )
        score_rect = score_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 110))
        screen.blit(score_text, score_rect)
