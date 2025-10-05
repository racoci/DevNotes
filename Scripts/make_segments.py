#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

MAX_SEG_SEC = 36_000  # 10 hours
DATE_TIME_RE = re.compile(r'^(\d{4}-\d{2}-\d{2}) \d{2}-\d{2}-\d{2}$')  # stem
DUP_RE = re.compile(r"\(\d+\)(?=\.[^.]+$)", re.IGNORECASE)  # ' (1).ext'

# ---------- logging / utils ----------

def log_error(error_dir: Path, msg: str) -> None:
    error_dir.mkdir(exist_ok=True)
    (error_dir / "error_log.txt").write_text(
        (error_dir / "error_log.txt").read_text(encoding="utf-8") + 
        f"{datetime.now():%Y-%m-%d %H:%M:%S}  {msg}\n"
        if (error_dir / "error_log.txt").exists() else
        f"{datetime.now():%Y-%m-%d %H:%M:%S}  {msg}\n",
        encoding="utf-8"
    )

def hhmmss(seconds: float) -> str:
    total = int(round(max(0.0, seconds)))
    h, r = divmod(total, 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def run(cmd: List[str], cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)

# ---------- ffprobe helpers ----------

def ffprobe_json(cmd: List[str]) -> Dict:
    res = run(cmd)
    return json.loads(res.stdout)

def get_orientation(mp4: Path) -> Optional[str]:
    """
    Returns 'H' or 'V' (or None on failure).
    """
    try:
        info = ffprobe_json([
            "ffprobe","-v","error","-select_streams","v:0",
            "-show_entries","stream=width,height","-of","json",str(mp4)
        ])
        st = info["streams"][0]
        w, h = int(st["width"]), int(st["height"])
        if w > h: return "H"
        if h > w: return "V"
        return "H"  # square -> treat as horizontal
    except Exception:
        return None

def get_duration_seconds(mp4: Path) -> Optional[float]:
    """
    Robust duration (seconds). Try stream durations (video/audio) max; fallback to format.duration.
    """
    try:
        # try video stream first
        v = ffprobe_json([
            "ffprobe","-v","error","-select_streams","v:0",
            "-show_entries","stream=duration","-of","json",str(mp4)
        ])
        vd = v.get("streams",[{}])[0].get("duration")
        vd = float(vd) if vd not in (None,"N/A") else 0.0
    except Exception:
        vd = 0.0

    try:
        a = ffprobe_json([
            "ffprobe","-v","error","-select_streams","a:0",
            "-show_entries","stream=duration","-of","json",str(mp4)
        ])
        ad = a.get("streams",[{}])[0].get("duration")
        ad = float(ad) if ad not in (None,"N/A") else 0.0
    except Exception:
        ad = 0.0

    cand = max(vd, ad)
    if cand > 0:
        return cand

    # fallback: format.duration (do NOT subtract start_time here; concat tends to track format duration)
    try:
        f = ffprobe_json([
            "ffprobe","-v","error","-show_entries","format=duration",
            "-of","json",str(mp4)
        ])
        fd = f["format"]["duration"]
        return float(fd) if fd not in (None,"N/A") else None
    except Exception:
        return None

# ---------- conversion ----------

def ensure_mp4_from_mkv(mkv: Path, error_dir: Path) -> Optional[Path]:
    mp4 = mkv.with_suffix(".mp4")
    if mp4.exists():
        return mp4
    try:
        print(f"[convert] {mkv.name} -> {mp4.name}")
        run(["ffmpeg","-y","-i",str(mkv),"-c","copy",str(mp4)])
        return mp4
    except subprocess.CalledProcessError as e:
        log_error(error_dir, f"[convert] {mkv.name}: {e.stderr.strip()}")
        try:
            error_dir.mkdir(exist_ok=True)
            shutil.move(str(mkv), error_dir / mkv.name)
        except Exception:
            pass
        return None

# ---------- main pipeline ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output","-o", type=str, default=None,
                    help="Diretório de saída (default: diretório atual)")
    args = ap.parse_args()

    root = Path.cwd()
    out_dir = Path(args.output) if args.output else root
    out_dir.mkdir(exist_ok=True)
    dup_dir = root / "duplicates"
    err_dir = root / "error"

    # 0) mover duplicatas '(n).ext' para ./duplicates
    for f in list(root.iterdir()):
        if f.is_file() and DUP_RE.search(f.name):
            dup_dir.mkdir(exist_ok=True)
            print(f"[duplicate] {f.name} -> duplicates/")
            try:
                shutil.move(str(f), dup_dir / f.name)
            except Exception as e:
                log_error(err_dir, f"[duplicate-move] {f}: {e}")

    # 1) coletar candidatos pelo padrão do nome (mp4/mkv)
    candidates: List[Path] = []
    for f in root.iterdir():
        if not f.is_file(): 
            continue
        if f.suffix.lower() not in (".mp4",".mkv"):
            continue
        if DATE_TIME_RE.match(f.stem):
            candidates.append(f)

    # 2) converter mkv -> mp4 (sem reencode) se preciso
    mp4s: List[Path] = []
    for f in sorted(candidates, key=lambda p: p.name.lower()):
        if f.suffix.lower() == ".mkv":
            mp4 = ensure_mp4_from_mkv(f, err_dir)
            if mp4:
                mp4s.append(mp4)
        else:
            mp4s.append(f)

    # 3) agrupar por data e orientação, movendo vídeos para ./YYYY-MM-DD/H|V/
    groups: Dict[Tuple[str,str], List[Tuple[Path,float]]] = {}
    for mp4 in sorted(mp4s, key=lambda p: p.name.lower()):
        date_m = DATE_TIME_RE.match(mp4.stem)
        if not date_m:
            # ignora silenciosamente (não bate o padrão)
            continue
        date_str = date_m.group(1)
        try:
            orient = get_orientation(mp4)
            if orient is None:
                raise RuntimeError("orientation detection failed")
            # mede duração
            dur = get_duration_seconds(mp4)
            if dur is None or dur <= 0:
                raise RuntimeError("duration detection failed")
            # cria diretórios de data/orientação e move o arquivo para lá
            date_dir = root / date_str
            orient_dir = date_dir / orient
            orient_dir.mkdir(parents=True, exist_ok=True)
            dest = orient_dir / mp4.name
            if mp4.resolve() != dest.resolve():
                try:
                    shutil.move(str(mp4), dest)
                    mp4 = dest
                except Exception as e:
                    log_error(err_dir, f"[move to orient] {mp4.name}: {e}")
                    continue
            groups.setdefault((date_str, orient), []).append((mp4, dur))
        except Exception as e:
            log_error(err_dir, f"[probe] {mp4.name}: {e}")
            try:
                err_dir.mkdir(exist_ok=True)
                shutil.move(str(mp4), err_dir / mp4.name)
            except Exception:
                pass

    # 4) para cada grupo (data, orientação), criar segmentos <= 10h na própria pasta
    for (date_str, orient), items in sorted(groups.items(), key=lambda kv: kv[0]):
        orient_dir = root / date_str / orient
        items_sorted = sorted(items, key=lambda t: t[0].name.lower())
        seg_idx = 1
        seg_elapsed = 0.0
        seg_dur = 0.0
        seg_files: List[Path] = []
        seg_timeline: List[str] = []

        def flush_segment():
            nonlocal seg_idx, seg_elapsed, seg_dur, seg_files, seg_timeline
            if not seg_files:
                return
            seg_dir = orient_dir / f"segment-{seg_idx}"
            seg_dir.mkdir(exist_ok=True)

            # mover arquivos do orient_dir para segment-N (intermediários ficam na estrutura)
            local_list = []
            for p in seg_files:
                dest = seg_dir / p.name
                if p.resolve() != dest.resolve():
                    try:
                        shutil.move(str(p), dest)
                        p = dest
                    except Exception as e:
                        log_error(err_dir, f"[move to segment] {p.name}: {e}")
                        continue
                local_list.append(f"file '{p.name}'")

            # escrever filelist/timeline dentro do segmento (intermediários)
            (seg_dir / "filelist.txt").write_text("\n".join(local_list), encoding="utf-8")
            # timeline final será movida para o output com o nome padronizado
            timeline_name = f"{date_str}-{orient}-{seg_idx}.txt"
            (seg_dir / timeline_name).write_text("\n".join(seg_timeline), encoding="utf-8")

            # merge
            merge_name = f"{date_str}-{orient}-{seg_idx}.mp4"
            try:
                run([
                    "ffmpeg","-y","-f","concat","-safe","0",
                    "-i","filelist.txt","-c","copy", merge_name
                ], cwd=seg_dir)
            except subprocess.CalledProcessError as e:
                log_error(err_dir, f"[merge] {seg_dir.name}: {e.stderr.strip()}")
            else:
                # mover APENAS os finais (mergeado e timeline) para o output
                try:
                    shutil.move(str(seg_dir / merge_name), out_dir / merge_name)
                    shutil.move(str(seg_dir / timeline_name), out_dir / timeline_name)
                except Exception as e:
                    log_error(err_dir, f"[move finals] {merge_name}: {e}")

            # reset
            seg_idx += 1
            seg_elapsed = 0.0
            seg_dur = 0.0
            seg_files = []
            seg_timeline = []

        for p, dur in items_sorted:
            # se esse arquivo estourar o limite e já temos algo, fecha o segmento
            if seg_dur + dur > MAX_SEG_SEC and seg_dur > 0:
                flush_segment()
            # adiciona ao segmento atual
            seg_files.append(p)
            seg_timeline.append(f"{hhmmss(seg_elapsed)}: {p.stem} ({hhmmss(dur)})")
            seg_elapsed += dur
            seg_dur += dur

        # último segmento
        flush_segment()

    print("Concluído. Finais em:", out_dir)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        root = Path.cwd()
        (root / "error").mkdir(exist_ok=True)
        log_error(root / "error", f"[fatal] {e}")
        print("Erro fatal — verifique error/error_log.txt")
        raise
