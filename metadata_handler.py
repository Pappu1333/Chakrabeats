"""
Metadata Handler for ChakraBeats
Extracts and displays song information from audio files
"""

import os
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SongMetadata:
    """Container for song metadata"""
    
    def __init__(self):
        self.title = ""
        self.artist = ""
        self.album = ""
        self.year = ""
        self.genre = ""
        self.track_number = ""
        self.duration = 0
        self.bitrate = 0
        self.sample_rate = 0
        self.channels = 0
        self.file_path = ""
        self.file_size = 0
        self.quote = ""  # Custom quote field
        
    def __str__(self):
        return f"{self.title} - {self.artist} ({self.album})"

class MetadataHandler:
    """Handles extraction and processing of audio metadata"""
    
    @staticmethod
    def extract_metadata(file_path):
        """Extract metadata from audio file"""
        metadata = SongMetadata()
        metadata.file_path = file_path
        
        try:
            # Get basic file info
            metadata.file_size = os.path.getsize(file_path)
            
            # Extract format-specific metadata
            if file_path.lower().endswith('.mp3'):
                metadata = MetadataHandler._extract_mp3_metadata(file_path, metadata)
            elif file_path.lower().endswith('.wav'):
                metadata = MetadataHandler._extract_wav_metadata(file_path, metadata)
            elif file_path.lower().endswith('.ogg'):
                metadata = MetadataHandler._extract_ogg_metadata(file_path, metadata)
            else:
                # Fallback for unsupported formats
                metadata.title = os.path.basename(file_path)
                
        except Exception as e:
            print(f"Error extracting metadata from {file_path}: {e}")
            # Set fallback values
            metadata.title = os.path.basename(file_path)
            metadata.artist = "Unknown Artist"
            metadata.album = "Unknown Album"
            
        return metadata
    
    @staticmethod
    def _extract_mp3_metadata(file_path, metadata):
        """Extract metadata from MP3 file"""
        try:
            # Get audio info
            audio = MP3(file_path)
            metadata.duration = int(audio.info.length)
            metadata.bitrate = audio.info.bitrate
            metadata.sample_rate = audio.info.sample_rate
            
            # Try to get ID3 tags
            try:
                id3 = ID3(file_path)
                if id3:
                    # Extract standard tags
                    if 'TIT2' in id3:
                        metadata.title = str(id3['TIT2'])
                    if 'TPE1' in id3:
                        metadata.artist = str(id3['TPE1'])
                    if 'TALB' in id3:
                        metadata.album = str(id3['TALB'])
                    if 'TYER' in id3:
                        metadata.year = str(id3['TYER'])
                    if 'TCON' in id3:
                        metadata.genre = str(id3['TCON'])
                    if 'TRCK' in id3:
                        metadata.track_number = str(id3['TRCK'])
                    if 'COMM' in id3:
                        metadata.quote = str(id3['COMM'])
                        
            except Exception:
                # Try EasyID3 as fallback
                try:
                    audio = EasyID3(file_path)
                    if audio:
                        if 'title' in audio:
                            metadata.title = audio['title'][0]
                        if 'artist' in audio:
                            metadata.artist = audio['artist'][0]
                        if 'album' in audio:
                            metadata.album = audio['album'][0]
                        if 'date' in audio:
                            metadata.year = audio['date'][0]
                        if 'genre' in audio:
                            metadata.genre = audio['genre'][0]
                        if 'tracknumber' in audio:
                            metadata.track_number = audio['tracknumber'][0]
                except Exception:
                    pass
                    
        except Exception as e:
            print(f"Error processing MP3 file {file_path}: {e}")
            
        return metadata
    
    @staticmethod
    def _extract_wav_metadata(file_path, metadata):
        """Extract metadata from WAV file"""
        try:
            audio = WAVE(file_path)
            metadata.duration = int(audio.info.length)
            metadata.sample_rate = audio.info.sample_rate
            metadata.channels = audio.info.channels
            
            # WAV files typically don't have rich metadata
            # Use filename as title
            metadata.title = os.path.splitext(os.path.basename(file_path))[0]
            metadata.artist = "Unknown Artist"
            metadata.album = "Unknown Album"
            
        except Exception as e:
            print(f"Error processing WAV file {file_path}: {e}")
            
        return metadata
    
    @staticmethod
    def _extract_ogg_metadata(file_path, metadata):
        """Extract metadata from OGG file"""
        try:
            audio = OggVorbis(file_path)
            metadata.duration = int(audio.info.length)
            metadata.bitrate = audio.info.bitrate
            metadata.sample_rate = audio.info.sample_rate
            
            # Extract Vorbis comments
            if audio.tags:
                tags = audio.tags
                if 'title' in tags:
                    metadata.title = tags['title'][0]
                if 'artist' in tags:
                    metadata.artist = tags['artist'][0]
                if 'album' in tags:
                    metadata.album = tags['album'][0]
                if 'date' in tags:
                    metadata.year = tags['date'][0]
                if 'genre' in tags:
                    metadata.genre = tags['genre'][0]
                if 'tracknumber' in tags:
                    metadata.track_number = tags['tracknumber'][0]
                if 'comment' in tags:
                    metadata.quote = tags['comment'][0]
                    
        except Exception as e:
            print(f"Error processing OGG file {file_path}: {e}")
            
        return metadata
    
    @staticmethod
    def format_duration(seconds):
        """Format duration in MM:SS or HH:MM:SS"""
        if seconds < 3600:
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes:02d}:{seconds:02d}"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    @staticmethod
    def format_file_size(bytes_size):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"

