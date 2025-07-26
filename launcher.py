#!/usr/bin/env python3
"""
ChakraBeats Launcher
Provides a startup experience with anime quotes and chakra effects
"""

import sys
import random
import time
from PyQt6.QtWidgets import (QApplication, QSplashScreen, QLabel, QVBoxLayout, 
                             QWidget, QProgressBar, QHBoxLayout)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QColor, QLinearGradient, QFont, QBrush

# Import the main application
from main import ChakraBeatsPlayer

class ChakraSplashScreen(QSplashScreen):
    """Anime-themed splash screen with chakra effects"""
    
    def __init__(self):
        # Create a custom pixmap for the splash screen
        pixmap = QPixmap(600, 400)
        pixmap.fill(QColor(0, 0, 0))
        
        super().__init__(pixmap)
        
        # Setup the splash screen
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        
        # Animation properties
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(50)  # 20 FPS
        
        self.time = 0
        self.progress = 0
        
        # Anime quotes for startup
        self.anime_quotes = [
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
            "Channel your chakra! - Naruto"
        ]
        
        self.current_quote = random.choice(self.anime_quotes)
        
        # Start the animation
        self.start_animation()
    
    def start_animation(self):
        """Start the splash screen animation"""
        self.show()
        self.animation_timer.start()
    
    def update_animation(self):
        """Update the splash screen animation"""
        self.time += 0.1
        self.progress += 1
        
        if self.progress >= 100:
            self.animation_timer.stop()
            self.close()
            return
        
        # Redraw the splash screen
        self.update()
    
    def paintEvent(self, event):
        """Custom paint event for chakra effects"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Create chakra gradient background
        gradient = QLinearGradient(0, 0, width, height)
        gradient.setColorAt(0, QColor("#FFD700"))  # Gold
        gradient.setColorAt(0.3, QColor("#FF4500"))  # Orange red
        gradient.setColorAt(0.7, QColor("#800080"))  # Purple
        gradient.setColorAt(1, QColor("#000000"))  # Black
        
        painter.fillRect(self.rect(), QBrush(gradient))
        
        # Draw animated chakra particles
        for i in range(20):
            x = (i * 30 + self.time * 50) % width
            y = (i * 25 + self.time * 30) % height
            size = 5 + 3 * abs(np.sin(self.time + i))
            
            # Particle color
            if i % 4 == 0:
                color = QColor(255, 215, 0, 150)  # Gold
            elif i % 4 == 1:
                color = QColor(255, 69, 0, 150)   # Orange red
            elif i % 4 == 2:
                color = QColor(128, 0, 128, 150)  # Purple
            else:
                color = QColor(255, 255, 255, 150)  # White
            
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(x - size/2, y - size/2, size, size)
        
        # Draw title
        title_font = QFont("Arial", 32, QFont.Weight.Bold)
        painter.setFont(title_font)
        painter.setPen(QColor(255, 255, 255))
        
        title_text = "🔥 ChakraBeats 🔥"
        title_rect = painter.fontMetrics().boundingRect(title_text)
        title_x = (width - title_rect.width()) // 2
        title_y = height // 3
        
        # Draw title with glow effect
        painter.setPen(QColor(255, 215, 0, 100))
        painter.drawText(title_x + 2, title_y + 2, title_text)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(title_x, title_y, title_text)
        
        # Draw subtitle
        subtitle_font = QFont("Arial", 14)
        painter.setFont(subtitle_font)
        painter.setPen(QColor(255, 255, 255, 200))
        
        subtitle_text = "Anime Music Player"
        subtitle_rect = painter.fontMetrics().boundingRect(subtitle_text)
        subtitle_x = (width - subtitle_rect.width()) // 2
        subtitle_y = title_y + 50
        
        painter.drawText(subtitle_x, subtitle_y, subtitle_text)
        
        # Draw anime quote
        quote_font = QFont("Arial", 12, QFont.Weight.Normal, italic=True)
        painter.setFont(quote_font)
        painter.setPen(QColor(255, 215, 0, 180))
        
        # Wrap quote text
        quote_lines = self.wrap_text(self.current_quote, painter, width - 40)
        quote_y = height * 2 // 3
        
        for line in quote_lines:
            line_rect = painter.fontMetrics().boundingRect(line)
            line_x = (width - line_rect.width()) // 2
            painter.drawText(line_x, quote_y, line)
            quote_y += 25
        
        # Draw progress bar
        bar_width = width * 0.8
        bar_height = 20
        bar_x = (width - bar_width) // 2
        bar_y = height - 60
        
        # Progress bar background
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 100)))
        painter.drawRoundedRect(bar_x, bar_y, bar_width, bar_height, 10, 10)
        
        # Progress bar fill
        fill_width = int(bar_width * self.progress / 100)
        if fill_width > 0:
            bar_gradient = QLinearGradient(bar_x, bar_y, bar_x + fill_width, bar_y)
            bar_gradient.setColorAt(0, QColor(255, 215, 0))  # Gold
            bar_gradient.setColorAt(1, QColor(255, 69, 0))   # Orange red
            
            painter.setBrush(QBrush(bar_gradient))
            painter.drawRoundedRect(bar_x, bar_y, fill_width, bar_height, 10, 10)
        
        # Progress text
        progress_font = QFont("Arial", 10)
        painter.setFont(progress_font)
        painter.setPen(QColor(255, 255, 255))
        
        progress_text = f"Loading... {self.progress}%"
        progress_rect = painter.fontMetrics().boundingRect(progress_text)
        progress_x = (width - progress_rect.width()) // 2
        progress_y = bar_y - 10
        
        painter.drawText(progress_x, progress_y, progress_text)
    
    def wrap_text(self, text, painter, max_width):
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_rect = painter.fontMetrics().boundingRect(test_line)
            
            if test_rect.width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines

class LoadingThread(QThread):
    """Thread for loading the main application"""
    
    progress_updated = pyqtSignal(int)
    loading_finished = pyqtSignal()
    
    def run(self):
        """Simulate loading process"""
        for i in range(101):
            self.progress_updated.emit(i)
            time.sleep(0.03)  # Simulate loading time
        
        self.loading_finished.emit()

def main():
    """Main launcher function"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("ChakraBeats")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Anime Warriors")
    
    # Create and show splash screen
    splash = ChakraSplashScreen()
    
    # Create loading thread
    loading_thread = LoadingThread()
    loading_thread.progress_updated.connect(lambda p: setattr(splash, 'progress', p))
    loading_thread.loading_finished.connect(lambda: splash.close())
    
    # Start loading
    loading_thread.start()
    
    # Process events until splash screen closes
    app.processEvents()
    
    # Create and show main window
    player = ChakraBeatsPlayer()
    player.show()
    
    # Start the application
    sys.exit(app.exec())

if __name__ == "__main__":
    import numpy as np  # Import here for splash screen
    main() 