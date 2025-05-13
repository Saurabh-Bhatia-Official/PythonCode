import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLineEdit, QLabel, QComboBox, QTextEdit, QDialog,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon, QKeyEvent


class HistoryDialog(QDialog):
    def __init__(self, history_list, parent_calculator_dark_mode_active, parent=None):
        super().__init__(parent)
        self.history_list = history_list
        self.dark_mode_active = parent_calculator_dark_mode_active
        self.setWindowTitle("Calculation History")
        self.setMinimumSize(300, 400)

        layout = QVBoxLayout(self)

        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        self.populate_history()
        layout.addWidget(self.history_display)

        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear History")
        clear_button.clicked.connect(self.clear_history)
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)

        button_layout.addWidget(clear_button)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        self.update_theme(self.dark_mode_active)

    def populate_history(self):
        self.history_display.setPlainText("\n".join(reversed(self.history_list)))

    def clear_history(self):
        self.history_list.clear()
        self.populate_history()

    def update_theme(self, dark_mode):
        dialog_palette = QPalette()
        text_edit_palette = QPalette()
        button_stylesheet = ""

        if dark_mode:
            dialog_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            dialog_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            text_edit_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            text_edit_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            button_stylesheet = """
                QPushButton { background-color: #353535; color: white; border: 1px solid #555; padding: 5px; }
                QPushButton:hover { background-color: #4a4a4a; }
                QPushButton:pressed { background-color: #2a2a2a; }"""
        else:
            text_edit_palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white)
            text_edit_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
            button_stylesheet = "QPushButton { padding: 5px; }"

        self.setPalette(dialog_palette)
        self.history_display.setPalette(text_edit_palette)
        for button in self.findChildren(QPushButton):
            button.setStyleSheet(button_stylesheet)


