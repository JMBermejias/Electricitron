"""Estilos CSS/QSS profesionales para Electricitron - Tema Azul Claro"""

MAIN_STYLESHEET = """
/* ===== GLOBAL ===== */
QWidget {
    font-family: 'Segoe UI', 'Roboto', 'Noto Sans', sans-serif;
    font-size: 13px;
    color: #2c3e50;
}

/* ===== MAIN WINDOW ===== */
QMainWindow {
    background-color: #f0f6fc;
}

/* ===== FRAMES ===== */
QFrame#sidebar {
    background-color: #1a5276;
    min-width: 260px;
    max-width: 260px;
}

QFrame#header {
    background-color: #2980b9;
    min-height: 60px;
    max-height: 60px;
    border-bottom: 2px solid #1a5276;
}

QFrame#content {
    background-color: #f0f6fc;
}

QFrame#statusBar {
    background-color: #2980b9;
    min-height: 28px;
    max-height: 28px;
}

/* ===== LABELS ===== */
QLabel {
    color: #2c3e50;
    font-size: 13px;
}

QLabel#titleLabel {
    color: #ffffff;
    font-size: 22px;
    font-weight: bold;
    padding-left: 15px;
}

QLabel#subtitleLabel {
    color: #d6eaf8;
    font-size: 12px;
    padding-left: 15px;
}

QLabel#sectionTitle {
    color: #1a5276;
    font-size: 18px;
    font-weight: bold;
    padding: 10px 0px;
}

QLabel#resultLabel {
    color: #1a5276;
    font-size: 14px;
    font-weight: bold;
}

QLabel#statusLabel {
    color: #ffffff;
    font-size: 11px;
}

/* ===== SIDEBAR BUTTONS ===== */
QPushButton#sidebarBtn {
    background-color: transparent;
    color: #d6eaf8;
    border: none;
    border-left: 4px solid transparent;
    text-align: left;
    padding: 12px 20px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#sidebarBtn:hover {
    background-color: rgba(255, 255, 255, 0.1);
    border-left: 4px solid #5dade2;
    color: #ffffff;
}

QPushButton#sidebarBtn:checked,
QPushButton#sidebarBtn[active="true"] {
    background-color: rgba(255, 255, 255, 0.15);
    border-left: 4px solid #85c1e9;
    color: #ffffff;
    font-weight: bold;
}

/* ===== SIDEBAR SECTION LABELS ===== */
QLabel#sidebarSection {
    color: #85c1e9;
    font-size: 11px;
    font-weight: bold;
    text-transform: uppercase;
    padding: 15px 20px 5px 20px;
    letter-spacing: 1px;
}

/* ===== PRIMARY BUTTONS ===== */
QPushButton#primaryBtn {
    background-color: #2980b9;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 24px;
    font-size: 13px;
    font-weight: bold;
    min-height: 36px;
}

QPushButton#primaryBtn:hover {
    background-color: #3498db;
}

QPushButton#primaryBtn:pressed {
    background-color: #1a5276;
}

QPushButton#primaryBtn:disabled {
    background-color: #bdc3c7;
    color: #7f8c8d;
}

/* ===== SECONDARY BUTTONS ===== */
QPushButton#secondaryBtn {
    background-color: #ecf0f1;
    color: #2c3e50;
    border: 1px solid #bdc3c7;
    border-radius: 6px;
    padding: 8px 18px;
    font-size: 12px;
    min-height: 32px;
}

QPushButton#secondaryBtn:hover {
    background-color: #d5dbdb;
    border-color: #95a5a6;
}

/* ===== DANGER BUTTONS ===== */
QPushButton#dangerBtn {
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 18px;
    font-size: 12px;
    min-height: 32px;
}

QPushButton#dangerBtn:hover {
    background-color: #c0392b;
}

/* ===== SUCCESS BUTTONS ===== */
QPushButton#successBtn {
    background-color: #27ae60;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 18px;
    font-size: 12px;
    min-height: 32px;
}

QPushButton#successBtn:hover {
    background-color: #229954;
}

/* ===== INPUT FIELDS ===== */
QLineEdit, QSpinBox, QDoubleSpinBox {
    background-color: #ffffff;
    border: 2px solid #d5dbdb;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    color: #2c3e50;
    min-height: 20px;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid #2980b9;
    background-color: #fafcfe;
}

QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    border-color: #85c1e9;
}

/* ===== COMBO BOX ===== */
QComboBox {
    background-color: #ffffff;
    border: 2px solid #d5dbdb;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    color: #2c3e50;
    min-height: 20px;
}

QComboBox:hover {
    border-color: #85c1e9;
}

QComboBox:focus {
    border: 2px solid #2980b9;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #2980b9;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #d5dbdb;
    selection-background-color: #2980b9;
    selection-color: #ffffff;
    padding: 4px;
}

/* ===== TABLES ===== */
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #d5dbdb;
    border-radius: 6px;
    gridline-color: #ecf0f1;
    font-size: 12px;
    selection-background-color: #d6eaf8;
    selection-color: #2c3e50;
}

QTableWidget::item {
    padding: 6px 10px;
    border-bottom: 1px solid #f2f3f4;
}

QTableWidget::item:selected {
    background-color: #d6eaf8;
}

QHeaderView::section {
    background-color: #2980b9;
    color: #ffffff;
    border: none;
    padding: 8px 10px;
    font-weight: bold;
    font-size: 12px;
}

QHeaderView::section:horizontal {
    border-right: 1px solid #1a5276;
}

QHeaderView::section:last {
    border-right: none;
}

/* ===== SCROLL BARS ===== */
QScrollBar:vertical {
    background-color: #f0f6fc;
    width: 10px;
    border: none;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #85c1e9;
    min-height: 30px;
    border-radius: 5px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background-color: #2980b9;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    background-color: #f0f6fc;
    height: 10px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #85c1e9;
    min-width: 30px;
    border-radius: 5px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #2980b9;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* ===== TAB WIDGET ===== */
QTabWidget::pane {
    border: 1px solid #d5dbdb;
    background-color: #ffffff;
    border-radius: 6px;
}

QTabBar::tab {
    background-color: #ecf0f1;
    color: #566573;
    border: 1px solid #d5dbdb;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-size: 12px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #2980b9;
    font-weight: bold;
    border-bottom: 2px solid #2980b9;
}

QTabBar::tab:hover:!selected {
    background-color: #d6eaf8;
}

/* ===== GROUP BOX ===== */
QGroupBox {
    font-weight: bold;
    font-size: 13px;
    color: #1a5276;
    border: 2px solid #d5dbdb;
    border-radius: 8px;
    margin-top: 12px;
    padding: 20px 12px 12px 12px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px;
    background-color: #f0f6fc;
}

/* ===== SCROLL AREA ===== */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollArea > QWidget > QWidget {
    background-color: transparent;
}

/* ===== SPLITTER ===== */
QSplitter::handle {
    background-color: #d5dbdb;
}

QSplitter::handle:horizontal {
    width: 2px;
}

QSplitter::handle:vertical {
    height: 2px;
}

/* ===== TOOLTIP ===== */
QToolTip {
    background-color: #2c3e50;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 11px;
}

/* ===== MESSAGE BOX ===== */
QMessageBox {
    background-color: #f0f6fc;
}

QMessageBox QPushButton {
    min-width: 80px;
}

/* ===== LINE ===== */
QFrame#separator {
    background-color: #d5dbdb;
    max-height: 1px;
}

/* ===== PROGRESS BAR ===== */
QProgressBar {
    background-color: #ecf0f1;
    border: none;
    border-radius: 4px;
    text-align: center;
    height: 8px;
}

QProgressBar::chunk {
    background-color: #2980b9;
    border-radius: 4px;
}

/* ===== RESULT CARD ===== */
QFrame#resultCard {
    background-color: #ffffff;
    border: 1px solid #d5dbdb;
    border-radius: 8px;
    padding: 15px;
}

QFrame#resultCard:hover {
    border-color: #85c1e9;
}
"""
