from flask import Flask, render_template,request,flash,url_for,redirect,session
import requests


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Ali091903'

SPOONACULAR_API_KEY = '523486f7110648bf9f7af1d422f2f117'
API_URL = 'https://api.spoonacular.com'

USUARIOS_REGISTRADOS = {
    "24308060610613@cetis61.edu.mx":{
        "Nombre": "Alicia",
        "Apellido": "Campos",
        "Contra": "Ali091903."
    }
}

FA = {
    "sedentario": 1.2,
    "ligera": 1.375,
    "moderada": 1.55,
    "alta": 1.725,
    "intensa": 1.9

}

@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route('/sesion')
def sesion():
    return render_template("sesion.html")

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('inicio'))

@app.route('/ValidaSesion', methods=['GET', 'POST'])
def ValidaSesion():
    if request.method == "POST":
        email = request.form.get('Email', '').strip()
        contra = request.form.get('Contra', '').strip()

        if not email or not contra:
            flash('Por favor ingresa email y contraseña', 'error')
            return redirect(url_for('sesion'))

        if not email in USUARIOS_REGISTRADOS:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('sesion'))

        usuario = USUARIOS_REGISTRADOS[email]

        if usuario['Contra'] != contra:
            flash('Contraseña incorrecta', 'error')
            return redirect(url_for('sesion'))

        session['usuario_email'] = email
        session['usuario'] = usuario['Nombre']
        session['loggeado'] = True

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
        session['loggeado'] = True

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

@app.route("/IMC")
def IMC():
    return render_template("IMC.html")

@app.route("/calcular_imc", methods=["GET", "POST"])
def calcular_imc():
    resultado = None

    if request.method == "POST":
        try:
            peso = float(request.form.get("peso"))
            altura = float(request.form.get("altura"))

            if altura < 3 and altura >0:
               resultado = round((peso / (altura ** 2 )),2)
            else:
                flash ("Error, Altura no valida","error")
                
        except:
            flash ("Error, ingrese denuevo los datos")
            return render_template("IMC.html")

    return render_template ("IMC.html", resultado=resultado)

@app.route("/TMB")
def TMB():
    return render_template("TMB.html")

@app.route("/calcular_tmb", methods=["GET", "POST"])
def calcular_tmb():
    resultado = None

    if request.method == "POST":
        try:
            sexo = request.form.get("sexo")
            peso = float(request.form.get("peso"))
            altura = float(request.form.get("altura"))
            edad = int(request.form.get("edad"))

            if sexo == "hombre":
                resultado = round(((10 * peso) + (6.25 * altura) - (5 * edad) + 5),2)

            elif sexo == "mujer":
                resultado = round(((10 * peso) + (6.25 * altura) - (5 * edad) - 161), 2)

        except:
            flash ("Error, ingrese denuevo los datos")
            return render_template("TMB.html")

    return render_template("TMB.html", resultado=resultado)

@app.route("/GCT")
def GCT():
    return render_template("GCT.html")

@app.route("/calcular_gct", methods=["GET", "POST"])
def calcular_gct():
    resultado = None

    if request.method == "POST":
        try:
            sexo = request.form.get("sexo")
            peso = float(request.form.get("peso"))
            altura = float(request.form.get("altura"))
            edad = int(request.form.get("edad"))
            actividad = request.form.get("actividad")

            if sexo == "hombre":
                resultado = (10 * peso) + (6.25 * altura) - (5 * edad) + 5

            elif sexo == "mujer":
                resultado = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

            factor = FA.get(actividad, 1)

            resultado = round((resultado * factor), 2)

        except:
            flash ("Error, ingrese denuevo los datos")
            return render_template("GCI.html")
        
    return render_template("GCT.html", resultado=resultado)

@app.route("/PCI")
def PCI():
    return render_template("PCI.html")

@app.route("/calcular_pci", methods=["GET", "POST"])
def calcular_pci():

    if request.method == "POST":
        try:
            altura = float(request.form["altura"])
            peso = float(request.form["peso"])

            peso_min = round(18.5 * (altura ** 2), 2)
            peso_max = round(24.9 * (altura ** 2), 2)

            if peso < peso_min:
                rango = "Estas por debajo de tu peso ideal"

            elif peso > peso_max:
                rango = "Estas por encima de tu peso ideal"
            
            else:
                rango = "Estas dentro de tu peso ideal"

        except:
            flash ("Error, ingrese denuevo los datos")
            return render_template("PCI.html")
        
    return render_template("PCI.html", 
                                peso_min = (peso_min),
                                peso_max = (peso_max),
                                rango = (rango))
        
@app.route("/MACRO")
def MACRO():
    return render_template("MACRO.html")