class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Calculator")
        self.setMinimumSize(450, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.dark_mode = False
        self.current_theme = "light"

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.basic_calc = BasicCalculator(dark_mode_ref=lambda: self.dark_mode)
        self.scientific_calc = ScientificCalculator(dark_mode_ref=lambda: self.dark_mode)
        self.programmer_calc = ProgrammerCalculator(dark_mode_ref=lambda: self.dark_mode)

        self.tabs.addTab(self.basic_calc, "Basic")
        self.tabs.addTab(self.scientific_calc, "Scientific")
        self.tabs.addTab(self.programmer_calc, "Programmer")

        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        main_layout.addLayout(theme_layout)

        self.change_theme("Light")
        # self.setFocusPolicy(Qt.FocusPolicy.StrongFocus) # Main window can also handle keys if needed

    def change_theme(self, theme):
        self.current_theme = theme.lower()
        self.dark_mode = (self.current_theme == "dark")
        app_palette = QPalette()
        combo_stylesheet = ""
        if self.dark_mode:
            app_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            app_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            app_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            app_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            app_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
            app_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
            app_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            app_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            app_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            app_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            app_palette.setColor(QPalette.ColorRole.Highlight, QColor(142, 45, 197).lighter())
            app_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
            combo_stylesheet = """
                QComboBox { background-color: #353535; color: white; border: 1px solid #555; padding: 3px; }
                QComboBox::drop-down { border: none; }
                QComboBox QAbstractItemView { background-color: #252525; color: white; selection-background-color: #8e2dc5; }"""
        else:
            app = QApplication.instance()
            if app: app_palette = app.style().standardPalette()
            combo_stylesheet = ""

        self.setPalette(app_palette)
        self.tabs.setPalette(app_palette)
        self.theme_combo.setStyleSheet(combo_stylesheet)

        self.basic_calc.update_theme(self.dark_mode)
        self.scientific_calc.update_theme(self.dark_mode)
        self.programmer_calc.update_theme(self.dark_mode)

    # If you want main window to handle some global keys, uncomment and implement
    # def keyPressEvent(self, event: QKeyEvent):
    #     current_widget = self.tabs.currentWidget()
    #     if hasattr(current_widget, "keyPressEvent"):
    #         # Forward the event if the current tab widget wants to handle it specifically
    #         # However, child widgets usually get precedence for key events if they have focus.
    #         # current_widget.keyPressEvent(event)
    #         pass # Child widgets should handle their own key presses
    #     super().keyPressEvent(event)


class BaseCalculatorMixin:
    def _setup_common_styles(self, dark_mode):
        display_palette = QPalette()
        preview_label_palette = QPalette()  # For basic calc's preview
        conversion_label_color_css = ""  # For programmer calc's labels

        base_font_style = "padding: 8px; font-size: 15px;"  # Consistent button font

        general_button_style, equals_button_style, clear_button_style, hist_button_style, angle_mode_button_style = "", "", "", "", ""

        if dark_mode:
            display_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            display_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            preview_label_palette.setColor(QPalette.ColorRole.WindowText, QColor(180, 180, 180))
            conversion_label_color_css = "color: #b4b4b4;"

            general_button_style = f"QPushButton {{ background-color: #383838; color: white; border: 1px solid #505050; {base_font_style} }} QPushButton:hover {{ background-color: #484848; }} QPushButton:pressed {{ background-color: #282828; }}"
            equals_button_style = f"QPushButton {{ background-color: #006900; color: white; border: 1px solid #008000; {base_font_style} }} QPushButton:hover {{ background-color: #007f00; }} QPushButton:pressed {{ background-color: #004f00; }}"
            clear_button_style = f"QPushButton {{ background-color: #aa0000; color: white; border: 1px solid #c30000; {base_font_style} }} QPushButton:hover {{ background-color: #c30000; }} QPushButton:pressed {{ background-color: #880000; }}"
            hist_button_style = f"QPushButton {{ background-color: #2c3e50; color: white; border: 1px solid #34495e; {base_font_style} }} QPushButton:hover {{ background-color: #34495e; }} QPushButton:pressed {{ background-color: #1a242f; }}"
            angle_mode_button_style = f"QPushButton {{ background-color: #404040; color: white; border: 1px solid #555555; padding: 5px; font-size: 12px; }} QPushButton:hover {{ background-color: #505050; }} QPushButton:pressed {{ background-color: #303030; }}"
        else:  # Light Mode
            # display_palette uses default system palette for light mode base/text
            preview_label_palette.setColor(QPalette.ColorRole.WindowText, QColor(100, 100, 100))
            conversion_label_color_css = "color: #646464;"

            general_button_style = f"QPushButton {{ background-color: #f0f0f0; color: black; border: 1px solid #c0c0c0; {base_font_style} }} QPushButton:hover {{ background-color: #e0e0e0; }} QPushButton:pressed {{ background-color: #d0d0d0; }}"
            equals_button_style = f"QPushButton {{ background-color: #5cb85c; color: white; border: 1px solid #4cae4c; {base_font_style} }} QPushButton:hover {{ background-color: #4cae4c; }} QPushButton:pressed {{ background-color: #449d44; }}"
            clear_button_style = f"QPushButton {{ background-color: #d9534f; color: white; border: 1px solid #d43f3a; {base_font_style} }} QPushButton:hover {{ background-color: #c9302c; }} QPushButton:pressed {{ background-color: #ac2925; }}"
            hist_button_style = f"QPushButton {{ background-color: #aec9e0; color: black; border: 1px solid #9ab3c9; {base_font_style} }} QPushButton:hover {{ background-color: #9ab3c9; }} QPushButton:pressed {{ background-color: #869db3; }}"  # Light blue-gray
            angle_mode_button_style = f"QPushButton {{ background-color: #e0e0e0; color: black; border: 1px solid #bbbbbb; padding: 5px; font-size: 12px; }} QPushButton:hover {{ background-color: #d0d0d0; }} QPushButton:pressed {{ background-color: #c0c0c0; }}"

        if hasattr(self, 'display'): self.display.setPalette(display_palette)
        if hasattr(self, 'expression_preview_label'): self.expression_preview_label.setPalette(preview_label_palette)
        if hasattr(self, 'conversion_labels'):
            for l_widget in self.conversion_labels.values(): l_widget.setStyleSheet(conversion_label_color_css)

        for button in self.findChildren(QPushButton):
            btn_text = button.text()
            is_hist_btn = hasattr(button, '_is_hist_btn') and button._is_hist_btn
            is_angle_mode_btn = hasattr(self, 'angle_mode_button') and button is self.angle_mode_button

            if is_hist_btn:
                button.setStyleSheet(hist_button_style)
            elif is_angle_mode_btn:  # Specific for Scientific calc's RAD/DEG
                button.setStyleSheet(angle_mode_button_style)
            elif btn_text == '=':
                button.setStyleSheet(equals_button_style)
            elif btn_text in ['C', 'CE', 'Clr']:
                button.setStyleSheet(clear_button_style)
            else:
                button.setStyleSheet(general_button_style)

    def show_history_dialog(self):
        dialog = HistoryDialog(self.history, self.dark_mode_ref(), self)
        dialog.exec()

    def _get_history_icon(self):
        icon = QIcon.fromTheme("document-open-recent", QIcon.fromTheme("view-history"))
        # Fallback is handled by button text if icon.isNull()
        return icon

    def _find_and_click_button(self, target_text):
        for button in self.findChildren(QPushButton):
            is_hist_btn_target = (target_text == "Hist")  # Keyboard "H" or similar could map to "Hist"
            actual_btn_is_hist = hasattr(button, '_is_hist_btn') and button._is_hist_btn

            if is_hist_btn_target and actual_btn_is_hist:
                if button.isEnabled(): button.click(); return True
            elif button.text() == target_text:
                if button.isEnabled(): button.click(); return True
        return False


class BasicCalculator(QWidget, BaseCalculatorMixin):
    def __init__(self, dark_mode_ref):
        super().__init__()
        self.dark_mode_ref = dark_mode_ref
        self.current_input = ""
        self.stored_value = None
        self.current_operation = None
        self.reset_input_on_next_digit = False
        self.expression_preview_text = ""
        self.history = []
        self._init_keymap()
        self.init_ui()
        self._update_display()
        self.update_theme(self.dark_mode_ref())
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _init_keymap(self):
        self.key_map = {
            Qt.Key.Key_0: "0", Qt.Key.Key_1: "1", Qt.Key.Key_2: "2", Qt.Key.Key_3: "3",
            Qt.Key.Key_4: "4", Qt.Key.Key_5: "5", Qt.Key.Key_6: "6", Qt.Key.Key_7: "7",
            Qt.Key.Key_8: "8", Qt.Key.Key_9: "9",
            Qt.Key.Key_Period: ".",
            Qt.Key.Key_Plus: "+",
            Qt.Key.Key_Minus: "-",
            Qt.Key.Key_Asterisk: "*",
            Qt.Key.Key_Slash: "/",
            Qt.Key.Key_Enter: "=", Qt.Key.Key_Return: "=",
            Qt.Key.Key_Backspace: "⌫",
            Qt.Key.Key_Escape: "C",
            # Qt.Key.Key_Delete: "CE", # If desired for CE
            Qt.Key.Key_H: "Hist"  # For History
        }

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        char_from_event = event.text()
        target_button_text = None

        if key in self.key_map:
            target_button_text = self.key_map[key]
        elif char_from_event and char_from_event in ".+-*/":  # Allow direct operator chars
            target_button_text = char_from_event

        if target_button_text:
            if self._find_and_click_button(target_button_text):
                event.accept()
                return
        super().keyPressEvent(event)

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.expression_preview_label = QLabel()
        self.expression_preview_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.expression_preview_label.setFont(QFont("Arial", 14))
        self.expression_preview_label.setMinimumHeight(30)
        layout.addWidget(self.expression_preview_label)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont("Arial", 28))
        self.display.setMinimumHeight(60)
        layout.addWidget(self.display)

        button_layout = QGridLayout()
        buttons_config = [
            ('C', 0, 0), ('CE', 0, 1), ('⌫', 0, 2), ('Hist', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('±', 4, 0), ('0', 4, 1), ('.', 4, 2), ('+', 4, 3),
            ('=', 5, 0, 1, 4)
        ]

        for config in buttons_config:
            text, r, c = config[0], config[1], config[2]
            rs = config[3] if len(config) > 3 else 1
            cs = config[4] if len(config) > 4 else 1

            button = QPushButton(text)
            if text == 'Hist':
                hist_icon = self._get_history_icon()
                if not hist_icon.isNull():
                    button.setIcon(hist_icon); button.setIconSize(QSize(20, 20))
                else:
                    button.setText("🕒 Hist")
                button._is_hist_btn = True

            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            # Font is set by _setup_common_styles
            button.clicked.connect(self.on_button_click)
            button_layout.addWidget(button, r, c, rs, cs)
        layout.addLayout(button_layout)

    def _update_display(self):
        self.display.setText(self.current_input if self.current_input else "0")
        self.expression_preview_label.setText(self.expression_preview_text)

    def _perform_calculation(self, val1, val2, op):
        try:
            if op == '+': return val1 + val2
            if op == '-': return val1 - val2
            if op == '*': return val1 * val2
            if op == '/':
                if val2 == 0: return "Error: Div by 0"
                return val1 / val2
        except Exception:
            return "Error"
        return "Error: Unknown op"

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()
        if hasattr(sender, '_is_hist_btn') and sender._is_hist_btn: text = "Hist"

        try:
            if text.isdigit():
                if self.reset_input_on_next_digit: self.current_input = ""; self.reset_input_on_next_digit = False
                if self.current_input == "0" and text != "0":
                    self.current_input = text
                elif self.current_input == "0" and text == "0":
                    pass
                else:
                    self.current_input += text
            elif text == '.':
                if self.reset_input_on_next_digit: self.current_input = "0"; self.reset_input_on_next_digit = False
                if not self.current_input: self.current_input = "0"
                if '.' not in self.current_input: self.current_input += '.'
            elif text in '+-*/':
                if self.current_input:
                    val_current = float(self.current_input)
                    if self.stored_value is not None and self.current_operation:
                        result = self._perform_calculation(self.stored_value, val_current, self.current_operation)
                        if isinstance(result, str) and "Error" in result:
                            self.expression_preview_text = "";
                            self.current_input = result
                            self.stored_value = None;
                            self.current_operation = None;
                            self.reset_input_on_next_digit = True
                        else:
                            self.history.append(
                                f"{self.stored_value} {self.current_operation} {val_current} = {result}")
                            self.stored_value = result
                    else:
                        self.stored_value = val_current
                    self.current_operation = text
                    self.expression_preview_text = f"{self.stored_value:.10g} {self.current_operation} "
                    self.current_input = "";
                    self.reset_input_on_next_digit = False
                elif self.stored_value is not None:
                    self.current_operation = text
                    self.expression_preview_text = f"{self.stored_value:.10g} {self.current_operation} "
                    self.current_input = "";
                    self.reset_input_on_next_digit = False
            elif text == '=':
                if self.stored_value is not None and self.current_operation and self.current_input:
                    val_current = float(self.current_input)
                    full_expr = f"{self.stored_value:.10g} {self.current_operation} {val_current:.10g}"
                    result = self._perform_calculation(self.stored_value, val_current, self.current_operation)
                    if isinstance(result, str) and "Error" in result:
                        self.current_input = result;
                        self.expression_preview_text = f"{full_expr} ="
                        self.stored_value = None;
                        self.current_operation = None
                    else:
                        self.history.append(f"{full_expr} = {result:.10g}")
                        self.current_input = f"{result:.10g}";
                        self.expression_preview_text = f"{full_expr} ="
                        self.stored_value = result;
                        self.current_operation = None
                    self.reset_input_on_next_digit = True
            elif text == 'C':
                self.current_input = "";
                self.stored_value = None;
                self.current_operation = None
                self.expression_preview_text = "";
                self.reset_input_on_next_digit = False
            elif text == 'CE':
                if self.reset_input_on_next_digit and self.current_operation is None:
                    self.current_input = "";
                    self.stored_value = None;
                    self.current_operation = None
                    self.expression_preview_text = "";
                    self.reset_input_on_next_digit = False
                else:
                    self.current_input = ""; self.reset_input_on_next_digit = False
            elif text == '⌫':
                if self.reset_input_on_next_digit:
                    self.current_input = ""; self.reset_input_on_next_digit = False
                elif self.current_input:
                    self.current_input = self.current_input[:-1]
            elif text == '±':
                if self.current_input and self.current_input != "0":
                    if self.current_input.startswith('-'):
                        self.current_input = self.current_input[1:]
                    else:
                        self.current_input = '-' + self.current_input
                elif self.stored_value is not None and self.current_operation is None:
                    self.stored_value *= -1;
                    self.current_input = f"{self.stored_value:.10g}"
                    self.reset_input_on_next_digit = True
            elif text == 'Hist':
                self.show_history_dialog()
        except ValueError:
            self.current_input = "Error: Invalid Input"; self.reset_input_on_next_digit = True
        except Exception as e:
            print(f"BasicCalc Error: {e}"); self.current_input = "Error"; self.reset_input_on_next_digit = True
        self._update_display()

    def update_theme(self, dark_mode):
        self._setup_common_styles(dark_mode)


class ScientificCalculator(QWidget, BaseCalculatorMixin):
    def __init__(self, dark_mode_ref):
        super().__init__()
        self.dark_mode_ref = dark_mode_ref
        self.expression = ""
        self.history = []
        self.angle_mode = "RAD"
        self.safe_globals = {
            "math": math, "abs": abs, "pow": pow, "sqrt": math.sqrt,
            "log10": math.log10, "ln": math.log, "sin": math.sin,
            "cos": math.cos, "tan": math.tan, "asin": math.asin,
            "acos": math.acos, "atan": math.atan, "factorial": math.factorial,
            "pi": math.pi, "e": math.e, "radians": math.radians, "degrees": math.degrees
        }
        self._init_keymap()
        self.init_ui()
        self.update_theme(self.dark_mode_ref())
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _init_keymap(self):
        # Common keys
        self.key_map = {
            Qt.Key.Key_0: "0", Qt.Key.Key_1: "1", Qt.Key.Key_2: "2", Qt.Key.Key_3: "3",
            Qt.Key.Key_4: "4", Qt.Key.Key_5: "5", Qt.Key.Key_6: "6", Qt.Key.Key_7: "7",
            Qt.Key.Key_8: "8", Qt.Key.Key_9: "9",
            Qt.Key.Key_Period: ".",
            Qt.Key.Key_Plus: "+",
            Qt.Key.Key_Minus: "-",
            Qt.Key.Key_Asterisk: "*",  # Button might be x^y or other
            Qt.Key.Key_Slash: "/",
            Qt.Key.Key_Enter: "=", Qt.Key.Key_Return: "=",
            Qt.Key.Key_Backspace: "⌫",
            Qt.Key.Key_Escape: "C",  # Clear All
            Qt.Key.Key_ParenLeft: "(",
            Qt.Key.Key_ParenRight: ")",
            Qt.Key.Key_Percent: "%",
            Qt.Key.Key_H: "Hist"  # For History
            # Add mappings for s (sin), c (cos), t (tan), l (log), etc. if desired
        }
        # Direct char to button text (if button text matches char)
        self.char_to_button_map = {
            's': 'sin', 'c': 'cos', 't': 'tan',  # Example, if buttons are "sin", "cos"
            'l': 'log', 'n': 'ln',  # Needs button "ln" for 'n'
            'p': 'π', 'e': 'e', '^': 'x^y'
        }

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        char_from_event = event.text()
        target_button_text = None

        if key in self.key_map:
            target_button_text = self.key_map[key]
        elif char_from_event:
            if char_from_event.lower() in self.char_to_button_map:
                target_button_text = self.char_to_button_map[char_from_event.lower()]
            elif char_from_event in "()+-*/.%":  # General chars that might be button texts
                target_button_text = char_from_event

        if target_button_text:
            if self._find_and_click_button(target_button_text):
                event.accept()
                return
        super().keyPressEvent(event)

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont("Arial", 24))
        self.display.setMinimumHeight(50)
        layout.addWidget(self.display)

        top_row_layout = QHBoxLayout()
        self.angle_mode_button = QPushButton(self.angle_mode)
        self.angle_mode_button.setCheckable(True)  # Checkable for RAD/DEG state
        self.angle_mode_button.setChecked(self.angle_mode == "RAD")  # Initial check state
        self.angle_mode_button.clicked.connect(self.toggle_angle_mode)
        top_row_layout.addWidget(self.angle_mode_button)

        hist_button_sci = QPushButton()
        hist_icon_sci = self._get_history_icon()
        if not hist_icon_sci.isNull():
            hist_button_sci.setIcon(hist_icon_sci); hist_button_sci.setIconSize(QSize(20, 20))
        else:
            hist_button_sci.setText("🕒 Hist")
        hist_button_sci._is_hist_btn = True
        hist_button_sci.clicked.connect(self.show_history_dialog)
        top_row_layout.addWidget(hist_button_sci)
        layout.addLayout(top_row_layout)

        button_layout = QGridLayout()
        buttons = [
            ('(', 0, 0), (')', 0, 1), ('%', 0, 2), ('CE', 0, 3), ('C', 0, 4),
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('log', 1, 3), ('ln', 1, 4),
            ('x^y', 2, 0), ('x²', 2, 1), ('x³', 2, 2), ('√', 2, 3), ('∛', 2, 4),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3), ('⌫', 3, 4),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3), ('π', 4, 4),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3), ('e', 5, 4),
            ('0', 6, 0, 1, 2), ('.', 6, 2), ('±', 6, 3), ('+', 6, 4),
            ('=', 7, 0, 1, 5)
        ]
        for item in buttons:
            text, r, c = item[0], item[1], item[2]
            rs = item[3] if len(item) > 3 else 1
            cs = item[4] if len(item) > 4 else 1
            button = QPushButton(text)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.clicked.connect(self.on_button_click)
            button_layout.addWidget(button, r, c, rs, cs)
        layout.addLayout(button_layout)
        self._update_display()

    def toggle_angle_mode(self):
        if self.angle_mode_button.isChecked():  # Is RAD
            self.angle_mode = "RAD"
        else:  # Is DEG
            self.angle_mode = "DEG"
        self.angle_mode_button.setText(self.angle_mode)
        # self.update_theme(self.dark_mode_ref()) # Style already applied in _setup_common_styles

    def _update_display(self):
        self.display.setText(self.expression if self.expression else "0")

    def _prepare_eval_string(self, expr_str):
        # Basic replacements
        replacements = {
            'π': 'pi', 'e': 'e', '√(': 'sqrt(', '∛(': 'pow(',  # For ∛(x) -> pow(x,1/3)
            'x²': '**2', 'x³': '**3', 'x^y': '**', 'log(': 'log10(', 'ln(': 'ln('
        }
        for old, new in replacements.items():
            expr_str = expr_str.replace(old, new)

        # Handle trig functions with angle mode
        # This is a simplified approach. A proper parser would be more robust.
        # For now, it assumes functions are followed by '('.
        import re
        def replace_trig(match):
            func_name = match.group(1)
            # Correctly access math module functions via safe_globals
            if self.angle_mode == "DEG":
                # Wrap argument in radians() for math functions
                return f"{func_name}(radians("
            return f"{func_name}("  # Already in radians

        # Need to be careful if 'radians' or 'degrees' are already in safe_globals for direct use
        # The eval string needs to call math.radians if we use it this way.
        # Simplified: expect user to use radians for math functions directly if using eval,
        # or the buttons handle this. The _prepare_eval_string should make it eval-ready.

        # For eval, ensure math.sin etc. are called.
        # If button "sin" adds "sin(" to expression, and we want DEG mode:
        # "sin(30)" should become "math.degrees(math.asin(math.radians(math.sin(math.radians(30)))))"
        # This is too complex for simple string replacement.
        # The current design directly puts math functions into safe_globals.
        # If a user types "sin(pi/2)", it works.
        # If they click "sin", then "30", then ")", in DEG mode, we need "sin(radians(30))".

        # Let's assume _prepare_eval_string is for text already in a mostly Python-math-compatible form.
        # The on_button_click for 'sin' etc. should handle adding 'radians()' if in DEG mode.

        # Correcting ∛: if "pow(" was inserted, it might need a second argument for 1/3
        expr_str = re.sub(r'pow\((\d+)\)', r'pow(\1, 1/3)', expr_str)  # If ∛(number) becomes pow(number)

        return expr_str

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()
        try:
            if text == '=':
                if self.expression:
                    processed_expr = self.expression
                    # Smartly add closing parentheses for radians if needed
                    open_rad = processed_expr.count("radians(")
                    open_paren = processed_expr.count("(")
                    close_paren = processed_expr.count(")")

                    # Add necessary closing parens for radians wrapper
                    # and then for the function itself
                    # This is heuristic and might not be perfect
                    needed_closing_for_radians = open_rad - processed_expr.count("))")  # Approx

                    # Add general closing parentheses
                    needed_closing_general = open_paren - close_paren

                    processed_expr += ")" * (needed_closing_general)

                    eval_str = self._prepare_eval_string(processed_expr)
                    print(f"Evaluating (Sci): {eval_str}")
                    result = eval(eval_str, {"__builtins__": {}}, self.safe_globals)
                    self.history.append(f"{self.expression} = {result:.10g}")
                    self.expression = f"{result:.10g}"
            elif text == 'C':
                self.expression = ""
            elif text == 'CE':
                self.expression = ""  # Simplified
            elif text == '⌫':
                self.expression = self.expression[:-1]
            elif text == '±':
                if self.expression and self.expression.lstrip('-').replace('.', '', 1).isdigit():
                    if self.expression.startswith('-'):
                        self.expression = self.expression[1:]
                    else:
                        self.expression = '-' + self.expression
                elif self.expression and not self.expression.startswith("-("):  # Add negation to whole expression
                    self.expression = f"-({self.expression})"
                elif self.expression.startswith("-("):  # Remove negation
                    self.expression = self.expression[2:-1]

            elif text in ['sin', 'cos', 'tan']:  # Trig functions
                self.expression += text + ("(radians(" if self.angle_mode == "DEG" else "(")
            elif text in ['log', 'ln', '√', '∛', 'asin', 'acos', 'atan']:  # Other functions needing (
                # For ∛, we'll use 'pow(' and expect a number and ',1/3)' later or handle it in eval.
                fn_text = text
                if text == '√':
                    fn_text = 'sqrt'
                elif text == '∛':
                    fn_text = 'pow'  # Will become pow(val, 1/3)
                elif text == 'log':
                    fn_text = 'log10'
                self.expression += fn_text + "("
                if text == '∛': self.expression += ""  # Expect user to type number, then we add ",1/3)" later or on =
            elif text == 'x²':
                self.expression += "**2"
            elif text == 'x³':
                self.expression += "**3"
            elif text == 'x^y':
                self.expression += "**"
            else:
                self.expression += text
        except Exception as e:
            self.expression = "Error"
            print(f"ScientificCalc Error: {e}\nExpression was: {self.expression}")
        self._update_display()

    def update_theme(self, dark_mode):
        self._setup_common_styles(dark_mode)


