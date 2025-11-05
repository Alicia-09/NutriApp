from flask import Flask, render_template,request,flash,url_for,redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("inicio.html")

@app.route("/inicio")
def index():
    return render_template("inicio.html")

@app.route("/crearCuenta" , methods = ["GET", "POST"])
def crearCuenta():

    error=None
    if request.method == "POST":
        Nombre = request.form["Nombre"]
        Apellido = request.form["Apellido"]
        Fecha = request.form["Fecha"]
        Genero = request.form["Genero"]
        Email = request.form["Email"]
        Contra = request.form["Contra"]
        ContraConfirm = request.form["ContraConfirm"]
    
        if Contra != ContraConfirm:
            error = "La contraseña no coincide"
            if error != None:
                flash(error)
            return render_template("crearCuenta.html")
            
        flash(f"Registro exitoso para el usuario:{Nombre} {Apellido}")
        return redirect (url_for ("inicio.html"))
    
    return render_template("crearCuenta.html")



if __name__ == "__main__":
    app.run(debug=True)