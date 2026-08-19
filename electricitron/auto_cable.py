"""Calculadora automática de sección de conductor según normativa vigente (REBT/IEC)."""
import math

# Tabla de secciones normalizadas (mm²)
SECCIONES_NORM = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400]

# Intensidad admisible base (A) según ITC-BT-19,-method B2 (cable en tubo enterrado), una sola fase
# Referencia: 30°C, 1 conductores cargados, instalación en tubo aislado (B2)
INTENSIDAD_ADMISIBLE = {
    1.5:  17.5,
    2.5:  24,
    4:    32,
    6:    41,
    10:   57,
    16:   76,
    25:   97,
    35:   117,
    50:   144,
    70:   176,
    95:   209,
    120:  237,
    150:  264,
    185:  295,
    240:  338,
    300:  382,
    400:  435,
}

# Resistividad a 20°C (Ohm·mm²/m) y coeficiente de temperatura
RHO_CU_20 = 0.01786  # cobre
RHO_AL_20 = 0.02941  # aluminio
ALPHA_CU = 0.00393
ALPHA_AL = 0.00403

# Factor de caída de tensión máxima (%)
CAIDA_TENSION_ILUMINACION = 3.0  # REBT: 3% iluminación
CAIDA_TENSION_FUERZA = 5.0      # REBT: 5% fuerza

# Factores de corrección por temperatura ambiente (tablas ITC-BT-19)
FACTORES_TEMP = {
    10: 1.22, 15: 1.15, 20: 1.09, 25: 1.04,
    30: 1.00, 35: 0.94, 40: 0.87, 45: 0.79,
    50: 0.71, 55: 0.61,
}

# Factores de corrección por número de conductores activos en tubo/conducción
FACTORES_CONDUCTORES = {
    1: 1.00, 2: 0.80, 3: 0.70, 4: 0.65, 5: 0.60,
    6: 0.57, 7: 0.54, 8: 0.52, 9: 0.50, 10: 0.48,
    12: 0.45, 14: 0.43, 16: 0.41, 18: 0.40, 20: 0.39,
}

# Secciones máximas paraProtectores unipolares (Interruptores automáticos)
CORRIENTES_INTERRUPCION = {
    10: [0.5, 1, 1.6, 2, 2.5, 3, 4, 5, 6, 8, 10],
    16: [0.5, 1, 1.6, 2, 2.5, 3, 4, 5, 6, 8, 10, 13, 16],
    25: [1, 1.6, 2, 2.5, 3, 4, 5, 6, 8, 10, 13, 16, 20, 25],
    32: [1.6, 2, 2.5, 3, 4, 5, 6, 8, 10, 13, 16, 20, 25, 32],
    40: [2.5, 3, 4, 5, 6, 8, 10, 13, 16, 20, 25, 32, 40],
    50: [4, 5, 6, 8, 10, 13, 16, 20, 25, 32, 40, 50],
    63: [6, 8, 10, 13, 16, 20, 25, 32, 40, 50, 63],
}


def factor_temperatura(temp_amb: int) -> float:
    """Factor de corrección por temperatura ambiente (ITC-BT-19)."""
    if temp_amb <= 10:
        return 1.22
    if temp_amb >= 55:
        return 0.61
    keys = sorted(FACTORES_TEMP.keys())
    for i in range(len(keys) - 1):
        if keys[i] <= temp_amb <= keys[i + 1]:
            t1, t2 = keys[i], keys[i + 1]
            f1, f2 = FACTORES_TEMP[t1], FACTORES_TEMP[t2]
            ratio = (temp_amb - t1) / (t2 - t1)
            return f1 + ratio * (f2 - f1)
    return 1.0


def factor_conductores(n: int) -> float:
    """Factor de corrección por número de conductores activos en una tubería."""
    if n <= 1:
        return 1.0
    if n >= 20:
        return 0.39
    keys = sorted(FACTORES_CONDUCTORES.keys())
    for i in range(len(keys) - 1):
        if keys[i] <= n <= keys[i + 1]:
            c1, c2 = FACTORES_CONDUCTORES[keys[i]], FACTORES_CONDUCTORES[keys[i + 1]]
            ratio = (n - keys[i]) / (keys[i + 1] - keys[i])
            return c1 + ratio * (c2 - c1)
    return 0.39


