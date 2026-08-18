#!/usr/bin/env python3
"""Script de build para Electricitron - Linux DEB."""
import subprocess
import sys
import os
import shutil


def build_linux_deb():
    """Build .deb package for Debian/Ubuntu."""
    version = "1.0.0"
    pkg_name = "electricitron"
    build_dir = f"deb_build/{pkg_name}_{version}_amd64"
    bin_dir = f"{build_dir}/usr/bin"
    deb_dir = f"{build_dir}/DEBIAN"
    share_dir = f"{build_dir}/usr/share/applications"
    icon_dir = f"{build_dir}/usr/share/icons/hicolor/256x256/apps"

    if os.path.exists("deb_build"):
        shutil.rmtree("deb_build")
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(deb_dir, exist_ok=True)
    os.makedirs(share_dir, exist_ok=True)
    os.makedirs(icon_dir, exist_ok=True)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=electricitron",
        "--windowed",
        "--onefile",
        "--add-data=assets:assets",
        "--clean",
        "--noconfirm",
        "--distpath=deb_build/usr/bin",
        "electricitron/main.py"
    ]
    if os.path.exists("assets/icon.png"):
        cmd.insert(5, "--icon=assets/icon.png")
    print("Compilando ejecutable...")
    subprocess.run(cmd, check=True)

    control = f"""Package: {pkg_name}
Version: {version}
Section: utils
Priority: optional
Architecture: amd64
Depends: libgl1-mesa-glx, libglib2.0-0, libfontconfig1, libxrender1
Maintainer: jmbernabeu <jmbernabeu@users.noreply.github.com>
Description: Electricitron - Cálculos Eléctricos y Telecomunicaciones
 Software profesional para cálculos eléctricos, secciones de cables,
 protecciones, instalaciones, telecomunicaciones y distancias.
 Exporta informes en PDF y Excel.
"""
    with open(f"{deb_dir}/control", "w") as f:
        f.write(control)

    desktop = f"""[Desktop Entry]
Name=Electricitron
Comment=Software de cálculos eléctricos y telecomunicaciones
Exec=/usr/bin/electricitron
Icon=electricitron
Terminal=false
Type=Application
Categories=Utility;Engineering;Education;
"""
    with open(f"{share_dir}/electricitron.desktop", "w") as f:
        f.write(desktop)

    if os.path.exists("assets/icon.png"):
        shutil.copy("assets/icon.png", f"{icon_dir}/electricitron.png")

    deb_file = f"{pkg_name}_{version}_amd64.deb"
    cmd = ["dpkg-deb", "--build", build_dir, deb_file]
    subprocess.run(cmd, check=True)
    print(f"Build DEB completado: {deb_file}")
    return deb_file


if __name__ == "__main__":
    build_linux_deb()
