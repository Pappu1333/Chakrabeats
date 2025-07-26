#!/usr/bin/env python3
"""
ChakraBeats - Anime-Themed Music Player
A spiritual audio experience for otakus, creators, and warriors of rhythm.
"""

import sys
import os
import json
import random
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QSlider, 
                             QFileDialog, QListWidget, QListWidgetItem,
                             QFrame, QProgressBar, QComboBox, QCheckBox,
                             QTextEdit, QSplitter, QScrollArea, QTabWidget)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QPainter, QBrush, QLinearGradient
import pygame
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Import our custom modules
from visualizer import ChakraVisualizer, VisualizerModeSelector
from metadata_handler import MetadataHandler, MetadataDisplayWidget, PlaylistMetadataManager

class ChakraTheme:
    """Chakra-themed color schemes and styling"""
    
    THEMES = {
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
    
    ANIME_QUOTES = [
        "Believe it! - Naruto Uzumaki",
        "I am the bone of my sword - Emiya Shirou",
        "Plus Ultra! - All Might",
        "I'll become the Pirate King! - Monkey D. Luffy",
        "I am the hope of the universe! - Goku",
        "I am the shadow, the true self - Persona 5",
        "The world is cruel, but also beautiful - Attack on Titan",
        "I'll show you the power of a true hero! - My Hero Academia"
    ]

class AudioPlayer(QThread):
    """Audio playback thread with pygame"""
    
    track_changed = pyqtSignal(str)
    position_changed = pyqtSignal(int)
    playback_finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.current_file = None
        self.is_playing = False
        self.is_paused = False
        self.position = 0
        self.duration = 0
        
    def load_file(self, file_path):
        """Load and prepare audio file"""
        try:
            pygame.mixer.music.load(file_path)
            self.current_file = file_path
            self.track_changed.emit(file_path)
            
            # Get duration
            if file_path.lower().endswith('.mp3'):
                audio = MP3(file_path)
            elif file_path.lower().endswith('.wav'):
                audio = WAVE(file_path)
            elif file_path.lower().endswith('.ogg'):
                audio = OggVorbis(file_path)
            else:
                self.duration = 0
                return
                
            self.duration = int(audio.info.length * 1000)  # Convert to milliseconds
        except Exception as e:
            print(f"Error loading file: {e}")
    
    def play(self):
        """Start playback"""
        if self.current_file:
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
    
    def pause(self):
        """Pause playback"""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
    
    def unpause(self):
        """Resume playback"""
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
    
    def stop(self):
        """Stop playback"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.position = 0
    
    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)"""
        pygame.mixer.music.set_volume(volume / 100.0)
    
    def seek(self, position):
        """Seek to position (in milliseconds)"""
        if self.current_file and self.duration > 0:
            # Note: pygame doesn't support seeking, so we restart from position
            # This is a limitation, but works for basic functionality
            pass

# Note: VisualizerWidget is now replaced by ChakraVisualizer from visualizer.py

class ChakraBeatsPlayer(QMainWindow):
    """Main ChakraBeats application window"""
    
    def __init__(self):
        super().__init__()
        self.audio_player = AudioPlayer()
        self.current_theme = "Kaminari Mode"
        self.favorites = []
        self.playlist = []
        self.current_index = 0
        self.shuffle_mode = False
        self.repeat_mode = False
        
        # Initialize metadata manager
        self.metadata_manager = PlaylistMetadataManager()
        
        self.init_ui()
        self.load_settings()
        self.apply_theme()
        
        # Connect audio player signals
        self.audio_player.track_changed.connect(self.on_track_changed)
        self.audio_player.playback_finished.connect(self.on_playback_finished)
        
        # Update timer for seek bar
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_seek_bar)
        self.update_timer.start(100)
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("ChakraBeats - Anime Music Player")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Title with anime quote
        title_layout = QHBoxLayout()
        title_label = QLabel("🔥 ChakraBeats 🔥")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title_label)
        
        # Theme selector
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(ChakraTheme.THEMES.keys())
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        title_layout.addWidget(QLabel("Chakra Mode:"))
        title_layout.addWidget(self.theme_combo)
        
        main_layout.addLayout(title_layout)
        
        # Enhanced Visualizer
        self.visualizer = ChakraVisualizer()
        main_layout.addWidget(self.visualizer)
        
        # Splitter for playlist and controls
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Playlist section
        playlist_widget = QWidget()
        playlist_layout = QVBoxLayout(playlist_widget)
        
        playlist_label = QLabel("🎵 Playlist")
        playlist_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        playlist_layout.addWidget(playlist_label)
        
        # Playlist controls
        playlist_controls = QHBoxLayout()
        add_button = QPushButton("➕ Add Songs")
        add_button.clicked.connect(self.add_songs)
        playlist_controls.addWidget(add_button)
        
        clear_button = QPushButton("🗑️ Clear")
        clear_button.clicked.connect(self.clear_playlist)
        playlist_controls.addWidget(clear_button)
        
        self.shuffle_check = QCheckBox("🔀 Shuffle")
        self.shuffle_check.toggled.connect(self.toggle_shuffle)
        playlist_controls.addWidget(self.shuffle_check)
        
        self.repeat_check = QCheckBox("🔁 Repeat")
        self.repeat_check.toggled.connect(self.toggle_repeat)
        playlist_controls.addWidget(self.repeat_check)
        
        playlist_layout.addLayout(playlist_controls)
        
        # Playlist
        self.playlist_widget = QListWidget()
        self.playlist_widget.itemDoubleClicked.connect(self.play_selected)
        playlist_layout.addWidget(self.playlist_widget)
        
        splitter.addWidget(playlist_widget)
        
        # Controls section
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        
        # Now playing info
        self.now_playing_label = QLabel("No track selected")
        self.now_playing_label.setFont(QFont("Arial", 12))
        self.now_playing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(self.now_playing_label)
        
        # Seek bar
        self.seek_bar = QSlider(Qt.Orientation.Horizontal)
        self.seek_bar.sliderMoved.connect(self.seek_to_position)
        controls_layout.addWidget(self.seek_bar)
        
        # Time labels
        time_layout = QHBoxLayout()
        self.current_time_label = QLabel("0:00")
        self.total_time_label = QLabel("0:00")
        time_layout.addWidget(self.current_time_label)
        time_layout.addStretch()
        time_layout.addWidget(self.total_time_label)
        controls_layout.addLayout(time_layout)
        
        # Control buttons
        controls_layout.addStretch()
        
        # Main controls
        main_controls = QHBoxLayout()
        
        self.prev_button = QPushButton("⏮️")
        self.prev_button.clicked.connect(self.previous_track)
        main_controls.addWidget(self.prev_button)
        
        self.play_button = QPushButton("▶️")
        self.play_button.clicked.connect(self.toggle_play)
        main_controls.addWidget(self.play_button)
        
        self.stop_button = QPushButton("⏹️")
        self.stop_button.clicked.connect(self.stop_playback)
        main_controls.addWidget(self.stop_button)
        
        self.next_button = QPushButton("⏭️")
        self.next_button.clicked.connect(self.next_track)
        main_controls.addWidget(self.next_button)
        
        controls_layout.addLayout(main_controls)
        
        # Volume control
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("🔊"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.valueChanged.connect(self.change_volume)
        volume_layout.addWidget(self.volume_slider)
        controls_layout.addLayout(volume_layout)
        
        # Anime quote display
        self.quote_label = QLabel(random.choice(ChakraTheme.ANIME_QUOTES))
        self.quote_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quote_label.setStyleSheet("font-style: italic; color: #FFD700;")
        controls_layout.addWidget(self.quote_label)
        
        # Create tab widget for additional features
        tab_widget = QTabWidget()
        
        # Metadata tab
        self.metadata_widget = MetadataDisplayWidget()
        tab_widget.addTab(self.metadata_widget, "📄 Song Info")
        
        # Visualizer modes tab
        self.visualizer_selector = VisualizerModeSelector()
        self.visualizer_selector.set_visualizer(self.visualizer)
        tab_widget.addTab(self.visualizer_selector, "🔮 Visualizer")
        
        # Add tabs to controls
        controls_layout.addWidget(tab_widget)
        
        splitter.addWidget(controls_widget)
        splitter.setSizes([400, 800])
        
        main_layout.addWidget(splitter)
        
    def apply_theme(self):
        """Apply the current chakra theme"""
        theme = ChakraTheme.THEMES[self.current_theme]
        
        style = f"""
        QMainWindow {{
            background-color: {theme['background']};
            color: {theme['text']};
        }}
        
        QWidget {{
            background-color: {theme['background']};
            color: {theme['text']};
        }}
        
        QPushButton {{
            background-color: {theme['primary']};
            color: {theme['secondary']};
            border: 2px solid {theme['accent']};
            border-radius: 10px;
            padding: 8px;
            font-weight: bold;
            font-size: 14px;
        }}
        
        QPushButton:hover {{
            background-color: {theme['accent']};
            border-color: {theme['primary']};
        }}
        
        QPushButton:pressed {{
            background-color: {theme['secondary']};
            color: {theme['primary']};
        }}
        
        QSlider::groove:horizontal {{
            border: 1px solid {theme['accent']};
            height: 8px;
            background: {theme['secondary']};
            border-radius: 4px;
        }}
        
        QSlider::handle:horizontal {{
            background: {theme['primary']};
            border: 2px solid {theme['accent']};
            width: 18px;
            margin: -2px 0;
            border-radius: 9px;
        }}
        
        QListWidget {{
            background-color: {theme['secondary']};
            border: 2px solid {theme['accent']};
            border-radius: 5px;
            color: {theme['text']};
        }}
        
        QListWidget::item:selected {{
            background-color: {theme['primary']};
            color: {theme['secondary']};
        }}
        
        QComboBox {{
            background-color: {theme['secondary']};
            border: 2px solid {theme['accent']};
            border-radius: 5px;
            color: {theme['text']};
            padding: 5px;
        }}
        
        QCheckBox {{
            color: {theme['text']};
            font-weight: bold;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
        }}
        
        QCheckBox::indicator:unchecked {{
            border: 2px solid {theme['accent']};
            background-color: {theme['secondary']};
        }}
        
        QCheckBox::indicator:checked {{
            border: 2px solid {theme['primary']};
            background-color: {theme['primary']};
        }}
        """
        
        self.setStyleSheet(style)
        
    def change_theme(self, theme_name):
        """Change the current theme"""
        self.current_theme = theme_name
        self.apply_theme()
        self.save_settings()
        
    def add_songs(self):
        """Add songs to playlist"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Audio Files",
            "",
            "Audio Files (*.mp3 *.wav *.ogg);;MP3 Files (*.mp3);;WAV Files (*.wav);;OGG Files (*.ogg)"
        )
        
        for file_path in files:
            if file_path not in self.playlist:
                self.playlist.append(file_path)
                
                # Get metadata for better display
                metadata = self.metadata_manager.get_metadata(file_path)
                if metadata.title and metadata.artist:
                    display_text = f"🎵 {metadata.title} - {metadata.artist}"
                else:
                    display_text = f"🎵 {os.path.basename(file_path)}"
                
                item = QListWidgetItem(display_text)
                item.setData(Qt.ItemDataRole.UserRole, file_path)
                self.playlist_widget.addItem(item)
        
        self.save_settings()
        
    def clear_playlist(self):
        """Clear the playlist"""
        self.playlist.clear()
        self.playlist_widget.clear()
        self.audio_player.stop()
        self.now_playing_label.setText("No track selected")
        self.save_settings()
        
    def play_selected(self, item):
        """Play the selected track"""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.current_index = self.playlist.index(file_path)
        self.load_and_play(file_path)
        
    def load_and_play(self, file_path):
        """Load and play a track"""
        self.audio_player.load_file(file_path)
        self.audio_player.play()
        self.play_button.setText("⏸️")
        
        # Update display
        filename = os.path.basename(file_path)
        self.now_playing_label.setText(f"🎵 Now Playing: {filename}")
        
        # Update seek bar
        self.seek_bar.setRange(0, self.audio_player.duration)
        
        # Update metadata display
        metadata = self.metadata_manager.get_metadata(file_path)
        self.metadata_widget.update_metadata(metadata)
        
    def toggle_play(self):
        """Toggle play/pause"""
        if not self.playlist:
            return
            
        if self.audio_player.is_playing:
            if self.audio_player.is_paused:
                self.audio_player.unpause()
                self.play_button.setText("⏸️")
            else:
                self.audio_player.pause()
                self.play_button.setText("▶️")
        else:
            if self.current_index < len(self.playlist):
                self.load_and_play(self.playlist[self.current_index])
            else:
                self.current_index = 0
                if self.playlist:
                    self.load_and_play(self.playlist[0])
                    
    def stop_playback(self):
        """Stop playback"""
        self.audio_player.stop()
        self.play_button.setText("▶️")
        self.seek_bar.setValue(0)
        self.current_time_label.setText("0:00")
        
    def next_track(self):
        """Play next track"""
        if not self.playlist:
            return
            
        if self.shuffle_mode:
            self.current_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            
        self.load_and_play(self.playlist[self.current_index])
        self.playlist_widget.setCurrentRow(self.current_index)
        
    def previous_track(self):
        """Play previous track"""
        if not self.playlist:
            return
            
        if self.shuffle_mode:
            self.current_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            
        self.load_and_play(self.playlist[self.current_index])
        self.playlist_widget.setCurrentRow(self.current_index)
        
    def change_volume(self, value):
        """Change volume"""
        self.audio_player.set_volume(value)
        
    def seek_to_position(self, position):
        """Seek to position in track"""
        self.audio_player.seek(position)
        
    def update_seek_bar(self):
        """Update seek bar position"""
        if self.audio_player.is_playing and not self.audio_player.is_paused:
            # Get current position from pygame (approximate)
            current_pos = pygame.mixer.music.get_pos()
            if current_pos >= 0:
                self.seek_bar.setValue(current_pos)
                self.current_time_label.setText(self.format_time(current_pos))
                
    def format_time(self, milliseconds):
        """Format time in MM:SS"""
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"
        
    def toggle_shuffle(self, enabled):
        """Toggle shuffle mode"""
        self.shuffle_mode = enabled
        self.save_settings()
        
    def toggle_repeat(self, enabled):
        """Toggle repeat mode"""
        self.repeat_mode = enabled
        self.save_settings()
        
    def on_track_changed(self, file_path):
        """Handle track change"""
        pass
        
    def on_playback_finished(self):
        """Handle playback finished"""
        if self.repeat_mode:
            # Repeat current track
            if self.current_index < len(self.playlist):
                self.load_and_play(self.playlist[self.current_index])
        else:
            # Play next track
            self.next_track()
            
    def load_settings(self):
        """Load application settings"""
        try:
            if os.path.exists("chakrabeats_settings.json"):
                with open("chakrabeats_settings.json", "r") as f:
                    settings = json.load(f)
                    
                self.current_theme = settings.get("theme", "Kaminari Mode")
                self.playlist = settings.get("playlist", [])
                self.shuffle_mode = settings.get("shuffle", False)
                self.repeat_mode = settings.get("repeat", False)
                
                # Update UI
                self.theme_combo.setCurrentText(self.current_theme)
                self.shuffle_check.setChecked(self.shuffle_mode)
                self.repeat_check.setChecked(self.repeat_mode)
                
                # Load playlist
                for file_path in self.playlist:
                    if os.path.exists(file_path):
                        filename = os.path.basename(file_path)
                        item = QListWidgetItem(f"🎵 {filename}")
                        item.setData(Qt.ItemDataRole.UserRole, file_path)
                        self.playlist_widget.addItem(item)
        except Exception as e:
            print(f"Error loading settings: {e}")
            
    def save_settings(self):
        """Save application settings"""
        try:
            settings = {
                "theme": self.current_theme,
                "playlist": self.playlist,
                "shuffle": self.shuffle_mode,
                "repeat": self.repeat_mode
            }
            
            with open("chakrabeats_settings.json", "w") as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
            
    def closeEvent(self, event):
        """Handle application close"""
        self.save_settings()
        self.audio_player.stop()
        event.accept()

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("ChakraBeats")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Anime Warriors")
    
    # Create and show the main window
    player = ChakraBeatsPlayer()
    player.show()
    
    # Start the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 