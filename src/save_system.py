"""Save and load game progress."""
import json
from pathlib import Path
from typing import Dict, Any, Optional


class SaveSystem:
    """Handles saving and loading game progress."""
    
    def __init__(self, save_dir: Path):
        self.save_dir = save_dir
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.save_file = self.save_dir / "progress.json"
    
    def save_progress(self, player_name: str, completed_levels: list, current_level: int, total_score: int):
        """Save player progress to file."""
        data = {
            "player_name": player_name,
            "completed_levels": completed_levels,
            "current_level": current_level,
            "total_score": total_score
        }
        
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving progress: {e}")
            return False
    
    def load_progress(self) -> Optional[Dict[str, Any]]:
        """Load player progress from file."""
        if not self.save_file.exists():
            return None
        
        try:
            with open(self.save_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading progress: {e}")
            return None
    
    def has_save(self) -> bool:
        """Check if a save file exists."""
        return self.save_file.exists()
    
    def delete_save(self):
        """Delete the save file."""
        if self.save_file.exists():
            self.save_file.unlink()
