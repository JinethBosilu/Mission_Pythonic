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
    PAUSE = "pause"
    SETTINGS = "settings"
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
        
        # Timer state
        self.level_start_time = 0
        self.elapsed_time = 0
        self.timer_active = False
        self.timer_paused = False
        self.pause_start_time = 0
        
        # Troll messages for various situations
        self.time_up_messages = [
            "You can't even solve this? Pathetic.",
            "A snail could code faster than you.",
            "Security detected your incompetence.",
            "Maybe Python isn't for you...",
            "The firewall laughs at your attempt.",
            "Too slow! The system has locked you out.",
            "Amateur hour is over. Try again.",
            "Did you fall asleep at the keyboard?",
            "This is beginner level and you failed...",
            "The AI just called you 'obsolete'."
        ]
        
        self.failure_taunts = [
            "Wrong! Did you even read the instructions?",
            "Nice try... NOT.",
            "Error 404: Brain not found.",
            "The system rejects your mediocrity.",
            "Syntax error: Intelligence missing.",
            "This code is worse than a malware.",
            "Security system: 'Is this a joke?'",
            "Even a script kiddie could do better.",
            "Runtime error: Skill not installed."
        ]
        
        self.multiple_failures = [
            "Again? Seriously?",
            "How many times are you going to fail?",
            "The definition of insanity...",
            "Maybe use the hints? Just saying...",
            "The system is getting bored watching you fail.",
            "Perhaps coding isn't your calling?",
            "CTRL+C, CTRL+V. Learn it."
        ]
        
        self.attempt_count = 0
    
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
            self.reset_attempts()
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
            # Apply time penalty if over time
            penalty = self.get_time_penalty()
            points_earned = max(10, level.points - penalty)  # Minimum 10 points
            self.total_score += points_earned
            self.stop_timer()
            self.save_game()
            return points_earned, penalty
        return 0, 0
    
    def is_game_complete(self) -> bool:
        """Check if all levels are completed."""
        return len(self.completed_levels) >= self.level_loader.get_level_count()
    
    def start_level_timer(self):
        """Start the timer for the current level."""
        import time
        self.level_start_time = time.time()
        self.elapsed_time = 0
        self.timer_active = True
        self.timer_paused = False
    
    def update_timer(self):
        """Update elapsed time if timer is active."""
        if self.timer_active and not self.timer_paused:
            import time
            self.elapsed_time = time.time() - self.level_start_time
    
    def pause_timer(self):
        """Pause the timer."""
        if self.timer_active and not self.timer_paused:
            import time
            self.timer_paused = True
            self.pause_start_time = time.time()
    
    def resume_timer(self):
        """Resume the timer."""
        if self.timer_active and self.timer_paused:
            import time
            pause_duration = time.time() - self.pause_start_time
            self.level_start_time += pause_duration
            self.timer_paused = False
    
    def stop_timer(self):
        """Stop the timer."""
        self.timer_active = False
        self.timer_paused = False
    
    def get_time_remaining(self) -> float:
        """Get remaining time for current level."""
        level = self.get_current_level()
        if not level or not hasattr(level, 'time_limit'):
            return float('inf')
        return level.time_limit - self.elapsed_time
    
    def is_time_up(self) -> bool:
        """Check if time has run out."""
        return self.get_time_remaining() <= 0
    
    def get_time_penalty(self) -> int:
        """Calculate point penalty for going over time."""
        overtime = -self.get_time_remaining()
        if overtime <= 0:
            return 0
        # Lose 5 points per 10 seconds overtime
        return min(50, int(overtime / 10) * 5)
    
    def get_time_up_message(self) -> str:
        """Get a random trolling message for time running out."""
        import random
        return random.choice(self.time_up_messages)
    
    def get_failure_message(self) -> str:
        """Get a trolling message for failed attempts."""
        import random
        self.attempt_count += 1
        if self.attempt_count > 3:
            return random.choice(self.multiple_failures)
        return random.choice(self.failure_taunts)
    
    def reset_attempts(self):
        """Reset attempt counter for new level."""
        self.attempt_count = 0
