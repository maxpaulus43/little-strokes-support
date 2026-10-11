#!/usr/bin/env python3
"""Rebuild the offline catalog, preserving original dictionary/graphic JSON records."""
import json
import pathlib
import sqlite3
import unicodedata
import urllib.request
from family_definitions import family_definition

ROOT = pathlib.Path(__file__).resolve().parents[1]
REVISION = "bddc96d41bef78427ed0e034e9f7e31d71fd1b92"
BASE = f"https://raw.githubusercontent.com/skishore/makemeahanzi/{REVISION}/"
DEST = ROOT / "HanziPractice/Resources"

def fetch(path):
    with urllib.request.urlopen(BASE + path) as response:
        return response.read()

def normalize(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.lower()) if not unicodedata.combining(c))

def main():
    DEST.mkdir(parents=True, exist_ok=True)
    database = DEST / "hanzi.sqlite"
    database.unlink(missing_ok=True)
    graphics = {}
    for line in fetch("graphics.txt").decode().splitlines():
        record = json.loads(line)
        graphics[record["character"]] = line
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE characters (character TEXT PRIMARY KEY, pinyin TEXT, definition TEXT, search TEXT, dictionary_json TEXT, graphics_json TEXT)")
        for line in fetch("dictionary.txt").decode().splitlines():
            record = json.loads(line)
            char = record["character"]
            if char not in graphics:
                continue
            pinyin = " · ".join(record.get("pinyin", []))
            definition = family_definition(record.get("definition") or "", char)
            connection.execute("INSERT INTO characters VALUES (?, ?, ?, ?, ?, ?)",
                (char, pinyin, definition, normalize(char + " " + pinyin + " " + definition), line, graphics[char]))
        connection.execute("CREATE TABLE provenance (revision TEXT, source TEXT, note TEXT)")
        connection.execute("INSERT INTO provenance VALUES (?, ?, ?)", (REVISION, "https://github.com/skishore/makemeahanzi", "2026-10-08: Original JSON records repackaged in SQLite; added normalized search keys. 2026-10-10: Family-facing English definitions and search keys filtered; original JSON preserved. Dictionary: LGPL-3.0-or-later. Graphics: Arphic Public License. No stroke geometry changes."))
        print(f"Bundled {connection.execute('SELECT count(*) FROM characters').fetchone()[0]} characters")
    for source, name in [("COPYING", "COPYING.txt"), ("LGPL", "LGPL.txt"), ("APL/english/ARPHICPL.TXT", "ARPHICPL.txt")]:
        (DEST / "Licenses" / name).write_bytes(fetch(source))
    with urllib.request.urlopen("https://www.gnu.org/licenses/gpl-3.0.txt") as response:
        (DEST / "Licenses/GPL.txt").write_bytes(response.read())
    (DEST / "Licenses/NOTICE.txt").write_text(f"Make Me a Hanzi by Skishore et al.\nhttps://github.com/skishore/makemeahanzi\nRevision: {REVISION}\n\nDictionary derived from Unihan and CJKlib: LGPL version 3 or later.\nStroke graphics derived from Arphic PL KaitiM GB and Arphic PL UKai.\nCopyright (C) 1999 Arphic Technology Co., Ltd.\nGraphics may be redistributed under the Arphic Public License. No warranty.\n\n2026-10-08: Data repackaged in SQLite with normalized search keys.\nOriginal dictionary and graphics JSON preserved in database columns.\nNo changes to stroke geometry. Export original records with Scripts/export_hanzi.py.\nThe repackaged data is freely available under its respective upstream licenses.\nSee COPYING.txt, LGPL.txt, and ARPHICPL.txt.\n")

    with (DEST / "Licenses/NOTICE.txt").open("a") as notice:
        notice.write("\n2026-10-10: Family-facing English definitions and search keys filtered.\nSome common definitions use selected neutral meanings; unsuitable definitions\nare omitted from displayed/searchable fields. Original JSON is unchanged.\n")

if __name__ == "__main__":
    main()
