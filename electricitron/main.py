"""Electricitron - Software profesional de cálculos eléctricos y telecomunicaciones."""
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QPushButton, QLabel, QLineEdit, QComboBox, QDoubleSpinBox,
    QSpinBox, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
    QGroupBox, QMessageBox, QFileDialog, QSplitter, QStackedWidget,
    QTabWidget, QSizePolicy, QAbstractItemView
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QAction, QColor

from electricitron.styles import MAIN_STYLESHEET
from electricitron.modules.elec_basic import ElectricalBasic
from electricitron.modules.cable_calc import CableCalculations
from electricitron.modules.protections import ProtectionCalculations
from electricitron.modules.installations import InstallationCalculations
from electricitron.modules.telecom import TelecomCalculations
from electricitron.modules.distances import DistanceCalculations
from electricitron.reports.pdf_report import ReportManager
from electricitron.reports.excel_report import ExcelReportManager


class CalculationEngine:
    """Motor central de cálculos."""

    def __init__(self):
        self.basic = ElectricalBasic()
        self.cable = CableCalculations()
        self.protections = ProtectionCalculations()
        self.installations = InstallationCalculations()
        self.telecom = TelecomCalculations()
        self.distances = DistanceCalculations()


class ReportStore:
    """Almacén central de resultados."""

    def __init__(self):
        self.pdf_manager = ReportManager()
        self.excel_manager = ExcelReportManager()
        self.results = []

    def add(self, category, title, params, results, notes=None):
        rec_pdf = self.pdf_manager.add_record(category, title, params, results, notes)
        rec_xl = self.excel_manager.add_record(category, title, params, results, notes)
        entry = {
            "id": rec_pdf["id"],
            "category": category,
            "title": title,
            "params": params,
            "results": results,
            "notes": notes or [],
        }
        self.results.append(entry)
        return entry

    def delete(self, record_id):
        self.pdf_manager.delete_record(record_id)
        self.excel_manager.delete_record(record_id)
        self.results = [r for r in self.results if r["id"] != record_id]

    def modify(self, record_id, **kwargs):
        self.pdf_manager.modify_record(record_id, **kwargs)
        self.excel_manager.modify_record(record_id, **kwargs)
        for r in self.results:
            if r["id"] == record_id:
                r.update(kwargs)

    def clear(self):
        self.pdf_manager.clear_all()
        self.excel_manager.clear_all()
        self.results.clear()


class SidebarButton(QPushButton):
    """Botón personalizado para el sidebar."""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("sidebarBtn")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(44)


