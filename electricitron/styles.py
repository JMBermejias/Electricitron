"""Estilos CSS/QSS para Electricitron - Azul claro limpio, redondeado."""

MAIN_STYLESHEET = """
/* ===== GLOBAL ===== */
* {
    font-family: 'Segoe UI', 'SF Pro Display', 'Noto Sans', 'Ubuntu', sans-serif;
    font-size: 13px;
    color: #34495e;
    outline: none;
}

QMainWindow {
    background-color: #f5f9fd;
}

/* ===== SIDEBAR ===== */
QFrame#sidebar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1e88e5, stop:0.5 #1565c0, stop:1 #0d47a1);
    min-width: 250px;
    max-width: 250px;
    border-right: none;
}

/* ===== HEADER ===== */
QFrame#header {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #42a5f5, stop:1 #1e88e5);
    min-height: 56px;
    max-height: 56px;
    border-bottom: none;
}

/* ===== STATUS BAR ===== */
QFrame#statusBar {
    background-color: #1e88e5;
    min-height: 26px;
    max-height: 26px;
    border-top: none;
}

/* ===== LABELS ===== */
QLabel {
    color: #34495e;
    font-size: 13px;
    background: transparent;
}

QLabel#titleLabel {
    color: #ffffff;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

QLabel#subtitleLabel {
    color: rgba(255,255,255,0.8);
    font-size: 11px;
}

QLabel#sectionTitle {
    color: #1565c0;
    font-size: 16px;
    font-weight: 700;
}

QLabel#statusLabel {
    color: #ffffff;
    font-size: 11px;
}

/* ===== SIDEBAR BUTTONS ===== */
QPushButton#sidebarBtn {
    background-color: rgba(255, 255, 255, 0.12);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.15);
    text-align: left;
    padding: 10px 16px;
    font-size: 13px;
    font-weight: 500;
    margin: 3px 10px;
    border-radius: 10px;
}

QPushButton#sidebarBtn:hover {
    background-color: rgba(255, 255, 255, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: #ffffff;
}

QPushButton#sidebarBtn:checked,
QPushButton#sidebarBtn[active="true"] {
    background-color: rgba(255, 255, 255, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.5);
    color: #ffffff;
    font-weight: 700;
}

QLabel#sidebarSection {
    color: rgba(255,255,255,0.6);
    font-size: 10px;
    font-weight: 700;
    padding: 16px 18px 4px 18px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* ===== PRIMARY BUTTONS ===== */
QPushButton#primaryBtn {
    background-color: #1565c0;
    color: #ffffff;
    border: 2px solid #0d47a1;
    border-radius: 12px;
    padding: 12px 32px;
    font-size: 14px;
    font-weight: 700;
    min-height: 42px;
    letter-spacing: 0.5px;
}

QPushButton#primaryBtn:hover {
    background-color: #1976d2;
    border-color: #1565c0;
}

QPushButton#primaryBtn:pressed {
    background-color: #0d47a1;
    border-color: #0a3d8f;
}

QPushButton#primaryBtn:disabled {
    background-color: #90a4ae;
    border-color: #78909c;
    color: #cfd8dc;
}

/* ===== SECONDARY ===== */
QPushButton#secondaryBtn {
    background-color: #e3f2fd;
    color: #0d47a1;
    border: 2px solid #90caf9;
    border-radius: 12px;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: 600;
    min-height: 36px;
}

QPushButton#secondaryBtn:hover {
    background-color: #bbdefb;
    border-color: #42a5f5;
}

/* ===== DANGER ===== */
QPushButton#dangerBtn {
    background-color: #d32f2f;
    color: #ffffff;
    border: 2px solid #b71c1c;
    border-radius: 12px;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: 600;
    min-height: 36px;
}

QPushButton#dangerBtn:hover {
    background-color: #e53935;
    border-color: #c62828;
}

/* ===== SUCCESS ===== */
QPushButton#successBtn {
    background-color: #2e7d32;
    color: #ffffff;
    border: 2px solid #1b5e20;
    border-radius: 12px;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: 600;
    min-height: 36px;
}

QPushButton#successBtn:hover {
    background-color: #388e3c;
    border-color: #2e7d32;
}

/* ===== INPUTS ===== */
QLineEdit, QSpinBox, QDoubleSpinBox {
    background-color: #ffffff;
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    padding: 9px 14px;
    font-size: 13px;
    color: #34495e;
    min-height: 20px;
    selection-background-color: #90caf9;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid #42a5f5;
    background-color: #fafcfe;
}

QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    border-color: #90caf9;
}

/* ===== COMBO BOX ===== */
QComboBox {
    background-color: #ffffff;
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    padding: 9px 14px;
    font-size: 13px;
    color: #34495e;
    min-height: 20px;
}

QComboBox:hover {
    border-color: #90caf9;
}

QComboBox:focus {
    border: 2px solid #42a5f5;
}

QComboBox::drop-down {
    border: none;
    width: 32px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #1e88e5;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    selection-background-color: #e3f2fd;
    selection-color: #1565c0;
    padding: 4px;
    outline: none;
}

/* ===== TABLES ===== */
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    gridline-color: #f5f5f5;
    font-size: 12px;
    selection-background-color: #e3f2fd;
    selection-color: #1565c0;
    outline: none;
}

QTableWidget::item {
    padding: 8px 10px;
    border-bottom: 1px solid #fafafa;
}

QTableWidget::item:selected {
    background-color: #e3f2fd;
}

QHeaderView::section {
    background-color: #e3f2fd;
    color: #1565c0;
    border: none;
    border-bottom: 2px solid #bbdefb;
    padding: 10px 12px;
    font-weight: 600;
    font-size: 12px;
}

QHeaderView::section:horizontal {
    border-right: 1px solid #e3f2fd;
}

QHeaderView::section:last {
    border-right: none;
}

/* ===== SCROLL BARS ===== */
QScrollBar:vertical {
    background-color: transparent;
    width: 8px;
    border: none;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #b0bec5;
    min-height: 30px;
    border-radius: 4px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background-color: #78909c;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 8px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #b0bec5;
    min-width: 30px;
    border-radius: 4px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #78909c;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* ===== TABS ===== */
QTabWidget::pane {
    border: 1px solid #e0e0e0;
    background-color: #ffffff;
    border-radius: 14px;
    padding: 8px;
    top: -1px;
}

QTabBar::tab {
    background-color: #f5f5f5;
    color: #78909c;
    border: none;
    padding: 10px 22px;
    margin-right: 3px;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    font-size: 12px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #1e88e5;
    font-weight: 700;
    border-bottom: 3px solid #42a5f5;
}

QTabBar::tab:hover:!selected {
    background-color: #e3f2fd;
    color: #1565c0;
}

/* ===== GROUP BOX ===== */
QGroupBox {
    font-weight: 700;
    font-size: 13px;
    color: #1565c0;
    border: 2px solid #e3f2fd;
    border-radius: 14px;
    margin-top: 14px;
    padding: 22px 14px 14px 14px;
    background-color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 16px;
    padding: 0 10px;
    background-color: #f5f9fd;
    border-radius: 6px;
}

/* ===== SCROLL AREA ===== */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollArea > QWidget > QWidget {
    background-color: transparent;
}

/* ===== TOOLTIP ===== */
QToolTip {
    background-color: #1565c0;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 11px;
}

/* ===== MESSAGE BOX ===== */
QMessageBox {
    background-color: #f5f9fd;
}

QMessageBox QPushButton {
    min-width: 90px;
    border-radius: 10px;
    padding: 8px 16px;
}

/* ===== PROGRESS BAR ===== */
QProgressBar {
    background-color: #e3f2fd;
    border: none;
    border-radius: 6px;
    text-align: center;
    height: 8px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #42a5f5, stop:1 #1e88e5);
    border-radius: 6px;
}

/* ===== RESULT CARD ===== */
QFrame#resultCard {
    background-color: #ffffff;
    border: 2px solid #e3f2fd;
    border-radius: 16px;
    padding: 16px;
}

QFrame#resultCard:hover {
    border-color: #90caf9;
    background-color: #fafcff;
}

/* ===== ACTION BUTTONS (Guardar/PDF/Excel) ===== */
QPushButton#saveBtn,
QPushButton#pdfBtn,
QPushButton#excelBtn {
    background-color: #1565c0;
    color: #ffffff;
    border: 2px solid #0d47a1;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
    min-height: 28px;
}

QPushButton#saveBtn:hover,
QPushButton#pdfBtn:hover,
QPushButton#excelBtn:hover {
    background-color: #1976d2;
    border-color: #1565c0;
}

/* ===== SEPARATOR ===== */
QFrame#separator {
    background-color: #e0e0e0;
    max-height: 1px;
}
"""
