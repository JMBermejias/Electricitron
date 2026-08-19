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
    pixmap_dir = f"{build_dir}/usr/share/pixmaps"

    if os.path.exists("deb_build"):
        shutil.rmtree("deb_build")

    dirs = [bin_dir, deb_dir, share_dir, mime_dir, pixmap_dir]
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
        "--distpath=deb_build/electricitron_1.0.0_amd64/usr/bin",
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
Installed-Size: {int(os.path.getsize(f'{build_dir}/usr/bin/electricitron') / 1024)}
Depends: libgl1, libglib2.0-0, libfontconfig1, libxrender1
Maintainer: jmbernabeu <jmbernabeu@users.noreply.github.com>
Homepage: https://github.com/JMBermejias/Electricitron
Description: Electricitron - Calculos Electricos y Telecomunicaciones
 Software profesional para calculos electricos, secciones de cables,
 protecciones, instalaciones, telecomunicaciones y distancias.
 Exporta informes en PDF y Excel.
"""
    with open(f"{deb_dir}/control", "w") as f:
        f.write(control)

    conffiles = "/etc/electricitron/electricitron.conf\n"
    os.makedirs(f"{build_dir}/etc/electricitron", exist_ok=True)
    with open(f"{build_dir}/etc/electricitron/electricitron.conf", "w") as f:
        f.write("# Electricitron configuration\n")
    with open(f"{deb_dir}/conffiles", "w") as f:
        f.write(conffiles)

    postinst = """#!/bin/bash
set -e

# Update icon cache for all sizes
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
fi
if command -v gtk-update-icon-cache-3.0 >/dev/null 2>&1; then
    gtk-update-icon-cache-3.0 -f -t /usr/share/icons/hicolor 2>/dev/null || true
fi
if command -v gtk-update-icon-cache-4.0 >/dev/null 2>&1; then
    gtk-update-icon-cache-4.0 -f -t /usr/share/icons/hicolor 2>/dev/null || true
fi

# Also copy to pixmaps as fallback
if [ -f /usr/share/icons/hicolor/256x256/apps/electricitron.png ]; then
    cp /usr/share/icons/hicolor/256x256/apps/electricitron.png /usr/share/pixmaps/electricitron.png 2>/dev/null || true
fi
if [ -f /usr/share/icons/hicolor/128x128/apps/electricitron.png ]; then
    cp /usr/share/icons/hicolor/128x128/apps/electricitron.png /usr/share/pixmaps/electricitron.png 2>/dev/null || true
fi

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications 2>/dev/null || true
fi

# Validate desktop file
if command -v desktop-file-validate >/dev/null 2>&1; then
    desktop-file-validate /usr/share/applications/electricitron.desktop 2>/dev/null || true
fi

# Mark as trusted on GNOME
if command -v gio >/dev/null 2>&1; then
    gio set /usr/share/applications/electricitron.desktop "metadata::trusted" true 2>/dev/null || true
fi

# Force desktop reload
if command -v dbus-send >/dev/null 2>&1; then
    dbus-send --session --type=method_call --dest=org.gnome.Shell /org/gnome/Shell org.gnome.Shell.Eval string:"global.reexec_self()" 2>/dev/null || true
fi

exit 0
"""
    with open(f"{deb_dir}/postinst", "w") as f:
        f.write(postinst)
    os.chmod(f"{deb_dir}/postinst", 0o755)

    postrm = """#!/bin/bash
set -e
case "$1" in
    remove|purge)
        rm -f /usr/share/pixmaps/electricitron.png 2>/dev/null || true
        rm -f /usr/share/icons/hicolor/16x16/apps/electricitron.png 2>/dev/null || true
        rm -f /usr/share/icons/hicolor/32x32/apps/electricitron.png 2>/dev/null || true
        rm -f /usr/share/icons/hicolor/48x48/apps/electricitron.png 2>/dev/null || true
        rm -f /usr/share/icons/hicolor/64x64/apps/electricitron.png 2>/dev/null || true
        rm -f /usr/share/icons/hicolor/128x128/apps/electricitron.png 2>/dev/null || true
        rm -f /usr/share/icons/hicolor/256x256/apps/electricitron.png 2>/dev/null || true
        rm -f /usr/share/applications/electricitron.desktop 2>/dev/null || true
        if command -v gtk-update-icon-cache >/dev/null 2>&1; then
            gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
        fi
        if command -v update-desktop-database >/dev/null 2>&1; then
            update-desktop-database /usr/share/applications 2>/dev/null || true
        fi
        ;;
esac
exit 0
"""
    with open(f"{deb_dir}/postrm", "w") as f:
        f.write(postrm)
    os.chmod(f"{deb_dir}/postrm", 0o755)

    desktop = "[Desktop Entry]\nName=Electricitron\nGenericName=Calculos Electricos\nComment=Software de calculos electricos y telecomunicaciones\nExec=/usr/bin/electricitron %F\nIcon=electricitron\nTerminal=false\nType=Application\nStartupNotify=true\nCategories=Utility;Engineering;Education;Science;\nKeywords=electricidad;electrical;calculation;telecom;\n"
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
            os.chmod(dst, 0o644)
            print(f"  Icon: {src} -> {dst}")

    if os.path.exists("assets/icon.png"):
        shutil.copy("assets/icon.png", f"{pixmap_dir}/electricitron.png")
        os.chmod(f"{pixmap_dir}/electricitron.png", 0o644)
        if "assets/icon_256.png" not in icon_files or not os.path.exists("assets/icon_256.png"):
            shutil.copy("assets/icon.png", f"{icons_dir}/256x256/apps/electricitron.png")
            os.chmod(f"{icons_dir}/256x256/apps/electricitron.png", 0o644)

    deb_file = f"{pkg_name}_{version}_amd64.deb"

    for root, dirs_list, files in os.walk(build_dir):
        for fname in files:
            fpath = os.path.join(root, fname)
            os.chmod(fpath, 0o644)
        for dname in dirs_list:
            dpath = os.path.join(root, dname)
            os.chmod(dpath, 0o755)

    os.chmod(f"{deb_dir}/postinst", 0o755)
    os.chmod(f"{deb_dir}/postrm", 0o755)
    os.chmod(f"{build_dir}/usr/bin/electricitron", 0o755)

    cmd = ["fakeroot", "dpkg-deb", "--build", "--root-owner-group", build_dir, deb_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("fakeroot no disponible, usando dpkg-deb directo...")
        cmd = ["dpkg-deb", "--build", "--root-owner-group", build_dir, deb_file]
        subprocess.run(cmd, check=True)

    print(f"\nBuild DEB completado: {deb_file}")
    print(f"\nEstructura del .deb:")
    for root, dirs_list, files in os.walk(build_dir):
        for fname in files:
            fpath = os.path.join(root, fname)
            print(f"  {fpath.replace(build_dir, '')}")
    return deb_file


if __name__ == "__main__":
    build_linux_deb()
