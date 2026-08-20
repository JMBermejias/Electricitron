"""Generación de informes PDF con ReportLab."""
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable,
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class ReportGenerator:
    """Generador de informes PDF profesionales."""

    COLORS = {
        "primary": colors.HexColor("#2980b9"),
        "primary_dark": colors.HexColor("#1a5276"),
        "accent": colors.HexColor("#85c1e9"),
        "bg_light": colors.HexColor("#f0f6fc"),
        "bg_table": colors.HexColor("#eaf2f8"),
        "text_dark": colors.HexColor("#2c3e50"),
        "text_light": colors.HexColor("#5d6d7e"),
        "success": colors.HexColor("#27ae60"),
        "warning": colors.HexColor("#f39c12"),
        "danger": colors.HexColor("#e74c3c"),
        "white": colors.white,
        "border": colors.HexColor("#d5dbdb"),
    }

    def __init__(self, output_path, project_name="Instalación Eléctrica", engineer="Ingeniero"):
        self.output_path = output_path
        self.project_name = project_name
        self.engineer = engineer
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
        )
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.elements = []

    def _setup_custom_styles(self):
        """Configurar estilos personalizados."""
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=self.COLORS["primary_dark"],
            spaceAfter=6,
            alignment=TA_CENTER,
        ))
        self.styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=self.COLORS["text_light"],
            alignment=TA_CENTER,
            spaceAfter=20,
        ))
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=self.COLORS["primary_dark"],
            spaceBefore=20,
            spaceAfter=10,
            borderWidth=0,
        ))
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Heading2'],
            fontSize=13,
            textColor=self.COLORS["primary"],
            spaceBefore=12,
            spaceAfter=6,
        ))
        self.styles.add(ParagraphStyle(
            name='BodyText2',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.COLORS["text_dark"],
            spaceAfter=4,
        ))
        self.styles.add(ParagraphStyle(
            name='ResultText',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.COLORS["primary_dark"],
            fontName='Helvetica-Bold',
            spaceAfter=4,
        ))
        self.styles.add(ParagraphStyle(
            name='FooterStyle',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=self.COLORS["text_light"],
            alignment=TA_CENTER,
        ))

    def add_cover_page(self):
        """Añadir portada al informe."""
        self.elements.append(Spacer(1, 3 * cm))
        self.elements.append(Paragraph("ELECTRICITRON", self.styles['ReportTitle']))
        self.elements.append(Spacer(1, 0.5 * cm))
        self.elements.append(HRFlowable(
            width="80%", thickness=2, color=self.COLORS["primary"],
            spaceAfter=20, spaceBefore=10
        ))
        self.elements.append(Paragraph(self.project_name, self.styles['ReportSubtitle']))
        self.elements.append(Paragraph(
            f"Ingeniero: {self.engineer}",
            self.styles['ReportSubtitle']
        ))
        self.elements.append(Paragraph(
            f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            self.styles['ReportSubtitle']
        ))
        self.elements.append(Spacer(1, 2 * cm))
        self.elements.append(Paragraph(
            "Software de cálculos eléctricos y telecomunicaciones",
            self.styles['ReportSubtitle']
        ))
        self.elements.append(PageBreak())

    def add_section(self, title, content):
        """Añadir sección al informe."""
        self.elements.append(Paragraph(title, self.styles['SectionHeader']))
        self.elements.append(HRFlowable(
            width="100%", thickness=1, color=self.COLORS["accent"],
            spaceAfter=10
        ))
        if isinstance(content, str):
            self.elements.append(Paragraph(content, self.styles['BodyText2']))
        elif isinstance(content, list):
            for item in content:
                self.elements.append(Paragraph(f"• {item}", self.styles['BodyText2']))

    def add_table(self, title, headers, data, column_widths=None):
        """Añadir tabla al informe."""
        self.elements.append(Paragraph(title, self.styles['SubHeader']))
        table_data = [headers] + data
        if column_widths is None:
            col_w = (A4[0] - 4 * cm) / len(headers)
            column_widths = [col_w] * len(headers)

        table = Table(table_data, colWidths=column_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS["primary"]),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.COLORS["white"]),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, -1), self.COLORS["white"]),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [self.COLORS["white"], self.COLORS["bg_table"]]),
            ('GRID', (0, 0), (-1, -1), 0.5, self.COLORS["border"]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        self.elements.append(table)
        self.elements.append(Spacer(1, 0.5 * cm))

    def add_results_table(self, title, results_dict):
        """Añadir tabla de resultados key-value."""
        self.elements.append(Paragraph(title, self.styles['SubHeader']))
        data = []
        for key, value in results_dict.items():
            clean_key = key.replace("_", " ").title()
            data.append([clean_key, str(value)])
        headers = ["Parámetro", "Valor"]
        table = Table([headers] + data, colWidths=[8 * cm, 8 * cm], repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS["primary"]),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.COLORS["white"]),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (0, -1), self.COLORS["bg_table"]),
            ('GRID', (0, 0), (-1, -1), 0.5, self.COLORS["border"]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        self.elements.append(table)
        self.elements.append(Spacer(1, 0.5 * cm))

    def add_calculation_result(self, title, params, results, notes=None):
        """Añadir resultado de cálculo completo."""
        self.elements.append(Paragraph(title, self.styles['SubHeader']))
        self.elements.append(HRFlowable(
            width="100%", thickness=0.5, color=self.COLORS["accent"],
            spaceAfter=8
        ))
        if params:
            self.elements.append(Paragraph("<b>Entrada:</b>", self.styles['BodyText2']))
            for k, v in params.items():
                clean = k.replace("_", " ").title()
                self.elements.append(Paragraph(f"  {clean}: {v}", self.styles['BodyText2']))
            self.elements.append(Spacer(1, 0.3 * cm))

        self.elements.append(Paragraph("<b>Resultado:</b>", self.styles['ResultText']))
        for k, v in results.items():
            clean = k.replace("_", " ").title()
            self.elements.append(Paragraph(f"  {clean}: <b>{v}</b>", self.styles['BodyText2']))

        if notes:
            self.elements.append(Spacer(1, 0.3 * cm))
            self.elements.append(Paragraph("<b>Notas:</b>", self.styles['BodyText2']))
            for note in notes:
                self.elements.append(Paragraph(f"  • {note}", self.styles['BodyText2']))
        self.elements.append(Spacer(1, 0.5 * cm))

    def add_page_break(self):
        """Añadir salto de página."""
        self.elements.append(PageBreak())

    def add_footer_note(self, text):
        """Añadir nota al pie de página."""
        self.elements.append(Spacer(1, 1 * cm))
        self.elements.append(HRFlowable(
            width="100%", thickness=1, color=self.COLORS["border"],
            spaceAfter=8
        ))
        self.elements.append(Paragraph(text, self.styles['FooterStyle']))

    def generate(self):
        """Generar el archivo PDF."""
        self.doc.build(self.elements)
        return self.output_path


class ReportManager:
    """Gestión de informes: crear, editar, eliminar registros."""

    def __init__(self):
        self.records = []
        self.current_record = None

    def add_record(self, category, title, params, results, notes=None):
        """Añadir registro al informe."""
        record = {
            "id": len(self.records) + 1,
            "category": category,
            "title": title,
            "params": params,
            "results": results,
            "notes": notes or [],
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        self.records.append(record)
        return record

    def modify_record(self, record_id, **kwargs):
        """Modificar un registro existente."""
        for record in self.records:
            if record["id"] == record_id:
                for key, value in kwargs.items():
                    if key in record:
                        record[key] = value
                return record
        return None

    def delete_record(self, record_id):
        """Eliminar un registro."""
        self.records = [r for r in self.records if r["id"] != record_id]

    def get_records_by_category(self, category):
        """Obtener registros por categoría."""
        return [r for r in self.records if r["category"] == category]

    def get_all_records(self):
        """Obtener todos los registros."""
        return self.records

    def clear_all(self):
        """Limpiar todos los registros."""
        self.records.clear()

    def generate_pdf(self, output_path, project_name="Instalación Eléctrica", engineer="Ingeniero"):
        """Generar PDF con todos los registros."""
        generator = ReportGenerator(output_path, project_name, engineer)
        generator.add_cover_page()

        categories = {}
        for record in self.records:
            cat = record["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(record)

        category_names = {
            "basico": "Cálculos Eléctricos Básicos",
            "cable": "Secciones y Cables",
            "proteccion": "Protecciones",
            "instalacion": "Instalaciones Eléctricas",
            "telecom": "Telecomunicaciones",
            "distancia": "Distancias y Líneas",
        }

        for cat, records in categories.items():
            generator.add_section(category_names.get(cat, cat.title()))
            for rec in records:
                generator.add_calculation_result(
                    rec["title"], rec["params"], rec["results"], rec["notes"]
                )
            generator.add_page_break()

        generator.add_footer_note(
            f"Generado por Electricitron v1.1.3 | {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )
        return generator.generate()
