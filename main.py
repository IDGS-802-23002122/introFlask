import math
from flask import Flask, render_template, request

app=Flask(__name__)

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

@app.route("/distancia")
def distancia():
    return render_template("distancia.html")

@app.route("/calculoDistancia", methods=["GET", "POST"])
def calculo():
    distancia = None # Esto sirve para almacenar el resultado
    
    if request.method == "POST":
        # 1. Convertir a float para poder operar
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))

        distancia = ((x2 - x1)**2 + (y2 - y1)**2)**0.5

    return render_template("distancia.html", resultado=distancia)

@app.route("/cinepolis")
def cinepolis():
    return render_template("cinepolis.html")

@app.route('/calculoBoletos', methods=['POST'])
def calculo_boletos():
    # Recibimos los datos del formulario
    nombre = request.form.get('nombre')
    compradores = int(request.form.get('comprador'))
    boletos = int(request.form.get('boletos'))
    usa_tarjeta = request.form.get('tarjeta') # 'si' o 'no'

    # REGLA: Máximo 7 boletos por persona
    limite_boletos = compradores * 7
    
    if boletos > limite_boletos:
        # Si excede el límite, podemos retornar un mensaje o limpiar el campo
        mensaje_error = f"Error: {compradores} personas solo pueden comprar máximo {limite_boletos} boletos."
        return render_template('cinepolis.html', total=mensaje_error)

    # Cálculo base
    precio_boleto = 12000
    subtotal = boletos * precio_boleto

    # DESCUENTO POR CANTIDAD DE BOLETOS
    descuento_cantidad = 0
    if boletos > 5:
        descuento_cantidad = 0.15 # 15%
    elif boletos >= 3: 
        descuento_cantidad = 0.10 # 10%
    
    # Aplicamos el primer descuento
    subtotal = subtotal - (subtotal * descuento_cantidad)

    # DESCUENTO POR TARJETA CINECO (10% adicional)
    if usa_tarjeta == "si":
        subtotal = subtotal - (subtotal * 0.10)

    # Resultado al formulario
    return render_template('cinepolis.html', total=f"${subtotal:,.0f}")
  

if __name__ == '__main__':
    app.run(debug=True) #debug para modo programador, se actualiza cualquier dato sin necesidad de apagar y prender entorno

