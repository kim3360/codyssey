import sys
from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontMetrics
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from calculator import Calculator


class CalculatorWindow(QWidget):
    DISPLAY_MAX_PT = 48
    DISPLAY_MIN_PT = 18

    def __init__(self):
        super().__init__()
        self._calc = Calculator()
        self.setWindowTitle('계산기')
        self.setFixedSize(320, 480)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        self._display = QLabel('0')
        self._display.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self._display.setMinimumHeight(72)
        self._display_font_pt = self.DISPLAY_MAX_PT
        self._apply_display_font()
        root.addWidget(self._display)

        grid = QGridLayout()
        grid.setSpacing(8)

        specs = [
            ('AC', 0, 0, 'ac', '#a6a6a6', '#000000'),
            ('+/-', 0, 1, 'sign', '#a6a6a6', '#000000'),
            ('%', 0, 2, 'pct', '#a6a6a6', '#000000'),
            ('÷', 0, 3, 'div', '#ff9f0a', '#ffffff'),
            ('7', 1, 0, '7', '#333333', '#ffffff'),
            ('8', 1, 1, '8', '#333333', '#ffffff'),
            ('9', 1, 2, '9', '#333333', '#ffffff'),
            ('×', 1, 3, 'mul', '#ff9f0a', '#ffffff'),
            ('4', 2, 0, '4', '#333333', '#ffffff'),
            ('5', 2, 1, '5', '#333333', '#ffffff'),
            ('6', 2, 2, '6', '#333333', '#ffffff'),
            ('-', 2, 3, 'sub', '#ff9f0a', '#ffffff'),
            ('1', 3, 0, '1', '#333333', '#ffffff'),
            ('2', 3, 1, '2', '#333333', '#ffffff'),
            ('3', 3, 2, '3', '#333333', '#ffffff'),
            ('+', 3, 3, 'add', '#ff9f0a', '#ffffff'),
            ('0', 4, 0, '0', '#333333', '#ffffff'),
            ('.', 4, 2, 'dot', '#333333', '#ffffff'),
            ('=', 4, 3, 'eq', '#ff9f0a', '#ffffff'),
        ]

        self._ac_button = None
        for text, r, c, role, bg, fg in specs:
            btn = QPushButton(text)
            btn.setFixedHeight(56)
            btn.setStyleSheet(
                f'QPushButton {{ background-color: {bg}; color: {fg}; '
                f'border-radius: 28px; font-size: 22px; font-weight: 500; }}'
                f'QPushButton:pressed {{ background-color: #666666; }}'
            )
            if role == '0':
                grid.addWidget(btn, r, c, 1, 2)
            elif role == 'ac':
                self._ac_button = btn
                btn.clicked.connect(self._on_ac)
                grid.addWidget(btn, r, c)
            elif role == 'sign':
                btn.clicked.connect(self._tap_sign)
                grid.addWidget(btn, r, c)
            elif role == 'pct':
                btn.clicked.connect(self._tap_percent)
                grid.addWidget(btn, r, c)
            elif role == 'div':
                btn.clicked.connect(partial(self._tap_op, 'divide'))
                grid.addWidget(btn, r, c)
            elif role == 'mul':
                btn.clicked.connect(partial(self._tap_op, 'multiply'))
                grid.addWidget(btn, r, c)
            elif role == 'sub':
                btn.clicked.connect(partial(self._tap_op, 'subtract'))
                grid.addWidget(btn, r, c)
            elif role == 'add':
                btn.clicked.connect(partial(self._tap_op, 'add'))
                grid.addWidget(btn, r, c)
            elif role == 'dot':
                btn.clicked.connect(self._on_dot)
                grid.addWidget(btn, r, c)
            elif role == 'eq':
                btn.clicked.connect(self._on_equal)
                grid.addWidget(btn, r, c)
            else:
                btn.clicked.connect(partial(self._on_digit, text))
                grid.addWidget(btn, r, c)

        root.addLayout(grid)
        self._sync()

    def _sync(self):
        if self._ac_button is not None:
            self._ac_button.setText('AC' if self._calc.is_ac_label() else 'C')
        text = self._calc.display_value()
        self._fit_display_font(text)
        self._display.setText(text)

    def _apply_display_font(self):
        f = QFont()
        f.setPointSize(self._display_font_pt)
        self._display.setFont(f)

    def _fit_display_font(self, text: str):
        w = self._display.width() - 8
        if w <= 0:
            return
        pt = self.DISPLAY_MAX_PT
        while pt >= self.DISPLAY_MIN_PT:
            f = QFont()
            f.setPointSize(pt)
            fm = QFontMetrics(f)
            if fm.horizontalAdvance(text) <= w:
                self._display_font_pt = pt
                self._apply_display_font()
                return
            pt -= 1
        self._display_font_pt = self.DISPLAY_MIN_PT
        self._apply_display_font()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._sync()

    def _on_ac(self):
        if self._calc.is_ac_label():
            self._calc.reset()
        else:
            self._calc.clear_entry()
        self._sync()

    def _on_digit(self, digit: str):
        self._calc.press_digit(digit)
        self._sync()

    def _on_dot(self):
        self._calc.press_decimal()
        self._sync()

    def _tap_sign(self):
        self._calc.negative_positive()
        self._sync()

    def _tap_percent(self):
        self._calc.percent()
        self._sync()

    def _tap_op(self, op: str):
        getattr(self._calc, op)()
        self._sync()

    def _on_equal(self):
        self._calc.equal()
        self._sync()


def main():
    app = QApplication(sys.argv)
    win = CalculatorWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
