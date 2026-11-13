from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "plazas.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS plazas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ubicacion TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            latitud REAL NOT NULL,
            longitud REAL NOT NULL,
            estado TEXT NOT NULL,
            imagen TEXT,
            es_demo INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS opiniones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plaza_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            opinion TEXT NOT NULL,
            fecha TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (plaza_id) REFERENCES plazas(id) ON DELETE CASCADE
        )
        """
    )

    if conn.execute("SELECT COUNT(*) FROM plazas").fetchone()[0] == 0:
        conn.executemany(
            """
            INSERT INTO plazas (nombre, ubicacion, descripcion, latitud, longitud, estado, imagen, es_demo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "Plaza San Martín",
                    "Centro de Las Heras, Mendoza",
                    "Espacio público de referencia con áreas verdes, bancos y circulación peatonal activa.",
                    -32.8416,
                    -68.8018,
                    "Buen estado",
                    "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=900&q=80",
                    1,
                ),
                (
                    "Plaza 25 de Mayo",
                    "Calle Principal y Avenida del Libertador, Las Heras",
                    "Un punto de encuentro vecinal donde se realizan actividades comunitarias y eventos locales.",
                    -32.8452,
                    -68.8032,
                    "Estado regular",
                    "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?auto=format&fit=crop&w=900&q=80",
                    1,
                ),
                (
                    "Parque del Bicentenario",
                    "Zona norte de Las Heras, Mendoza",
                    "Área verde con senderos, áreas de juego y una importante trazabilidad de tránsito vecinal.",
                    -32.8376,
                    -68.7928,
                    "Mal estado",
                    "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?auto=format&fit=crop&w=900&q=80",
                    1,
                ),
                (
                    "Plaza del Barrio Sur",
                    "Barrio Sur, Las Heras",
                    "Plaza cercana a viviendas familiares con menos mantenimiento y demanda de mejoras urbanas.",
                    -32.8495,
                    -68.8159,
                    "Buen estado",
                    "https://images.unsplash.com/photo-1511497584788-876760111969?auto=format&fit=crop&w=900&q=80",
                    1,
                ),
            ],
        )

    conn.commit()
    conn.close()


def get_plazas(estado: str = "Todas", query: str = "") -> list[dict[str, Any]]:
    conn = get_connection()
    sql = "SELECT * FROM plazas WHERE 1=1"
    params: list[Any] = []

    if estado and estado != "Todas":
        sql += " AND estado = ?"
        params.append(estado)

    if query:
        like_query = f"%{query}%"
        sql += " AND (LOWER(nombre) LIKE LOWER(?) OR LOWER(ubicacion) LIKE LOWER(?))"
        params.extend([like_query, like_query])

    sql += " ORDER BY nombre ASC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_plaza_by_id(plaza_id: int) -> dict[str, Any] | None:
    conn = get_connection()
    row = conn.execute("SELECT * FROM plazas WHERE id = ?", (plaza_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_opiniones_by_plaza(plaza_id: int) -> list[dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM opiniones WHERE plaza_id = ? ORDER BY fecha DESC, id DESC",
        (plaza_id,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def insert_opinion(plaza_id: int, nombre: str, apellido: str, opinion: str) -> int:
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO opiniones (plaza_id, nombre, apellido, opinion, fecha) VALUES (?, ?, ?, ?, datetime('now'))",
        (plaza_id, nombre, apellido, opinion),
    )
    conn.commit()
    opinion_id = cursor.lastrowid
    conn.close()
    return int(opinion_id)


def get_total_opiniones(plaza_id: int) -> int:
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM opiniones WHERE plaza_id = ?", (plaza_id,)).fetchone()[0]
    conn.close()
    return int(count)


def get_demo_message() -> str:
    return "Datos de demostración: estas plazas y opiniones pueden modificarse desde la base de datos SQLite local."
