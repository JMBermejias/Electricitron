"""Módulo de cálculos de telecomunicaciones y enlaces de datos."""
import math


FRECUENCIAS_WIFI = {
    "2.4GHz": {"canal_1": 2412, "canal_6": 2437, "canal_11": 2462, "ancho_banda": 40, "max_dbm": 20},
    "5GHz": {"canal_36": 5180, "canal_52": 5260, "canal_149": 5745, "ancho_banda": 80, "max_dbm": 23},
}

CABLES_DATOS = {
    "Cat5e": {"velocidad": "1 Gbps", "frecuencia": 100, "max_longitud": 100, "par": 4},
    "Cat6": {"velocidad": "10 Gbps", "frecuencia": 250, "max_longitud": 100, "par": 4},
    "Cat6a": {"velocidad": "10 Gbps", "frecuencia": 500, "max_longitud": 100, "par": 4},
    "Cat7": {"velocidad": "10 Gbps", "frecuencia": 600, "max_longitud": 100, "par": 4},
    "Cat8": {"velocidad": "25/40 Gbps", "frecuencia": 2000, "max_longitud": 30, "par": 4},
    "OM3": {"velocidad": "10 Gbps", "frecuencia": "multimodo", "max_longitud": 300, "par": 0},
    "OM4": {"velocidad": "100 Gbps", "frecuencia": "multimodo", "max_longitud": 400, "par": 0},
    "OS2": {"velocidad": "100 Gbps", "frecuencia": "monomodo", "max_longitud": 100000, "par": 0},
}

TIPOSEÑAL = ["RJ45 (cobre)", "Fibra óptica multimodo (OM3/OM4)", "Fibra óptica monomodo (OS2)", "Microondas", "Satelital"]


class TelecomCalculations:
    """Cálculos de telecomunicaciones."""

    @staticmethod
    def enlace_inalambrico(distancia_km, frecuencia_ghz, atenuacion_lluvia_dbkm=0):
        """Cálculo de enlace inalámbrico punto a punto."""
        atenuacion_freespace = 20 * math.log10(4 * math.pi * distancia_km * frecuencia_ghz / 0.3)
        atenuacion_total = atenuacion_freespace + (atenuacion_lluvia_dbkm * distancia_km)
        return {
            "distancia_km": distancia_km,
            "frecuencia_ghz": frecuencia_ghz,
            "atenuacion_freespace_db": round(atenuacion_freespace, 2),
            "atenuacion_lluvia_db": round(atenuacion_lluvia_dbkm * distancia_km, 2),
            "atenuacion_total_db": round(atenuacion_total, 2),
        }

    @staticmethod
    def perdida_cable_red(longitud, tipo_cable="Cat6"):
        """Pérdida de inserción del cable de red."""
        datos = CABLES_DATOS.get(tipo_cable, CABLES_DATOS["Cat6"])
        atenuacion_db_100m = {"Cat5e": 19.8, "Cat6": 19.8, "Cat6a": 19.8, "Cat7": 20.0, "Cat8": 32.0}
        atenuacion_base = atenuacion_db_100m.get(tipo_cable, 19.8)
        atenuacion = (longitud / 100) * atenuacion_base
        return {
            "longitud": longitud,
            "tipo_cable": tipo_cable,
            "velocidad": datos["velocidad"],
            "perdida_db": round(atenuacion, 2),
            "longitud_maxima": datos["max_longitud"],
            "dentro_norma": longitud <= datos["max_longitud"],
        }

    @staticmethod
    def fibra_optica(tipo="monomodo", distancia_km=1):
        """Cálculo de enlace de fibra óptica."""
        atenuaciones = {"monomodo": 0.35, "multimodo": 2.5}
        atenuacion = atenuaciones.get(tipo, 0.35)
        perdida_total = atenuacion * distancia_km
        return {
            "tipo": tipo,
            "distancia_km": distancia_km,
            "atenuacion_db_km": atenuacion,
            "perdida_total_db": round(perdida_total, 2),
            "distancia_maxima": 100000 if tipo == "monomodo" else 400,
        }

    @staticmethod
    def potencia_receptor_dbm(potencia_tx_dbm, ganancia_tx_dbi, ganancia_rx_dbi, atenuacion_cable_db, atenuacion_atmosferica_db):
        """Nivel de señal en receptor."""
        prx = potencia_tx_dbm + ganancia_tx_dbi + ganancia_rx_dbi - atenuacion_cable_db - atenuacion_atmosferica_db
        return {
            "potencia_receptor_dbm": round(prx, 2),
            "potencia_tx": potencia_tx_dbm,
            "ganancia_total_dbi": round(ganancia_tx_dbi + ganancia_rx_dbi, 2),
            "perdidas_total_db": round(atenuacion_cable_db + atenuacion_atmosferica_db, 2),
        }

    @staticmethod
    def balance_enlace(prx_dbm, sensibilidad_rx_dbm):
        """Balance de enlace radioeléctrico."""
        margen = prx_dbm - sensibilidad_rx_dbm
        return {
            "potencia_rx": prx_dbm,
            "sensibilidad_rx": sensibilidad_rx_dbm,
            "margen_db": round(margen, 2),
            "suficiente": margen >= 3,
            "recomendacion": "Enlace viable" if margen >= 3 else "Enlace insuficiente",
        }

    @staticmethod
    def ruido_thermal_dbm(frecuencia_hz, ancho_banda_hz):
        """Ruido térmico kTB."""
        k = 1.38e-23
        T = 290
        N = k * T * ancho_banda_hz
        n_dbm = 10 * math.log10(N) + 30
        return {"ruido_dbm": round(n_dbm, 2), "frecuencia_hz": frecuencia_hz, "ancho_banda_hz": ancho_banda_hz}

    @staticmethod
    def sectores_wifi(num_dispositivos, ancho_banda_requerido_mbps):
        """Dimensionamiento de red WiFi."""
        ap_necesarios = math.ceil(num_dispositivos / 25)
        return {
            "num_dispositivos": num_dispositivos,
            "ap_necesarios": ap_necesarios,
            "ancho_banda_requerido": ancho_banda_requerido_mbps,
            "ancho_banda_por_ap": round(ancho_banda_requerido_mbps / ap_necesarios, 2),
        }

    @staticmethod
    def fiber_channel(distancia_km, tipo_fibra="monomodo"):
        """Cálculo de canal de fibra óptica con pérdida total."""
        datos_fibra = TelecomCalculations.fibra_optica(tipo_fibra, distancia_km)
        conectores = 4 * 0.5
        empalmes = math.ceil(distancia_km / 2) * 0.1
        perdida_total = datos_fibra["perdida_total_db"] + conectores + empalmes
        return {
            **datos_fibra,
            "perdida_conectores_db": round(conectores, 2),
            "perdida_empalmes_db": round(empalmes, 2),
            "perdida_total_sistema_db": round(perdida_total, 2),
        }

    @staticmethod
    def potencia_fibra_needed(distancia_km, potencia_tx_dbm=0, margen_seguridad_db=3, tipo_fibra="monomodo"):
        """Potencia mínima del transmisor."""
        datos = TelecomCalculations.fibra_optica(tipo_fibra, distancia_km)
        potencia_min = datos["perdida_total_db"] + margen_seguridad_db
        return {
            "potencia_tx_recomendada_dbm": round(potencia_min, 2),
            "potencia_tx_dbm": potencia_tx_dbm,
            "margen_seguridad": margen_seguridad_db,
            "suficiente": potencia_tx_dbm >= potencia_min,
        }
