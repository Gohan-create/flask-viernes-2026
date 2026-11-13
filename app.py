from __future__ import annotations

import re
import secrets
from datetime import datetime

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

from database import get_opiniones_by_plaza, get_plaza_by_id, get_plazas, init_db, insert_opinion

app = Flask(__name__)
app.config["SECRET_KEY"] = "mi-plaza-segura-secret-key"


@app.before_request
def ensure_db_and_csrf() -> None:
    init_db()
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)


@app.context_processor
def inject_global_data():
    return {
        "current_year": datetime.now().year,
    }


@app.route("/")
def inicio():
    plazas = get_plazas()[:3]
    return render_template("index.html", plazas=plazas)


@app.route("/mapa")
def mapa():
    estado = request.args.get("estado", "Todas")
    query = request.args.get("q", "").strip()
    plazas = get_plazas(estado=estado, query=query)
    return render_template("mapa.html", plazas=plazas, estado=estado, query=query)


@app.route("/plaza/<int:plaza_id>")
def plaza_detalle(plaza_id: int):
    plaza = get_plaza_by_id(plaza_id)
    if plaza is None:
        abort(404)

    opiniones = get_opiniones_by_plaza(plaza_id)
    return render_template(
        "plaza_detalle.html",
        plaza=plaza,
        total_opiniones=len(opiniones),
    )


@app.route("/plaza/<int:plaza_id>/formulario", methods=["GET", "POST"])
def formulario_plaza(plaza_id: int):
    plaza = get_plaza_by_id(plaza_id)
    if plaza is None:
        abort(404)

    if request.method == "POST":
        csrf_token = request.form.get("csrf_token", "")
        if csrf_token != session.get("csrf_token"):
            abort(403)

        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        opinion = request.form.get("opinion", "").strip()

        if not nombre or not apellido or not opinion:
            flash("Todos los campos son obligatorios.", "error")
            return render_template(
                "formulario.html",
                plaza=plaza,
                nombre=nombre,
                apellido=apellido,
                opinion=opinion,
            )

        if len(nombre) < 2 or len(apellido) < 2:
            flash("Nombre y apellido deben tener al menos 2 caracteres.", "error")
            return render_template(
                "formulario.html",
                plaza=plaza,
                nombre=nombre,
                apellido=apellido,
                opinion=opinion,
            )

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñüÜ\s'-]+", nombre) or not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñüÜ\s'-]+", apellido):
            flash("Nombre y apellido solo pueden contener letras, espacios, apóstrofes y guiones.", "error")
            return render_template(
                "formulario.html",
                plaza=plaza,
                nombre=nombre,
                apellido=apellido,
                opinion=opinion,
            )

        if len(opinion) < 10 or len(opinion) > 500:
            flash("La opinión debe contener entre 10 y 500 caracteres.", "error")
            return render_template(
                "formulario.html",
                plaza=plaza,
                nombre=nombre,
                apellido=apellido,
                opinion=opinion,
            )

        insert_opinion(plaza_id, nombre, apellido, opinion)
        flash("Gracias por compartir tu opinión. Tu aporte quedó registrado.", "success")
        return redirect(url_for("inicio"))

    return render_template("formulario.html", plaza=plaza)


@app.route("/plaza/<int:plaza_id>/opiniones")
def opiniones_plaza(plaza_id: int):
    plaza = get_plaza_by_id(plaza_id)
    if plaza is None:
        abort(404)

    opiniones = get_opiniones_by_plaza(plaza_id)
    return render_template("opiniones.html", plaza=plaza, opiniones=opiniones)


@app.route("/sobre")
def sobre():
    return redirect(url_for("inicio") + "#sobre")


@app.errorhandler(404)
def not_found(error):
    return render_template("index.html", plazas=get_plazas()[:3]), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)