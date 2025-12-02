"""Load and manage game levels."""
import json
from pathlib import Path
from typing import Optional, Dict, Any


class Level:
    """Represents a game level."""
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data["id"]
        self.title = data["title"]
        self.mission_log = data["mission_log"]
        self.challenge = data["challenge"]
        self.starter_code = data["starter_code"]
        self.solution = data["solution"]
        self.checker = data["checker"]
        self.hints = data.get("hints", [])
        self.points = data.get("points", 100)
        self.difficulty = data.get("difficulty", "beginner")
        self.requires_file = data.get("requires_file", None)
        self.time_limit = data.get("time_limit", 300)  # Default 5 minutes
        self.time_warning = data.get("time_warning", 60)  # Warning at 1 minute left


class LevelLoader:
    """Loads levels from JSON files."""
    
    def __init__(self, levels_dir: Path):
        self.levels_dir = levels_dir
        self.levels = {}
        self._load_all_levels()
    
    def _load_all_levels(self):
        """Load all level files from the levels directory."""
        if not self.levels_dir.exists():
            print(f"Warning: Levels directory not found: {self.levels_dir}")
            return
        
        level_files = sorted(self.levels_dir.glob("level_*.json"))
        for level_file in level_files:
            try:
                with open(level_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    level = Level(data)
                    self.levels[level.id] = level
            except Exception as e:
                print(f"Error loading {level_file.name}: {e}")
    
    def get_level(self, level_id: str) -> Optional[Level]:
        """Get a level by its ID."""
        return self.levels.get(level_id)
    
    def get_all_levels(self):
        """Get all levels sorted by ID."""
        return [self.levels[key] for key in sorted(self.levels.keys())]
    
    def get_level_count(self) -> int:
        """Get total number of levels."""
        return len(self.levels)
