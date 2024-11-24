import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obtener los datos del formulario
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Validar los datos
        if not name or not month or not day:
            print("Faltan datos, redireccionando...")
            return redirect("/")

        try:
            month = int(month)
            day = int(day)
        except ValueError:
            print("Valores no válidos, redireccionando...")
            return redirect("/")

        if month < 1 or month > 12 or day < 1 or day > 31:
            print("Fecha no válida, redireccionando...")
            return redirect("/")

        # Insertar los datos en la base de datos
        db.execute("INSERT INTO birthdays (name, month, day) VALUES (:name, :month, :day)",
                   name=name, month=month,day=day)
        print(f"Cumpleaños agregado: {name}, {month}/{day}")

        # Redirigir de nuevo a la página principal
        return redirect("/")

    else:
        # Consultar todos los cumpleaños
        birthdays = db.execute("SELECT * FROM birthdays")
        print(f"Cargando cumpleaños: {birthdays}")

        # Renderizar la página index.html con los datos de cumpleaños
        return render_template("index.html", birthdays=birthdays)

# Habilitar el modo de depuración
if __name__ == "__main__":
    app.run(debug=True)
