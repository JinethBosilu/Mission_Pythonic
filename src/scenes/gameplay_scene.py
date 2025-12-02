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
        self.restart_button = None
        self.next_button = None
        self.result_label = None
        self.level_completed = False
    
    def setup(self):
        """Initialize the gameplay scene."""
        level = self.game.game_state.get_current_level()
        if not level:
            return
        
        # Reset completion state
        self.level_completed = False
        
        # Cleanup old elements
        if self.code_textbox is not None:
            self.code_textbox.kill()
        if self.run_button is not None:
            self.run_button.kill()
        if self.hint_button is not None:
            self.hint_button.kill()
        if self.solution_button is not None:
            self.solution_button.kill()
        if self.back_button is not None:
            self.back_button.kill()
        if self.restart_button is not None:
            self.restart_button.kill()
        if self.next_button is not None:
            self.next_button.kill()
        if self.result_label is not None:
            self.result_label.kill()
        
        # Start timer for this level
        self.game.game_state.start_level_timer()
        
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
        
        # Restart button
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((520, 610), (150, 40)),
            text='RESTART',
            manager=self.game.ui_manager
        )
        
        # Back button
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((680, 610), (150, 40)),
            text='BACK TO MENU',
            manager=self.game.ui_manager
        )
        
        # Next level button (hidden initially)
        self.next_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((840, 610), (160, 40)),
            text='NEXT LEVEL >>',
            manager=self.game.ui_manager
        )
        self.next_button.hide()
        
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
            elif event.ui_element == self.restart_button:
                self._restart_level()
            elif event.ui_element == self.next_button:
                self._next_level()
            elif event.ui_element == self.back_button:
                self.game.game_state.stop_timer()
                self.game.change_scene(GameScene.LEVEL_SELECT)
        
        # Handle keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                self._run_code()
            elif event.key == pygame.K_ESCAPE:
                # Pause game
                self.game.game_state.pause_timer()
                self.game.change_scene(GameScene.PAUSE)
    
    def _run_code(self):
        """Run the user's code."""
        level = self.game.game_state.get_current_level()
        if not level:
            return
        
        # Get code from textbox
        user_code = self.code_textbox.get_text()
        self.game.game_state.user_code = user_code
        
        # Check if time is up
        if self.game.game_state.is_time_up():
            penalty = self.game.game_state.get_time_penalty()
            self.result_label.set_text(f"[HACKED!] Time's up! Security detected you. Penalty: -{penalty} points")
            return
        
        # Evaluate the code
        success, message = self.game.game_state.evaluator.evaluate_level(user_code, level)
        
        if success:
            self.level_completed = True
            points_earned, penalty = self.game.game_state.complete_current_level()
            
            if penalty > 0:
                self.result_label.set_text(f"[SUCCESS!] {message} | Earned: {points_earned} pts (Penalty: -{penalty})")
            else:
                self.result_label.set_text(f"[SUCCESS!] {message} | Earned: {points_earned} pts")
            
            # Show next level button
            if not self.game.game_state.is_game_complete():
                self.next_button.show()
            else:
                # All levels complete - go to victory
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
    
    def _restart_level(self):
        """Restart the current level."""
        level = self.game.game_state.get_current_level()
        if not level:
            return
        
        # Reset level state
        self.code_textbox.set_text(level.starter_code)
        self.game.game_state.user_code = level.starter_code
        self.game.game_state.current_hint_index = 0
        self.game.game_state.show_solution = False
        self.result_label.set_text("Level restarted.")
        self.level_completed = False
        self.next_button.hide()
        
        # Restart timer
        self.game.game_state.start_level_timer()
    
    def _next_level(self):
        """Go to the next level."""
        if self.game.game_state.go_to_next_level():
            # Reinitialize gameplay scene with new level
            self.game.ui_manager.clear_and_reset()
            self.setup()
        else:
            # No more levels - go to victory
            self.game.change_scene(GameScene.VICTORY)
    
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
        
        # Draw timer
        time_remaining = self.game.game_state.get_time_remaining()
        minutes = int(time_remaining // 60)
        seconds = int(time_remaining % 60)
        
        # Change color based on time remaining
        if time_remaining <= 0:
            timer_color = self.game.RED
            timer_text = "TIME'S UP!"
        elif time_remaining <= level.time_warning:
            timer_color = self.game.RED
            timer_text = f"TIME: {minutes}:{seconds:02d} [WARNING!]"
        else:
            timer_color = self.game.GREEN
            timer_text = f"TIME: {minutes}:{seconds:02d}"
        
        timer_surface = self.game.heading_font.render(timer_text, True, timer_color)
        screen.blit(timer_surface, (20, 420))
    
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
