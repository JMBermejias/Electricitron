"""Módulo de secciones de conductor y caída de tensión."""
import math


CABLE_TABLES = {
    "Cu flexible": {
        "0.5": 9, "0.75": 12, "1": 16, "1.5": 20, "2.5": 28, "4": 38,
        "6": 50, "10": 70, "16": 95, "25": 125, "35": 160, "50": 200,
        "70": 255, "95": 310, "120": 360, "150": 420, "185": 480, "240": 580, "300": 700
    },
    "Cu rígido": {
        "1.5": 17.5, "2.5": 24, "4": 32, "6": 41, "10": 57, "16": 76,
        "25": 101, "35": 125, "50": 157, "70": 200, "95": 245, "120": 286,
        "150": 330, "185": 378, "240": 450, "300": 530, "400": 650, "500": 780, "630": 940
    },
    "Al rígido": {
        "16": 46, "25": 64, "35": 82, "50": 104, "70": 136, "95": 170,
        "120": 196, "150": 225, "185": 261, "240": 313, "300": 368, "400": 448, "500": 535, "630": 650
    }
}

SECTION_STANDARDS = ["0.75", "1", "1.5", "2.5", "4", "6", "10", "16", "25", "35", "50", "70", "95", "120", "150", "185", "240", "300", "400", "500", "630"]


class CableCalculations:
    """Cálculos de secciones de conductor y caída de tensión."""

    @staticmethod
    def seccion_por_corriente(corriente, tipo_cable="Cu rígido"):
        """Determinar sección mínima según corriente transportada."""
        tabla = CABLE_TABLES.get(tipo_cable, CABLE_TABLES["Cu rígido"])
        for seccion, ampacidad in sorted(tabla.items(), key=lambda x: float(x[0])):
            if ampacidad >= corriente:
                return {"seccion_min": seccion, "ampacidad": ampacidad, "tipo": tipo_cable}
        return {"seccion_min": "No encontrada", "ampacidad": None, "tipo": tipo_cable}

    @staticmethod
    def seccion_por_caida_tension(voltaje, longitud, corriente, caida_max_pct=3, tipo_cable="Cu rígido", trifasico=True):
        """Sección mínima según caída de tensión admisible."""
        rho = 0.0178 if "Cu" in tipo_cable else 0.0282
        caida_max = voltaje * caida_max_pct / 100
        if trifasico:
            seccion = math.sqrt(3) * rho * longitud * corriente / caida_max
        else:
            seccion = 2 * rho * longitud * corriente / caida_max
        seccion_redondeada = CableCalculations._redondear_seccion(seccion)
        return {
            "seccion_exacta": round(seccion, 4),
            "seccion_recomendada": seccion_redondeada,
            "caida_tension_max": round(caida_max, 4),
            "porcentaje": caida_max_pct
        }

    @staticmethod
    def caida_tension_conductor(voltaje, longitud, corriente, seccion, tipo_cable="Cu rígido", trifasico=True):
        """Calcular caída de tensión real."""
        rho = 0.0178 if "Cu" in tipo_cable else 0.0282
        if trifasico:
            dv = math.sqrt(3) * rho * longitud * corriente / seccion
        else:
            dv = 2 * rho * longitud * corriente / seccion
        porcentaje = (dv / voltaje) * 100
        return {
            "caida_tension_v": round(dv, 4),
            "caida_tension_pct": round(porcentaje, 2),
            "voltaje_final": round(voltaje - dv, 4),
            "dentro_norma": porcentaje <= 3
        }

    @staticmethod
    def ampacidad_seccion(seccion, tipo_cable="Cu rígido", temperatura=30):
        """Obtener ampacidad para una sección dada."""
        tabla = CABLE_TABLES.get(tipo_cable, CABLE_TABLES["Cu rígido"])
        amp = tabla.get(str(seccion))
        if amp is None:
            return {"seccion": seccion, "ampacidad": None, "mensaje": "Sección no encontrada en tabla"}
        factor_temp = 1 - 0.01 * (temperatura - 30) if temperatura > 30 else 1 + 0.005 * (30 - temperatura)
        amp_corregida = round(amp * factor_temp, 1)
        return {"seccion": seccion, "ampacidad_base": amp, "ampacidad_corregida": amp_corregida, "temperatura": temperatura}

    @staticmethod
    def capacidad_carga(voltaje, corriente, fp=1.0, trifasico=True):
        """Capacidad de carga en kW."""
        if trifasico:
            return round(math.sqrt(3) * voltaje * corriente * fp / 1000, 4)
        return round(voltaje * corriente * fp / 1000, 4)

    @staticmethod
    def num_circuitos(total_corriente, corriente_por_circuito):
        """Número de circuitos necesarios."""
        num = math.ceil(total_corriente / corriente_por_circuito)
        return {"num_circuitos": num, "total_corriente": total_corriente, "corriente_circuito": corriente_por_circuito}

    @staticmethod
    def tabla_secciones_disponibles(tipo_cable="Cu rígido"):
        """Retorna tabla de secciones y ampacidades."""
        tabla = CABLE_TABLES.get(tipo_cable, CABLE_TABLES["Cu rígido"])
        resultado = []
        for seccion, ampacidad in sorted(tabla.items(), key=lambda x: float(x[0])):
            resultado.append({"seccion_mm2": seccion, "ampacidad_a": ampacidad})
        return resultado

    @staticmethod
    def _redondear_seccion(seccion_exacta):
        """Redondear a la sección estándar superior."""
        for s in SECTION_STANDARDS:
            if float(s) >= seccion_exacta:
                return s
        return SECTION_STANDARDS[-1]

    @staticmethod
    def potencia_maxima_circuito(voltaje, seccion, tipo_cable="Cu rígido", fp=1.0, trifasico=True):
        """Potencia máxima según sección y corriente."""
        tabla = CABLE_TABLES.get(tipo_cable, CABLE_TABLES["Cu rígido"])
        ampacidad = tabla.get(str(seccion), 0)
        if trifasico:
            return round(math.sqrt(3) * voltaje * ampacidad * fp / 1000, 4)
        return round(voltaje * ampacidad * fp / 1000, 4)
