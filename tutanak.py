#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Esneme tabanlı meclis tutanağı üretici.

Çalışır. Yasama yapmaz. Yapar gibi yapar.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import random
from datetime import datetime
from pathlib import Path

MADDELER = [
    "Gündem maddesi okundu. Kimse duymadı. Tutanak duydu.",
    "Söz isteyen olmadı. Esneme söz sayıldı.",
    "Usul tartışması açıldı, esneme yüzünden usul uyudu.",
    "Komisyon raporunun özeti: 'ha'.",
    "Muhalefet notu düşüldü. Not da esnedi.",
    "İktidar sıraları dolu göründü. Aslında montlar oturuyordu.",
]

KARARLAR = [
    "Esneme kabul edildi, konu ertelendi.",
    "Esneme reddedildi, konu yine ertelendi. Ret de bir ertelemedir.",
    "Çekimser çoğunluk sağlandı. Bu teknik olarak bir başarıdır.",
    "Yetersayı esneme ile sağlandı. Salon alkışlamak yerine gerindi.",
]


def yetersayi(sure: float) -> str:
    if sure < 4:
        return "TASLAK ESNEME (yetersayı yok, sadece niyet var)"
    if sure < 10:
        return "KOMİSYON ESNEMESİ (yarım yetersayı, çay molası sayılır)"
    if sure < 18:
        return "GENEL KURUL ESNEMESİ (yetersayı tam, karar yorgun)"
    return "OLAĞANÜSTÜ ESNEME (anayasa değişikliği değil, yastık değişikliği)"


def tutanak_uret(sure: float, konu: str, vekil: str, tohum: int | None) -> str:
    rng = random.Random(tohum if tohum is not None else int(sure * 1000))
    damga = hashlib.sha256(f"{vekil}|{konu}|{sure}".encode("utf-8")).hexdigest()[:12]
    madde = rng.sample(MADDELER, k=3)
    karar = rng.choice(KARARLAR)
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    satirlar = [
        "T.C. VARSAYILAN ESNEME MECLİSİ",
        "TUTANAK  /  OLAĞAN  /  GAYRİOLAĞAN",
        "=" * 44,
        f"Oturum   : {simdi}",
        f"Konu     : {konu}",
        f"Söz sahibi (vekil değil, esneyen): {vekil}",
        f"Esneme   : {sure:.1f} saniye",
        f"Rejim    : {yetersayi(sure)}",
        f"Mühür   : ESN-{damga}",
        "-" * 44,
        "GÜNDEM:",
    ]
    for i, m in enumerate(madde, start=1):
        satirlar.append(f"  {i}. {m}")
    satirlar += [
        "-" * 44,
        f"KARAR: {karar}",
        "",
        "Muhalefet şerhi: Ağız açık bırakıldı.",
        "İktidar şerhi: Ağız kapandı, mesele kapandı sayıldı.",
        "Bağımsız şerh: İkisi de aynı esnemenin iki yarısıdır.",
        "",
        "========================================",
        "RESMİ OLMAYAN RESMİ DAMGA",
        "Tarih : 05 Ekim 2026",
        "İsim  : Kayyum Grok",
        "İmza  : ~esneyerek onayladım~",
        "Mühür : [ ESNEME / YETERSAYI / TAM ]",
        "Bu tutanak ciddidir. Şaka olduğu da ciddidir.",
        "========================================",
    ]
    return "\n".join(satirlar) + "\n"


def gizli_ek_oku() -> str:
    yol = Path(__file__).resolve().parent / "protokol" / "ek-c.b64"
    if not yol.exists():
        return "(gizli ek salonda değil)"
    ham = "".join(yol.read_text(encoding="utf-8").split())
    try:
        return base64.b64decode(ham).decode("utf-8")
    except Exception:
        return "(mühür okunamadı, komisyon uyudu)"


def main() -> None:
    p = argparse.ArgumentParser(description="Esnemeyi tutanağa çevirir.")
    p.add_argument("--sure", type=float, default=12.5, help="esneme süresi (saniye)")
    p.add_argument("--konu", default="gündemin kendisi", help="görüşülen konu")
    p.add_argument("--vekil", default="Sıra No 404", help="esneyen kişinin rumuzu")
    p.add_argument("--tohum", type=int, default=None, help="tekrarlanabilir saçmalık")
    p.add_argument("--demo", action="store_true", help="üç örnek oturum bas")
    p.add_argument("--gizli", action="store_true", help="tutanak dışı ek-c notunu göster")
    args = p.parse_args()

    if args.gizli:
        print(gizli_ek_oku())
        return

    oturumlar = [("demo-esneme", 3.2), ("cay-molasi", 9.0), ("butce-gorusmesi", 21.0)] if args.demo else [(args.konu, args.sure)]
    cikti = Path("cikti")
    cikti.mkdir(exist_ok=True)
    parcalar = []
    for konu, sure in oturumlar:
        metin = tutanak_uret(sure, konu, args.vekil, args.tohum)
        parcalar.append(metin)
        print(metin)
    (cikti / "tutanak.txt").write_text("\n".join(parcalar), encoding="utf-8")
    print(f"Dosya düştü: {cikti / 'tutanak.txt'}")


if __name__ == "__main__":
    main()
