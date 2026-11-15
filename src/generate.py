#!/usr/bin/env python3
"""
On-Demand Dynamic Challenge File Generator — Baratieri's War Council Console (AdwaCTF).

Environment variables:
  - FLAG: Dynamic participant-specific flag (e.g. AdwaCTF{...})
  - USER_ID: Optional participant or team identifier
  - OUTPUT_FILENAME: Primary output file name (default: app.py)
  - OUTPUT_DIR: Target directory to write to
  - OUTPUT_PATH: Explicit destination file path
"""

import os
import sys
import shutil
from pathlib import Path

DEFAULT_FLAG = "AdwaCTF{5571_b4r4713r1_0rd3r5_d15rup73d}"


def get_flag() -> str:
    flag = os.environ.get("FLAG", "").strip()
    if flag:
        return flag
    for c in ["flag.txt", "/app/flag.txt", "/flag.txt", "../flag.txt"]:
        if os.path.isfile(c):
            try:
                val = open(c, encoding="utf-8").read().strip()
                if val:
                    return val
            except OSError:
                pass
    return DEFAULT_FLAG


def plant_server_flag(flag: str):
    """Plants the flag on the server filesystem for SSTI / RCE recovery."""
    here = Path(__file__).resolve().parent.parent
    flag_locations = [
        here / "flag.txt",
        Path("/flag.txt"),
        Path("/app/flag.txt"),
        Path.cwd() / "flag.txt",
    ]

    for p in flag_locations:
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(flag.strip() + "\n", encoding="utf-8")
            os.chmod(p, 0o644)
        except OSError:
            pass


def main():
    flag = get_flag()
    user_id = os.environ.get("USER_ID", "sauria_operative").strip()
    here = Path(__file__).resolve().parent.parent

    # Always ensure server-side flag.txt is planted
    plant_server_flag(flag)

    output_path = os.environ.get("OUTPUT_PATH", "").strip()
    if output_path:
        target_file = Path(output_path).resolve()
        target_dir = target_file.parent
        target_app_name = target_file.name
    elif len(sys.argv) > 1 and sys.argv[1].strip():
        arg_path = Path(sys.argv[1].strip()).resolve()
        if arg_path.is_dir() or sys.argv[1].endswith("/"):
            target_dir = arg_path
            target_app_name = "app.py"
        else:
            target_dir = arg_path.parent
            target_app_name = arg_path.name
    else:
        env_dir = os.environ.get("OUTPUT_DIR", "").strip()
        if env_dir:
            target_dir = Path(env_dir).resolve()
        elif Path("/output").is_dir():
            target_dir = Path("/output")
        else:
            target_dir = here / "output"
        target_app_name = os.environ.get("OUTPUT_FILENAME", "app.py").strip()

    target_dir.mkdir(parents=True, exist_ok=True)

    notice_content = f"""===============================================================================
COMANDO SUPERIORE DELLE TRUPPE COLONIALI — QUARTIER GENERALE DI SAURIA
DISPACCIO TELEGRAFICO CAMPALE & ORDINE DI MARCIA NOTTURNO
SESSIONE OPERATIVA: {user_id}
===============================================================================

DISPOSIZIONI OPERATIVE:
Il Tenente Generale Oreste Baratieri ordina l'avanzata delle quattro brigate
(Albertone, Arimondi, Dabormida, Ellena) verso le alture di Adua alle ore 21:00.

SISTEMA TELEGRAFICO:
I dispacci e gli ordini di marcia vengono elaborati dalla console campale attiva
sulla rete interna del battaglione trasmissioni. Il sistema e protetto da un
modulo di censura militare che blocca sequenze sovversive prima della formattazione.

OBIETTIVO DI SICUREZZA:
Analizzare il codice sorgente allegato della console (`app.py`), individuare la
falla nel motore di elaborazione dei dispacci ed eludere il filtro di censura per
intercettare gli ordini confidenziali dello Stato Maggiore.

ACCESSO AL SERVIZIO:
Collegarsi all'indirizzo della console telegrafica fornito dalla piattaforma.
===============================================================================
"""

    src_app = here / "src" / "app.py"
    if not src_app.is_file():
        src_app = Path("/app/src/app.py")
    if not src_app.is_file():
        src_app = Path("/app/app.py")

    env_dir = os.environ.get("OUTPUT_DIR", "").strip()

    dirs_to_write = {target_dir}
    if Path("/output").is_dir():
        dirs_to_write.add(Path("/output"))
    if (here / "output").is_dir() and not env_dir and not output_path and len(sys.argv) <= 1:
        dirs_to_write.add(here / "output")

    for d in dirs_to_write:
        try:
            d.mkdir(parents=True, exist_ok=True)
            app_dest = d / target_app_name
            if src_app.is_file():
                shutil.copy2(src_app, app_dest)
                os.chmod(app_dest, 0o644)
            notice_file = d / "console_notice.txt"
            with open(notice_file, "w", encoding="utf-8") as f:
                f.write(notice_content)
            os.chmod(notice_file, 0o644)
        except OSError as e:
            print(f"[generator] Warning writing to {d}: {e}", file=sys.stderr)

    if (here / "dist").is_dir() and not env_dir and not output_path and len(sys.argv) <= 1:
        try:
            if src_app.is_file():
                shutil.copy2(src_app, here / "dist" / "app.py")
            with open(here / "dist" / "console_notice.txt", "w", encoding="utf-8") as f:
                f.write(notice_content)
        except OSError as e:
            print(f"[generator] Warning updating dist: {e}", file=sys.stderr)

    print(f"[generator] user_id={user_id}")
    print(f"[generator] target_dir={target_dir}")
    print(f"[generator] generated: {target_app_name}, console_notice.txt")


if __name__ == "__main__":
    main()
