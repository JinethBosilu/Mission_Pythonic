"""Gameplay scene - main level playing interface."""
import pygame
import pygame_gui
from ..game_state import GameScene


class GameplayScene:
    """Main gameplay scene with code editor and level info."""
    
    def __init__(self, game):
        self.game = game
        self.code_textbox = None
        self.run_button = None
        self.hint_button = None
        self.solution_button = None
        self.back_button = None
        self.result_label = None
    
    def setup(self):
        """Initialize the gameplay scene."""
        level = self.game.game_state.get_current_level()
        if not level:
            return
        
        # Code editor text box
        self.code_textbox = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect((520, 150), (480, 400)),
            manager=self.game.ui_manager
        )
        
        # Make it editable (we'll use a text entry instead)
        self.code_textbox.kill()
        self.code_textbox = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((520, 150), (480, 400)),
            manager=self.game.ui_manager
        )
        
        # Set starter code if user code is empty
        if not self.game.game_state.user_code:
            self.game.game_state.user_code = level.starter_code
        
        self.code_textbox.set_text(self.game.game_state.user_code)
        
        # Run button
        self.run_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((520, 560), (150, 40)),
            text='RUN (F5)',
            manager=self.game.ui_manager
        )
        
        # Hint button
        self.hint_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((680, 560), (150, 40)),
            text='HINT',
            manager=self.game.ui_manager
        )
        
        # Solution button
        self.solution_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((840, 560), (160, 40)),
            text='SHOW SOLUTION',
            manager=self.game.ui_manager
        )
        
        # Back button
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((520, 610), (150, 40)),
            text='BACK TO MENU',
            manager=self.game.ui_manager
        )
        
        # Result label
        self.result_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((520, 660), (480, 80)),
            text="",
            manager=self.game.ui_manager
        )
    
    def handle_event(self, event):
        """Handle events for gameplay scene."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.run_button:
                self._run_code()
            elif event.ui_element == self.hint_button:
                self._show_hint()
            elif event.ui_element == self.solution_button:
                self._show_solution()
            elif event.ui_element == self.back_button:
                self.game.change_scene(GameScene.LEVEL_SELECT)
        
        # Handle F5 key for running code
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                self._run_code()
    
    def _run_code(self):
        """Run the user's code."""
        level = self.game.game_state.get_current_level()
        if not level:
            return
        
        # Get code from textbox
        user_code = self.code_textbox.get_text()
        self.game.game_state.user_code = user_code
        
        # Evaluate the code
        success, message = self.game.game_state.evaluator.evaluate_level(user_code, level)
        
        if success:
            self.result_label.set_text(f"[SUCCESS!] {message}")
            self.game.game_state.complete_current_level()
            
            # Check if game is complete
            if self.game.game_state.is_game_complete():
                self.game.change_scene(GameScene.VICTORY)
        else:
            self.result_label.set_text(f"[FAILED] {message}")
    
    def _show_hint(self):
        """Show the next hint."""
        level = self.game.game_state.get_current_level()
        if not level or not level.hints:
            self.result_label.set_text("No hints available.")
            return
        
        hint_index = self.game.game_state.current_hint_index
        if hint_index < len(level.hints):
            hint = level.hints[hint_index]
            self.result_label.set_text(f"HINT {hint_index + 1}: {hint}")
            self.game.game_state.current_hint_index += 1
        else:
            self.result_label.set_text("No more hints available.")
    
    def _show_solution(self):
        """Show the solution."""
        level = self.game.game_state.get_current_level()
        if not level:
            return
        
        self.code_textbox.set_text(level.solution)
        self.game.game_state.user_code = level.solution
        self.result_label.set_text("Solution loaded. Press RUN to test it.")
    
    def update(self, dt):
        """Update gameplay scene."""
        pass
    
    def draw(self, screen):
        """Draw gameplay scene."""
        level = self.game.game_state.get_current_level()
        if not level:
            return
        
        # Draw level title
        title_text = self.game.heading_font.render(level.title, True, self.game.GREEN)
        screen.blit(title_text, (20, 20))
        
        # Draw mission log (left panel)
        self._draw_text_panel(screen, "MISSION LOG:", level.mission_log, 20, 70, 480, 150)
        
        # Draw challenge (left panel)
        self._draw_text_panel(screen, "OBJECTIVE:", level.challenge, 20, 240, 480, 120)
        
        # Draw level info
        difficulty_color = self.game.GREEN if level.difficulty == "beginner" else self.game.BRIGHT_GREEN
        difficulty_text = self.game.text_font.render(
            f"Difficulty: {level.difficulty.upper()} | Points: {level.points}", 
            True, 
            difficulty_color
        )
        screen.blit(difficulty_text, (20, 380))
    
    def _draw_text_panel(self, screen, title, text, x, y, width, height):
        """Draw a bordered text panel."""
        # Draw border
        pygame.draw.rect(screen, self.game.DARK_GREEN, (x, y, width, height), 2)
        
        # Draw title
        title_surface = self.game.text_font.render(title, True, self.game.GREEN)
        screen.blit(title_surface, (x + 10, y + 5))
        
        # Draw text (word wrap)
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            test_surface = self.game.text_font.render(test_line, True, self.game.GREEN)
            if test_surface.get_width() <= width - 20:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word + " "
        
        if current_line:
            lines.append(current_line)
        
        # Draw lines
        line_y = y + 30
        for line in lines:
            line_surface = self.game.text_font.render(line.strip(), True, self.game.GREEN)
            screen.blit(line_surface, (x + 10, line_y))
            line_y += 20
            if line_y > y + height - 10:
                break
