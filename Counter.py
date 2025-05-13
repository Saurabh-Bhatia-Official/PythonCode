import sys
import logging
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CounterApp(QWidget):
    """
    A professional counter application with theme support using PyQt6.
    """

    WINDOW_TITLE = "Professional Counter with Themes"
    WINDOW_WIDTH = 350
    WINDOW_HEIGHT = 250
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE = 40

    def __init__(self) -> None:
        super().__init__()
        self.counter_value: int = 0
        self.current_theme: str = "light"
        self._init_ui()

    def _init_ui(self) -> None:
        """Initializes the user interface."""
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # Layouts
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        theme_layout = QHBoxLayout()

        # Counter display
        self.counter_label = QLabel(str(self.counter_value))
        self.counter_label.setFont(QFont(self.FONT_FAMILY, self.FONT_SIZE))
        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Theme toggle button
        self.theme_toggle_btn = QPushButton("Switch to Dark Theme")
        self.theme_toggle_btn.clicked.connect(self._toggle_theme)

        # Action buttons
        self.increment_btn = QPushButton("Increment")
        self.increment_btn.clicked.connect(self._increment)

        self.decrement_btn = QPushButton("Decrement")
        self.decrement_btn.clicked.connect(self._decrement)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self._reset)

        # Assemble layouts
        button_layout.addWidget(self.decrement_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.increment_btn)

        theme_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        theme_layout.addWidget(self.theme_toggle_btn)
        theme_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        main_layout.addWidget(self.counter_label)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(theme_layout)

        self.setLayout(main_layout)

        self._apply_theme()  # Apply initial theme

    def _increment(self) -> None:
        self.counter_value += 1
        logging.info(f"Counter incremented to {self.counter_value}")
        self._update_label()

    def _decrement(self) -> None:
        self.counter_value -= 1
        logging.info(f"Counter decremented to {self.counter_value}")
        self._update_label()

    def _reset(self) -> None:
        self.counter_value = 0
        logging.info("Counter reset to 0")
        self._update_label()

    def _update_label(self) -> None:
        self.counter_label.setText(str(self.counter_value))

    def _toggle_theme(self) -> None:
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        logging.info(f"Switched to {self.current_theme} theme")
        self._apply_theme()

    def _apply_theme(self) -> None:
        """Apply current theme to the application."""
        if self.current_theme == "dark":
            self.setStyleSheet("""
                QWidget {
                    background-color: #2b2b2b;
                    color: #f0f0f0;
                }
                QPushButton {
                    background-color: #444;
                    color: white;
                    border: 1px solid #666;
                    padding: 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #555;
                }
            """)
            self.theme_toggle_btn.setText("Switch to Light Theme")
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f5f5f5;
                    color: #2b2b2b;
                }
                QPushButton {
                    background-color: #ffffff;
                    color: #000;
                    border: 1px solid #aaa;
                    padding: 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            self.theme_toggle_btn.setText("Switch to Dark Theme")


def run_app() -> None:
    app = QApplication(sys.argv)
    window = CounterApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
