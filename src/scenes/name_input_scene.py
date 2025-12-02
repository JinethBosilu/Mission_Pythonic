"""Name input scene."""
import pygame
import pygame_gui
from ..game_state import GameScene


class NameInputScene:
    """Scene for entering player name."""
    
    def __init__(self, game):
        self.game = game
        self.name_input = None
        self.submit_button = None
    
    def setup(self):
        """Initialize the name input scene."""
        # Create name input field
        self.name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((312, 350), (400, 50)),
            manager=self.game.ui_manager
        )
        self.name_input.set_text_length_limit(20)
        
        # Create submit button
        self.submit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((362, 420), (300, 50)),
            text='BEGIN MISSION',
            manager=self.game.ui_manager
        )
    
    def handle_event(self, event):
        """Handle events for name input scene."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.submit_button:
                name = self.name_input.get_text().strip()
                if name:
                    self.game.game_state.player_name = name
                    self.game.change_scene(GameScene.LEVEL_SELECT)
        
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == self.name_input:
                name = self.name_input.get_text().strip()
                if name:
                    self.game.game_state.player_name = name
                    self.game.change_scene(GameScene.LEVEL_SELECT)
    
    def update(self, dt):
        """Update name input scene."""
        pass
    
    def draw(self, screen):
        """Draw name input scene."""
        # Draw prompt
        prompt_text = self.game.heading_font.render("ENTER HACKER CODENAME:", True, self.game.GREEN)
        prompt_rect = prompt_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 280))
        screen.blit(prompt_text, prompt_rect)
