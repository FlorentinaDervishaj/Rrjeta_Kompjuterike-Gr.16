import os
from datetime import datetime

from config import SERVER_FILES_DIR
from auth.privileges import check_privilege_by_addr
from utils.logger import log


def _safe_path(filename: str) -> str:
    return os.path.join(SERVER_FILES_DIR, os.path.basename(filename))


# ── /list ─────────────────────────────────────────────────────────────────────
def cmd_list(addr_str: str) -> str:
    if not check_privilege_by_addr(addr_str, "admin"):
        return "DENIED Qasje e mohuar! Duhet privilegje admin."
    try:
        files = os.listdir(SERVER_FILES_DIR)
        if not files:
            return "LIST Folderi është bosh."
        return "Fajllat:\n" + "\n".join(files)
    except Exception as e:
        return f"ERROR /list dështoi: {e}"


# ── /read <filename> ──────────────────────────────────────────────────────────
def cmd_read(arg: str, addr_str: str) -> str:
    if not check_privilege_by_addr(addr_str, "admin"):
        return "DENIED Qasje e mohuar! Duhet privilegje admin."
    if not arg:
        return "ERROR Sintaksa: /read <filename>"
    path = _safe_path(arg)
    if not os.path.exists(path):
        return f"ERROR Skedari '{arg}' nuk ekziston."
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"=== {arg} ===\n{content}"
    except Exception as e:
        return f"ERROR /read: {e}"


# ── /upload <filename> <të dhënat> ────────────────────────────────────────────
def cmd_upload(arg: str, addr_str: str) -> str:
    if not check_privilege_by_addr(addr_str, "admin"):
        return "DENIED Qasje e mohuar! Duhet privilegje admin."
    if not arg:
        return "ERROR Sintaksa: /upload <emër> <të dhënat>"
    parts = arg.split(" ", 1)
    if len(parts) < 2:
        return "ERROR Sintaksa: /upload <emër> <të dhënat>"
    filename, content = parts[0].strip(), parts[1]
    filepath = _safe_path(filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        log.info(f"[UPLOAD] {addr_str} ngarkoi: {filename}")
        return f"UPLOAD_OK Fajlli '{filename}' u ngarkua me sukses."
    except Exception as e:
        return f"ERROR /upload: {e}"


# ── /download <filename> ──────────────────────────────────────────────────────
def cmd_download(arg: str, addr_str: str) -> str:
    if not check_privilege_by_addr(addr_str, "admin"):
        return "DENIED Qasje e mohuar! Duhet privilegje admin."
    if not arg:
        return "ERROR Sintaksa: /download <filename>"
    path = _safe_path(arg)
    if not os.path.exists(path):
        return f"ERROR '{arg}' nuk u gjet."
    try:
        with open(path, "rb") as f:
            content = f.read()
        header  = f"DOWNLOAD:{arg}:{len(content)}\n"
        encoded = content.decode("latin-1")
        return header + encoded
    except Exception as e:
        return f"ERROR /download: {e}"


# ── /delete <filename> ────────────────────────────────────────────────────────
def cmd_delete(arg: str, addr_str: str) -> str:
    if not check_privilege_by_addr(addr_str, "admin"):
        return "DENIED Qasje e mohuar! Duhet privilegje admin."
    if not arg:
        return "ERROR Sintaksa: /delete <filename>"
    path = _safe_path(arg)
    if not os.path.exists(path):
        return f"ERROR '{arg}' nuk ekziston."
    try:
        os.remove(path)
        log.info(f"[DEL] {addr_str} fshiu: {arg}")
        return f"DELETE_OK Fajlli '{arg}' u fshi me sukses."
    except Exception as e:
        return f"ERROR /delete: {e}"


# ── /search <keyword> ─────────────────────────────────────────────────────────
def cmd_search(arg: str, addr_str: str) -> str:
    if not check_privilege_by_addr(addr_str, "admin"):
        return "DENIED Qasje e mohuar! Duhet privilegje admin."
    if not arg:
        return "ERROR Sintaksa: /search <keyword>"
    try:
        results = []
        for fname in os.listdir(SERVER_FILES_DIR):
            fpath = os.path.join(SERVER_FILES_DIR, fname)
            if not os.path.isfile(fpath):
                continue
            if arg.lower() in fname.lower():
                results.append(f"{fname}  [emri]")
                continue
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    if arg.lower() in f.read().lower():
                        results.append(f"{fname}  [permbajtja]")
            except Exception:
                pass
        if not results:
            return f"SEARCH_EMPTY Nuk u gjet '{arg}' në asnjë skedar."
        return f"U gjet '{arg}' në:\n" + "\n".join(results)
    except Exception as e:
        return f"ERROR /search: {e}"


# ── /info <filename> ──────────────────────────────────────────────────────────
def cmd_info(arg: str, addr_str: str) -> str:
    if not arg:
        return "ERROR Sintaksa: /info <filename>"
    path = _safe_path(arg)
    if not os.path.exists(path):
        return f"ERROR '{arg}' nuk ekziston."
    try:
        stat  = os.stat(path)
        size  = stat.st_size
        mtime = datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds")
        ctime = datetime.fromtimestamp(stat.st_ctime).isoformat(timespec="seconds")
        return (
            f"INFO '{arg}':\n"
            f"  Madhësia  : {size} bytes\n"
            f"  Krijuar   : {ctime}\n"
            f"  Modifikuar: {mtime}"
        )
    except Exception as e:
        return f"ERROR /info: {e}"