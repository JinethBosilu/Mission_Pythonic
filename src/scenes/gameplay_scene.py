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
        self.flash_screen = False
        self.flash_timer = 0
        self.timeout_overlay = False
        self.timeout_restart_button = None
        self.timeout_menu_button = None
        self.timeout_message = ""
        self.timeout_restart_rect = None
        self.timeout_menu_rect = None
    
    def setup(self, preserve_timer=False):
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
        
        # Start timer for this level (unless preserving from resize)
        if not preserve_timer:
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
        
        # Handle mouse clicks on timeout overlay buttons
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.timeout_overlay:
                mouse_pos = pygame.mouse.get_pos()
                if self.timeout_restart_rect and self.timeout_restart_rect.collidepoint(mouse_pos):
                    self._restart_level()
                elif self.timeout_menu_rect and self.timeout_menu_rect.collidepoint(mouse_pos):
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
            return
        
        # Evaluate the code
        success, message = self.game.game_state.evaluator.evaluate_level(user_code, level)
        
        if success:
            self.level_completed = True
            points_earned, penalty = self.game.game_state.complete_current_level()
            
            import random
            success_msgs = [
                "Finally!",
                "Took you long enough.",
                "Not bad... for a beginner.",
                "Success! Barely.",
                "You did it. Congratulations, I guess.",
                "Correct. Even a broken clock is right twice a day.",
                "Success! The bar was low, but you cleared it.",
                "Nice. Now try the next one without hints."
            ]
            
            sass = random.choice(success_msgs)
            
            if penalty > 0:
                self.result_label.set_text(f"[{sass}] Earned: {points_earned} pts (Penalty: -{penalty}pts - Too slow!)")
            else:
                self.result_label.set_text(f"[{sass}] Earned: {points_earned} pts")
            
            # Spawn success particles
            for i in range(50):
                self.game.spawn_particles(
                    self.game.SCREEN_WIDTH // 2,
                    self.game.SCREEN_HEIGHT // 2,
                    count=1,
                    color=self.game.GREEN
                )
            
            # Show next level button
            if not self.game.game_state.is_game_complete():
                self.next_button.show()
            else:
                # All levels complete - go to victory
                self.game.change_scene(GameScene.VICTORY)
        else:
            troll_msg = self.game.game_state.get_failure_message()
            self.result_label.set_text(f"[FAILED] {message} | {troll_msg}")
    
    def _show_hint(self):
        """Show the next hint."""
        level = self.game.game_state.get_current_level()
        if not level or not level.hints:
            self.result_label.set_text("No hints available. You're on your own, genius.")
            return
        
        hint_index = self.game.game_state.current_hint_index
        if hint_index < len(level.hints):
            hint = level.hints[hint_index]
            
            # Add sarcastic comments based on hint count
            if hint_index == 0:
                prefix = "HINT 1"
            elif hint_index == 1:
                prefix = "HINT 2 (Really?)"
            elif hint_index == 2:
                prefix = "HINT 3 (Last one, try harder)"
            else:
                prefix = f"HINT {hint_index + 1}"
            
            self.result_label.set_text(f"{prefix}: {hint}")
            self.game.game_state.current_hint_index += 1
        else:
            import random
            no_hint_msgs = [
                "No more hints. Figure it out yourself.",
                "That's all the help you're getting.",
                "Hints exhausted. Good luck, you'll need it.",
                "Out of hints. Time to use that brain.",
                "No more hints available. Maybe try reading?"
            ]
            self.result_label.set_text(random.choice(no_hint_msgs))
    
    def _show_solution(self):
        """Show the solution."""
        level = self.game.game_state.get_current_level()
        if not level:
            return
        
        import random
        solution_taunts = [
            "Giving up already? Typical.",
            "Can't solve it yourself? Disappointing.",
            "So much for being a 'hacker'...",
            "Solution loaded. At least try to understand it.",
            "Cheater. The AI judges you.",
            "Solution revealed. Don't pretend you could've done it.",
            "Pathetic. But here's the answer anyway.",
            "Even with the solution, you'll probably mess it up."
        ]
        
        self.code_textbox.set_text(level.solution)
        self.game.game_state.user_code = level.solution
        self.result_label.set_text(random.choice(solution_taunts))
    
    def _show_timeout_overlay(self):
        """Show timeout overlay with restart and menu buttons."""
        # Store button rectangles for click detection
        button_width = 250
        button_height = 50
        spacing = 20
        center_x = self.game.SCREEN_WIDTH // 2
        center_y = self.game.SCREEN_HEIGHT // 2
        
        self.timeout_restart_rect = pygame.Rect(
            center_x - button_width - spacing // 2, 
            center_y + 80,
            button_width, 
            button_height
        )
        
        self.timeout_menu_rect = pygame.Rect(
            center_x + spacing // 2, 
            center_y + 80,
            button_width, 
            button_height
        )
    
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
        
        # Reset timeout overlay
        self.timeout_overlay = False
        self.timeout_message = ""
        self.timeout_restart_rect = None
        self.timeout_menu_rect = None
        
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
        # Check if time is up (not during level completion)
        if not self.level_completed and not self.timeout_overlay and self.game.game_state.is_time_up():
            self.timeout_overlay = True
            self.timeout_message = self.game.game_state.get_time_up_message()
            self.flash_screen = True
            self.flash_timer = 0.3
            self._show_timeout_overlay()
        
        # Update flash effect
        if self.flash_screen:
            self.flash_timer -= dt
            if self.flash_timer <= 0:
                self.flash_screen = False
    
    def draw(self, screen):
        """Draw gameplay scene."""
        level = self.game.game_state.get_current_level()
        if not level:
            return
        
        # Draw red flash overlay if time is up
        if self.flash_screen:
            flash_surface = pygame.Surface((self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT))
            flash_surface.set_alpha(100)
            flash_surface.fill(self.game.RED)
            screen.blit(flash_surface, (0, 0))
        
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
    
    def draw_overlay(self, screen):
        """Draw overlays that should appear on top of UI elements."""
        # Draw timeout overlay if active
        if self.timeout_overlay:
            self._draw_timeout_overlay(screen)
    
    def _draw_timeout_overlay(self, screen):
        """Draw the timeout overlay on top of everything."""
        import math
        # Semi-transparent dark overlay
        overlay = pygame.Surface((self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Use stored troll message
        troll_msg = self.timeout_message
        
        # Draw border box
        box_width = 700
        box_height = 300
        box_x = (self.game.SCREEN_WIDTH - box_width) // 2
        box_y = (self.game.SCREEN_HEIGHT - box_height) // 2 - 20
        
        pygame.draw.rect(screen, self.game.RED, (box_x, box_y, box_width, box_height), 3)
        pygame.draw.rect(screen, self.game.DARK_GREEN, (box_x + 4, box_y + 4, box_width - 8, box_height - 8), 1)
        
        # Draw corner brackets
        corner_size = 20
        corners = [
            (box_x, box_y),
            (box_x + box_width, box_y),
            (box_x, box_y + box_height),
            (box_x + box_width, box_y + box_height)
        ]
        for cx, cy in corners:
            if cx == box_x:
                pygame.draw.line(screen, self.game.RED, (cx, cy), (cx + corner_size, cy), 4)
            else:
                pygame.draw.line(screen, self.game.RED, (cx, cy), (cx - corner_size, cy), 4)
            
            if cy == box_y:
                pygame.draw.line(screen, self.game.RED, (cx, cy), (cx, cy + corner_size), 4)
            else:
                pygame.draw.line(screen, self.game.RED, (cx, cy), (cx, cy - corner_size), 4)
        
        # Draw TIME'S UP title
        self.game.draw_glow_text(
            screen,
            "TIME'S UP!",
            (self.game.SCREEN_WIDTH // 2, box_y + 60),
            self.game.title_font,
            self.game.RED,
            glow_size=3,
            center=True
        )
        
        # Draw troll message (word wrap)
        words = troll_msg.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            test_surface = self.game.text_font.render(test_line, True, self.game.GREEN)
            if test_surface.get_width() <= box_width - 80:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        # Draw lines
        line_y = box_y + 140
        for line in lines:
            self.game.draw_glow_text(
                screen,
                line,
                (self.game.SCREEN_WIDTH // 2, line_y),
                self.game.text_font,
                self.game.GREEN,
                glow_size=1,
                center=True
            )
            line_y += 30
        
        # Draw custom buttons on top of overlay
        if self.timeout_restart_rect and self.timeout_menu_rect:
            mouse_pos = pygame.mouse.get_pos()
            
            # Restart button
            restart_hover = self.timeout_restart_rect.collidepoint(mouse_pos)
            restart_color = self.game.BRIGHT_GREEN if restart_hover else self.game.GREEN
            pygame.draw.rect(screen, restart_color, self.timeout_restart_rect, 3)
            pygame.draw.rect(screen, (0, 0, 0), self.timeout_restart_rect)
            
            restart_text = self.game.text_font.render('RESTART LEVEL', True, restart_color)
            restart_text_rect = restart_text.get_rect(center=self.timeout_restart_rect.center)
            screen.blit(restart_text, restart_text_rect)
            
            # Menu button
            menu_hover = self.timeout_menu_rect.collidepoint(mouse_pos)
            menu_color = self.game.BRIGHT_GREEN if menu_hover else self.game.GREEN
            pygame.draw.rect(screen, menu_color, self.timeout_menu_rect, 3)
            pygame.draw.rect(screen, (0, 0, 0), self.timeout_menu_rect)
            
            menu_text = self.game.text_font.render('BACK TO MENU', True, menu_color)
            menu_text_rect = menu_text.get_rect(center=self.timeout_menu_rect.center)
            screen.blit(menu_text, menu_text_rect)
    
    def _draw_text_panel(self, screen, title, text, x, y, width, height):
        """Draw a bordered text panel with glow effect."""
        # Draw background with slight transparency effect
        panel_surface = pygame.Surface((width, height))
        panel_surface.set_alpha(30)
        panel_surface.fill(self.game.DARK_GREEN)
        screen.blit(panel_surface, (x, y))
        
        # Draw double border for depth
        pygame.draw.rect(screen, self.game.DARK_GREEN, (x, y, width, height), 2)
        pygame.draw.rect(screen, self.game.GREEN, (x + 2, y + 2, width - 4, height - 4), 1)
        
        # Draw corner accents
        corner_size = 10
        corners = [(x, y), (x + width, y), (x, y + height), (x + width, y + height)]
        for cx, cy in corners:
            pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx - 5, cy), (cx + 5, cy), 2)
            pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx, cy - 5), (cx, cy + 5), 2)
        
        # Draw title with glow
        self.game.draw_glow_text(screen, title, (x + 10, y + 5), self.game.text_font, self.game.BRIGHT_GREEN, glow_size=1, center=False)
        
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
