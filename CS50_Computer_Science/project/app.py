import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

# Configuración de la aplicación
app = Flask(__name__)

# Configurar la base de datos SQLite
db = SQL("sqlite:///data/pickleball.db")

# Configurar la sesión
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Deshabilitar el cacheo de respuestas
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Ruta de inicio
@app.route("/")
def index():
    # Verificar si el usuario ya ha iniciado sesión
    if session.get("user_id"):
        return redirect("/reservations")

    # Si no ha iniciado sesión, mostrar la página principal con opciones de login/registro
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# Ruta de registro de usuarios (sin login_required)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Obtener datos del formulario
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Verificar que los campos no estén vacíos
        if not username or not password or not confirmation:
            flash("Falta información", "error")
            return redirect("/register")

        # Verificar que las contraseñas coincidan
        if password != confirmation:
            flash("Las contraseñas no coinciden", "error")
            return redirect("/register")

        # Hashear la contraseña
        password_hash = generate_password_hash(password)

        # Intentar insertar el usuario en la base de datos
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)
        except:
            flash("El usuario ya existe", "error")
            return redirect("/register")

        # Redirigir al inicio de sesión
        flash("Registro exitoso. Inicia sesión.", "success")
        return redirect("/login")

    # Si la solicitud es GET, mostrar el formulario
    return render_template("register.html")

# Ruta de inicio de sesión (sin login_required)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Obtener datos del formulario
        username = request.form.get("username")
        password = request.form.get("password")

        # Verificar que los campos no estén vacíos
        if not username or not password:
            flash("Falta información", "error")
            return redirect("/login")

        # Consultar el usuario en la base de datos
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Verificar que el usuario exista y la contraseña sea correcta
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Usuario o contraseña incorrectos", "error")
            return redirect("/login")

        # Iniciar la sesión del usuario y almacenar el rol en la sesión
        session["user_id"] = rows[0]["id"]
        session["role"] = rows[0]["role"]

        # Redirigir a la página principal
        return redirect("/")

    # Si la solicitud es GET, mostrar el formulario
    return render_template("login.html")

# Ruta de cierre de sesión
@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión", "info")
    return redirect("/")

# Ruta de reservas (con login_required)
@app.route("/reservations", methods=["GET", "POST"])
@login_required
def reservations():
    """Show available courts and allow users to make a reservation"""

    if request.method == "POST":
        # Obtener los datos del formulario
        court_id = request.form.get("court_id")
        date = request.form.get("date")
        hour = request.form.get("hour")
        minute = request.form.get("minute")

        # Componer la hora en formato HH:MM
        time = f"{hour}:{minute}"

        from datetime import datetime, timedelta
        reservation_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        reservation_end_time = reservation_time + timedelta(hours=1)

        # Verificar si ya hay una reserva que coincida en el rango de una hora
        existing_reservation = db.execute("""
            SELECT * FROM reservations
            WHERE court_id = ?
            AND date = ?
            AND time BETWEEN ? AND ?
        """, court_id, date, time, reservation_end_time.strftime("%H:%M"))

        if existing_reservation:
            # Pasar el mensaje a la plantilla de error
            return render_template("reservation.html", courts=db.execute("SELECT * FROM courts"), message="La pista ya está reservada dentro de este rango de tiempo.")

        # Hacer la reserva en la base de datos
        user_id = session["user_id"]
        db.execute("""
            INSERT INTO reservations (user_id, court_id, date, time)
            VALUES (?, ?, ?, ?)
        """, user_id, court_id, date, time)

        # Pasar el mensaje a la plantilla de éxito
        return render_template("reservation.html", courts=db.execute("SELECT * FROM courts"), message="Reserva realizada con éxito.")

    else:
        # Obtener las pistas disponibles
        courts = db.execute("SELECT * FROM courts")

        # Mostrar las pistas en la página
        return render_template("reservation.html", courts=courts)

# Ruta del historial de reservas (con login_required)
@app.route("/history")
@login_required
def history():
    """Show the user's reservation history"""

    # Obtener el id del usuario actual
    user_id = session["user_id"]

    # Consultar el historial de reservas del usuario
    reservations = db.execute("""
        SELECT reservations.id, courts.court_name, reservations.date, reservations.time
        FROM reservations
        JOIN courts ON reservations.court_id = courts.id
        WHERE reservations.user_id = ?
        ORDER BY reservations.date DESC, reservations.time DESC
    """, user_id)

    # Mostrar la página del historial de reservas
    return render_template("history.html", reservations=reservations)

# Ruta para que los usuarios eliminen sus propias reservas
@app.route("/delete_reservation_user", methods=["POST"])
@login_required
def delete_reservation_user():
    """Eliminar una reserva (por el propio usuario)"""

    # Obtener el ID de la reserva a eliminar
    reservation_id = request.form.get("reservation_id")

    # Verificar si la reserva pertenece al usuario actual
    user_id = session["user_id"]
    reservation = db.execute("SELECT * FROM reservations WHERE id = ? AND user_id = ?", reservation_id, user_id)

    if not reservation:
        flash("No puedes eliminar esta reserva.", "error")
        return redirect("/history")

    # Eliminar la reserva de la base de datos
    db.execute("DELETE FROM reservations WHERE id = ?", reservation_id)

    flash("Reserva eliminada con éxito.", "success")
    return redirect("/history")

