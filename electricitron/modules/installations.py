"""Módulo de instalaciones eléctricas - BT, MT, HT, esquemas unifilares."""
import math


SCHEMES = {
    "TN-S": {"descripcion": "Neutro y PE separados", "uso": "Instalaciones industriales y terciarias"},
    "TN-C": {"descripcion": "PEN unificado", "uso": "Instalaciones antiguas, ya no recomendado"},
    "TN-C-S": {"descripcion": "PEN hasta cuadro, separación después", "uso": "Edificios residenciales"},
    "TT": {"descripcion": "Masas a tierra local", "uso": "Zonas rurales, industria"},
    "IT": {"descripcion": "Aislamiento de fase", "uso": "Hospitales, centros de datos"},
}

CIRCUITS = [
    "General de mando y protección",
    "Iluminación",
    "Tomas de corriente generales",
    "Tomas de corriente de cocina",
    "Tomas de corriente de baño",
    "Tomas de corriente específicas",
    "Calefacción/Refrigeración",
    "AC (Aire acondicionado)",
    "Motores/Industrial",
    "Ascensores",
    "Bomberos",
    "CCTV/Seguridad",
]


class InstallationCalculations:
    """Cálculos para instalaciones eléctricas."""

    @staticmethod
    def potencia_instalacion(cargas):
        """Calcular potencia total de la instalación."""
        total_activa = sum(c.get("potencia", 0) * c.get("demanda", 1.0) for c in cargas)
        total_reactiva = sum(c.get("potencia", 0) * c.get("demanda", 1.0) * math.tan(math.acos(c.get("fp", 1.0))) for c in cargas)
        fp_medio = math.cos(math.atan(total_reactiva / total_activa)) if total_activa > 0 else 0
        total_aparente = math.sqrt(total_activa**2 + total_reactiva**2)
        return {
            "potencia_activa": round(total_activa, 2),
            "potencia_reactiva": round(total_reactiva, 2),
            "potencia_aparente": round(total_aparente, 2),
            "factor_potencia": round(fp_medio, 4),
            "num_cargas": len(cargas),
        }

    @staticmethod
    def intensidad_general(potencia_activa, tension, fp=0.9, trifasico=True, sobrecarga=1.25):
        """Intensidad en bornes del origen de alimentación."""
        if trifasico:
            I = potencia_activa / (math.sqrt(3) * tension * fp)
        else:
            I = potencia_activa / (tension * fp)
        return {
            "intensidad_nominal": round(I, 2),
            "intensidad_con_sobrecarga": round(I * sobrecarga, 2),
            "tension": tension,
            "fp": fp,
        }

    @staticmethod
    def seccion_linea_alimentacion(intensidad, longitud, voltaje, caida_max=3, trifasico=True):
        """Sección de la línea de alimentación."""
        rho = 0.0178
        caida = voltaje * caida_max / 100
        if trifasico:
            seccion = math.sqrt(3) * rho * longitud * intensidad / caida
        else:
            seccion = 2 * rho * longitud * intensidad / caida
        from .cable_calc import CableCalculations
        rec = CableCalculations._redondear_seccion(seccion)
        return {
            "seccion_exacta": round(seccion, 4),
            "seccion_recomendada": rec,
            "caida_tension_pct": caida_max,
        }

    @staticmethod
    def esquema_proteccion(tipo_sistema="TN-S", corriente_resistencia=None):
        """Generar esquema de protección según norma."""
        info = SCHEMES.get(tipo_sistema, SCHEMES["TN-S"])
        return {
            "sistema": tipo_sistema,
            "descripcion": info["descripcion"],
            "uso_recomendado": info["uso"],
            "proteccion": [
                "Interruptor magnetotermico general",
                "Diferencial 30mA en circuitos de baño",
                "Diferencial 300mA en circuitos generales",
                "Protección contra sobretensiones (PRT)",
            ],
            "normas": ["REBT", "IEC 60364", "IEC 61439"],
        }

    @staticmethod
    def criterios_diseno(tension_nominal, sistema="TN-S"):
        """Criterios de diseño de la instalación."""
        niveles = {
            "BT": {"tension_max": 1000, "tension_nom": 400, "descripcion": "Baja tensión"},
            "MT": {"tension_max": 36000, "tension_nom": 20000, "descripcion": "Media tensión"},
            "HT": {"tension_max": 300000, "tension_nom": 132000, "descripcion": "Alta tensión"},
        }
        nivel = "BT" if tension_nominal <= 1000 else "MT" if tension_nominal <= 36000 else "HT"
        return {
            "nivel_tension": nivel,
            "descripcion": niveles[nivel]["descripcion"],
            "tension_nominal": tension_nominal,
            "criterios": [
                "Coordinación de protecciones",
                "Continuidad de servicio",
                "Selectividad",
                "Limitación de corrientes de defecto",
            ],
        }

    @staticmethod
    def selectividad(In_sup, In_inf, curva_sup="C", curva_inf="C"):
        """Verificar selectividad entre protecciones."""
        return {
            "In_superior": In_sup,
            "In_inferior": In_inf,
            "ratio": round(In_sup / In_inf, 2) if In_inf > 0 else 0,
            "selectivo": In_sup >= 2.5 * In_inf,
            "recomendacion": "Selectivo" if In_sup >= 2.5 * In_inf else "Parcial o no selectivo",
        }

    @staticmethod
    def acometida(tipo_acometida="subterranea", longitud=50):
        """Dimensionamiento de acometida."""
        tipos = {
            "subterranea": {"seccion_min": "16 mm² Cu", "proteccion": "En cabecera", "ejecucion": "Enterrado"},
            "aerea": {"seccion_min": "16 mm² Cu / 25 mm² Al", "proteccion": "En entrada", "ejecucion": "Aérea"},
            "baja_tension": {"seccion_min": "10 mm² Cu", "proteccion": "En tablero general", "ejecucion": "Mixta"},
        }
        info = tipos.get(tipo_acometida, tipos["subterranea"])
        return {
            "tipo": tipo_acometida,
            "longitud": longitud,
            **info,
        }

    @staticmethod
    def lineas_generales(tension, potencia, longitud, fp=0.9, caida_max=3):
        """Dimensionamiento de líneas generales."""
        I = potencia / (math.sqrt(3) * tension * fp)
        rho = 0.0178
        caida = tension * caida_max / 100
        seccion = math.sqrt(3) * rho * longitud * I / caida
        from .cable_calc import CableCalculations
        rec = CableCalculations._redondear_seccion(seccion)
        return {
            "intensidad": round(I, 2),
            "seccion_exacta": round(seccion, 4),
            "seccion_recomendada": rec,
            "potencia": potencia,
            "longitud": longitud,
        }

    @staticmethod
    def circuitos_mandos_cargas(cargas):
        """Dimensionar circuitos individuales."""
        resultados = []
        for i, carga in enumerate(cargas, 1):
            V = carga.get("tension", 230)
            P = carga.get("potencia", 0)
            fp = carga.get("fp", 1.0)
            I = P / (V * fp) if V > 0 and fp > 0 else 0
            from .cable_calc import CableCalculations
            secc = CableCalculations.seccion_por_corriente(I)
            from .protections import ProtectionCalculations
            prot = ProtectionCalculations.seleccionar_interruptor(I)
            resultados.append({
                "circuito": i,
                "descripcion": carga.get("descripcion", f"Carga {i}"),
                "intensidad": round(I, 2),
                "seccion": secc["seccion_min"],
                "proteccion": f"{prot['In_seleccionado']}A curva {prot['curva']}",
            })
        return resultados

    @staticmethod
    def condiciones_ambiente(temperatura=30, altitud=0, humedad=50):
        """Condiciones ambientales para selección de equipos."""
        return {
            "temperatura": temperatura,
            "altitud": altitud,
            "humedad_relativa": humedad,
            "correccion_temperatura": round(1 - 0.01 * (temperatura - 30), 2) if temperatura > 30 else 1,
            "correccion_altitud": round(1 - 0.005 * max(0, (altitud - 1000) / 100), 2),
        }
