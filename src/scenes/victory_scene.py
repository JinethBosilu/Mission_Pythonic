"""Victory scene shown when all levels are complete."""
import pygame
import pygame_gui
from ..game_state import GameScene


class VictoryScene:
    """Victory screen shown when all levels are completed."""
    
    def __init__(self, game):
        self.game = game
        self.menu_button = None
    
    def setup(self):
        """Initialize the victory scene."""
        # Cleanup old elements
        if self.menu_button is not None:
            self.menu_button.kill()
        
        # Create menu button (centered)
        button_width = 300
        button_height = 60
        x = (self.game.SCREEN_WIDTH - button_width) // 2
        y = self.game.SCREEN_HEIGHT - 150
        
        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, y), (button_width, button_height)),
            text='RETURN TO MENU',
            manager=self.game.ui_manager
        )
    
    def handle_event(self, event):
        """Handle events for victory scene."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.menu_button:
                self.game.change_scene(GameScene.LEVEL_SELECT)
    
    def update(self, dt):
        """Update victory scene."""
        pass
    
    def draw(self, screen):
        """Draw victory scene."""
        # Draw congratulations message
        congrats_text = self.game.title_font.render("MISSION COMPLETE!", True, self.game.GREEN)
        congrats_rect = congrats_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 200))
        screen.blit(congrats_text, congrats_rect)
        
        # Draw player name
        name_text = self.game.heading_font.render(
            f"Agent {self.game.game_state.player_name}", 
            True, 
            self.game.BRIGHT_GREEN
        )
        name_rect = name_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 280))
        screen.blit(name_text, name_rect)
        
        # Draw final score
        score_text = self.game.heading_font.render(
            f"Final Score: {self.game.game_state.total_score}", 
            True, 
            self.game.GREEN
        )
        score_rect = score_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 340))
        screen.blit(score_text, score_rect)
        
        # Draw success message
        success_lines = [
            "You have successfully completed all Python hacking missions.",
            "Your skills are now at expert level.",
            "The Matrix awaits your next adventure..."
        ]
        
        y = 400
        for line in success_lines:
            line_text = self.game.text_font.render(line, True, self.game.DARK_GREEN)
            line_rect = line_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, y))
            screen.blit(line_text, line_rect)
            y += 30