def intensidad_admisible(seccion: float, temp_amb: int = 30,
                         n_conductores: int = 1, material: str = "cobre") -> float:
    """Intensidad admisible corregida para una sección dada."""
    if seccion not in INTENSIDAD_ADMISIBLE:
        closest = min(INTENSIDAD_ADMISIBLE.keys(), key=lambda x: abs(x - seccion))
        base = INTENSIDAD_ADMISIBLE[closest]
    else:
        base = INTENSIDAD_ADMISIBLE[seccion]

    ft = factor_temperatura(temp_amb)
    fc = factor_conductores(n_conductores)
    factor_material = 1.0 if material == "cobre" else 0.78  # aluminio ~78% del cobre

    return base * ft * fc * factor_material


def resistencia_20(seccion: float, material: str = "cobre") -> float:
    """Resistencia por metro a 20°C (Ohm/m)."""
    rho = RHO_CU_20 if material == "cobre" else RHO_AL_20
    return rho / seccion


def resistencia_temp(seccion: float, temp: float, material: str = "cobre") -> float:
    """Resistencia por metro a temperatura de operación (Ohm/m)."""
    rho0 = RHO_CU_20 if material == "cobre" else RHO_AL_20
    alpha = ALPHA_CU if material == "cobre" else ALPHA_AL
    return (rho0 * (1 + alpha * (temp - 20))) / seccion


def caida_tension_calc(seccion: float, intensidad: float, longitud: float,
                       material: str = "cobre", temp: float = 40,
                       num_fases: int = 1) -> float:
    """Caída de tensión (%) para una sección, corriente y longitud dadas."""
    r = resistencia_temp(seccion, temp, material)
    if num_fases == 1:
        v_drop = 2 * r * longitud * intensidad  # monofásico: ida y vuelta
    else:
        v_drop = math.sqrt(3) * r * longitud * intensidad  # trifásico
    return v_drop


def caida_tension_relativa(seccion: float, intensidad: float, longitud: float,
                           voltaje: float, material: str = "cobre",
                           temp: float = 40, num_fases: int = 1) -> float:
    """Caída de tensión relativa (%)."""
    v_drop = caida_tension_calc(seccion, intensidad, longitud, material, temp, num_fases)
    return (v_drop / voltaje) * 100


