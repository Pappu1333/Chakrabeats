"""
Configuration file for ChakraBeats
Contains default settings, constants, and configuration options
"""

import os
from pathlib import Path

# Application Information
APP_NAME = "ChakraBeats"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Anime-Themed Music Player"
APP_AUTHOR = "Anime Warriors"

# File Paths
SETTINGS_FILE = "chakrabeats_settings.json"
FAVORITES_FILE = "chakrabeats_favorites.json"
PLAYLISTS_FILE = "chakrabeats_playlists.json"

# Audio Settings
SUPPORTED_FORMATS = ['.mp3', '.wav', '.ogg']
DEFAULT_VOLUME = 70
MAX_VOLUME = 100

# Visualizer Settings
VISUALIZER_FPS = 30
DEFAULT_VISUALIZER_MODE = "chakra_bars"
VISUALIZER_MODES = [
    "chakra_bars",
    "sharingan_circle", 
    "chakra_waves",
    "dragon_flames",
    "particle_system"
]

# Theme Settings
DEFAULT_THEME = "Kaminari Mode"
AVAILABLE_THEMES = [
    "Kaminari Mode",
    "Susanoo Mode", 
    "Dragon God Mode"
]

# UI Settings
DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Animation Settings
ANIMATION_SPEED = 0.05
PARTICLE_COUNT = 20
BAR_COUNT = 32

# Metadata Settings
METADATA_CACHE_SIZE = 1000
METADATA_TIMEOUT = 300  # seconds

# Anime Quotes
ANIME_QUOTES = [
    "Believe it! - Naruto Uzumaki",
    "I am the bone of my sword - Emiya Shirou",
    "Plus Ultra! - All Might",
    "I'll become the Pirate King! - Monkey D. Luffy",
    "I am the hope of the universe! - Goku",
    "I am the shadow, the true self - Persona 5",
    "The world is cruel, but also beautiful - Attack on Titan",
    "I'll show you the power of a true hero! - My Hero Academia",
    "Wake up, samurai! - Cyberpunk 2077",
    "The only truth is music! - FLCL",
    "Music is the universal language! - Your Lie in April",
    "Let's make some noise! - Beck",
    "The rhythm of life! - Cowboy Bebop",
    "Feel the beat! - Initial D",
    "Channel your chakra! - Naruto",
    "The power of friendship! - Fairy Tail",
    "Never give up! - One Piece",
    "The heart is the strongest muscle! - My Hero Academia",
    "The future is not set in stone! - Steins;Gate",
    "The world is full of possibilities! - Charlotte"
]

# Chakra Colors
CHAKRA_COLORS = {
    "Kaminari Mode": {
        "primary": "#FFD700",      # Electric yellow
        "secondary": "#000000",    # Black
        "accent": "#FFA500",       # Orange
        "background": "#1a1a1a",   # Dark gray
        "text": "#FFFFFF"          # White
    },
    "Susanoo Mode": {
        "primary": "#0066CC",      # Blue
        "secondary": "#000000",    # Black
        "accent": "#00CCFF",       # Light blue
        "background": "#0a0a0a",   # Very dark
        "text": "#FFFFFF"          # White
    },
    "Dragon God Mode": {
        "primary": "#DC143C",      # Crimson
        "secondary": "#800080",    # Purple
        "accent": "#FF4500",       # Orange red
        "background": "#2d1b3d",   # Dark purple
        "text": "#FFFFFF"          # White
    }
}

# Default Settings
DEFAULT_SETTINGS = {
    "theme": DEFAULT_THEME,
    "playlist": [],
    "shuffle": False,
    "repeat": False,
    "volume": DEFAULT_VOLUME,
    "visualization_mode": DEFAULT_VISUALIZER_MODE,
    "window_geometry": {
        "x": 100,
        "y": 100,
        "width": DEFAULT_WINDOW_WIDTH,
        "height": DEFAULT_WINDOW_HEIGHT
    },
    "favorites": [],
    "last_played": "",
    "last_position": 0
}

# Error Messages
ERROR_MESSAGES = {
    "file_not_found": "File not found: {}",
    "unsupported_format": "Unsupported audio format: {}",
    "playback_error": "Error during playback: {}",
    "metadata_error": "Error reading metadata: {}",
    "settings_error": "Error loading/saving settings: {}"
}

# Success Messages
SUCCESS_MESSAGES = {
    "file_loaded": "Successfully loaded: {}",
    "playlist_saved": "Playlist saved successfully",
    "settings_saved": "Settings saved successfully",
    "favorite_added": "Added to favorites: {}",
    "favorite_removed": "Removed from favorites: {}"
}

def get_app_data_dir():
    """Get the application data directory"""
    if os.name == 'nt':  # Windows
        return os.path.join(os.getenv('APPDATA'), APP_NAME)
    else:  # Unix/Linux/Mac
        return os.path.join(os.path.expanduser('~'), f'.{APP_NAME.lower()}')

def ensure_app_data_dir():
    """Ensure the application data directory exists"""
    data_dir = get_app_data_dir()
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def get_settings_path():
    """Get the full path to the settings file"""
    data_dir = ensure_app_data_dir()
    return os.path.join(data_dir, SETTINGS_FILE)

def get_favorites_path():
    """Get the full path to the favorites file"""
    data_dir = ensure_app_data_dir()
    return os.path.join(data_dir, FAVORITES_FILE)

def get_playlists_path():
    """Get the full path to the playlists file"""
    data_dir = ensure_app_data_dir()
    return os.path.join(data_dir, PLAYLISTS_FILE) 