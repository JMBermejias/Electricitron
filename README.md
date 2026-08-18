# Electricitron

Software profesional de cálculos eléctricos y telecomunicaciones.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)

## Funcionalidades

### Cálculos Eléctricos Básicos
- Ley de Ohm (V, I, R)
- Potencia DC, monofásica y trifásica
- Energía (kWh)
- Impedancia (Z)
- Factor de potencia
- Potencia reactiva y aparente

### Secciones y Cables
- Selección de sección por corriente transportada
- Caída de tensión en conductores
- Tablas de ampacidades (Cu rígido, Cu flexible, Al rígido)
- Capacidad de carga por circuito

### Protecciones
- Selección de interruptor automático (Curvas B, C, D, K, Z)
- Interruptor diferencial (30mA, 100mA, 300mA)
- Fusibles (gG, aM, gR)
- Tabla de corrientes magnéticas
- Coordinación y selectividad

### Instalaciones Eléctricas
- Cálculo de potencia de instalación
- Esquemas de protección (TN-S, TN-C, TN-C-S, TT, IT)
- Verificación de selectividad
- Condiciones ambientales
- Dimensionamiento de líneas generales

### Telecomunicaciones
- Enlaces inalámbricos punto a punto
- Fibra óptica (monomodo y multimodo)
- Pérdida de cable de red (Cat5e, Cat6, Cat6a, Cat7, Cat8)
- Dimensionamiento WiFi

### Distancias y Líneas
- Distancia entre puntos (3D)
- Zona de postes
- Caída de tensión en líneas largas
- Factores ambientales para líneas

### Informes
- Exportación a PDF con tablas profesionales
- Exportación a Excel con hojas organizadas
- Gestión de registros (modificar, eliminar)

## Instalación

### Windows
Descarga el archivo `Electricitron.exe` desde la sección [Releases](https://github.com/jmbernabeu/Electricitron/releases) y ejecútalo directamente.

### Linux (Debian/Ubuntu)
```bash
# Descargar el .deb desde Releases
sudo dpkg -i electricitron_1.0.0_amd64.deb
sudo apt-get install -f  # Para resolver dependencias
```

### Linux (Ejecutable directo)
Descarga el ejecutable AppImage desde Releases:
```bash
chmod +x electricitron
./electricitron
```

### Instalación desde código fuente
```bash
git clone https://github.com/jmbernabeu/Electricitron.git
cd Electricitron
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
python -m electricitron.main
```

## Requisitos
- Python 3.10 o superior
- PyQt6
- reportlab (PDF)
- openpyxl (Excel)
- numpy, scipy, matplotlib

## Desarrollo
```bash
# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install pyinstaller

# Ejecutar en modo desarrollo
python -m electricitron.main

# Build Windows
python build_windows.py

# Build Linux DEB
python build_linux.py
```

## Estructura del Proyecto
```
Electricitron/
├── electricitron/
│   ├── __init__.py
│   ├── main.py              # Aplicación principal y UI
│   ├── styles.py            # Estilos CSS/QSS
│   ├── modules/
│   │   ├── elec_basic.py    # Cálculos básicos
│   │   ├── cable_calc.py    # Secciones y cables
│   │   ├── protections.py   # Protecciones
│   │   ├── installations.py # Instalaciones
│   │   ├── telecom.py       # Telecomunicaciones
│   │   └── distances.py     # Distancias y líneas
│   └── reports/
│       ├── pdf_report.py    # Generador PDF
│       └── excel_report.py  # Generador Excel
├── assets/
├── .github/workflows/
│   └── build_release.yml    # CI/CD para releases
├── build_windows.py
├── build_linux.py
├── requirements.txt
└── pyproject.toml
```

## Licencia
MIT License - Ver archivo LICENSE para más detalles.

## Autor
 jmbernabeu
