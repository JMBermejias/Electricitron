"""Módulo de cálculos de distancias y tensiones en líneas eléctricas."""
import math


class DistanceCalculations:
    """Cálculos de distancias para líneas eléctricas."""

    @staticmethod
    def distancia_linea_electrica(punto_a, punto_b):
        """Distancia entre dos puntos (3D) con diferencias de nivel."""
        dx = punto_b[0] - punto_a[0]
        dy = punto_b[1] - punto_a[1]
        dz = punto_b[2] - punto_a[2]
        horizontal = math.sqrt(dx**2 + dy**2)
        distancia_real = math.sqrt(dx**2 + dy**2 + dz**2)
        angulo = math.degrees(math.atan2(dz, horizontal)) if horizontal > 0 else 0
        return {
            "distancia_horizontal": round(horizontal, 4),
            "distancia_real": round(distancia_real, 4),
            "diferencia_nivel": round(dz, 4),
            "angulo_pendiente": round(angulo, 2),
        }

    @staticmethod
    def desplazamiento_holddown(carga, longitud_cable, peso_cable_por_m, viento_kmh, carga_viento):
        """Cálculo de desplazamiento lateral del conductor."""
        w_cable = peso_cable_por_m * 9.81
        w_viento = carga_viento * viento_kmh**2 / 1000
        f_total = math.sqrt(w_cable**2 + w_viento**2)
        desplazamiento = f_total * longitud_cable**2 / (8 * carga)
        return {
            "fuerza_cable": round(w_cable, 2),
            "fuerza_viento": round(w_viento, 2),
            "fuerza_total": round(f_total, 2),
            "desplazamiento_m": round(desplazamiento, 4),
        }

    @staticmethod
    def longitud_cable_entre_postos(altura_poste, dist_h_postos, flecha_cable):
        """Longitud de cable entre dos postos."""
        s_cable = dist_h_postos + 8 * flecha_cable**2 / (3 * dist_h_postos)
        return {
            "distancia_horizontal": dist_h_postos,
            "flecha": flecha_cable,
            "longitud_cable_estimada": round(s_cable, 4),
            "altura_poste": altura_poste,
        }

    @staticmethod
    def tension_mecanica_cable(carga_traccion, tension_superior, dist_postos, seccion):
        """Tensión mecánica máxima del conductor."""
        H = carga_traccion
        angulo = math.atan2(tension_superior, dist_postos) if dist_postos > 0 else 0
        T_max = H * math.sqrt(1 + (math.tan(angulo))**2)
        esfuerzo = T_max / seccion if seccion > 0 else 0
        return {
            "tension_maxima_n": round(T_max, 2),
            "esfuerzo_mpa": round(esfuerzo, 2),
            "angulo_cable": round(math.degrees(angulo), 2),
            "carga_inicial": carga_traccion,
        }

    @staticmethod
    def zona_postes(distancia_total, separacion_postes=50):
        """Número de postos y separación."""
        num_postos = math.ceil(distancia_total / separacion_postes)
        separacion_real = distancia_total / num_postos
        return {
            "distancia_total": distancia_total,
            "num_postos": num_postos,
            "separacion_media": round(separacion_real, 2),
            "num_tramos": num_postos - 1,
        }

    @staticmethod
    def caida_tension_linea_larga(voltaje, corriente, resistencia_por_km, distancia_km, trifasico=True):
        """Caída de tensión en líneas largas."""
        R_total = resistencia_por_km * distancia_km
        if trifasico:
            dv = math.sqrt(3) * corriente * R_total
        else:
            dv = 2 * corriente * R_total
        pct = (dv / voltaje) * 100
        return {
            "resistencia_total": round(R_total, 4),
            "caida_tension_v": round(dv, 4),
            "caida_tension_pct": round(pct, 2),
            "voltaje_final": round(voltaje - dv, 4),
        }

    @staticmethod
    def capacity_linea_larga(voltaje, corriente_max, longitud_km, tipo="cobre"):
        """Capacidad de transmisión de la línea."""
        resistencias = {"cobre": 0.0178, "aluminio": 0.0282}
        rho = resistencias.get(tipo, 0.0178)
        R = rho * longitud_km
        Vd = math.sqrt(3) * corriente_max * R if voltaje > 1000 else 2 * corriente_max * R
        P = math.sqrt(3) * voltaje * corriente_max if voltaje > 1000 else voltaje * corriente_max
        return {
            "capacidad_kw": round(P / 1000, 2),
            "capacidad_kva": round(P / 1000, 2),
            "corriente_max": corriente_max,
            "resistencia_total": round(R, 4),
            "caida_tension_max": round(Vd, 4),
        }

    @staticmethod
    def factores_ambientales_linea(temperatura_max=40, altitud=0, viento=60):
        """Factores de corrección para líneas."""
        factor_temp = 1 - 0.005 * max(0, temperatura_max - 25)
        factor_alt = 1 - 0.005 * max(0, (altitud - 1000) / 100) if altitud > 1000 else 1
        factor_viento = 1 + 0.002 * (viento - 40) if viento > 40 else 1
        return {
            "temperatura": temperatura_max,
            "altitud": altitud,
            "viento": viento,
            "factor_temperatura": round(factor_temp, 3),
            "factor_altitud": round(factor_alt, 3),
            "factor_viento": round(factor_viento, 3),
            "factor_global": round(factor_temp * factor_alt * factor_viento, 3),
        }

    @staticmethod
    def defasado_cables(largos_cables):
        """Cálculo de defasaje entre fases para líneas largas."""
        Z = []
        for z in largos_cables:
            Z.append(complex(z[0], z[1]))
        desequilibrio = max(Z) - min(Z) if Z else 0
        return {
            "impedancias": [f"{z.real}+j{z.imag}Ω" for z in Z],
            "desequilibrio_max": round(abs(desequilibrio), 4),
            "seccion_media": round(sum(abs(z) for z in Z) / len(Z), 4) if Z else 0,
        }
