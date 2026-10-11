#!/usr/bin/env python3
"""Export bundled data in its original format for reuse under its upstream licenses."""
import pathlib
import sqlite3
import sys
root = pathlib.Path(__file__).resolve().parents[1]
destination = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "exported-hanzi")
destination.mkdir(parents=True, exist_ok=True)
with sqlite3.connect(root / "HanziPractice/Resources/hanzi.sqlite") as db:
    for column, name in [("dictionary_json", "dictionary.txt"), ("graphics_json", "graphics.txt")]:
        with (destination / name).open("w") as output:
            for row in db.execute(f"SELECT {column} FROM characters ORDER BY rowid"):
                output.write(row[0] + "\n")
import shutil
shutil.copytree(root / "HanziPractice/Resources/Licenses", destination / "Licenses", dirs_exist_ok=True)
print(destination.resolve())