class ProgrammerCalculator(QWidget, BaseCalculatorMixin):
    def __init__(self, dark_mode_ref):
        super().__init__()
        self.dark_mode_ref = dark_mode_ref
        self.current_value_int = 0
        self.input_str = "0"
        self.display_base = "DEC"
        self.history = []
        self.stored_value_int = None
        self.pending_operation = None
        self._init_keymap()
        self.init_ui()
        self.update_theme(self.dark_mode_ref())
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _init_keymap(self):
        self.key_map = {
            Qt.Key.Key_0: "0", Qt.Key.Key_1: "1", Qt.Key.Key_2: "2", Qt.Key.Key_3: "3",
            Qt.Key.Key_4: "4", Qt.Key.Key_5: "5", Qt.Key.Key_6: "6", Qt.Key.Key_7: "7",
            Qt.Key.Key_8: "8", Qt.Key.Key_9: "9",
            Qt.Key.Key_A: "A", Qt.Key.Key_B: "B", Qt.Key.Key_C: "C",  # Hex C, not Clear C
            Qt.Key.Key_D: "D", Qt.Key.Key_E: "E", Qt.Key.Key_F: "F",
            Qt.Key.Key_Plus: "+", Qt.Key.Key_Minus: "-",
            Qt.Key.Key_Asterisk: "*", Qt.Key.Key_Slash: "/",
            Qt.Key.Key_Enter: "=", Qt.Key.Key_Return: "=",
            Qt.Key.Key_Backspace: "⌫",
            Qt.Key.Key_Escape: "Clr",  # Clear All for Programmer
            Qt.Key.Key_ParenLeft: "(", Qt.Key.Key_ParenRight: ")",
            Qt.Key.Key_M: "MOD",  # Example for MOD
            Qt.Key.Key_H: "Hist"  # For History
            # Add more for AND, OR, XOR, Lsh, Rsh if desired (e.g., '&', '|', '^', '<', '>')
        }
        # Mapping from typed character to button text if they differ or for convenience
        self.char_to_button_map = {
            '&': "AND", '|': "OR", '^': "XOR",  # If buttons are "AND", "OR", "XOR"
            '<': "Lsh", '>': "Rsh"
        }

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        char_from_event = event.text()
        target_button_text = None

        if key in self.key_map:
            # Special handling for 'C' key if it means Clear vs Hex 'C'
            if key == Qt.Key.Key_C and self.display_base == "HEX":
                target_button_text = "C"  # The Hex digit C
            else:
                target_button_text = self.key_map[key]
        elif char_from_event:
            # Use char_from_event directly if it's a digit or A-F (for current base)
            valid_chars = "0123456789ABCDEF"  # Max set
            if self.display_base == "DEC":
                valid_chars = "0123456789"
            elif self.display_base == "OCT":
                valid_chars = "01234567"
            elif self.display_base == "BIN":
                valid_chars = "01"

            if char_from_event.upper() in valid_chars:
                target_button_text = char_from_event.upper()
            elif char_from_event in self.char_to_button_map:
                target_button_text = self.char_to_button_map[char_from_event]
            elif char_from_event in "+-*/()":  # General operators
                target_button_text = char_from_event

        if target_button_text:
            if self._find_and_click_button(target_button_text):
                event.accept()
                return
        super().keyPressEvent(event)

    def init_ui(self):
        layout = QVBoxLayout(self)
        top_bar_layout = QHBoxLayout()
        self.num_system_combo = QComboBox()
        self.num_system_combo.addItems(["DEC", "HEX", "BIN", "OCT"])
        self.num_system_combo.currentTextChanged.connect(self.change_base)
        top_bar_layout.addWidget(self.num_system_combo)

        hist_button_prog = QPushButton()
        hist_icon_prog = self._get_history_icon()
        if not hist_icon_prog.isNull():
            hist_button_prog.setIcon(hist_icon_prog); hist_button_prog.setIconSize(QSize(20, 20))
        else:
            hist_button_prog.setText("🕒 Hist")
        hist_button_prog._is_hist_btn = True
        hist_button_prog.clicked.connect(self.show_history_dialog)
        top_bar_layout.addWidget(hist_button_prog)
        layout.addLayout(top_bar_layout)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont("Arial", 20))  # Main display font
        layout.addWidget(self.display)

        self.conversion_labels = {}
        conversion_layout = QGridLayout()
        bases_for_labels = ["HEX", "DEC", "OCT", "BIN"]
        for i, base_name in enumerate(bases_for_labels):
            label_text_widget = QLabel(f"{base_name}:")
            label_text_widget.setFont(QFont("Arial", 9))  # Smaller font for base names
            val_label = QLabel("0")
            val_label.setFont(QFont("Monospace", 10))  # Monospace for number alignment
            conversion_layout.addWidget(label_text_widget, i, 0)
            conversion_layout.addWidget(val_label, i, 1, 1, 3)  # Value spans more columns
            self.conversion_labels[base_name] = val_label
        layout.addLayout(conversion_layout)

        button_layout = QGridLayout()
        self.hex_buttons = {}
        prog_buttons = [
            ('A', 0, 0), ('B', 0, 1), ('AND', 0, 2), ('OR', 0, 3), ('XOR', 0, 4), ('NOT', 0, 5),
            ('C', 1, 0), ('D', 1, 1), ('Lsh', 1, 2), ('Rsh', 1, 3), ('MOD', 1, 4), ('(', 1, 5),
            ('E', 2, 0), ('F', 2, 1), ('7', 2, 2), ('8', 2, 3), ('9', 2, 4), (')', 2, 5),
            ('CE', 3, 0), ('Clr', 3, 1), ('4', 3, 2), ('5', 3, 3), ('6', 3, 4), ('/', 3, 5),
            ('⌫', 4, 0), ('±', 4, 1), ('1', 4, 2), ('2', 4, 3), ('3', 4, 4), ('*', 4, 5),
            ('0', 5, 0, 1, 2), ('.', 5, 2), ('-', 5, 3), ('+', 5, 4), (' ', 5, 5),  # 0 spans 2, . is placeholder
            ('=', 6, 0, 1, 6)
        ]
        for item in prog_buttons:
            text, r, c = item[0], item[1], item[2]
            rs = item[3] if len(item) > 3 else 1
            cs = item[4] if len(item) > 4 else 1
            if text.strip() == "": continue
            button = QPushButton(text)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.clicked.connect(self.on_button_click)
            button_layout.addWidget(button, r, c, rs, cs)
            if text in "ABCDEF": self.hex_buttons[text] = button
            if text == '.': button.setEnabled(False)  # Period not used in integer prog calc

        layout.addLayout(button_layout)
        self.change_base(self.display_base)
        self._update_displays()

    def _update_displays(self):
        base_map_out = {"HEX": hex, "DEC": str, "OCT": oct, "BIN": bin}
        val_to_display_str = self.input_str
        if not self.input_str and self.pending_operation:  # Show stored value if input is empty during op
            val_to_display_str = \
            base_map_out[self.display_base](self.stored_value_int).upper().split('X')[-1].split('B')[-1].split('O')[-1]
            if not val_to_display_str: val_to_display_str = "0"
        elif not self.input_str:
            val_to_display_str = "0"
        self.display.setText(val_to_display_str)

        current_val_for_conversion = self.current_value_int
        if self.input_str:  # If there's active input, use that for conversion display
            try:
                current_val_for_conversion = int(self.input_str,
                                                 {"HEX": 16, "DEC": 10, "OCT": 8, "BIN": 2}[self.display_base])
            except ValueError:
                pass  # Keep last valid current_value_int

        for base_name, label_widget in self.conversion_labels.items():
            raw_val = base_map_out[base_name](current_val_for_conversion).upper()
            # Strip 0x, 0b, 0o prefixes
            processed_val = raw_val.split('X')[-1].split('B')[-1].split('O')[-1]
            label_widget.setText(processed_val if processed_val else "0")

    def change_base(self, new_base):
        base_map_out = {"HEX": hex, "DEC": str, "OCT": oct, "BIN": bin}
        self.display_base = new_base
        # Convert current_value_int to the new base's string representation for input_str
        raw_new_input_str = base_map_out[new_base](self.current_value_int).upper()
        self.input_str = raw_new_input_str.split('X')[-1].split('B')[-1].split('O')[-1]
        if not self.input_str: self.input_str = "0"

        for btn_widget in self.findChildren(QPushButton):
            txt = btn_widget.text()
            if txt in "0123456789ABCDEF":  # Hex/Digit buttons
                is_enabled = False
                if txt in "01":
                    is_enabled = True  # Always enable 0, 1
                elif self.display_base == "OCT" and txt in "234567":
                    is_enabled = True
                elif self.display_base == "DEC" and txt in "23456789":
                    is_enabled = True
                elif self.display_base == "HEX" and txt in "23456789ABCDEF":
                    is_enabled = True
                btn_widget.setEnabled(is_enabled)
            elif txt == '.':
                btn_widget.setEnabled(False)  # Disable dot for all prog bases

        self._update_displays()

    def _get_current_input_as_int(self):
        base_map_in = {"HEX": 16, "DEC": 10, "OCT": 8, "BIN": 2}
        try:
            return int(self.input_str if self.input_str else "0", base_map_in[self.display_base])
        except ValueError:
            return self.current_value_int

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()
        if hasattr(sender, '_is_hist_btn') and sender._is_hist_btn: text = "Hist"

        valid_chars_map = {"HEX": "0123456789ABCDEF", "DEC": "0123456789", "OCT": "01234567", "BIN": "01"}
        try:
            if text in valid_chars_map[self.display_base]:
                if self.input_str == "0" and text != "0":
                    self.input_str = text
                elif self.input_str == "0" and text == "0":
                    pass  # Avoid multiple zeros
                else:
                    self.input_str += text
                self.current_value_int = self._get_current_input_as_int()
            elif text == 'Clr':
                self.input_str = "0";
                self.current_value_int = 0
                self.stored_value_int = None;
                self.pending_operation = None
            elif text == 'CE':
                self.input_str = "0"; self.current_value_int = 0
            elif text == '⌫':
                self.input_str = self.input_str[:-1] if len(self.input_str) > 1 else "0"
                self.current_value_int = self._get_current_input_as_int()
            elif text == '±':
                self.current_value_int = -self._get_current_input_as_int()
                self.change_base("DEC")  # Switch to DEC to show sign naturally
                self.num_system_combo.setCurrentText("DEC")  # Update combo box
            elif text in ['AND', 'OR', 'XOR', 'MOD', 'Lsh', 'Rsh', '+', '-', '*', '/']:
                current_op_val = self._get_current_input_as_int()
                if self.stored_value_int is not None and self.pending_operation:
                    op_result = self.perform_prog_op(self.stored_value_int, current_op_val, self.pending_operation)
                    if isinstance(op_result, str) and "Error" in op_result:  # Error occurred
                        self.input_str = op_result;
                        self.current_value_int = 0;
                        self.stored_value_int = None;
                        self.pending_operation = None
                    else:
                        self.history.append(
                            f"{self.stored_value_int} {self.pending_operation} {current_op_val} = {op_result} (DEC)")
                        self.stored_value_int = op_result;
                        self.current_value_int = op_result
                else:
                    self.stored_value_int = current_op_val
                self.pending_operation = text
                self.input_str = ""  # Ready for next number, display will show stored_value_int in current base
            elif text == 'NOT':
                self.current_value_int = ~self._get_current_input_as_int()
                self.history.append(f"NOT {self.input_str} = {self.current_value_int} (DEC)")
                self.change_base("DEC")  # Result of NOT often shown in DEC
                self.num_system_combo.setCurrentText("DEC")
            elif text == '=':
                if self.pending_operation and self.stored_value_int is not None:
                    second_operand = self._get_current_input_as_int()
                    op_result = self.perform_prog_op(self.stored_value_int, second_operand, self.pending_operation)
                    if isinstance(op_result, str) and "Error" in op_result:
                        self.input_str = op_result;
                        self.current_value_int = 0
                    else:
                        self.history.append(
                            f"{self.stored_value_int} {self.pending_operation} {second_operand} = {op_result} (DEC)")
                        self.current_value_int = op_result
                    self.change_base(self.display_base)  # Updates input_str from current_value_int
                    self.stored_value_int = None  # Reset for next independent calculation
                    self.pending_operation = None
            elif text == 'Hist':
                self.show_history_dialog()
        except Exception as e:
            self.input_str = "Error"; print(f"ProgrammerCalc Error: {e}")
        self._update_displays()

    def perform_prog_op(self, val1, val2, op):
        try:
            if op == 'AND': return val1 & val2
            if op == 'OR': return val1 | val2
            if op == 'XOR': return val1 ^ val2
            if op == 'MOD': return val1 % val2 if val2 != 0 else "Error: Mod by 0"
            if op == 'Lsh': return val1 << val2
            if op == 'Rsh': return val1 >> val2
            if op == '+': return val1 + val2
            if op == '-': return val1 - val2
            if op == '*': return val1 * val2
            if op == '/': return val1 // val2 if val2 != 0 else "Error: Div by 0"
        except Exception as e:
            return f"Error: {e}"
        return "Error: Op?"

    def update_theme(self, dark_mode):
        self._setup_common_styles(dark_mode)
        combo_stylesheet = ""
        if dark_mode:
            combo_stylesheet = """
                QComboBox { background-color: #353535; color: white; border: 1px solid #555; padding: 3px; margin-bottom: 5px;}
                QComboBox::drop-down { border: none; }
                QComboBox QAbstractItemView { background-color: #252525; color: white; selection-background-color: #8e2dc5; }"""
        else:
            combo_stylesheet = "QComboBox { margin-bottom: 5px; }"  # Add margin for spacing
        self.num_system_combo.setStyleSheet(combo_stylesheet)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = CalculatorApp()
    calculator.show()
    sys.exit(app.exec())