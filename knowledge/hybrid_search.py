"""
SAORI TACTICAL - Hybrid SQLite FTS5 Local Search Engine
Motor de búsqueda de texto completo con SQLite FTS5 incorporado en Python.
Cero dependencias externas pesadas, 100% offline, persistente en disco y ultra-rápido.
"""

import sqlite3
import os
from typing import List, Dict
from pathlib import Path

from .vault import SURVIVAL_VAULT
from radio.freq_db import FREQUENCIES

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "survival_index.db"


class TacticalSearchEngine:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Inicializa las tablas virtuales FTS5 e inserta los datos curados."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Tabla de supervivencia con FTS5
        cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS survival_fts USING fts5(
                item_id UNINDEXED,
                category,
                title,
                summary,
                steps,
                warnings,
                tokenize = 'porter unicode61'
            )
        """)

        # Tabla de frecuencias con FTS5
        cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS radio_fts USING fts5(
                freq_id UNINDEXED,
                category,
                name,
                freq_mhz UNINDEXED,
                mode UNINDEXED,
                usage,
                tokenize = 'porter unicode61'
            )
        """)

        # Si están vacías, poblar desde el vault y freq_db
        cur.execute("SELECT count(*) FROM survival_fts")
        if cur.fetchone()[0] == 0:
            for item in SURVIVAL_VAULT:
                cur.execute(
                    "INSERT INTO survival_fts VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        item["id"],
                        item["category"],
                        item["title"],
                        item["summary"],
                        "\n".join(item["steps"]),
                        item.get("warnings", "")
                    )
                )

        cur.execute("SELECT count(*) FROM radio_fts")
        if cur.fetchone()[0] == 0:
            for f in FREQUENCIES:
                cur.execute(
                    "INSERT INTO radio_fts VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        f["id"],
                        f["category"],
                        f["name"],
                        str(f["freq_mhz"]),
                        f["mode"],
                        f["usage"]
                    )
                )

        conn.commit()
        conn.close()

    def search_all(self, query: str, limit: int = 5) -> Dict[str, List[Dict]]:
        """Busca simultáneamente en protocolos de supervivencia y en frecuencias de radio."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Limpiar query para FTS5
        clean_q = "".join([c if c.isalnum() or c.isspace() else " " for c in query]).strip()
        if not clean_q:
            conn.close()
            return {"survival": [], "radio": []}

        fts_query = " OR ".join(clean_q.split())

        # Búsqueda en supervivencia
        survival_results = []
        try:
            cur.execute("""
                SELECT item_id, category, title, summary, steps, warnings, rank
                FROM survival_fts
                WHERE survival_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (fts_query, limit))
            for row in cur.fetchall():
                survival_results.append({
                    "id": row[0],
                    "category": row[1],
                    "title": row[2],
                    "summary": row[3],
                    "steps": row[4].split("\n"),
                    "warnings": row[5]
                })
        except Exception:
            pass

        # Búsqueda en radio
        radio_results = []
        try:
            cur.execute("""
                SELECT freq_id, category, name, freq_mhz, mode, usage, rank
                FROM radio_fts
                WHERE radio_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (fts_query, limit))
            for row in cur.fetchall():
                radio_results.append({
                    "id": row[0],
                    "category": row[1],
                    "name": row[2],
                    "freq_mhz": float(row[3]),
                    "mode": row[4],
                    "usage": row[5]
                })
        except Exception:
            pass

        conn.close()
        return {
            "survival": survival_results,
            "radio": radio_results
        }
