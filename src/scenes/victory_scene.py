"""Victory scene shown when all levels are complete."""
import pygame
import pygame_gui
from ..game_state import GameScene


class VictoryScene:
    """Victory screen shown when all levels are completed."""
    
    def __init__(self, game):
        self.game = game
        self.menu_button = None
        self.pulse_timer = 0
        self.scroll_offset = 0
        self.particles_spawned = False
    
    def setup(self):
        """Initialize the victory scene."""
        # Cleanup old elements
        if self.menu_button is not None:
            self.menu_button.kill()
        
        # Reset animation state
        self.particles_spawned = False
        self.scroll_offset = 0
        
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
        self.pulse_timer += dt * 2
        self.scroll_offset += 20 * dt
        
        # Spawn particles once at start
        if not self.particles_spawned:
            self.particles_spawned = True
            # Spawn multiple particle bursts across screen
            for i in range(5):
                x = (i + 1) * (self.game.SCREEN_WIDTH // 6)
                self.game.spawn_particles(x, 150, 30, self.game.BRIGHT_GREEN)
    
    def draw(self, screen):
        """Draw victory scene."""
        import math
        
        # Draw pulsing glowing congratulations message
        pulse = math.sin(self.pulse_timer)
        pulse_size = int(3 + pulse * 1.5)
        self.game.draw_glow_text(
            screen,
            "MISSION COMPLETE!",
            (self.game.SCREEN_WIDTH // 2, 200),
            self.game.title_font,
            self.game.BRIGHT_GREEN,
            glow_size=pulse_size
        )
        
        # Draw border box around title
        box_width = 600
        box_height = 120
        box_x = (self.game.SCREEN_WIDTH - box_width) // 2
        box_y = 160
        pygame.draw.rect(screen, self.game.DARK_GREEN, (box_x, box_y, box_width, box_height), 3)
        pygame.draw.rect(screen, self.game.GREEN, (box_x + 4, box_y + 4, box_width - 8, box_height - 8), 1)
        
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
                pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx, cy), (cx + corner_size, cy), 3)
            else:
                pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx, cy), (cx - corner_size, cy), 3)
            
            if cy == box_y:
                pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx, cy), (cx, cy + corner_size), 3)
            else:
                pygame.draw.line(screen, self.game.BRIGHT_GREEN, (cx, cy), (cx, cy - corner_size), 3)
        
        # Draw player name with glow
        self.game.draw_glow_text(
            screen,
            f"Agent {self.game.game_state.player_name}",
            (self.game.SCREEN_WIDTH // 2, 310),
            self.game.heading_font,
            self.game.BRIGHT_GREEN,
            glow_size=2
        )
        
        # Draw final score with glow
        self.game.draw_glow_text(
            screen,
            f"Final Score: {self.game.game_state.total_score}",
            (self.game.SCREEN_WIDTH // 2, 360),
            self.game.heading_font,
            self.game.GREEN,
            glow_size=2
        )
        
        # Draw scrolling success message with subtle animation
        success_lines = [
            "You have successfully completed all Python hacking missions.",
            "Your skills are now at expert level.",
            "The Matrix awaits your next adventure..."
        ]
        
        y = 420
        for i, line in enumerate(success_lines):
            # Add subtle wave effect to text position
            wave_offset = int(5 * math.sin(self.pulse_timer + i * 0.5))
            self.game.draw_glow_text(
                screen,
                line,
                (self.game.SCREEN_WIDTH // 2 + wave_offset, y),
                self.game.text_font,
                self.game.GREEN,
                glow_size=1
            )
            y += 35
