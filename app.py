from flask import Flask, render_template,request,flash,url_for,redirect,session

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Ali091903'


USUARIOS_REGISTRADOS = {
    "24308060610613@cetis61.edu.mx"
        "Nombre": "Alicia",
        "Apellido": "Campos",
        "Contra": "Ali091903."

}

@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route('/sesion')
def sesion():
    return render_template("sesion.html")

@app.route('/ValidaSesion', methods=['GET', 'POST'])
def ValidaSesion():
    if request.method == "POST":
        email = request.form.get('Email', '').strip()
        contra = request.form.get('Contra', '').strip()

        if not email or not contra:
            flash('Por favor ingresa email y contraseña', 'error')
            return redirect(url_for('sesion'))

        if email not in USUARIOS_REGISTRADOS:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('sesion'))

        usuario = USUARIOS_REGISTRADOS[email]

        if usuario['Contra'] != contra:
            flash('Contraseña incorrecta', 'error')
            return redirect(url_for('sesion'))

        session['usuario_email'] = email
        session['usuario'] = usuario['Nombre']
        session['logueado'] = True

        flash(f"Bienvenido {usuario['Nombre']}!", 'success')
        return redirect(url_for('inicio'))

    return redirect(url_for('sesion'))


@app.route("/crearCuenta", methods=["GET", "POST"])
def crearCuenta():
    if request.method == "POST":
        nombre = request.form.get("Nombre")  
        apellido = request.form.get("Apellido")  
        fecha = request.form.get("Fecha")       
        genero = request.form.get("Genero")     
        email = request.form.get("Email")      
        contra = request.form.get("Contra")     
        contraConfirm = request.form.get("ContraConfirm") 

        if contra != contraConfirm:
            flash("La contraseña no coincide", "error")
            return render_template("crearCuenta.html")

        USUARIOS_REGISTRADOS[email] = {
            "Nombre": nombre,
            "Apellido": apellido,
            "Fecha": fecha,
            "Genero": genero,
            "Contra": contra
        }

        session['usuario_email'] = email
        session['usuario'] = nombre
        session['logueado'] = True

        flash(f"Cuenta creada correctamente para el usuario:{nombre} {apellido}, continúa llenando tus datos", "success")
        return redirect(url_for("usuario"))

    return render_template("crearCuenta.html")

@app.route('/usuario', methods=['GET', 'POST'])
def usuario():
    if 'usuario_email' not in session:
        flash('Por favor inicia sesión primero', 'error')
        return redirect(url_for('sesion'))
    
    if request.method == "POST":
        peso = request.form.get("Peso")
        altura = request.form.get("Altura")
        actividad = request.form.get("Actividad")
        objetivos = request.form.get("Objetivos")
        preferencias = request.form.get("Preferencias")
        experiencia = request.form.get("Experiencia")

        flash("Datos guardados correctamente ", "success")
        return redirect(url_for('inicio'))
    return render_template('usuario.html')

@app.route("/educacion")
def educacion():
    return render_template("educacion.html")

@app.route("/calculadoras")
def calculadoras():
    return render_template("calculadoras.html")

@app.route("/IMC", methods=["GET"])
def IMC():
    return render_template("IMC.html")

@app.route("/calcular_imc", methods=["POST"])
def calcular_imc():
    resultado = None

    if request.method == "POST":
        try:
           peso = float(request.form["peso"])
           altura = float(request.form["altura"])

           if altura > 0:
               resultado = (peso / (altura ** 2 ))

        except:
            resultado= "Error"

    return render_template ("IMC.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)