def calcular_seccion_automatica(
    intensidad: float,
    longitud: float,
    voltaje: float,
    temp_amb: int = 30,
    n_conductores: int = 3,
    material: str = "cobre",
    tipo_carga: str = "iluminacion",
    num_fases: int = 1,
    temp_operacion: float = 70,
) -> dict:
    """
    Calcula la sección mínima de conductor según normativa REBT/IEC.

    Parámetros:
        intensidad: Corriente de carga (A)
        longitud: Distancia del tramo (m)
        voltaje: Tensión nominal (V)
        temp_amb: Temperatura ambiente (°C)
        n_conductores: Nº de conductores activos en la tubería
        material: "cobre" o "aluminio"
        tipo_carga: "iluminacion" (3%) o "fuerza" (5%)
        num_fases: 1 (monofásico) o 3 (trifásico)
        temp_operacion: Temperatura de servicio del cable (°C)

    Retorna dict con resultados detallados.
    """
    max_caida = CAIDA_TENSION_ILUMINACION if tipo_carga == "iluminacion" else CAIDA_TENSION_FUERZA

    # 1. Sección mínima por intensidad admisible (corregida)
    seccion_min_ia = None
    ia_detail = None
    for sec in SECCIONES_NORM:
        ia = intensidad_admisible(sec, temp_amb, n_conductores, material)
        if ia >= intensidad:
            seccion_min_ia = sec
            ia_detail = {
                "seccion": sec,
                "ia_admisible": round(ia, 2),
                "ia_necesaria": intensidad,
                "margen": round(((ia - intensidad) / intensidad) * 100, 1),
            }
            break

    # 2. Sección mínima por caída de tensión
    seccion_min_ct = None
    ct_detail = None
    for sec in SECCIONES_NORM:
        pct = caida_tension_relativa(sec, intensidad, longitud, voltaje,
                                     material, temp_operacion, num_fases)
        if pct <= max_caida:
            seccion_min_ct = sec
            # Calcular también con la sección anterior si existe
            prev_idx = SECCIONES_NORM.index(sec) - 1
            pct_anterior = None
            if prev_idx >= 0:
                pct_anterior = caida_tension_relativa(
                    SECCIONES_NORM[prev_idx], intensidad, longitud, voltaje,
                    material, temp_operacion, num_fases
                )
            ct_detail = {
                "seccion": sec,
                "caida_pct": round(pct, 3),
                "caida_max_pct": max_caida,
                "caida_voltios": round(caida_tension_calc(sec, intensidad, longitud,
                                                          material, temp_operacion, num_fases), 3),
                "pct_seccion_anterior": round(pct_anterior, 3) if pct_anterior else None,
            }
            break

    # 3. Sección recomendada = la mayor de las dos
    secciones_candidatas = []
    if seccion_min_ia is not None:
        secciones_candidatas.append(seccion_min_ia)
    if seccion_min_ct is not None:
        secciones_candidatas.append(seccion_min_ct)

    if not secciones_candidatas:
        seccion_final = None
        motivo = "No se encontró sección adecuada. Verifique los datos de entrada."
    else:
        seccion_final = max(secciones_candidatas)
        motivo_parts = []
        if seccion_min_ia and seccion_min_ct:
            if seccion_min_ia > seccion_min_ct:
                motivo = (f"Sección limitada por intensidad admisible "
                          f"({seccion_min_ia} mm² > {seccion_min_ct} mm² por caída de tensión)")
            elif seccion_min_ct > seccion_min_ia:
                motivo = (f"Sección limitada por caída de tensión "
                          f"({seccion_min_ct} mm² > {seccion_min_ia} mm² por intensidad admisible)")
            else:
                motivo = (f"Ambos criterios coinciden en {seccion_final} mm²")
        elif seccion_min_ia:
            motivo = f"Sección según intensidad admisible ({seccion_min_ia} mm²)"
        else:
            motivo = f"Sección según caída de tensión ({seccion_min_ct} mm²)"

    # Verificación final con la sección elegida
    verificacion = {}
    if seccion_final:
        ia_final = intensidad_admisible(seccion_final, temp_amb, n_conductores, material)
        ct_final = caida_tension_relativa(seccion_final, intensidad, longitud,
                                          voltaje, material, temp_operacion, num_fases)
        ct_v = caida_tension_calc(seccion_final, intensidad, longitud,
                                  material, temp_operacion, num_fases)
        v_regimen = voltaje - ct_v

        verificacion = {
            "seccion": seccion_final,
            "ia_admisible_corregida": round(ia_final, 2),
            "ia_carga": intensidad,
            "margen_ia_pct": round(((ia_final - intensidad) / intensidad) * 100, 1),
            "caida_tension_pct": round(ct_final, 3),
            "caida_tension_v": round(ct_v, 3),
            "caida_tension_max_pct": max_caida,
            "v_regimen": round(v_regimen, 3),
            "cumple_ia": ia_final >= intensidad,
            "cumple_ct": ct_final <= max_caida,
            "cumple": (ia_final >= intensidad) and (ct_final <= max_caida),
        }

    # Calcular caída para todas las secciones (para tabla comparativa)
    tabla_comparativa = []
    for sec in SECCIONES_NORM:
        ia_sec = intensidad_admisible(sec, temp_amb, n_conductores, material)
        ct_sec = caida_tension_relativa(sec, intensidad, longitud,
                                        voltaje, material, temp_operacion, num_fases)
        ct_v_sec = caida_tension_calc(sec, intensidad, longitud,
                                      material, temp_operacion, num_fases)
        tabla_comparativa.append({
            "seccion": sec,
            "ia_admisible": round(ia_sec, 2),
            "ia_suficiente": ia_sec >= intensidad,
            "caida_pct": round(ct_sec, 3),
            "caida_v": round(ct_v_sec, 3),
            "ct_cumple": ct_sec <= max_caida,
            "ambos_cumplen": (ia_sec >= intensidad) and (ct_sec <= max_caida),
        })

    # Interruptor recomendado
    interruptor_rec = None
    for i_a in sorted([10, 16, 25, 32, 40, 50, 63]):
        if i_a >= intensidad * 1.25:  # margen 25% sobre la carga
            interruptor_rec = i_a
            break
    if interruptor_rec is None:
        interruptor_rec = 63

    return {
        "seccion_min_ia": ia_detail,
        "seccion_min_ct": ct_detail,
        "seccion_recomendada": seccion_final,
        "motivo": motivo,
        "verificacion": verificacion,
        "tabla_comparativa": tabla_comparativa,
        "interruptor_recomendado": interruptor_rec,
        "parametros_entrada": {
            "intensidad": intensidad,
            "longitud": longitud,
            "voltaje": voltaje,
            "temp_amb": temp_amb,
            "n_conductores": n_conductores,
            "material": material,
            "tipo_carga": tipo_carga,
            "num_fases": num_fases,
            "temp_operacion": temp_operacion,
        },
    }
