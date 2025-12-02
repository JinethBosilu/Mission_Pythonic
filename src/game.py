"""Main game engine using Pygame."""
import pygame
import pygame_gui
from pathlib import Path
from .game_state import GameState, GameScene
from .scenes.title_scene import TitleScene
from .scenes.name_input_scene import NameInputScene
from .scenes.level_select_scene import LevelSelectScene
from .scenes.gameplay_scene import GameplayScene
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
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
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
            GameScene.VICTORY: VictoryScene(self),
        }
        
        # Load font
        self.load_fonts()
    
    def load_fonts(self):
        """Load fonts for the game."""
        # Try to load a monospace font for code
        self.code_font = pygame.font.SysFont('consolas', 14)
        self.title_font = pygame.font.SysFont('consolas', 48, bold=True)
        self.heading_font = pygame.font.SysFont('consolas', 24, bold=True)
        self.text_font = pygame.font.SysFont('consolas', 16)
    
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
                
                # Pass events to UI manager
                self.ui_manager.process_events(event)
                
                # Pass events to current scene
                current_scene = self.scenes.get(self.game_state.current_scene)
                if current_scene:
                    current_scene.handle_event(event)
            
            # Update
            self.ui_manager.update(time_delta)
            
            current_scene = self.scenes.get(self.game_state.current_scene)
            if current_scene:
                current_scene.update(time_delta)
            
            # Draw
            self.screen.fill(self.BLACK)
            
            if current_scene:
                current_scene.draw(self.screen)
            
            self.ui_manager.draw_ui(self.screen)
            
            pygame.display.flip()
        
        pygame.quit()


def main():
    """Entry point for the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
