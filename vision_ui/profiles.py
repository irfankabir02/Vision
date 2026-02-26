"""
LIMITATIONS:

This file uses keyword matching for safety, which is insufficient for production without classifier context.
"""

"""
vision_ui.profiles

Profile management for multi-device summarization.
Supports loading named profiles (laptop, phone, slides, tweet) with screen dimensions.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
import json
import os
from pathlib import Path


@dataclass
class Profile:
    """Device profile with screen dimensions and font settings."""
    name: str
    width_px: int
    height_px: int
    font_size_px: int = 14
    editor_ruler_columns: int = 80
    buffer: float = 0.9
    image_regions: Optional[List[Dict[str, Any]]] = None  # For screenshot-aware layouts
    
    def to_dict(self) -> Dict:
        """Convert profile to dictionary for serialization."""
        return {
            "name": self.name,
            "width_px": self.width_px,
            "height_px": self.height_px,
            "font_size_px": self.font_size_px,
            "editor_ruler_columns": self.editor_ruler_columns,
            "buffer": self.buffer
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Profile":
        """Create profile from dictionary."""
        return cls(**data)


# Default built-in profiles
DEFAULT_PROFILES: Dict[str, Profile] = {
    "laptop": Profile(
        name="laptop",
        width_px=1920,
        height_px=1080,
        font_size_px=14,
        editor_ruler_columns=80,
        buffer=0.9
    ),
    "phone": Profile(
        name="phone",
        width_px=375,
        height_px=667,
        font_size_px=12,
        editor_ruler_columns=40,
        buffer=0.85
    ),
    "slides": Profile(
        name="slides",
        width_px=1024,
        height_px=768,
        font_size_px=18,
        editor_ruler_columns=60,
        buffer=0.8
    ),
    "tweet": Profile(
        name="tweet",
        width_px=280,
        height_px=400,
        font_size_px=14,
        editor_ruler_columns=40,
        buffer=0.9
    )
}


def get_profile_dir() -> Path:
    """Get the directory where user profiles are stored."""
    # Store profiles in vision_ui/profiles/ relative to this file
    return Path(__file__).parent / "profiles"


def load_profile(name_or_path: Union[str, Path]) -> Profile:
    """
    Load a profile by name or from a JSON file path.
    
    Args:
        name_or_path: Either a profile name (e.g., "laptop") or path to JSON file
        
    Returns:
        Profile object
        
    Raises:
        ValueError: If profile cannot be found or loaded
    """
    # Check if it's a built-in profile
    if isinstance(name_or_path, str) and name_or_path in DEFAULT_PROFILES:
        return DEFAULT_PROFILES[name_or_path]
    
    # Try to load from file
    profile_path = Path(name_or_path)
    if not profile_path.exists():
        # Try relative to profile directory
        profile_path = get_profile_dir() / f"{name_or_path}.json"
    
    if profile_path.exists():
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Profile.from_dict(data)
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            raise ValueError(f"Invalid profile file {profile_path}: {e}")
    
    raise ValueError(f"Profile not found: {name_or_path}")


def list_profiles() -> List[str]:
    """List all available profile names (built-in + user profiles)."""
    names = list(DEFAULT_PROFILES.keys())
    
    # Add user profiles
    profile_dir = get_profile_dir()
    if profile_dir.exists():
        for json_file in profile_dir.glob("*.json"):
            names.append(json_file.stem)
    
    return sorted(names)


def save_profile(profile: Profile, filename: Optional[str] = None) -> Path:
    """
    Save a profile to a JSON file.
    
    Args:
        profile: Profile to save
        filename: Optional filename (defaults to profile name)
        
    Returns:
        Path to saved file
    """
    if filename is None:
        filename = f"{profile.name}.json"
    
    profile_dir = get_profile_dir()
    profile_dir.mkdir(exist_ok=True)
    
    profile_path = profile_dir / filename
    with open(profile_path, 'w', encoding='utf-8') as f:
        json.dump(profile.to_dict(), f, indent=2)
    
    return profile_path


def parse_profiles_from_cli(profile_names: str, buffer_override: Optional[float] = None) -> List[Profile]:
    """
    Parse profile names from CLI and return Profile objects.
    
    Supports:
    - Comma-separated names (e.g., "phone,laptop")
    - @path files containing JSON or newline/comma-separated names
    - Optional buffer_override to apply uniformly without mutating defaults
    
    Args:
        profile_names: Comma-separated profile names or @path to a file
        buffer_override: Optional buffer value to override per-profile buffer
        
    Returns:
        List of Profile objects
    """
    if not profile_names.strip():
        return []

    def _load_names_from_file(path_str: str) -> List[str]:
        profile_path = Path(path_str)
        if not profile_path.exists():
            raise ValueError(f"Profile file not found: {profile_path}")
        content = profile_path.read_text(encoding="utf-8").strip()
        if not content:
            raise ValueError(f"Profile file is empty: {profile_path}")
        # Try JSON first
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return [str(item) for item in data if str(item).strip()]
            if isinstance(data, dict) and "profiles" in data and isinstance(data["profiles"], list):
                return [str(item) for item in data["profiles"] if str(item).strip()]
            # If it's a dict describing a single profile, allow direct load via path
            if isinstance(data, dict):
                return [str(profile_path)]
        except json.JSONDecodeError:
            pass
        # Fallback: newline or comma separated text
        if "\n" in content:
            return [line.strip() for line in content.splitlines() if line.strip()]
        return [name.strip() for name in content.split(',') if name.strip()]

    names: List[str]
    if profile_names.strip().startswith('@'):
        names = _load_names_from_file(profile_names.strip()[1:])
    else:
        names = [name.strip() for name in profile_names.split(',') if name.strip()]

    profiles: List[Profile] = []
    for name in names:
        try:
            loaded = load_profile(name)
            if buffer_override is not None:
                loaded = Profile(
                    name=loaded.name,
                    width_px=loaded.width_px,
                    height_px=loaded.height_px,
                    font_size_px=loaded.font_size_px,
                    editor_ruler_columns=loaded.editor_ruler_columns,
                    buffer=buffer_override,
                    image_regions=loaded.image_regions,
                )
            profiles.append(loaded)
        except ValueError as e:
            raise ValueError(f"Failed to load profile '{name}': {e}")
    
    return profiles
