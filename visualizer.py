"""
Enhanced Visualizer Module for ChakraBeats
Multiple anime-themed visualization modes with chakra effects
"""

import numpy as np
import random
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QPen, QFont

class ChakraVisualizer(QWidget):
    """Advanced anime-themed music visualizer with multiple modes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        
        # Animation properties
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update)
        self.animation_timer.start(30)  # 33 FPS for smooth animation
        
        # Visualizer state
        self.time = 0
        self.mode = "chakra_bars"  # Default mode
        self.audio_data = np.random.rand(64) * 0.3  # Simulated audio data
        
        # Chakra effects
        self.chakra_particles = []
        self.init_chakra_particles()
        
        # Mode-specific properties
        self.bar_count = 32
        self.circle_radius = 50
        self.wave_points = 100
        
    def init_chakra_particles(self):
        """Initialize chakra particle system"""
        self.chakra_particles = []
        for _ in range(20):
            particle = {
                'x': random.uniform(0, 1),
                'y': random.uniform(0, 1),
                'vx': random.uniform(-0.02, 0.02),
                'vy': random.uniform(-0.02, 0.02),
                'size': random.uniform(2, 8),
                'life': random.uniform(0.5, 1.0),
                'color': random.choice(['gold', 'orange', 'red', 'purple'])
            }
            self.chakra_particles.append(particle)
    
    def set_visualization_mode(self, mode):
        """Set the visualization mode"""
        self.mode = mode
        
    def update_audio_data(self, data):
        """Update audio data for visualization"""
        if data is not None:
            self.audio_data = data
    
    def paintEvent(self, event):
        """Main painting method"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Update time
        self.time += 0.05
        
        # Choose visualization method based on mode
        if self.mode == "chakra_bars":
            self.draw_chakra_bars(painter, width, height)
        elif self.mode == "sharingan_circle":
            self.draw_sharingan_circle(painter, width, height)
        elif self.mode == "chakra_waves":
            self.draw_chakra_waves(painter, width, height)
        elif self.mode == "dragon_flames":
            self.draw_dragon_flames(painter, width, height)
        elif self.mode == "particle_system":
            self.draw_particle_system(painter, width, height)
        else:
            self.draw_chakra_bars(painter, width, height)  # Default fallback
    
    def draw_chakra_bars(self, painter, width, height):
        """Draw animated chakra bars"""
        # Create gradient background
        gradient = QLinearGradient(0, 0, width, height)
        gradient.setColorAt(0, QColor("#FFD700"))  # Gold
        gradient.setColorAt(0.3, QColor("#FF4500"))  # Orange red
        gradient.setColorAt(0.7, QColor("#800080"))  # Purple
        gradient.setColorAt(1, QColor("#000000"))  # Black
        
        painter.fillRect(self.rect(), QBrush(gradient))
        
        # Draw animated bars
        bar_width = width // self.bar_count
        
        for i in range(self.bar_count):
            # Get audio data for this bar
            data_index = int(i * len(self.audio_data) / self.bar_count)
            base_height = self.audio_data[data_index] if data_index < len(self.audio_data) else 0.3
            
            # Animate bar height
            animated_height = base_height + 0.2 * np.sin(self.time + i * 0.3)
            animated_height = max(0.1, min(1.0, animated_height))
            
            x = i * bar_width
            bar_height_pixels = int(animated_height * height * 0.7)
            y = height - bar_height_pixels
            
            # Create glowing effect
            glow_color = QColor(255, 215, 0, 80)  # Gold glow
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(glow_color))
            painter.drawRect(x, y, bar_width - 1, bar_height_pixels)
            
            # Main bar with gradient
            bar_gradient = QLinearGradient(x, y, x, y + bar_height_pixels)
            bar_gradient.setColorAt(0, QColor(255, 69, 0))  # Orange red
            bar_gradient.setColorAt(1, QColor(255, 215, 0))  # Gold
            
            painter.setBrush(QBrush(bar_gradient))
            painter.drawRect(x + 1, y + 1, bar_width - 3, bar_height_pixels - 2)
    
    def draw_sharingan_circle(self, painter, width, height):
        """Draw Sharingan-inspired circular visualizer"""
        center_x = width // 2
        center_y = height // 2
        max_radius = min(width, height) // 3
        
        # Background
        painter.fillRect(self.rect(), QColor("#000000"))
        
        # Draw multiple concentric circles
        for i in range(5):
            radius = max_radius * (i + 1) / 5
            animated_radius = radius + 10 * np.sin(self.time + i)
            
            # Circle gradient
            gradient = QLinearGradient(
                center_x - animated_radius, center_y - animated_radius,
                center_x + animated_radius, center_y + animated_radius
            )
            
            if i % 2 == 0:
                gradient.setColorAt(0, QColor(255, 0, 0, 100))  # Red
                gradient.setColorAt(1, QColor(255, 0, 0, 50))
            else:
                gradient.setColorAt(0, QColor(255, 215, 0, 100))  # Gold
                gradient.setColorAt(1, QColor(255, 215, 0, 50))
            
            painter.setPen(QPen(QColor(255, 255, 255, 100), 2))
            painter.setBrush(QBrush(gradient))
            painter.drawEllipse(center_x - animated_radius, center_y - animated_radius,
                              animated_radius * 2, animated_radius * 2)
        
        # Draw tomoe (curved shapes)
        for i in range(3):
            angle = self.time + i * 2 * np.pi / 3
            tomoe_x = center_x + int(max_radius * 0.7 * np.cos(angle))
            tomoe_y = center_y + int(max_radius * 0.7 * np.sin(angle))
            
            painter.setPen(QPen(QColor(255, 0, 0), 3))
            painter.setBrush(QBrush(QColor(255, 0, 0)))
            painter.drawEllipse(tomoe_x - 5, tomoe_y - 5, 10, 10)
    
    def draw_chakra_waves(self, painter, width, height):
        """Draw flowing chakra waves"""
        # Background
        gradient = QLinearGradient(0, 0, width, height)
        gradient.setColorAt(0, QColor("#0066CC"))  # Blue
        gradient.setColorAt(1, QColor("#000000"))  # Black
        painter.fillRect(self.rect(), QBrush(gradient))
        
        # Draw multiple wave layers
        for layer in range(3):
            points = []
            amplitude = height * 0.1 * (layer + 1)
            frequency = 0.02 * (layer + 1)
            
            for x in range(0, width, 5):
                y = height // 2 + amplitude * np.sin(frequency * x + self.time + layer)
                points.append((x, y))
            
            # Draw wave
            if len(points) > 1:
                pen_color = QColor(0, 204, 255, 150 - layer * 30)  # Light blue
                painter.setPen(QPen(pen_color, 3 - layer))
                
                for i in range(len(points) - 1):
                    painter.drawLine(int(points[i][0]), int(points[i][1]),
                                   int(points[i + 1][0]), int(points[i + 1][1]))
    
    def draw_dragon_flames(self, painter, width, height):
        """Draw dragon flame effects"""
        # Background
        gradient = QLinearGradient(0, 0, width, height)
        gradient.setColorAt(0, QColor("#DC143C"))  # Crimson
        gradient.setColorAt(0.5, QColor("#800080"))  # Purple
        gradient.setColorAt(1, QColor("#000000"))  # Black
        painter.fillRect(self.rect(), QBrush(gradient))
        
        # Draw flame particles
        for _ in range(50):
            x = random.uniform(0, width)
            y = random.uniform(0, height)
            size = random.uniform(2, 15)
            
            # Flame gradient
            flame_gradient = QLinearGradient(x, y, x, y + size)
            flame_gradient.setColorAt(0, QColor(255, 255, 255, 200))  # White center
            flame_gradient.setColorAt(0.3, QColor(255, 69, 0, 150))   # Orange
            flame_gradient.setColorAt(0.7, QColor(220, 20, 60, 100))  # Crimson
            flame_gradient.setColorAt(1, QColor(128, 0, 128, 50))     # Purple
            
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(flame_gradient))
            painter.drawEllipse(x - size/2, y - size/2, size, size)
    
    def draw_particle_system(self, painter, width, height):
        """Draw chakra particle system"""
        # Update particles
        self.update_particles(width, height)
        
        # Background
        painter.fillRect(self.rect(), QColor("#1a1a1a"))
        
        # Draw particles
        for particle in self.chakra_particles:
            x = particle['x'] * width
            y = particle['y'] * height
            size = particle['size']
            
            # Particle color based on type
            if particle['color'] == 'gold':
                color = QColor(255, 215, 0, int(255 * particle['life']))
            elif particle['color'] == 'orange':
                color = QColor(255, 69, 0, int(255 * particle['life']))
            elif particle['color'] == 'red':
                color = QColor(220, 20, 60, int(255 * particle['life']))
            else:  # purple
                color = QColor(128, 0, 128, int(255 * particle['life']))
            
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(x - size/2, y - size/2, size, size)
    
    def update_particles(self, width, height):
        """Update particle positions and properties"""
        for particle in self.chakra_particles:
            # Update position
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Bounce off boundaries
            if particle['x'] <= 0 or particle['x'] >= 1:
                particle['vx'] *= -1
            if particle['y'] <= 0 or particle['y'] >= 1:
                particle['vy'] *= -1
            
            # Update life
            particle['life'] -= 0.01
            if particle['life'] <= 0:
                # Reset particle
                particle['x'] = random.uniform(0, 1)
                particle['y'] = random.uniform(0, 1)
                particle['life'] = random.uniform(0.5, 1.0)
                particle['color'] = random.choice(['gold', 'orange', 'red', 'purple'])

class VisualizerModeSelector(QWidget):
    """Widget for selecting visualization modes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.visualizer = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the mode selector UI"""
        from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🔮 Visualization Modes")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #FFD700;")
        layout.addWidget(title)
        
        # Mode buttons
        modes = [
            ("⚡ Chakra Bars", "chakra_bars"),
            ("👁️ Sharingan Circle", "sharingan_circle"),
            ("🌊 Chakra Waves", "chakra_waves"),
            ("🐉 Dragon Flames", "dragon_flames"),
            ("✨ Particle System", "particle_system")
        ]
        
        for mode_name, mode_id in modes:
            btn = QPushButton(mode_name)
            btn.setProperty("mode_id", mode_id)
            btn.clicked.connect(self.on_mode_selected)
            layout.addWidget(btn)
        
        layout.addStretch()
    
    def set_visualizer(self, visualizer):
        """Set the visualizer to control"""
        self.visualizer = visualizer
    
    def on_mode_selected(self):
        """Handle mode selection"""
        if self.visualizer:
            mode_id = self.sender().property("mode_id")
            self.visualizer.set_visualization_mode(mode_id) 