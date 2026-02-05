from math import *
from flask import Flask, render_template, request
from flask import flash
from flask_wtf.csrf import CSRFProtect 
import forms
from forms import CinepolisForm


app=Flask(__name__)
app.secret_key='Clave secreta'
csrf=CSRFProtect(app)


@app.route('/')
def index():
    titulo=     "IDGS-802-Flask"                 #así se crean las variables
    list=['Juan', 'Karla', 'Ana', 'Miguel']      #así se crean las listas
    return render_template('index.html', titulo=titulo, list=list)  #Aquí se mandan

@app.route('/formularios')
def formularios():
    return render_template('formularios.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

@app.route('/hola') #Así se definen las rutas para el navegador
def hola():  
    return "¡Hola, hola!" #Siempre regresan algo.

#ruta de usuarios (recibe, NO manda)
@app.route('/user/<string:user>') #"String" se le pone para decir de que tipo será
def user(user):
    return f"Hello, {user}"

#ruta para entero
@app.route("/numero/<int:n>")
def numero(n):
    return "Numero: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id,username):
    return "ID: {} nombre: {}".format(id,username)

@app.route("/suma/<float:n1>/<float:n2>")
def func(n1, n2):
    return "La suma es: {}".format(n1+n2)

@app.route("/default/")
@app.route("/default/<string:param>")
def func2(param="juan"):  #se cambio a "func2" porque no puede haber dos con el name igual como "func" de nuevo
    return f"<h1>¡Hola, {param}!</h1>"

@app.route("/operas")
def operas():    #las tres comillas sirven para que lo que yo escriba sea multilinea
    return '''   
    <form>
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>

        <label for="name">apaterno:</label>
        <input type="text" id="name" name="name" required>
    </form>
                
          '''

@app.route("/operasBas")
def operas1():
    return render_template("operasBas.html")


@app.route("/resultado", methods=["GET", "POST"])
def resultado():
    # 1. Obtenemos los datos del formulario
    n1 = request.form.get("n1")
    n2 = request.form.get("n2")
    operacion = request.form.get("operacion")

    # Validación básica por si llegan vacíos
    if not n1 or not n2:
        return "Por favor, ingresa ambos números."

    # Los datos se convierten a float para realizar cálculos
    n1 = float(n1)
    n2 = float(n2)

    # 2. Lógica para decidir qué operación realizar
    if operacion == "sumar":
        resultado_final = n1 + n2
        accion = "suma"
    elif operacion == "restar":
        resultado_final = n1 - n2
        accion = "resta"
    elif operacion == "multiplicar":
        resultado_final = n1 * n2
        accion = "multiplicación"
    elif operacion == "dividir":
        if n2 == 0:
            return "Error: No se puede dividir entre cero."
        resultado_final = n1 / n2
        accion = "división"
    else:
        return "Operación no válida."

    # 3. Retorna el resultado
    return f"La {accion} de {n1} y {n2} es: {resultado_final}"

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/distancia", methods=["GET", "POST"])
def distancia():
    distancia_resultado = None
    if request.method == "POST":
        try:
            x1 = float(request.form.get("x1", 0))
            y1 = float(request.form.get("y1", 0))
            x2 = float(request.form.get("x2", 0))
            y2 = float(request.form.get("y2", 0))

            distancia_resultado = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        except (ValueError, TypeError):
            distancia_resultado = 0
            flash("¡Cálculo de distancia realizado!", "success") 
        except:
            flash("Error en los datos ingresados", "danger")
    return render_template("distancia.html", resultado=distancia_resultado)

@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():
        mat=0
        nom=''
        apa=''
        ama=''
        email=''
        usuarios_class=forms.UserForm(request.form)
        if request.method=='POST' and usuarios_class.validate():
            mat=usuarios_class.matricula.data
            nom=usuarios_class.nombre.data
            apaterno=usuarios_class.apaterno.data
            amaterno=usuarios_class.amaterno.data
            email=usuarios_class.email.data

            mensaje='Bienvenido {}'.format(nom)
            flash(mensaje)

        return render_template('usuarios.html',form=usuarios_class,
                               mat=mat,nom=nom,apa=apa,ama=ama,email=email
                               )


@app.route("/cinepolis", methods=['GET', 'POST'])
def cinepolis():
    form = CinepolisForm()
    total = None  

    if request.method == 'POST':
        if form.validate_on_submit():
            # 1. Recuperamos los datos si el formulario es válido (no está vacío)
            compradores = form.compradores.data
            boletos = form.boletos.data
            tarjeta = form.tarjeta.data == 'si'
            
            # 2. Validación de lógica de negocio (Máximo 7 boletos por persona)
            if boletos > (compradores * 7):
                flash(f"Error: No se pueden comprar {boletos} boletos para {compradores} personas (Máximo 7 por persona).", "danger")
            else:
                # 3. Cálculo si todo es correcto
                precio_boleto = 12.0
                subtotal = boletos * precio_boleto
                
                # Descuentos por cantidad
                if boletos > 5:
                    subtotal *= 0.85  # 15% desc
                elif 3 <= boletos <= 5:
                    subtotal *= 0.90  # 10% desc
                
                # Descuento extra por tarjeta Cineco
                if tarjeta:
                    subtotal *= 0.90  # 10% desc adicional
                
                total = round(subtotal, 2)
                flash(f"¡Venta procesada con éxito! Total: ${total}", "success")
        else:
            flash("Error en el formulario. Por favor, llena todos los campos correctamente.", "danger")

    return render_template("cinepolis.html", form=form, total=total)

if __name__ == '__main__':
    app.run(debug=True) #debug para modo programador, se actualiza cualquier dato sin necesidad de apagar y prender entorno

