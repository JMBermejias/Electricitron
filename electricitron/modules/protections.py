"""Módulo de protecciones eléctricas - Interruptores, fusibles, curvas."""
import math


BREAKER_CURVES = {
    "B": {"descripcion": "Resistente a sobrecargas, para cargas resistivas", "rango_i2_i1": (1.45, 5)},
    "C": {"descripcion": "Uso general, cargas mixtas", "rango_i2_i1": (1.45, 10)},
    "D": {"descripcion": "Cargas inductivas, motores", "rango_i2_i1": (1.45, 20)},
    "K": {"descripcion": "Motores y transformadores", "rango_i2_i1": (1.45, 12)},
    "Z": {"descripcion": "Cargas electrónicas sensibles", "rango_i2_i1": (1.45, 3)},
}

INTERRUPTOR_SIZES = [6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3200, 4000]

FUSIBLE_SIZES = [2, 4, 6, 8, 10, 12, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000]

PROTECTIONS = [
    "Interruptor automático unipolar",
    "Interruptor automático bipolar",
    "Interruptor automático tripolar",
    "Interruptor automático tetrapolar",
    "Interruptor diferencial 2P",
    "Interruptor diferencial 4P",
    "Fusible NH",
    "Fusible/cartucho",
    "PRT (Protector contra sobretensiones)",
    "IGBT / Disyuntor de potencia",
]


class ProtectionCalculations:
    """Cálculos de protecciones eléctricas."""

    @staticmethod
    def seleccionar_interruptor(corriente_circuito, curva="C"):
        """Seleccionar interruptor automático según corriente del circuito."""
        margen = 1.25
        in_min = corriente_circuito * margen
        seleccion = None
        for in_val in INTERRUPTOR_SIZES:
            if in_val >= in_min:
                seleccion = in_val
                break
        if seleccion is None:
            seleccion = INTERRUPTOR_SIZES[-1]
        info_curva = BREAKER_CURVES.get(curva, BREAKER_CURVES["C"])
        return {
            "in_seleccionado": seleccion,
            "curva": curva,
            "descripcion_curva": info_curva["descripcion"],
            "corriente_circuito": corriente_circuito,
            "margen": f"{(seleccion/corriente_circuito - 1)*100:.1f}%",
            "i2_i1_min": info_curva["rango_i2_i1"][0],
            "i2_i1_max": info_curva["rango_i2_i1"][1],
            "corriente_magnetica_min": round(seleccion * info_curva["rango_i2_i1"][0], 1),
            "corriente_magnetica_max": round(seleccion * info_curva["rango_i2_i1"][1], 1),
        }

    @staticmethod
    def seleccionar_diferencial(corriente_circuito, tipo="30mA"):
        """Seleccionar interruptor diferencial."""
        In = None
        for in_val in INTERRUPTOR_SIZES:
            if in_val >= corriente_circuito * 1.25:
                In = in_val
                break
        if In is None:
            In = INTERRUPTOR_SIZES[-1]
        sensibilidades = {
            "30mA": {"uso": "Protección de personas", "norma": "IEC 61008"},
            "100mA": {"uso": "Protección contra incendios", "norma": "IEC 61008"},
            "300mA": {"uso": "Detección de fugas", "norma": "IEC 61008"},
        }
        sens = sensibilidades.get(tipo, sensibilidades["30mA"])
        return {
            "In_seleccionado": In,
            "sensibilidad": tipo,
            "uso": sens["uso"],
            "norma": sens["norma"],
        }

    @staticmethod
    def seleccionar_fusible(corriente_circuito, tipo="gG"):
        """Seleccionar fusible de protección."""
        in_min = corriente_circuito * 1.25
        seleccion = None
        for in_val in FUSIBLE_SIZES:
            if in_val >= in_min:
                seleccion = in_val
                break
        if seleccion is None:
            seleccion = FUSIBLE_SIZES[-1]
        tipos = {
            "gG": "Protección general de cables",
            "aM": "Protección de motores",
            "gR": "Protección semiconductor",
        }
        return {
            "In_seleccionado": seleccion,
            "tipo": tipo,
            "descripcion": tipos.get(tipo, "General"),
            "corriente_circuito": corriente_circuito,
        }

    @staticmethod
    def proteccion_sobrecarga(corriente_nominal, tipo_equipo="general"):
        """Corriente de protección contra sobrecarga."""
        factores = {
            "general": 1.0,
            "motor": 1.5,
            "transformador": 1.25,
            "banco_condensadores": 1.3,
        }
        factor = factores.get(tipo_equipo, 1.0)
        Isob = round(corriente_nominal * factor, 2)
        return {
            "corriente_sobrecarga": Isob,
            "factor": factor,
            "tipo_equipo": tipo_equipo,
        }

    @staticmethod
    def coordenacion_protecciones(corriente_cortocircuito, interruptor_seleccionado):
        """Verificar capacidad de corte."""
        return {
            "icc": corriente_cortocircuito,
            "capacidad_corte_in": interruptor_seleccionado,
            "coordinado": interruptor_seleccionado >= corriente_cortocircuito,
        }

    @staticmethod
    def tabla_corriente_magnetica(In, curva="C"):
        """Tabla de corrientes magnéticas según curva."""
        info = BREAKER_CURVES.get(curva, BREAKER_CURVES["C"])
        i_min = In * info["rango_i2_i1"][0]
        i_max = In * info["rango_i2_i1"][1]
        return {
            "In": In,
            "curva": curva,
            "I_mag_min": round(i_min, 1),
            "I_mag_max": round(i_max, 1),
            "descripcion": info["descripcion"],
            "tabla_detallada": [
                {"regla": "I2/I1 ≥ 1.45 (sobrecarga)", "valor": round(i_min, 1)},
                {"regla": f"I ≤ {info['rango_i2_i1'][1]}×In (cortocircuito)", "valor": round(i_max, 1)},
            ]
        }

    @staticmethod
    def proteccion_descargadores(tension_sistema, categoria_UBO="II"):
        """Selección de descargadores de sobretensión."""
        niveles = {
            "I": {"limite_sobretension": 6.0, "descripcion": "Zona de transición"},
            "II": {"limite_sobretension": 4.0, "descripcion": "Instalaciones fijas"},
            "III": {"limite_sobretension": 2.5, "descripcion": "Equipos sensibles"},
            "IV": {"limite_sobretension": 1.5, "descripcion": "Electrónica de precisión"},
        }
        nivel = niveles.get(categoria_UBO, niveles["II"])
        Uo = tension_sistema
        Up = nivel["limite_sobretension"] * Uo
        return {
            "categoria": categoria_UBO,
            "Uo": Uo,
            "Up_max": round(Up, 2),
            "descripcion": nivel["descripcion"],
        }