# Ruta de panel de control para administradores (con login_required)
@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    """Admin panel to manage courts and view all reservations"""

    # Verificar si el usuario es administrador
    user_id = session["user_id"]
    user = db.execute("SELECT role FROM users WHERE id = ?", user_id)
    if user[0]["role"] != "admin":
        return "Acceso denegado", 403

    if request.method == "POST":
        # Añadir una nueva pista
        court_name = request.form.get("court_name")
        available_from = request.form.get("available_from")
        available_to = request.form.get("available_to")

        # Verificar que los campos no estén vacíos
        if not court_name or not available_from or not available_to:
            flash("Faltan datos", "error")
            return redirect("/admin")

        # Insertar la nueva pista en la base de datos
        db.execute("INSERT INTO courts (court_name, available_from, available_to) VALUES (?, ?, ?)",
                   court_name, available_from, available_to)

        flash("Pista añadida con éxito", "success")
        return redirect("/admin")

    else:
        # Obtener todas las pistas, reservas y usuarios
        courts = db.execute("SELECT * FROM courts")
        reservations = db.execute("""
            SELECT reservations.id, users.username, users.id AS user_id, courts.court_name, courts.id AS court_id, reservations.date, reservations.time
            FROM reservations
            JOIN users ON reservations.user_id = users.id
            JOIN courts ON reservations.court_id = courts.id
            ORDER BY reservations.date DESC, reservations.time DESC
        """)
        users = db.execute("SELECT id, username FROM users")

        # Renderizar el panel de control
        return render_template("admin.html", courts=courts, reservations=reservations, users=users)

# Ruta para modificar una reserva (por el administrador)
@app.route("/edit_reservation", methods=["POST"])
@login_required
def edit_reservation():
    """Modificar una reserva (solo para administradores)"""

    # Verificar si el usuario es administrador
    user_id = session["user_id"]
    user = db.execute("SELECT role FROM users WHERE id = ?", user_id)
    if user[0]["role"] != "admin":
        return "Acceso denegado", 403

    # Obtener los datos del formulario
    reservation_id = request.form.get("reservation_id")
    new_user_id = request.form.get("user_id")
    new_court_id = request.form.get("court_id")
    new_date = request.form.get("date")
    new_time = request.form.get("time")

    # Actualizar la reserva en la base de datos
    db.execute("""
        UPDATE reservations
        SET user_id = ?, court_id = ?, date = ?, time = ?
        WHERE id = ?
    """, new_user_id, new_court_id, new_date, new_time, reservation_id)

    flash("Reserva modificada con éxito", "success")
    return redirect("/admin")

# Ruta para eliminar una reserva (con login_required)
@app.route("/delete_reservation", methods=["POST"])
@login_required
def delete_reservation():
    """Eliminar una reserva (solo para administradores)"""

    # Verificar si el usuario es administrador
    user_id = session["user_id"]
    user = db.execute("SELECT role FROM users WHERE id = ?", user_id)
    if user[0]["role"] != "admin":
        return "Acceso denegado", 403

    # Obtener el ID de la reserva a eliminar
    reservation_id = request.form.get("reservation_id")

    # Eliminar la reserva de la base de datos
    db.execute("DELETE FROM reservations WHERE id = ?", reservation_id)

    flash("Reserva eliminada con éxito", "success")
    return redirect("/admin")

# Ruta para eliminar una pista (con login_required)
@app.route("/delete_court", methods=["POST"])
@login_required
def delete_court():
    """Eliminar una pista (solo para administradores)"""

    # Verificar si el usuario es administrador
    user_id = session["user_id"]
    user = db.execute("SELECT role FROM users WHERE id = ?", user_id)
    if user[0]["role"] != "admin":
        return "Acceso denegado", 403

    # Obtener el ID de la pista a eliminar
    court_id = request.form.get("court_id")

    # Eliminar la pista de la base de datos
    db.execute("DELETE FROM courts WHERE id = ?", court_id)

    flash("Pista eliminada con éxito", "success")
    return redirect("/admin")

# Ruta para editar una pista (con login_required)
@app.route("/edit_court", methods=["POST"])
@login_required
def edit_court():
    """Editar una pista (solo para administradores)"""

    # Verificar si el usuario es administrador
    user_id = session["user_id"]
    user = db.execute("SELECT role FROM users WHERE id = ?", user_id)
    if user[0]["role"] != "admin":
        return "Acceso denegado", 403

    # Obtener los datos del formulario
    court_id = request.form.get("court_id")
    court_name = request.form.get("court_name")
    available_from = request.form.get("available_from")
    available_to = request.form.get("available_to")

    # Actualizar la pista en la base de datos
    db.execute("""
        UPDATE courts
        SET court_name = ?, available_from = ?, available_to = ?
        WHERE id = ?
    """, court_name, available_from, available_to, court_id)

    flash("Pista editada con éxito", "success")
    return redirect("/admin")

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
