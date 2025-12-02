"""Game state management."""
from enum import Enum
from pathlib import Path
from .level_loader import LevelLoader
from .save_system import SaveSystem
from .code_evaluator import CodeEvaluator


class GameScene(Enum):
    """Game scenes/states."""
    TITLE = "title"
    NAME_INPUT = "name_input"
    LEVEL_SELECT = "level_select"
    GAMEPLAY = "gameplay"
    VICTORY = "victory"


class GameState:
    """Manages the overall game state."""
    
    def __init__(self):
        # Paths
        self.base_dir = Path(__file__).parent.parent
        self.levels_dir = self.base_dir / "levels"
        self.save_dir = Path.home() / ".mission_pythonic"
        
        # Systems
        self.level_loader = LevelLoader(self.levels_dir)
        self.save_system = SaveSystem(self.save_dir)
        self.evaluator = CodeEvaluator()
        
        # Game state
        self.current_scene = GameScene.TITLE
        self.player_name = ""
        self.current_level_id = "level_001"
        self.completed_levels = []
        self.total_score = 0
        self.current_hint_index = 0
        self.user_code = ""
        
        # UI state
        self.show_solution = False
        self.last_result = None
        self.last_message = ""
    
    def load_saved_game(self):
        """Load saved game progress."""
        data = self.save_system.load_progress()
        if data:
            self.player_name = data.get("player_name", "")
            self.completed_levels = data.get("completed_levels", [])
            self.current_level_id = f"level_{data.get('current_level', 1):03d}"
            self.total_score = data.get("total_score", 0)
            return True
        return False
    
    def save_game(self):
        """Save current game progress."""
        current_level_num = int(self.current_level_id.split('_')[-1])
        self.save_system.save_progress(
            self.player_name,
            self.completed_levels,
            current_level_num,
            self.total_score
        )
    
    def get_current_level(self):
        """Get the current level object."""
        return self.level_loader.get_level(self.current_level_id)
    
    def get_all_levels(self):
        """Get all levels."""
        return self.level_loader.get_all_levels()
    
    def go_to_next_level(self):
        """Advance to the next level."""
        current_num = int(self.current_level_id.split('_')[-1])
        next_num = current_num + 1
        next_id = f"level_{next_num:03d}"
        
        if self.level_loader.get_level(next_id):
            self.current_level_id = next_id
            self.current_hint_index = 0
            self.show_solution = False
            self.user_code = ""
            return True
        return False
    
    def is_level_completed(self, level_id: str) -> bool:
        """Check if a level is completed."""
        return level_id in self.completed_levels
    
    def complete_current_level(self):
        """Mark current level as completed."""
        level = self.get_current_level()
        if level and level.id not in self.completed_levels:
            self.completed_levels.append(level.id)
            self.total_score += level.points
            self.save_game()
    
    def is_game_complete(self) -> bool:
        """Check if all levels are completed."""
        return len(self.completed_levels) >= self.level_loader.get_level_count()
