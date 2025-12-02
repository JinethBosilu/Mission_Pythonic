"""Title screen scene."""
import pygame
import pygame_gui
from ..game_state import GameScene


class TitleScene:
    """Title screen with 'Press Start' prompt."""
    
    def __init__(self, game):
        self.game = game
        self.continue_button = None
        self.new_game_button = None
        self.settings_button = None
        self.quit_button = None
        self.blink_timer = 0
        self.show_text = True
    
    def setup(self):
        """Initialize the title scene."""
        # Cleanup old elements
        if self.continue_button is not None:
            self.continue_button.kill()
        if self.new_game_button is not None:
            self.new_game_button.kill()
        if self.settings_button is not None:
            self.settings_button.kill()
        if self.quit_button is not None:
            self.quit_button.kill()
        
        # Button dimensions
        button_width = 300
        button_height = 50
        spacing = 15
        x = (self.game.SCREEN_WIDTH - button_width) // 2
        start_y = self.game.SCREEN_HEIGHT // 2 + 50
        
        # Check if there's a saved game
        has_save = self.game.game_state.save_system.has_save()
        
        if has_save:
            # Show Continue button
            self.continue_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((x, start_y), (button_width, button_height)),
                text='[CONTINUE]',
                manager=self.game.ui_manager
            )
            # Show New Game button
            self.new_game_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((x, start_y + button_height + spacing), (button_width, button_height)),
                text='NEW GAME',
                manager=self.game.ui_manager
            )
        else:
            # Just show Start button
            self.new_game_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((x, start_y), (button_width, button_height)),
                text='[START GAME]',
                manager=self.game.ui_manager
            )
        
        # Settings button
        settings_y = start_y + (2 if has_save else 1) * (button_height + spacing)
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, settings_y), (button_width, button_height)),
            text='SETTINGS',
            manager=self.game.ui_manager
        )
        
        # Quit button
        quit_y = settings_y + button_height + spacing
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, quit_y), (button_width, button_height)),
            text='QUIT',
            manager=self.game.ui_manager
        )
    
    def handle_event(self, event):
        """Handle events for title scene."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.continue_button:
                # Load saved game
                self.game.game_state.load_saved_game()
                self.game.change_scene(GameScene.LEVEL_SELECT)
            elif event.ui_element == self.new_game_button:
                # Delete old save and start new
                if self.game.game_state.save_system.has_save():
                    self.game.game_state.save_system.delete_save()
                # Reset game state
                self.game.game_state.player_name = ""
                self.game.game_state.completed_levels = []
                self.game.game_state.total_score = 0
                self.game.change_scene(GameScene.NAME_INPUT)
            elif event.ui_element == self.settings_button:
                self.game.change_scene(GameScene.SETTINGS)
            elif event.ui_element == self.quit_button:
                self.game.running = False
    
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