class ResultCard(QFrame):
    """Widget de tarjeta para mostrar resultado."""

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("resultCard")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)

        self.title = QLabel(title)
        self.title.setObjectName("sectionTitle")
        self.title.setStyleSheet("font-size:14px; color:#1a5276; font-weight:bold; border:none; background:transparent;")
        layout.addWidget(self.title)

        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(4)
        layout.addLayout(self.content_layout)

    def add_result(self, label, value):
        row = QHBoxLayout()
        lbl = QLabel(f"{label}:")
        lbl.setStyleSheet("color:#566573; font-size:12px; border:none; background:transparent;")
        val = QLabel(str(value))
        val.setStyleSheet("color:#1a5276; font-size:12px; font-weight:bold; border:none; background:transparent;")
        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(val)
        self.content_layout.addLayout(row)

    def clear_results(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.layout():
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()


class MainWindow(QMainWindow):
    """Ventana principal de Electricitron."""

    def __init__(self):
        super().__init__()
        self.engine = CalculationEngine()
        self.store = ReportStore()
        self.current_sidebar = None
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("Electricitron v1.0.0 - Cálculos Eléctricos y Telecomunicaciones")
        self.setMinimumSize(1280, 800)
        self.resize(1440, 900)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._create_sidebar(main_layout)
        self._create_content_area(main_layout)

        self._setup_pages()
        self._update_status("Aplicación iniciada correctamente")

    def _create_sidebar(self, parent_layout):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        logo_frame = QFrame()
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(20, 20, 20, 10)
        logo_label = QLabel("⚡ ELECTRICITRON")
        logo_label.setStyleSheet("color:#ffffff; font-size:18px; font-weight:bold; border:none; background:transparent;")
        logo_layout.addWidget(logo_label)
        ver_label = QLabel("v1.0.0")
        ver_label.setStyleSheet("color:#85c1e9; font-size:10px; border:none; background:transparent;")
        logo_layout.addWidget(ver_label)
        sidebar_layout.addWidget(logo_frame)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color:#1a5276; max-height:1px;")
        sidebar_layout.addWidget(sep)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 8, 0, 8)
        scroll_layout.setSpacing(2)

        sections = [
            ("CÁLCULOS ELÉCTRICOS", [
                ("🔧 Ley de Ohm / Básicos", "basico"),
                ("🔌 Secciones y Cables", "cable"),
                ("⚡ Protecciones", "proteccion"),
                ("🏠 Instalaciones", "instalacion"),
            ]),
            ("INFRAESTRUCTURA", [
                ("📡 Telecomunicaciones", "telecom"),
                ("📏 Distancias y Líneas", "distancia"),
            ]),
            ("INFORMES", [
                ("📋 Ver Informe", "informe"),
                ("📊 Exportar PDF", "export_pdf"),
                ("📈 Exportar Excel", "export_excel"),
            ]),
            ("", [
                ("ℹ️ Acerca de", "acerca"),
            ]),
        ]

        self.sidebar_buttons = []
        for section_title, items in sections:
            if section_title:
                lbl = QLabel(section_title)
                lbl.setObjectName("sidebarSection")
                scroll_layout.addWidget(lbl)
            for text, key in items:
                btn = SidebarButton(text)
                btn.clicked.connect(lambda checked, k=key: self._navigate(k))
                scroll_layout.addWidget(btn)
                self.sidebar_buttons.append((btn, key))

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        scroll.setStyleSheet("QScrollArea{background:#1a5276; border:none;}")
        sidebar_layout.addWidget(scroll)

        parent_layout.addWidget(sidebar)
        self.sidebar = sidebar

    def _create_content_area(self, parent_layout):
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color:#f0f6fc;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        header = QFrame()
        header.setObjectName("header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        self.page_title = QLabel("Ley de Ohm y Cálculos Básicos")
        self.page_title.setObjectName("titleLabel")
        header_layout.addWidget(self.page_title)
        header_layout.addStretch()

        self.status_label = QLabel("Listo")
        self.status_label.setObjectName("statusLabel")
        header_layout.addWidget(self.status_label)
        content_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea{border:none; background:#f0f6fc;}")
        self.pages_stack = QStackedWidget()
        self.pages_stack.setStyleSheet("background:#f0f6fc;")
        scroll.setWidget(self.pages_stack)
        content_layout.addWidget(scroll)

        footer = QFrame()
        footer.setObjectName("statusBar")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(15, 0, 15, 0)
        self.footer_label = QLabel("Electricitron v1.0.0 | Software de cálculos eléctricos")
        self.footer_label.setObjectName("statusLabel")
        footer_layout.addWidget(self.footer_label)
        content_layout.addWidget(footer)

        parent_layout.addWidget(content_widget)

    def _setup_pages(self):
        self._create_basico_page()
        self._create_cable_page()
        self._create_proteccion_page()
        self._create_instalacion_page()
        self._create_telecom_page()
        self._create_distancia_page()
        self._create_informe_page()

        self._navigate("basico")

    def _create_basico_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        subtitle = QLabel("Realice cálculos fundamentales de electricidad usando las leyes de Ohm, potencia, energía y más.")
        subtitle.setStyleSheet("color:#566573; font-size:12px; margin-bottom:5px;")
        layout.addWidget(subtitle)

        tabs = QTabWidget()
        tabs.setStyleSheet("QTabWidget::pane{border:1px solid #d5dbdb; background:#ffffff; border-radius:6px; padding:10px;}")
        tabs.addTab(self._create_ohm_tab(), "Ley de Ohm")
        tabs.addTab(self._create_potencia_tab(), "Potencia")
        tabs.addTab(self._create_energia_tab(), "Energía")
        tabs.addTab(self._create_impedancia_tab(), "Impedancia")
        layout.addWidget(tabs)
        layout.addStretch()
        self.pages_stack.addWidget(page)

    def _create_ohm_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        group = QGroupBox("Ley de Ohm: V = I × R")
        form = QHBoxLayout(group)

        left = QVBoxLayout()
        left.addWidget(QLabel("Voltaje (V):"))
        self.ohm_voltaje = QDoubleSpinBox()
        self.ohm_voltaje.setRange(0, 100000)
        self.ohm_voltaje.setSuffix(" V")
        self.ohm_voltaje.setDecimals(2)
        left.addWidget(self.ohm_voltaje)

        left.addWidget(QLabel("Corriente (A):"))
        self.ohm_corriente = QDoubleSpinBox()
        self.ohm_corriente.setRange(0, 100000)
        self.ohm_corriente.setSuffix(" A")
        self.ohm_corriente.setDecimals(4)
        left.addWidget(self.ohm_corriente)

        left.addWidget(QLabel("Resistencia (Ω):"))
        self.ohm_resistencia = QDoubleSpinBox()
        self.ohm_resistencia.setRange(0, 100000)
        self.ohm_resistencia.setSuffix(" Ω")
        self.ohm_resistencia.setDecimals(4)
        left.addWidget(self.ohm_resistencia)
        form.addLayout(left)

        right = QVBoxLayout()
        self.ohm_result = ResultCard("Resultado")
        right.addWidget(self.ohm_result)
        form.addLayout(right)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        calc_btn = QPushButton("Calcular")
        calc_btn.setObjectName("primaryBtn")
        calc_btn.clicked.connect(self._calc_ohm)
        btn_row.addWidget(calc_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_potencia_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        group = QGroupBox("Cálculo de Potencia")
        form = QVBoxLayout(group)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Tipo:"))
        self.pot_tipo = QComboBox()
        self.pot_tipo.addItems(["DC (V×I)", "Monofásica (V×I×FP)", "Trifásica (√3×V×I×FP)"])
        row1.addWidget(self.pot_tipo)
        form.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Voltaje (V):"))
        self.pot_voltaje = QDoubleSpinBox()
        self.pot_voltaje.setRange(0, 100000)
        self.pot_voltaje.setSuffix(" V")
        row2.addWidget(self.pot_voltaje)
        row2.addWidget(QLabel("Corriente (A):"))
        self.pot_corriente = QDoubleSpinBox()
        self.pot_corriente.setRange(0, 100000)
        self.pot_corriente.setSuffix(" A")
        row2.addWidget(self.pot_corriente)
        row2.addWidget(QLabel("FP:"))
        self.pot_fp = QDoubleSpinBox()
        self.pot_fp.setRange(0, 1)
        self.pot_fp.setSingleStep(0.01)
        self.pot_fp.setValue(0.9)
        row2.addWidget(self.pot_fp)
        form.addLayout(row2)

        self.pot_result = ResultCard("Resultado")
        form.addWidget(self.pot_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        calc_btn = QPushButton("Calcular Potencia")
        calc_btn.setObjectName("primaryBtn")
        calc_btn.clicked.connect(self._calc_potencia)
        btn_row.addWidget(calc_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_energia_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        group = QGroupBox("Cálculo de Energía (E = P × t)")
        form = QVBoxLayout(group)

        row = QHBoxLayout()
        row.addWidget(QLabel("Potencia (W):"))
        self.ener_potencia = QDoubleSpinBox()
        self.ener_potencia.setRange(0, 1000000)
        self.ener_potencia.setSuffix(" W")
        row.addWidget(self.ener_potencia)
        row.addWidget(QLabel("Tiempo (h):"))
        self.ener_tiempo = QDoubleSpinBox()
        self.ener_tiempo.setRange(0, 8760)
        self.ener_tiempo.setSuffix(" h")
        self.ener_tiempo.setDecimals(1)
        row.addWidget(self.ener_tiempo)
        form.addLayout(row)

        self.ener_result = ResultCard("Resultado")
        form.addWidget(self.ener_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        calc_btn = QPushButton("Calcular Energía")
        calc_btn.setObjectName("primaryBtn")
        calc_btn.clicked.connect(self._calc_energia)
        btn_row.addWidget(calc_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_impedancia_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        group = QGroupBox("Cálculo de Impedancia (Z)")
        form = QVBoxLayout(group)

        row = QHBoxLayout()
        row.addWidget(QLabel("Resistencia (Ω):"))
        self.imp_r = QDoubleSpinBox()
        self.imp_r.setRange(0, 100000)
        self.imp_r.setSuffix(" Ω")
        row.addWidget(self.imp_r)
        row.addWidget(QLabel("Inductancia (H):"))
        self.imp_l = QDoubleSpinBox()
        self.imp_l.setRange(0, 100000)
        self.imp_l.setSuffix(" H")
        self.imp_l.setDecimals(6)
        row.addWidget(self.imp_l)
        row.addWidget(QLabel("Capacitancia (F):"))
        self.imp_c = QDoubleSpinBox()
        self.imp_c.setRange(0, 100000)
        self.imp_c.setSuffix(" F")
        self.imp_c.setDecimals(6)
        row.addWidget(self.imp_c)
        row.addWidget(QLabel("Frecuencia (Hz):"))
        self.imp_f = QDoubleSpinBox()
        self.imp_f.setRange(0, 100000)
        self.imp_f.setSuffix(" Hz")
        self.imp_f.setValue(50)
        row.addWidget(self.imp_f)
        form.addLayout(row)

        self.imp_result = ResultCard("Resultado")
        form.addWidget(self.imp_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        calc_btn = QPushButton("Calcular Impedancia")
        calc_btn.setObjectName("primaryBtn")
        calc_btn.clicked.connect(self._calc_impedancia)
        btn_row.addWidget(calc_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_cable_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        subtitle = QLabel("Dimensionamiento de conductores y verificación de caída de tensión.")
        subtitle.setStyleSheet("color:#566573; font-size:12px;")
        layout.addWidget(subtitle)

        tabs = QTabWidget()
        tabs.setStyleSheet("QTabWidget::pane{border:1px solid #d5dbdb; background:#ffffff; border-radius:6px; padding:10px;}")
        tabs.addTab(self._create_seccion_tab(), "Sección por Corriente")
        tabs.addTab(self._create_caida_tab(), "Caída de Tensión")
        tabs.addTab(self._create_tabla_tab(), "Tabla de Secciones")
        layout.addWidget(tabs)
        layout.addStretch()
        self.pages_stack.addWidget(page)

    def _create_seccion_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Selección de sección por corriente transportada")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("Corriente (A):"))
        self.sec_corriente = QDoubleSpinBox()
        self.sec_corriente.setRange(0, 5000)
        self.sec_corriente.setSuffix(" A")
        row.addWidget(self.sec_corriente)
        row.addWidget(QLabel("Tipo de cable:"))
        self.sec_tipo = QComboBox()
        self.sec_tipo.addItems(["Cu rígido", "Cu flexible", "Al rígido"])
        row.addWidget(self.sec_tipo)
        form.addLayout(row)

        self.sec_result = ResultCard("Resultado")
        form.addWidget(self.sec_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Calcular Sección")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_seccion)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_caida_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Caída de tensión en conductor")
        form = QVBoxLayout(group)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Voltaje (V):"))
        self.caida_v = QDoubleSpinBox()
        self.caida_v.setRange(0, 300000)
        self.caida_v.setSuffix(" V")
        self.caida_v.setValue(230)
        row1.addWidget(self.caida_v)
        row1.addWidget(QLabel("Corriente (A):"))
        self.caida_i = QDoubleSpinBox()
        self.caida_i.setRange(0, 5000)
        self.caida_i.setSuffix(" A")
        row1.addWidget(self.caida_i)
        row1.addWidget(QLabel("Longitud (m):"))
        self.caida_l = QDoubleSpinBox()
        self.caida_l.setRange(0, 100000)
        self.caida_l.setSuffix(" m")
        row1.addWidget(self.caida_l)
        form.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Sección (mm²):"))
        self.caida_s = QDoubleSpinBox()
        self.caida_s.setRange(0.1, 1000)
        self.caida_s.setSuffix(" mm²")
        self.caida_s.setDecimals(1)
        self.caida_s.setValue(2.5)
        row2.addWidget(self.caida_s)
        row2.addWidget(QLabel("Tipo cable:"))
        self.caida_tipo = QComboBox()
        self.caida_tipo.addItems(["Cu rígido", "Al rígido"])
        row2.addWidget(self.caida_tipo)
        row2.addWidget(QLabel("Sistema:"))
        self.caida_sys = QComboBox()
        self.caida_sys.addItems(["Trifásico", "Monofásico"])
        row2.addWidget(self.caida_sys)
        form.addLayout(row2)

        self.caida_result = ResultCard("Resultado")
        form.addWidget(self.caida_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Calcular Caída de Tensión")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_caida_tension)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_tabla_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Tabla de Secciones y Ampacidades")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("Tipo de cable:"))
        self.tabla_tipo = QComboBox()
        self.tabla_tipo.addItems(["Cu rígido", "Cu flexible", "Al rígido"])
        row.addWidget(self.tabla_tipo)
        btn = QPushButton("Mostrar Tabla")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._show_cable_table)
        row.addWidget(btn)
        row.addStretch()
        form.addLayout(row)

        self.tabla_cables = QTableWidget()
        self.tabla_cables.setColumnCount(2)
        self.tabla_cables.setHorizontalHeaderLabels(["Sección (mm²)", "Ampacidad (A)"])
        self.tabla_cables.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_cables.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        form.addWidget(self.tabla_cables)
        layout.addWidget(group)
        return tab

    def _create_proteccion_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        subtitle = QLabel("Selección y dimensionamiento de protecciones eléctricas.")
        subtitle.setStyleSheet("color:#566573; font-size:12px;")
        layout.addWidget(subtitle)

        tabs = QTabWidget()
        tabs.setStyleSheet("QTabWidget::pane{border:1px solid #d5dbdb; background:#ffffff; border-radius:6px; padding:10px;}")
        tabs.addTab(self._create_interrup_tab(), "Interruptor")
        tabs.addTab(self._create_diferencial_tab(), "Diferencial")
        tabs.addTab(self._create_fusible_tab(), "Fusible")
        tabs.addTab(self._create_curva_tab(), "Curva Magnética")
        layout.addWidget(tabs)
        layout.addStretch()
        self.pages_stack.addWidget(page)

    def _create_interrup_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Selección de Interruptor Automático")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("Corriente circuito (A):"))
        self.prot_corriente = QDoubleSpinBox()
        self.prot_corriente.setRange(0, 5000)
        self.prot_corriente.setSuffix(" A")
        row.addWidget(self.prot_corriente)
        row.addWidget(QLabel("Curva:"))
        self.prot_curva = QComboBox()
        self.prot_curva.addItems(["B", "C", "D", "K", "Z"])
        row.addWidget(self.prot_curva)
        form.addLayout(row)

        self.prot_result = ResultCard("Resultado")
        form.addWidget(self.prot_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Seleccionar Interruptor")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_interruptor)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_diferencial_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Selección de Interruptor Diferencial")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("Corriente circuito (A):"))
        self.diff_corriente = QDoubleSpinBox()
        self.diff_corriente.setRange(0, 5000)
        self.diff_corriente.setSuffix(" A")
        row.addWidget(self.diff_corriente)
        row.addWidget(QLabel("Sensibilidad:"))
        self.diff_sens = QComboBox()
        self.diff_sens.addItems(["30mA", "100mA", "300mA"])
        row.addWidget(self.diff_sens)
        form.addLayout(row)

        self.diff_result = ResultCard("Resultado")
        form.addWidget(self.diff_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Seleccionar Diferencial")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_diferencial)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_fusible_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Selección de Fusible")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("Corriente circuito (A):"))
        self.fus_corriente = QDoubleSpinBox()
        self.fus_corriente.setRange(0, 5000)
        self.fus_corriente.setSuffix(" A")
        row.addWidget(self.fus_corriente)
        row.addWidget(QLabel("Tipo:"))
        self.fus_tipo = QComboBox()
        self.fus_tipo.addItems(["gG", "aM", "gR"])
        row.addWidget(self.fus_tipo)
        form.addLayout(row)

        self.fus_result = ResultCard("Resultado")
        form.addWidget(self.fus_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Seleccionar Fusible")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_fusible)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_curva_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Tabla de Corrientes Magnéticas")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("In (A):"))
        self.curva_in = QSpinBox()
        self.curva_in.setRange(1, 4000)
        self.curva_in.setValue(16)
        row.addWidget(self.curva_in)
        row.addWidget(QLabel("Curva:"))
        self.curva_tipo = QComboBox()
        self.curva_tipo.addItems(["B", "C", "D", "K", "Z"])
        row.addWidget(self.curva_tipo)
        form.addLayout(row)

        self.curva_result = ResultCard("Resultado")
        form.addWidget(self.curva_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Calcular Curva")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_curva)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_instalacion_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        subtitle = QLabel("Dimensionamiento y diseño de instalaciones eléctricas.")
        subtitle.setStyleSheet("color:#566573; font-size:12px;")
        layout.addWidget(subtitle)

        tabs = QTabWidget()
        tabs.setStyleSheet("QTabWidget::pane{border:1px solid #d5dbdb; background:#ffffff; border-radius:6px; padding:10px;}")
        tabs.addTab(self._create_pot_inst_tab(), "Potencia Instalación")
        tabs.addTab(self._create_esquema_tab(), "Esquema Protección")
        tabs.addTab(self._create_selectividad_tab(), "Selectividad")
        layout.addWidget(tabs)
        layout.addStretch()
        self.pages_stack.addWidget(page)

    def _create_pot_inst_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Carga de Instalación")
        form = QVBoxLayout(group)

        self.inst_cargas = QTableWidget()
        self.inst_cargas.setColumnCount(5)
        self.inst_cargas.setHorizontalHeaderLabels(["Descripción", "Potencia (W)", "Tensión (V)", "FP", "Demanda"])
        self.inst_cargas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.inst_cargas.setRowCount(3)
        for i in range(3):
            for j in range(5):
                item = QTableWidgetItem()
                if j == 0:
                    item.setText(f"Carga {i+1}")
                elif j == 1:
                    item.setText("1000")
                elif j == 2:
                    item.setText("230")
                elif j == 3:
                    item.setText("0.9")
                elif j == 4:
                    item.setText("0.8")
                self.inst_cargas.setItem(i, j, item)
        form.addWidget(self.inst_cargas)

        row_btns = QHBoxLayout()
        add_btn = QPushButton("+ Añadir carga")
        add_btn.setObjectName("secondaryBtn")
        add_btn.clicked.connect(self._add_carga)
        row_btns.addWidget(add_btn)
        rem_btn = QPushButton("- Eliminar carga")
        rem_btn.setObjectName("dangerBtn")
        rem_btn.clicked.connect(self._rem_carga)
        row_btns.addWidget(rem_btn)
        row_btns.addStretch()
        form.addLayout(row_btns)

        self.inst_result = ResultCard("Resultado")
        form.addWidget(self.inst_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Calcular Potencia Instalación")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_pot_inst)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_esquema_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Esquema de Protección")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("Sistema:"))
        self.esq_tipo = QComboBox()
        self.esq_tipo.addItems(["TN-S", "TN-C", "TN-C-S", "TT", "IT"])
        row.addWidget(self.esq_tipo)
        row.addWidget(QLabel("Tensión (V):"))
        self.esq_tension = QDoubleSpinBox()
        self.esq_tension.setRange(0, 300000)
        self.esq_tension.setSuffix(" V")
        self.esq_tension.setValue(400)
        row.addWidget(self.esq_tension)
        form.addLayout(row)

        self.esq_result = ResultCard("Resultado")
        form.addWidget(self.esq_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Generar Esquema")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_esquema)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_selectividad_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Verificación de Selectividad")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("In Superior (A):"))
        self.sel_sup = QSpinBox()
        self.sel_sup.setRange(1, 4000)
        self.sel_sup.setValue(40)
        row.addWidget(self.sel_sup)
        row.addWidget(QLabel("In Inferior (A):"))
        self.sel_inf = QSpinBox()
        self.sel_inf.setRange(1, 4000)
        self.sel_inf.setValue(16)
        row.addWidget(self.sel_inf)
        form.addLayout(row)

        self.sel_result = ResultCard("Resultado")
        form.addWidget(self.sel_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Verificar Selectividad")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_selectividad)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_telecom_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        subtitle = QLabel("Cálculos de telecomunicaciones: enlaces inalámbricos, fibra óptica y redes de datos.")
        subtitle.setStyleSheet("color:#566573; font-size:12px;")
        layout.addWidget(subtitle)

        tabs = QTabWidget()
        tabs.setStyleSheet("QTabWidget::pane{border:1px solid #d5dbdb; background:#ffffff; border-radius:6px; padding:10px;}")
        tabs.addTab(self._create_enlace_tab(), "Enlace Inalámbrico")
        tabs.addTab(self._create_fibra_tab(), "Fibra Óptica")
        tabs.addTab(self._create_red_tab(), "Red de Datos")
        tabs.addTab(self._create_wifi_tab(), "WiFi")
        layout.addWidget(tabs)
        layout.addStretch()
        self.pages_stack.addWidget(page)

    def _create_enlace_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Enlace Inalámbrico Punto a Punto")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("Distancia (km):"))
        self.enl_dist = QDoubleSpinBox()
        self.enl_dist.setRange(0, 100)
        self.enl_dist.setSuffix(" km")
        self.enl_dist.setDecimals(2)
        row.addWidget(self.enl_dist)
        row.addWidget(QLabel("Frecuencia (GHz):"))
        self.enl_freq = QDoubleSpinBox()
        self.enl_freq.setRange(0.1, 100)
        self.enl_freq.setSuffix(" GHz")
        self.enl_freq.setDecimals(1)
        self.enl_freq.setValue(5.8)
        row.addWidget(self.enl_freq)
        row.addWidget(QLabel("Atenuación lluvia (dB/km):"))
        self.enl_lluvia = QDoubleSpinBox()
        self.enl_lluvia.setRange(0, 50)
        self.enl_lluvia.setSuffix(" dB/km")
        self.enl_lluvia.setDecimals(2)
        row.addWidget(self.enl_lluvia)
        form.addLayout(row)

        self.enl_result = ResultCard("Resultado")
        form.addWidget(self.enl_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Calcular Enlace")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_enlace)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_fibra_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Cálculo de Fibra Óptica")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("Tipo:"))
        self.fib_tipo = QComboBox()
        self.fib_tipo.addItems(["monomodo", "multimodo"])
        row.addWidget(self.fib_tipo)
        row.addWidget(QLabel("Distancia (km):"))
        self.fib_dist = QDoubleSpinBox()
        self.fib_dist.setRange(0, 100000)
        self.fib_dist.setSuffix(" km")
        self.fib_dist.setDecimals(2)
        row.addWidget(self.fib_dist)
        form.addLayout(row)

        self.fib_result = ResultCard("Resultado")
        form.addWidget(self.fib_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Calcular Fibra Óptica")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_fibra)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_red_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Pérdida de Cable de Red")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("Longitud (m):"))
        self.red_long = QDoubleSpinBox()
        self.red_long.setRange(0, 1000)
        self.red_long.setSuffix(" m")
        self.red_long.setValue(50)
        row.addWidget(self.red_long)
        row.addWidget(QLabel("Tipo cable:"))
        self.red_tipo = QComboBox()
        self.red_tipo.addItems(["Cat5e", "Cat6", "Cat6a", "Cat7", "Cat8", "OM3", "OM4", "OS2"])
        row.addWidget(self.red_tipo)
        form.addLayout(row)

        self.red_result = ResultCard("Resultado")
        form.addWidget(self.red_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Calcular Cable")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_cable_red)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_wifi_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Dimensionamiento WiFi")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("Nº dispositivos:"))
        self.wifi_n = QSpinBox()
        self.wifi_n.setRange(1, 10000)
        self.wifi_n.setValue(50)
        row.addWidget(self.wifi_n)
        row.addWidget(QLabel("Ancho banda requerido (Mbps):"))
        self.wifi_bw = QDoubleSpinBox()
        self.wifi_bw.setRange(1, 100000)
        self.wifi_bw.setSuffix(" Mbps")
        self.wifi_bw.setValue(500)
        row.addWidget(self.wifi_bw)
        form.addLayout(row)

        self.wifi_result = ResultCard("Resultado")
        form.addWidget(self.wifi_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Calcular WiFi")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_wifi)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_distancia_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        subtitle = QLabel("Cálculos de distancias, desplazamientos y dimensionamiento de líneas eléctricas.")
        subtitle.setStyleSheet("color:#566573; font-size:12px;")
        layout.addWidget(subtitle)

        tabs = QTabWidget()
        tabs.setStyleSheet("QTabWidget::pane{border:1px solid #d5dbdb; background:#ffffff; border-radius:6px; padding:10px;}")
        tabs.addTab(self._create_dist_ptos_tab(), "Distancia entre Puntos")
        tabs.addTab(self._create_zona_postes_tab(), "Zona de Postes")
        tabs.addTab(self._create_linea_larga_tab(), "Línea Larga")
        layout.addWidget(tabs)
        layout.addStretch()
        self.pages_stack.addWidget(page)

    def _create_dist_ptos_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Distancia entre dos puntos")
        form = QVBoxLayout(group)

        row = QHBoxLayout()
        row.addWidget(QLabel("Punto A (x,y,z):"))
        self.dist_ax = QDoubleSpinBox()
        self.dist_ax.setRange(-100000, 100000)
        self.dist_ax.setPrefix("x:")
        row.addWidget(self.dist_ax)
        self.dist_ay = QDoubleSpinBox()
        self.dist_ay.setRange(-100000, 100000)
        self.dist_ay.setPrefix("y:")
        row.addWidget(self.dist_ay)
        self.dist_az = QDoubleSpinBox()
        self.dist_az.setRange(-100000, 100000)
        self.dist_az.setPrefix("z:")
        row.addWidget(self.dist_az)
        form.addLayout(row)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Punto B (x,y,z):"))
        self.dist_bx = QDoubleSpinBox()
        self.dist_bx.setRange(-100000, 100000)
        self.dist_bx.setPrefix("x:")
        row2.addWidget(self.dist_bx)
        self.dist_by = QDoubleSpinBox()
        self.dist_by.setRange(-100000, 100000)
        self.dist_by.setPrefix("y:")
        row2.addWidget(self.dist_by)
        self.dist_bz = QDoubleSpinBox()
        self.dist_bz.setRange(-100000, 100000)
        self.dist_bz.setPrefix("z:")
        row2.addWidget(self.dist_bz)
        form.addLayout(row2)

        self.dist_result = ResultCard("Resultado")
        form.addWidget(self.dist_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Calcular Distancia")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_distancia)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_zona_postes_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Zona de Postes")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("Distancia total (m):"))
        self.zp_dist = QDoubleSpinBox()
        self.zp_dist.setRange(0, 100000)
        self.zp_dist.setSuffix(" m")
        self.zp_dist.setValue(500)
        row.addWidget(self.zp_dist)
        row.addWidget(QLabel("Separación (m):"))
        self.zp_sep = QDoubleSpinBox()
        self.zp_sep.setRange(10, 200)
        self.zp_sep.setSuffix(" m")
        self.zp_sep.setValue(50)
        row.addWidget(self.zp_sep)
        form.addLayout(row)

        self.zp_result = ResultCard("Resultado")
        form.addWidget(self.zp_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Calcular")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_zona_postes)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_linea_larga_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Caída de Tensión en Línea Larga")
        form = QVBoxLayout(group)
        row = QHBoxLayout()
        row.addWidget(QLabel("Voltaje (V):"))
        self.ll_voltaje = QDoubleSpinBox()
        self.ll_voltaje.setRange(0, 300000)
        self.ll_voltaje.setSuffix(" V")
        self.ll_voltaje.setValue(20000)
        row.addWidget(self.ll_voltaje)
        row.addWidget(QLabel("Corriente (A):"))
        self.ll_corriente = QDoubleSpinBox()
        self.ll_corriente.setRange(0, 5000)
        self.ll_corriente.setSuffix(" A")
        row.addWidget(self.ll_corriente)
        row.addWidget(QLabel("R (Ω/km):"))
        self.ll_r = QDoubleSpinBox()
        self.ll_r.setRange(0, 10)
        self.ll_r.setSuffix(" Ω/km")
        self.ll_r.setDecimals(4)
        self.ll_r.setValue(0.0282)
        row.addWidget(self.ll_r)
        form.addLayout(row)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Longitud (km):"))
        self.ll_long = QDoubleSpinBox()
        self.ll_long.setRange(0, 1000)
        self.ll_long.setSuffix(" km")
        self.ll_long.setValue(10)
        row2.addWidget(self.ll_long)
        row2.addWidget(QLabel("Sistema:"))
        self.ll_sys = QComboBox()
        self.ll_sys.addItems(["Trifásico", "Monofásico"])
        row2.addWidget(self.ll_sys)
        form.addLayout(row2)

        self.ll_result = ResultCard("Resultado")
        form.addWidget(self.ll_result)
        layout.addWidget(group)

        btn_row = QHBoxLayout()
        btn = QPushButton("Calcular Línea Larga")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._calc_linea_larga)
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        return tab

    def _create_informe_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        subtitle = QLabel("Gestione los cálculos realizados y exporte informes.")
        subtitle.setStyleSheet("color:#566573; font-size:12px;")
        layout.addWidget(subtitle)

        btn_row = QHBoxLayout()
        pdf_btn = QPushButton("📄 Exportar PDF")
        pdf_btn.setObjectName("primaryBtn")
        pdf_btn.clicked.connect(self._export_pdf)
        btn_row.addWidget(pdf_btn)

        excel_btn = QPushButton("📊 Exportar Excel")
        excel_btn.setObjectName("successBtn")
        excel_btn.clicked.connect(self._export_excel)
        btn_row.addWidget(excel_btn)

        clear_btn = QPushButton("🗑 Limpiar Todo")
        clear_btn.setObjectName("dangerBtn")
        clear_btn.clicked.connect(self._clear_report)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        info_label = QLabel("Registros guardados:")
        info_label.setStyleSheet("font-weight:bold; color:#1a5276; font-size:14px; margin-top:10px;")
        layout.addWidget(info_label)

        self.report_table = QTableWidget()
        self.report_table.setColumnCount(7)
        self.report_table.setHorizontalHeaderLabels([
            "ID", "Categoría", "Título", "Parámetros", "Resultados", "Notas", "Fecha"
        ])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.report_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.report_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        layout.addWidget(self.report_table)

        del_row = QHBoxLayout()
        del_id_label = QLabel("ID a eliminar:")
        del_row.addWidget(del_id_label)
        self.del_id = QSpinBox()
        self.del_id.setRange(0, 99999)
        del_row.addWidget(self.del_id)
        del_btn = QPushButton("Eliminar registro")
        del_btn.setObjectName("dangerBtn")
        del_btn.clicked.connect(self._delete_record)
        del_row.addWidget(del_btn)
        del_row.addStretch()
        layout.addLayout(del_row)

        self.pages_stack.addWidget(page)

    def _navigate(self, key):
        for btn, k in self.sidebar_buttons:
            btn.setChecked(k == key)
            btn.setProperty("active", k == key)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        page_titles = {
            "basico": "Ley de Ohm y Cálculos Básicos",
            "cable": "Secciones y Cables",
            "proteccion": "Protecciones Eléctricas",
            "instalacion": "Instalaciones Eléctricas",
            "telecom": "Telecomunicaciones",
            "distancia": "Distancias y Líneas",
            "informe": "Gestión de Informes",
            "export_pdf": "Exportar PDF",
            "export_excel": "Exportar Excel",
            "acerca": "Acerca de",
        }

        page_index = {
            "basico": 0, "cable": 1, "proteccion": 2, "instalacion": 3,
            "telecom": 4, "distancia": 5, "informe": 6,
        }

        if key in page_index:
            self.pages_stack.setCurrentIndex(page_index[key])
            self.page_title.setText(page_titles.get(key, key))
        elif key == "export_pdf":
            self._export_pdf()
        elif key == "export_excel":
            self._export_excel()
        elif key == "acerca":
            self._show_about()

    def _show_about(self):
        QMessageBox.about(
            self, "Acerca de Electricitron",
            "<h2>⚡ Electricitron v1.0.0</h2>"
            "<p>Software profesional de cálculos eléctricos y telecomunicaciones.</p>"
            "<p>Incluye: cálculos básicos, secciones de cables, protecciones, "
            "instalaciones, telecomunicaciones y cálculo de distancias.</p>"
            "<p>Exporta informes en PDF y Excel.</p>"
            "<hr>"
            "<p>© 2026 Electricitron. Todos los derechos reservados.</p>"
        )

    def _update_status(self, msg):
        self.status_label.setText(msg)
        self.footer_label.setText(f"Electricitron v1.0.0 | {msg}")

    # ============ CÁLCULOS ============

    def _calc_ohm(self):
        try:
            v = self.ohm_voltaje.value() or None
            i = self.ohm_corriente.value() or None
            r = self.ohm_resistencia.value() or None
            if v == 0: v = None
            if i == 0: i = None
            if r == 0: r = None
            if sum(x is not None for x in [v, i, r]) < 2:
                QMessageBox.warning(self, "Error", "Introduce al menos 2 valores.")
                return
            result = self.engine.basic.ley_ohm(v, i, r)
            self.ohm_result.clear_results()
            for k, val in result.items():
                self.ohm_result.add_result(k.title(), val)
            self.store.add("basico", "Ley de Ohm",
                           {"V": v, "I": i, "R": r}, result)
            self._update_status("Cálculo de Ley de Ohm realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_potencia(self):
        try:
            v = self.pot_voltaje.value()
            i = self.pot_corriente.value()
            fp = self.pot_fp.value()
            tipo = self.pot_tipo.currentIndex()
            if tipo == 0:
                p = self.engine.basic.potencia_dc(v, i)
            elif tipo == 1:
                p = self.engine.basic.potencia_monofasica(v, i, fp)
            else:
                p = self.engine.basic.potencia_trifasica(v, i, fp)
            self.pot_result.clear_results()
            self.pot_result.add_result("Potencia", f"{p} W")
            self.store.add("basico", "Potencia",
                           {"V": v, "I": i, "FP": fp, "Tipo": ["DC", "Monofásica", "Trifásica"][tipo]},
                           {"potencia_w": p})
            self._update_status("Cálculo de potencia realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_energia(self):
        try:
            p = self.ener_potencia.value()
            t = self.ener_tiempo.value()
            e = self.engine.basic.energia(p, t)
            self.ener_result.clear_results()
            self.ener_result.add_result("Energía", f"{e} kWh")
            self.store.add("basico", "Energía",
                           {"P": p, "t": t}, {"energia_kwh": e})
            self._update_status("Cálculo de energía realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_impedancia(self):
        try:
            r = self.imp_r.value()
            l = self.imp_l.value()
            c = self.imp_c.value()
            f = self.imp_f.value()
            result = self.engine.basic.impedancia(r, l, c, f)
            self.imp_result.clear_results()
            for k, val in result.items():
                self.imp_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("basico", "Impedancia",
                           {"R": r, "L": l, "C": c, "f": f}, result)
            self._update_status("Cálculo de impedancia realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_seccion(self):
        try:
            i = self.sec_corriente.value()
            tipo = self.sec_tipo.currentText()
            result = self.engine.cable.seccion_por_corriente(i, tipo)
            self.sec_result.clear_results()
            for k, val in result.items():
                self.sec_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("cable", "Sección por Corriente",
                           {"corriente": i, "tipo": tipo}, result)
            self._update_status("Selección de sección realizada")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_caida_tension(self):
        try:
            v = self.caida_v.value()
            i = self.caida_i.value()
            l = self.caida_l.value()
            s = self.caida_s.value()
            tipo = self.caida_tipo.currentText()
            trifasico = self.caida_sys.currentIndex() == 0
            result = self.engine.cable.caida_tension_conductor(v, l, i, s, tipo, trifasico)
            self.caida_result.clear_results()
            for k, val in result.items():
                self.caida_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("cable", "Caída de Tensión",
                           {"V": v, "I": i, "L": l, "S": s, "tipo": tipo, "trifasico": trifasico}, result)
            self._update_status("Cálculo de caída de tensión realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _show_cable_table(self):
        try:
            tipo = self.tabla_tipo.currentText()
            tabla = self.engine.cable.tabla_secciones_disponibles(tipo)
            self.tabla_cables.setRowCount(len(tabla))
            for i, row in enumerate(tabla):
                self.tabla_cables.setItem(i, 0, QTableWidgetItem(str(row["seccion_mm2"])))
                self.tabla_cables.setItem(i, 1, QTableWidgetItem(str(row["ampacidad_a"])))
            self._update_status(f"Tabla de {tipo} cargada")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_interruptor(self):
        try:
            i = self.prot_corriente.value()
            curva = self.prot_curva.currentText()
            result = self.engine.protections.seleccionar_interruptor(i, curva)
            self.prot_result.clear_results()
            for k, val in result.items():
                self.prot_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("proteccion", "Selección Interruptor",
                           {"corriente": i, "curva": curva}, result)
            self._update_status("Selección de interruptor realizada")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_diferencial(self):
        try:
            i = self.diff_corriente.value()
            sens = self.diff_sens.currentText()
            result = self.engine.protections.seleccionar_diferencial(i, sens)
            self.diff_result.clear_results()
            for k, val in result.items():
                self.diff_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("proteccion", "Selección Diferencial",
                           {"corriente": i, "sensibilidad": sens}, result)
            self._update_status("Selección de diferencial realizada")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_fusible(self):
        try:
            i = self.fus_corriente.value()
            tipo = self.fus_tipo.currentText()
            result = self.engine.protections.seleccionar_fusible(i, tipo)
            self.fus_result.clear_results()
            for k, val in result.items():
                self.fus_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("proteccion", "Selección Fusible",
                           {"corriente": i, "tipo": tipo}, result)
            self._update_status("Selección de fusible realizada")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_curva(self):
        try:
            in_val = self.curva_in.value()
            curva = self.curva_tipo.currentText()
            result = self.engine.protections.tabla_corriente_magnetica(in_val, curva)
            self.curva_result.clear_results()
            for k, val in result.items():
                if k != "tabla_detallada":
                    self.curva_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("proteccion", "Curva Magnética",
                           {"In": in_val, "curva": curva}, result)
            self._update_status("Cálculo de curva magnética realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _add_carga(self):
        row = self.inst_cargas.rowCount()
        self.inst_cargas.insertRow(row)
        for j in range(5):
            item = QTableWidgetItem()
            if j == 0: item.setText(f"Carga {row+1}")
            elif j == 1: item.setText("1000")
            elif j == 2: item.setText("230")
            elif j == 3: item.setText("0.9")
            elif j == 4: item.setText("0.8")
            self.inst_cargas.setItem(row, j, item)

    def _rem_carga(self):
        row = self.inst_cargas.currentRow()
        if row >= 0:
            self.inst_cargas.removeRow(row)

    def _calc_pot_inst(self):
        try:
            cargas = []
            for i in range(self.inst_cargas.rowCount()):
                carga = {
                    "descripcion": self.inst_cargas.item(i, 0).text() if self.inst_cargas.item(i, 0) else f"Carga {i+1}",
                    "potencia": float(self.inst_cargas.item(i, 1).text()) if self.inst_cargas.item(i, 1) else 0,
                    "tension": float(self.inst_cargas.item(i, 2).text()) if self.inst_cargas.item(i, 2) else 230,
                    "fp": float(self.inst_cargas.item(i, 3).text()) if self.inst_cargas.item(i, 3) else 1.0,
                    "demanda": float(self.inst_cargas.item(i, 4).text()) if self.inst_cargas.item(i, 4) else 1.0,
                }
                cargas.append(carga)
            result = self.engine.installations.potencia_instalacion(cargas)
            self.inst_result.clear_results()
            for k, val in result.items():
                self.inst_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("instalacion", "Potencia Instalación",
                           {"num_cargas": len(cargas)}, result)
            self._update_status("Cálculo de potencia de instalación realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_esquema(self):
        try:
            tipo = self.esq_tipo.currentText()
            tension = self.esq_tension.value()
            result = self.engine.installations.esquema_proteccion(tipo)
            self.esq_result.clear_results()
            for k, val in result.items():
                if isinstance(val, list):
                    self.esq_result.add_result(k.title(), ", ".join(str(v) for v in val))
                else:
                    self.esq_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("instalacion", "Esquema Protección",
                           {"sistema": tipo, "tension": tension}, result)
            self._update_status("Esquema de protección generado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_selectividad(self):
        try:
            sup = self.sel_sup.value()
            inf = self.sel_inf.value()
            result = self.engine.installations.selectividad(sup, inf)
            self.sel_result.clear_results()
            for k, val in result.items():
                self.sel_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("instalacion", "Selectividad",
                           {"In_sup": sup, "In_inf": inf}, result)
            self._update_status("Verificación de selectividad realizada")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_enlace(self):
        try:
            d = self.enl_dist.value()
            f = self.enl_freq.value()
            ll = self.enl_lluvia.value()
            result = self.engine.telecom.enlace_inalambrico(d, f, ll)
            self.enl_result.clear_results()
            for k, val in result.items():
                self.enl_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("telecom", "Enlace Inalámbrico",
                           {"distancia_km": d, "frecuencia_ghz": f, "lluvia_dbkm": ll}, result)
            self._update_status("Cálculo de enlace inalámbrico realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_fibra(self):
        try:
            tipo = self.fib_tipo.currentText()
            dist = self.fib_dist.value()
            result = self.engine.telecom.fibra_optica(tipo, dist)
            self.fib_result.clear_results()
            for k, val in result.items():
                self.fib_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("telecom", "Fibra Óptica",
                           {"tipo": tipo, "distancia_km": dist}, result)
            self._update_status("Cálculo de fibra óptica realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_cable_red(self):
        try:
            long = self.red_long.value()
            tipo = self.red_tipo.currentText()
            result = self.engine.telecom.perdida_cable_red(long, tipo)
            self.red_result.clear_results()
            for k, val in result.items():
                self.red_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("telecom", "Cable de Red",
                           {"longitud": long, "tipo": tipo}, result)
            self._update_status("Cálculo de cable de red realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_wifi(self):
        try:
            n = self.wifi_n.value()
            bw = self.wifi_bw.value()
            result = self.engine.telecom.sectores_wifi(n, bw)
            self.wifi_result.clear_results()
            for k, val in result.items():
                self.wifi_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("telecom", "WiFi",
                           {"dispositivos": n, "ancho_banda": bw}, result)
            self._update_status("Cálculo WiFi realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_distancia(self):
        try:
            a = (self.dist_ax.value(), self.dist_ay.value(), self.dist_az.value())
            b = (self.dist_bx.value(), self.dist_by.value(), self.dist_bz.value())
            result = self.engine.distances.distancia_linea_electrica(a, b)
            self.dist_result.clear_results()
            for k, val in result.items():
                self.dist_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("distancia", "Distancia entre Puntos",
                           {"punto_a": a, "punto_b": b}, result)
            self._update_status("Cálculo de distancia realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_zona_postes(self):
        try:
            d = self.zp_dist.value()
            s = self.zp_sep.value()
            result = self.engine.distances.zona_postes(d, s)
            self.zp_result.clear_results()
            for k, val in result.items():
                self.zp_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("distancia", "Zona de Postes",
                           {"distancia_total": d, "separacion": s}, result)
            self._update_status("Cálculo de zona de postes realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _calc_linea_larga(self):
        try:
            v = self.ll_voltaje.value()
            i = self.ll_corriente.value()
            r = self.ll_r.value()
            l = self.ll_long.value()
            trifasico = self.ll_sys.currentIndex() == 0
            result = self.engine.distances.caida_tension_linea_larga(v, i, r, l, trifasico)
            self.ll_result.clear_results()
            for k, val in result.items():
                self.ll_result.add_result(k.replace("_", " ").title(), val)
            self.store.add("distancia", "Línea Larga",
                           {"V": v, "I": i, "R": r, "L": l, "trifasico": trifasico}, result)
            self._update_status("Cálculo de línea larga realizado")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ============ INFORMES ============

    def _refresh_report_table(self):
        records = self.store.results
        self.report_table.setRowCount(len(records))
        for i, rec in enumerate(records):
            self.report_table.setItem(i, 0, QTableWidgetItem(str(rec["id"])))
            self.report_table.setItem(i, 1, QTableWidgetItem(rec["category"]))
            self.report_table.setItem(i, 2, QTableWidgetItem(rec["title"]))
            params = "; ".join(f"{k}={v}" for k, v in rec["params"].items())
            self.report_table.setItem(i, 3, QTableWidgetItem(params[:80]))
            results = "; ".join(f"{k}={v}" for k, v in rec["results"].items())
            self.report_table.setItem(i, 4, QTableWidgetItem(results[:80]))
            notes = "; ".join(rec["notes"]) if rec["notes"] else ""
            self.report_table.setItem(i, 5, QTableWidgetItem(notes))
            self.report_table.setItem(i, 6, QTableWidgetItem(rec.get("timestamp", "")))

    def _export_pdf(self):
        self._refresh_report_table()
        if not self.store.results:
            QMessageBox.information(self, "Información", "No hay cálculos para exportar. Realice algún cálculo primero.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar PDF", os.path.expanduser("~/Electricitron_Informe.pdf"),
            "Archivos PDF (*.pdf)"
        )
        if path:
            try:
                self.store.pdf_manager.generate_pdf(path)
                QMessageBox.information(self, "Éxito", f"PDF exportado correctamente:\n{path}")
                self._update_status("PDF exportado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error al exportar PDF", str(e))

    def _export_excel(self):
        self._refresh_report_table()
        if not self.store.results:
            QMessageBox.information(self, "Información", "No hay cálculos para exportar. Realice algún cálculo primero.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar Excel", os.path.expanduser("~/Electricitron_Informe.xlsx"),
            "Archivos Excel (*.xlsx)"
        )
        if path:
            try:
                self.store.excel_manager.generate_excel(path)
                QMessageBox.information(self, "Éxito", f"Excel exportado correctamente:\n{path}")
                self._update_status("Excel exportado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error al exportar Excel", str(e))

    def _delete_record(self):
        rid = self.del_id.value()
        if rid == 0:
            QMessageBox.warning(self, "Error", "Introduce un ID válido.")
            return
        self.store.delete(rid)
        self._refresh_report_table()
        self._update_status(f"Registro {rid} eliminado")

    def _clear_report(self):
        reply = QMessageBox.question(
            self, "Confirmar",
            "¿Eliminar todos los registros del informe?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.store.clear()
            self._refresh_report_table()
            self._update_status("Todos los registros eliminados")


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(MAIN_STYLESHEET)
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