class MetadataDisplayWidget(QWidget):
    """Widget for displaying song metadata"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.metadata = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the metadata display UI"""
        layout = QVBoxLayout(self)
        
        # Title
        self.title_label = QLabel("🎵 Song Information")
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Metadata fields
        self.metadata_layout = QVBoxLayout()
        
        # Song title
        self.song_title_label = QLabel("Title: No song selected")
        self.song_title_label.setWordWrap(True)
        self.metadata_layout.addWidget(self.song_title_label)
        
        # Artist
        self.artist_label = QLabel("Artist: Unknown")
        self.metadata_layout.addWidget(self.artist_label)
        
        # Album
        self.album_label = QLabel("Album: Unknown")
        self.metadata_layout.addWidget(self.album_label)
        
        # Duration
        self.duration_label = QLabel("Duration: 0:00")
        self.metadata_layout.addWidget(self.duration_label)
        
        # File info
        self.file_info_label = QLabel("File: No file selected")
        self.file_info_label.setWordWrap(True)
        self.metadata_layout.addWidget(self.file_info_label)
        
        # Quote section
        self.quote_label = QLabel("💭 Quote of the Song:")
        self.quote_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.metadata_layout.addWidget(self.quote_label)
        
        self.quote_text = QTextEdit()
        self.quote_text.setMaximumHeight(80)
        self.quote_text.setPlaceholderText("No quote available for this song...")
        self.quote_text.setReadOnly(True)
        self.metadata_layout.addWidget(self.quote_text)
        
        layout.addLayout(self.metadata_layout)
        layout.addStretch()
        
    def update_metadata(self, metadata):
        """Update the displayed metadata"""
        self.metadata = metadata
        
        if metadata:
            # Update labels
            title = metadata.title if metadata.title else "Unknown Title"
            artist = metadata.artist if metadata.artist else "Unknown Artist"
            album = metadata.album if metadata.album else "Unknown Album"
            
            self.song_title_label.setText(f"🎵 Title: {title}")
            self.artist_label.setText(f"👤 Artist: {artist}")
            self.album_label.setText(f"💿 Album: {album}")
            
            # Format duration
            duration_str = MetadataHandler.format_duration(metadata.duration)
            self.duration_label.setText(f"⏱️ Duration: {duration_str}")
            
            # File information
            file_name = os.path.basename(metadata.file_path)
            file_size = MetadataHandler.format_file_size(metadata.file_size)
            self.file_info_label.setText(f"📁 File: {file_name}\n📊 Size: {file_size}")
            
            # Quote
            if metadata.quote:
                self.quote_text.setText(metadata.quote)
            else:
                self.quote_text.setText("No quote available for this song...")
                
        else:
            # Clear display
            self.song_title_label.setText("Title: No song selected")
            self.artist_label.setText("Artist: Unknown")
            self.album_label.setText("Album: Unknown")
            self.duration_label.setText("Duration: 0:00")
            self.file_info_label.setText("File: No file selected")
            self.quote_text.setText("")
    
    def clear_display(self):
        """Clear the metadata display"""
        self.update_metadata(None)

class PlaylistMetadataManager:
    """Manages metadata for playlist items"""
    
    def __init__(self):
        self.metadata_cache = {}  # Cache metadata to avoid repeated extraction
        
    def get_metadata(self, file_path):
        """Get metadata for a file, using cache if available"""
        if file_path in self.metadata_cache:
            return self.metadata_cache[file_path]
        
        metadata = MetadataHandler.extract_metadata(file_path)
        self.metadata_cache[file_path] = metadata
        return metadata
    
    def clear_cache(self):
        """Clear the metadata cache"""
        self.metadata_cache.clear()
    
    def remove_from_cache(self, file_path):
        """Remove a file from the metadata cache"""
        if file_path in self.metadata_cache:
            del self.metadata_cache[file_path] 