#!/usr/bin/env python3
import sqlite3

from pathlib import Path

from library_definition import libraries, LibrarySpec
from generator import build_library

cache = Path("cache/cache.sqlite3")
output_folder = Path("build")

def main() -> None:
    cache_dir=Path(cache)
    root_dir = Path(__file__).resolve().parents[2] 
    db_path = root_dir / cache
    conn = sqlite3.connect(db_path)
    try:
        for definition in libraries:
            build_library(conn, definition, root_dir, output_folder)
    finally:
        conn.close()

if __name__ == "__main__":
    main()