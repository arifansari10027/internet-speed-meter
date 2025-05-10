import sys
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QMenu, QAction, QSystemTrayIcon, QColorDialog, QSlider, QInputDialog
from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPainter, QColor
from PyQt5.QtSvg import QSvgRenderer  # Added missing import

class SpeedWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize drag_position and other attributes
        self.drag_position = None
        self.icon_size = 30  # Default icon size
        self.show_labels = True  # Default: show speed labels

        # Window Settings
        self.setWindowTitle("Internet Speed Meter")
        self.setGeometry(100, 100, 250, 50)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #2E3440; border-radius: 10px;")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.9)

        # Main Layout (Single Row)
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(10)

        # Download Section
        self.download_icon = QLabel()
        self.download_icon.setFixedSize(self.icon_size, self.icon_size)
        self.download_icon.setPixmap(self.create_icon("download").scaled(self.icon_size, self.icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.download_label = QLabel("0.00 KB/s")
        self.download_label.setFont(QFont('Arial', 12))
        self.download_label.setStyleSheet("color: #00FF00; margin-left: 5px;")

        self.download_container = QHBoxLayout()
        self.download_container.addWidget(self.download_icon)
        self.download_container.addWidget(self.download_label)
        self.main_layout.addLayout(self.download_container)

        # Upload Section
        self.upload_icon = QLabel()
        self.upload_icon.setFixedSize(self.icon_size, self.icon_size)
        self.upload_icon.setPixmap(self.create_icon("upload").scaled(self.icon_size, self.icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.upload_label = QLabel("0.00 KB/s")
        self.upload_label.setFont(QFont('Arial', 12))
        self.upload_label.setStyleSheet("color: #FFA500; margin-left: 5px;")

        self.upload_container = QHBoxLayout()
        self.upload_container.addWidget(self.upload_icon)
        self.upload_container.addWidget(self.upload_label)
        self.main_layout.addLayout(self.upload_container)

        self.setLayout(self.main_layout)

        # Track previous counters
        self.prev_counters = psutil.net_io_counters()

        # Timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_speed)
        self.timer.start(1000)

        # System Tray
        self.tray_icon = QSystemTrayIcon(self.create_tray_icon(), self)
        self.tray_icon.setVisible(True)
        tray_menu = QMenu(self)
        self.add_customization_menu(tray_menu)
        self.tray_icon.setContextMenu(tray_menu)

    def create_icon(self, icon_type):
        # Load PNG icons (assumes download_icon.png and upload_icon.png are in the same directory)
        if icon_type == "download":
            pixmap = QPixmap("download_icon.png")
        else:
            pixmap = QPixmap("upload_icon.png")
        if pixmap.isNull():
            # Fallback if PNG is not found
            print(f"Warning: {icon_type}_icon.png not found, using default color square as fallback.")
            pixmap = QPixmap(30, 30)
            pixmap.fill(QColor("#00FF00" if icon_type == "download" else "#FFA500"))
        return pixmap

    def create_tray_icon(self):
        # Simple tray icon (cloud using SVG)
        svg_content = """
        <svg width="16" height="16" xmlns="http://www.w3.org/2000/svg">
            <path d="M2 8 A3 3 0 0 1 5 5 H11 A3 3 0 0 1 14 8 A2 2 0 0 1 12 10 H4 A2 2 0 0 1 2 8 Z" fill="#D8DEE9"/>
        </svg>
        """
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer = QSvgRenderer(bytearray(svg_content.encode('utf-8')))
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)

    def update_speed(self):
        current_counters = psutil.net_io_counters()
        download = (current_counters.bytes_recv - self.prev_counters.bytes_recv) / 1024  # KB/s
        upload = (current_counters.bytes_sent - self.prev_counters.bytes_sent) / 1024  # KB/s

        self.download_label.setText(f"{download:.2f} KB/s")
        self.upload_label.setText(f"{upload:.2f} KB/s")

        self.prev_counters = current_counters

    def add_customization_menu(self, tray_menu):
        # Change Background Color
        color_action = QAction("Change Background Color", self)
        color_action.triggered.connect(self.change_background_color)
        tray_menu.addAction(color_action)

        # Toggle Dark/Light Theme
        theme_action = QAction("Toggle Dark/Light Theme", self)
        theme_action.triggered.connect(self.toggle_theme)
        tray_menu.addAction(theme_action)

        # Change Icon Size
        icon_size_menu = QMenu("Change Icon Size", self)
        size_20_action = QAction("20px", self)
        size_20_action.triggered.connect(lambda: self.change_icon_size(20))
        size_30_action = QAction("30px", self)
        size_30_action.triggered.connect(lambda: self.change_icon_size(30))
        size_40_action = QAction("40px", self)
        size_40_action.triggered.connect(lambda: self.change_icon_size(40))
        icon_size_menu.addAction(size_20_action)
        icon_size_menu.addAction(size_30_action)
        icon_size_menu.addAction(size_40_action)
        tray_menu.addMenu(icon_size_menu)

        # Adjust Opacity
        opacity_action = QAction("Adjust Opacity", self)
        opacity_action.triggered.connect(self.adjust_opacity)
        tray_menu.addAction(opacity_action)

        # Toggle Speed Labels
        toggle_labels_action = QAction("Hide Speed Labels" if self.show_labels else "Show Speed Labels", self)
        toggle_labels_action.triggered.connect(self.toggle_labels)
        tray_menu.addAction(toggle_labels_action)

        # Quit
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet(f"background-color: {color.name()}; border-radius: 10px;")

    def toggle_theme(self):
        if "background-color: #2E3440" in self.styleSheet():
            self.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")
            self.download_label.setStyleSheet("color: #00FF00; margin-left: 5px;")
            self.upload_label.setStyleSheet("color: #FFA500; margin-left: 5px;")
        else:
            self.setStyleSheet("background-color: #2E3440; border-radius: 10px;")
            self.download_label.setStyleSheet("color: #00FF00; margin-left: 5px;")
            self.upload_label.setStyleSheet("color: #FFA500; margin-left: 5px;")

    def change_icon_size(self, size):
        self.icon_size = size
        self.download_icon.setFixedSize(self.icon_size, self.icon_size)
        self.upload_icon.setFixedSize(self.icon_size, self.icon_size)
        self.download_icon.setPixmap(self.create_icon("download").scaled(self.icon_size, self.icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.upload_icon.setPixmap(self.create_icon("upload").scaled(self.icon_size, self.icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # Adjust widget size based on icon size
        base_width = (self.icon_size * 2) + 150  # Approximate width considering labels
        if not self.show_labels:
            base_width = self.icon_size * 2 + 20
        self.setFixedSize(base_width, max(self.icon_size + 10, 50))

    def adjust_opacity(self):
        opacity, ok = QInputDialog.getDouble(self, "Adjust Opacity", "Opacity (0.1 to 1.0):", self.windowOpacity(), 0.1, 1.0, 1)
        if ok:
            self.setWindowOpacity(opacity)

    def toggle_labels(self):
        self.show_labels = not self.show_labels
        self.download_label.setVisible(self.show_labels)
        self.upload_label.setVisible(self.show_labels)
        # Update context menu text
        for action in self.tray_icon.contextMenu().actions():
            if "Speed Labels" in action.text():
                action.setText("Hide Speed Labels" if self.show_labels else "Show Speed Labels")
        # Adjust widget size
        base_width = (self.icon_size * 2) + 150 if self.show_labels else (self.icon_size * 2 + 20)
        self.setFixedSize(base_width, max(self.icon_size + 10, 50))

    def contextMenuEvent(self, event):
        # Show the same context menu as the tray icon when right-clicking the widget
        menu = self.tray_icon.contextMenu()
        menu.exec_(event.globalPos())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = SpeedWidget()
    widget.show()
    sys.exit(app.exec_())