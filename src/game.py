"""Main game engine using Pygame."""
import pygame
import pygame_gui
from pathlib import Path
from .game_state import GameState, GameScene
from .scenes.title_scene import TitleScene
from .scenes.name_input_scene import NameInputScene
from .scenes.level_select_scene import LevelSelectScene
from .scenes.gameplay_scene import GameplayScene
from .scenes.pause_scene import PauseScene
from .scenes.settings_scene import SettingsScene
from .scenes.victory_scene import VictoryScene


class Game:
    """Main game class."""
    
    # Colors (Matrix/Hacker theme - green on black)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 100, 0)
    BRIGHT_GREEN = (0, 200, 0)
    GRAY = (50, 50, 50)
    RED = (255, 0, 0)
    
    def __init__(self):
        pygame.init()
        
        # Screen settings
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Mission: Pythonic - Hacker Training")
        
        # Clock for FPS
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # UI Manager
        self.ui_manager = pygame_gui.UIManager((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Game state
        self.game_state = GameState()
        self.running = True
        
        # Scenes
        self.scenes = {
            GameScene.TITLE: TitleScene(self),
            GameScene.NAME_INPUT: NameInputScene(self),
            GameScene.LEVEL_SELECT: LevelSelectScene(self),
            GameScene.GAMEPLAY: GameplayScene(self),
            GameScene.PAUSE: PauseScene(self),
            GameScene.SETTINGS: SettingsScene(self),
            GameScene.VICTORY: VictoryScene(self),
        }
        
        # Load font
        self.load_fonts()
        
        # Particle system
        self.particles = []
        self.matrix_chars = []
        self.init_matrix_rain()
    
    def load_fonts(self):
        """Load fonts for the game."""
        # Try to load a monospace font for code with antialiasing
        self.code_font = pygame.font.SysFont('consolas', 16)
        self.title_font = pygame.font.SysFont('consolas', 56, bold=True)
        self.heading_font = pygame.font.SysFont('consolas', 28, bold=True)
        self.text_font = pygame.font.SysFont('consolas', 18)
        self.small_font = pygame.font.SysFont('consolas', 14)
    
    def init_matrix_rain(self):
        """Initialize Matrix rain effect."""
        import random
        for i in range(50):  # 50 columns of falling text
            self.matrix_chars.append({
                'x': random.randint(0, self.SCREEN_WIDTH),
                'y': random.randint(-self.SCREEN_HEIGHT, 0),
                'speed': random.randint(2, 8),
                'char': random.choice('01ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                'brightness': random.randint(50, 255)
            })
    
    def update_matrix_rain(self, dt):
        """Update matrix rain animation."""
        import random
        for char_data in self.matrix_chars:
            char_data['y'] += char_data['speed']
            if char_data['y'] > self.SCREEN_HEIGHT:
                char_data['y'] = random.randint(-100, 0)
                char_data['x'] = random.randint(0, self.SCREEN_WIDTH)
                char_data['char'] = random.choice('01ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            # Random brightness flicker
            if random.random() < 0.1:
                char_data['brightness'] = random.randint(50, 255)
    
    def draw_matrix_rain(self, screen):
        """Draw animated matrix rain background."""
        for char_data in self.matrix_chars:
            brightness = char_data['brightness']
            color = (0, brightness, 0)
            text = self.small_font.render(char_data['char'], True, color)
            screen.blit(text, (char_data['x'], char_data['y']))
    
    def draw_glow_text(self, screen, text, pos, font, color, glow_size=2, center=True):
        """Draw text with a glow effect."""
        # Render text to get dimensions
        main_text = font.render(text, True, color)
        
        # Calculate position (center if requested)
        if center:
            text_rect = main_text.get_rect(center=pos)
            draw_pos = text_rect.topleft
        else:
            draw_pos = pos
        
        # Draw glow (darker version)
        glow_color = (color[0] // 3, color[1] // 3, color[2] // 3)
        for offset_x in range(-glow_size, glow_size + 1):
            for offset_y in range(-glow_size, glow_size + 1):
                if offset_x != 0 or offset_y != 0:
                    glow_text = font.render(text, True, glow_color)
                    screen.blit(glow_text, (draw_pos[0] + offset_x, draw_pos[1] + offset_y))
        # Draw main text
        screen.blit(main_text, draw_pos)
    
    def spawn_particles(self, x, y, count=20, color=None):
        """Spawn particles at a position."""
        import random
        if color is None:
            color = self.GREEN
        for _ in range(count):
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-3, 3),
                'life': 1.0,
                'color': color
            })
    
    def update_particles(self, dt):
        """Update particle effects."""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravity
            particle['life'] -= dt * 2
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_particles(self, screen):
        """Draw particle effects."""
        for particle in self.particles:
            alpha = int(particle['life'] * 255)
            color = (*particle['color'], alpha)
            size = max(1, int(particle['life'] * 4))
            pos = (int(particle['x']), int(particle['y']))
            pygame.draw.circle(screen, particle['color'], pos, size)
    
    def change_scene(self, scene: GameScene):
        """Change the current game scene."""
        self.game_state.current_scene = scene
        self.ui_manager.clear_and_reset()
        
        # Initialize the new scene
        if scene in self.scenes:
            self.scenes[scene].setup()
    
    def run(self):
        """Main game loop."""
        # Start with title scene
        self.change_scene(GameScene.TITLE)
        
        while self.running:
            time_delta = self.clock.tick(self.FPS) / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Handle window resize
                if event.type == pygame.VIDEORESIZE:
                    self.SCREEN_WIDTH = event.w
                    self.SCREEN_HEIGHT = event.h
                    self.screen = pygame.display.set_mode(
                        (self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
                        pygame.RESIZABLE
                    )
                    self.ui_manager.set_window_resolution((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
                    # Clear and reinitialize current scene for new size
                    self.ui_manager.clear_and_reset()
                    if self.game_state.current_scene in self.scenes:
                        self.scenes[self.game_state.current_scene].setup()
                
                # Pass events to UI manager
                self.ui_manager.process_events(event)
                
                # Pass events to current scene
                current_scene = self.scenes.get(self.game_state.current_scene)
                if current_scene:
                    current_scene.handle_event(event)
            
            # Update
            self.ui_manager.update(time_delta)
            
            # Update game timer if in gameplay
            if self.game_state.current_scene == GameScene.GAMEPLAY:
                self.game_state.update_timer()
            
            # Update visual effects
            self.update_matrix_rain(time_delta)
            self.update_particles(time_delta)
            
            current_scene = self.scenes.get(self.game_state.current_scene)
            if current_scene:
                current_scene.update(time_delta)
            
            # Draw
            self.screen.fill(self.BLACK)
            
            # Draw matrix rain background
            self.draw_matrix_rain(self.screen)
            
            if current_scene:
                current_scene.draw(self.screen)
            
            # Draw particles on top
            self.draw_particles(self.screen)
            
            self.ui_manager.draw_ui(self.screen)
            
            pygame.display.flip()
        
        pygame.quit()


def main():
    """Entry point for the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
