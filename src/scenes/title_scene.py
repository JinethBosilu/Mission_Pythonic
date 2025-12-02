"""Title screen scene."""
import pygame
import pygame_gui
from ..game_state import GameScene


class TitleScene:
    """Title screen with 'Press Start' prompt."""
    
    def __init__(self, game):
        self.game = game
        self.start_button = None
        self.blink_timer = 0
        self.show_text = True
    
    def setup(self):
        """Initialize the title scene."""
        # Cleanup old elements
        if self.start_button is not None:
            self.start_button.kill()
        
        # Create start button (centered and responsive)
        button_width = 300
        button_height = 60
        x = (self.game.SCREEN_WIDTH - button_width) // 2
        y = self.game.SCREEN_HEIGHT // 2
        
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, y), (button_width, button_height)),
            text='[PRESS START]',
            manager=self.game.ui_manager
        )
    
    def handle_event(self, event):
        """Handle events for title scene."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                # Check if there's a saved game
                if self.game.game_state.save_system.has_save():
                    # Load saved game
                    self.game.game_state.load_saved_game()
                    self.game.change_scene(GameScene.LEVEL_SELECT)
                else:
                    # New game - ask for name
                    self.game.change_scene(GameScene.NAME_INPUT)
    
    def update(self, dt):
        """Update title scene."""
        # Blinking effect for title
        self.blink_timer += dt
        if self.blink_timer >= 0.5:
            self.blink_timer = 0
            self.show_text = not self.show_text
    
    def draw(self, screen):
        """Draw title scene."""
        # Draw title
        if self.show_text:
            title_text = self.game.title_font.render("MISSION: PYTHONIC", True, self.game.GREEN)
            title_rect = title_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 200))
            screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.game.text_font.render("Hacker Training Protocol", True, self.game.DARK_GREEN)
        subtitle_rect = subtitle_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 270))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Draw Matrix rain effect (simple version)
        self._draw_matrix_rain(screen)
    
    def _draw_matrix_rain(self, screen):
        """Draw a simple Matrix rain effect in the background."""
        # Simplified - just draw some random characters
        import random
        chars = "01"
        for x in range(0, self.game.SCREEN_WIDTH, 20):
            for y in range(0, self.game.SCREEN_HEIGHT, 40):
                if random.random() < 0.1:
                    char = random.choice(chars)
                    char_surface = self.game.text_font.render(char, True, self.game.DARK_GREEN)
                    screen.blit(char_surface, (x, y))