@app.route("/buscar_recetas", methods=["GET", "POST"])
def buscar_recetas():
    query = request.args.get('query', '')
    diet = request.args.get('diet', '')
    
    if query:
        url = f"{API_URL}/recipes/complexSearch"
        params = {
            'apiKey': SPOONACULAR_API_KEY,
            'query': query,
            'number': 10,
            'language': 'es',
            'addRecipeInformation': True,
            'instructionsRequired': True,
            'addRecipeNutrition': True
        }
        
        try:
            response = requests.get(url, params=params)
            resultados = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la API: {e}")
            return None
        
        if resultados:
            recetas = resultados['results']
            
            if diet:
                recetas = [r for r in recetas if getattr(r, diet, False)]
        
            
            return render_template("recetas.html", 
                                recetas=recetas,
                                query=query,
                                diet=diet)
        
    return render_template("recetas.html", 
                         recetas=[],
                         query=query,
                         diet=diet)

@app.route("/receta/<int:recipe_id>")
def detalle_receta(recipe_id):
    url_receta = f"{API_URL}/recipes/{recipe_id}/information"
    
    params_receta = {
        'apiKey': SPOONACULAR_API_KEY,
        'language': 'es',
        'includeNutrition': True
    }

    url_instrucciones = f"{API_URL}/recipes/{recipe_id}/analyzedInstructions"
    params_instrucciones = {
        'apiKey': SPOONACULAR_API_KEY,
        'language': 'es'
    }
    
    try:
        response = requests.get(url_receta, params=params_receta)
        receta = response.json()

        response = requests.get(url_instrucciones, params=params_instrucciones)
        instrucciones_analizadas = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error obteniendo receta {recipe_id}: {e}")
        return None
    
    if not receta:
        flash('Receta no encontrada', 'error')
        return redirect(url_for('buscar_recetas'))
    
    return render_template("info_receta.html",
                         receta=receta,
                         instrucciones=instrucciones_analizadas)

@app.route("/analizador", methods=['GET', 'POST'])

def analizador_recetas():
    analisis = None
    error = None
    if request.method == 'POST':
        tipo_analisis = request.form.get('tipo_analisis')
        
        if tipo_analisis == 'manual':
            titulo = request.form.get('titulo', '')
            porciones = request.form.get('porciones', '')
            ingredientes = request.form.get('ingredientes', '').split('\n')

            url = f"{API_URL}/recipes/analyze"
            params = {'apiKey': SPOONACULAR_API_KEY,                
                      'includeNutrition': True,
                      'language': 'es'}
            
            data = {
                'title': titulo,
                'ingredients': [ing for ing in ingredientes if ing.strip()],
                'servings': porciones,
            }

            try:
                response = requests.post(url, params=params, json=data)
                analisis = response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error analizando receta: {e}")
                return None
        
        if not analisis:
            error = 'No se pudo analizar la receta. Verifica los datos e intenta nuevamente.'
       
    return render_template("analizador.html",
                         analisis=analisis,
                         error=error)

@app.route("/calcular_macro", methods=["GET", "POST"])
def calcular_macro():
    if request.method == "POST":
        try:
            
            sexo = request.form.get("sexo")
            peso = float(request.form.get("peso"))
            altura = float(request.form.get("altura"))
            edad = int(request.form.get("edad"))
            actividad = request.form.get("actividad")
            objetivo = request.form.get("objetivo")

            if sexo == "hombre":
                    tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5

            elif sexo == "mujer":
                    tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161
        
            factor_actividad = FA[actividad]
            calorias_diarias = round((tmb * factor_actividad), 2)

            if objetivo == "bajar":
                calorias_objetivo = round((calorias_diarias * 0.85), 2)
            elif objetivo == "subir":
                calorias_objetivo = round((calorias_diarias * 1.15), 2)
            else:
                calorias_objetivo = calorias_diarias

            por_carbo = 0.50
            por_prote = 0.25
            por_grasas = 0.25

            gramos_carbo = round(((calorias_objetivo * por_carbo) / 4), 2)
            gramos_prote = round(((calorias_objetivo * por_prote) / 4), 2)
            gramos_grasas = round(((calorias_objetivo * por_grasas) / 9), 2)

        except:
            flash ("Error, ingrese denuevo los datos")
            return render_template("MACRO.html")
        
        return render_template("MACRO.html", 
                                    calorias = (calorias_objetivo),
                                    carbo = (gramos_carbo),
                                    prote = (gramos_prote),
                                    grasas = (gramos_grasas)) 

@app.route("/etiquetas")
def etiquetas():
    return render_template("etiquetas.html")

@app.route("/mitos")
def mitos():
    return render_template("mitos.html")

@app.route("/macronutrientes")
def macronutrientes():
    return render_template("macronutrientes.html")

@app.route("/hidratacion")
def hidratacion():
    return render_template("hidratacion.html")

if __name__ == "__main__":
    app.run(debug=True)