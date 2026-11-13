# Mi Plaza Segura

Aplicación web desarrollada con Flask para conocer, evaluar y mejorar las plazas de Las Heras, Mendoza.

## Requisitos

- Python 3.11+
- pip

## Instalación

```bash
cd /workspaces/flask-viernes-2026
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Inicializar la base de datos

La base de datos SQLite se crea automáticamente cuando se ejecuta la aplicación. Si querés crearla de forma explícita:

```bash
cd /workspaces/flask-viernes-2026
source .venv/bin/activate
python -c "from database import init_db; init_db(); print('Base de datos inicializada')"
```

## Ejecutar el proyecto

```bash
cd /workspaces/flask-viernes-2026
source .venv/bin/activate
python app.py
```

Luego abrir: http://127.0.0.1:5000

## Funcionalidades principales

- Inicio con estética dark inspirada en estética gótica elegante.
- Mapa interactivo con Leaflet y OpenStreetMap.
- Marcadores para plazas con filtros por estado y búsqueda por nombre.
- Ficha detallada de cada plaza.
- Formulario de opinión y reclamo asociado a la plaza elegida.
- Registro de opiniones en SQLite.
- Página de opiniones por plaza con ordenamiento por fecha.
- Persistencia de datos mediante SQLite.

## Estructura del proyecto

```text
mi_plaza_segura/
├── app.py
├── database.py
├── models.py
├── requirements.txt
├── README.md
├── database/
│   └── plazas.db
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── mapa.html
│   ├── plaza_detalle.html
│   ├── formulario.html
│   └── opiniones.html
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── mapa.js
│   └── img/
└── .venv/
```

## Base de datos

Las tablas creadas automáticamente son:

- `plazas`
- `opiniones`

Los registros iniciales se marcan como `es_demo = 1` para diferenciar datos de demostración.

## Cómo funciona cada sección

- Inicio: presenta la idea del proyecto y la misión vecinal.
- Mapa: muestra plazas con marcadores, filtros y búsqueda.
- Detalle de plaza: presenta ubicación, descripción y estado.
- Formulario: recoge nombre, apellido y opinión asociada a una plaza.
- Opiniones: lista todas las experiencias registradas ordenadas por fecha.

## Notas

- La aplicación usa SQLite local en `database/plazas.db`.
- El backend valida todos los campos y evita inyección SQL con consultas parametrizadas.
- El formulario incluye protección básica CSRF con token en sesión.
