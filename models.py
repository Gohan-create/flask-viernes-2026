from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Plaza:
    id: int
    nombre: str
    ubicacion: str
    descripcion: str
    latitud: float
    longitud: float
    estado: str
    imagen: str | None = None
    es_demo: int = 0


@dataclass
class Opinion:
    id: int
    plaza_id: int
    nombre: str
    apellido: str
    opinion: str
    fecha: str
