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
    mime_dir = f"{build_dir}/usr/share/mime/packages"
    icons_dir = f"{build_dir}/usr/share/icons/hicolor"

    if os.path.exists("deb_build"):
        shutil.rmtree("deb_build")

    dirs = [bin_dir, deb_dir, share_dir, mime_dir]
    for size in [16, 32, 48, 64, 128, 256]:
        dirs.append(f"{icons_dir}/{size}x{size}/apps")
    for d in dirs:
        os.makedirs(d, exist_ok=True)

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
Depends: libgl1, libglib2.0-0, libfontconfig1, libxrender1
Maintainer: jmbernabeu <jmbernabeu@users.noreply.github.com>
Description: Electricitron - Calculos Electricos y Telecomunicaciones
 Software profesional para calculos electricos, secciones de cables,
 protecciones, instalaciones, telecomunicaciones y distancias.
 Exporta informes en PDF y Excel.
"""
    with open(f"{deb_dir}/control", "w") as f:
        f.write(control)

    postinst = """#!/bin/bash
set -e

# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor || true
fi

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications || true
fi

# Update MIME database
if command -v update-mime-database >/dev/null 2>&1; then
    update-mime-database /usr/share/mime || true
fi

# Make desktop file trusted on GNOME
if command -v gio >/dev/null 2>&1; then
    gio set /usr/share/applications/electricitron.desktop "metadata::trusted" true 2>/dev/null || true
fi

echo "Electricitron installed successfully."
"""
    with open(f"{deb_dir}/postinst", "w") as f:
        f.write(postinst)
    os.chmod(f"{deb_dir}/postinst", 0o755)

    postrm = """#!/bin/bash
set -e

if [ "$1" = "remove" ] || [ "$1" = "purge" ]; then
    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
        gtk-update-icon-cache -f -t /usr/share/icons/hicolor || true
    fi
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database /usr/share/applications || true
    fi
fi
"""
    with open(f"{deb_dir}/postrm", "w") as f:
        f.write(postrm)
    os.chmod(f"{deb_dir}/postrm", 0o755)

    desktop = """[Desktop Entry]
Name=Electricitron
GenericName=Calculos Electricos
Comment=Software de calculos electricos y telecomunicaciones
Exec=/usr/bin/electricitron
Icon=electricitron
Terminal=false
Type=Application
StartupNotify=true
Categories=Utility;Engineering;Education;Science;
Keywords=electricidad;electrical;calculation;telecom;
MimeType=
"""
    with open(f"{share_dir}/electricitron.desktop", "w") as f:
        f.write(desktop)
    os.chmod(f"{share_dir}/electricitron.desktop", 0o644)

    mime_xml = """<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
  <mime-type type="application/x-electricitron-report">
    <comment>Electricitron Report</comment>
    <glob pattern="*.eitreport"/>
  </mime-type>
</mime-info>
"""
    with open(f"{mime_dir}/electricitron.xml", "w") as f:
        f.write(mime_xml)

    icon_files = {
        "assets/icon_256.png": f"{icons_dir}/256x256/apps/electricitron.png",
        "assets/icon_128.png": f"{icons_dir}/128x128/apps/electricitron.png",
        "assets/icon_64.png": f"{icons_dir}/64x64/apps/electricitron.png",
        "assets/icon_48.png": f"{icons_dir}/48x48/apps/electricitron.png",
        "assets/icon_32.png": f"{icons_dir}/32x32/apps/electricitron.png",
        "assets/icon_16.png": f"{icons_dir}/16x16/apps/electricitron.png",
    }
    for src, dst in icon_files.items():
        if os.path.exists(src):
            shutil.copy(src, dst)
            print(f"  Icon: {src} -> {dst}")

    deb_file = f"{pkg_name}_{version}_amd64.deb"
    cmd = ["dpkg-deb", "--build", "--root-owner-group", build_dir, deb_file]
    subprocess.run(cmd, check=True)
    print(f"Build DEB completado: {deb_file}")

    print("\nEstructura del .deb:")
    subprocess.run(["find", build_dir, "-type", "f"], check=False)
    return deb_file


if __name__ == "__main__":
    build_linux_deb()
