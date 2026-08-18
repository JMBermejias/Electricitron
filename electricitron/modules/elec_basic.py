"""Módulo de cálculos eléctricos básicos - Leyes de Ohm, Potencia, etc."""
import math


class ElectricalBasic:
    """Cálculos fundamentales de electricidad."""

    @staticmethod
    def ley_ohm(voltaje=None, corriente=None, resistencia=None):
        """Ley de Ohm: V = I × R"""
        vals = [voltaje, corriente, resistencia]
        if sum(v is not None for v in vals) < 2:
            raise ValueError("Se necesitan al menos 2 valores")
        if voltaje is None:
            return {"voltaje": round(corriente * resistencia, 4), "corriente": corriente, "resistencia": resistencia}
        if corriente is None:
            return {"voltaje": voltaje, "corriente": round(voltaje / resistencia, 4), "resistencia": resistencia}
        if resistencia is None:
            return {"voltaje": voltaje, "corriente": corriente, "resistencia": round(voltaje / corriente, 4)}
        return {"voltaje": voltaje, "corriente": corriente, "resistencia": resistencia}

    @staticmethod
    def potencia_dc(voltaje, corriente):
        """P = V × I"""
        return round(voltaje * corriente, 4)

    @staticmethod
    def potencia_trifasica(voltaje, corriente, fp=1.0):
        """P = √3 × V × I × cos(φ)"""
        return round(math.sqrt(3) * voltaje * corriente * fp, 4)

    @staticmethod
    def potencia_monofasica(voltaje, corriente, fp=1.0):
        """P = V × I × cos(φ)"""
        return round(voltaje * corriente * fp, 4)

    @staticmethod
    def corriente_dc(potencia, voltaje):
        """I = P / V"""
        return round(potencia / voltaje, 4)

    @staticmethod
    def corriente_trifasica(potencia, voltaje, fp=1.0):
        """I = P / (√3 × V × cos(φ))"""
        return round(potencia / (math.sqrt(3) * voltaje * fp), 4)

    @staticmethod
    def corriente_monofasica(potencia, voltaje, fp=1.0):
        """I = P / (V × cos(φ))"""
        return round(potencia / (voltaje * fp), 4)

    @staticmethod
    def potencia_reactiva(voltaje, corriente, fp):
        """Q = P × tan(φ)"""
        angulo = math.acos(fp)
        q = voltaje * corriente * math.sin(angulo)
        return round(q, 4)

    @staticmethod
    def factor_potencia(potencia_activa, voltaje, corriente, trifasico=True):
        """cos(φ) = P / (S)"""
        if trifasico:
            s = math.sqrt(3) * voltaje * corriente
        else:
            s = voltaje * corriente
        return round(potencia_activa / s, 4)

    @staticmethod
    def impedancia(resistencia, inductancia, capacitancia, frecuencia):
        """Z = √(R² + (XL - XC)²)"""
        wl = 2 * math.pi * frecuencia * inductancia
        wc = 1 / (2 * math.pi * frecuencia * capacitancia) if capacitancia > 0 else float('inf')
        xc = wc
        z = math.sqrt(resistencia**2 + (wl - xc)**2)
        angulo = math.degrees(math.atan2(wl - xc, resistencia))
        return {
            "impedancia": round(z, 4),
            "angulo": round(angulo, 2),
            "reactancia_neta": round(wl - xc, 4),
            "inductiva": round(wl, 4),
            "capacitiva": round(xc, 4) if xc != float('inf') else "inf"
        }

    @staticmethod
    def resistencia_conductor(rho, longitud, seccion):
        """R = ρ × L / S"""
        return round(rho * longitud / seccion, 4)

    @staticmethod
    def resistividad(tipo="cobre", temperatura=20):
        """Resistividad en Ω·mm²/m"""
        rho_base = {"cobre": 0.0178, "aluminio": 0.0282}
        rho20 = rho_base.get(tipo, 0.0178)
        return round(rho20 * (1 + 0.00393 * (temperatura - 20)), 6)

    @staticmethod
    def caida_tension(voltaje, corriente, resistencia, trifasico=True):
        """Caída de tensión"""
        if trifasico:
            dv = math.sqrt(3) * corriente * resistencia
        else:
            dv = 2 * corriente * resistencia
        porcentaje = (dv / voltaje) * 100
        return {"caida_v": round(dv, 4), "caida_pct": round(porcentaje, 2)}

    @staticmethod
    def energia(potencia, tiempo_horas):
        """E = P × t (kWh)"""
        return round(potencia * tiempo_horas / 1000, 4)

    @staticmethod
    def potencia_aparente(potencia_activa, potencia_reactiva):
        """S = √(P² + Q²)"""
        return round(math.sqrt(potencia_activa**2 + potencia_reactiva**2), 4)

    @staticmethod
    def angulo_fase(resistencia, reactivancia):
        """θ = arctan(X/R)"""
        return round(math.degrees(math.atan2(reactivancia, resistencia)), 2)

    @staticmethod
    def corriente_cortocircuito(tension_circuito, impedancia_cortocircuito):
        """Icc = U / Zcc"""
        return round(tension_circuito / impedancia_cortocircuito, 2)

    @staticmethod
    def potencia_cortocircuito(voltaje, corriente_cortocircuito):
        """Scc = U × Icc"""
        return round(voltaje * corriente_cortocircuito / 1000, 2)

    @staticmethod
    def escalera_cortocircuito(voltaje, potencia_cortocircuito, tiempo=0.1):
        """Icc = Scc / (√3 × U)"""
        return round(potencia_cortocircuito * 1000 / (math.sqrt(3) * voltaje), 2)
