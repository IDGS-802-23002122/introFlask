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

from flask import Flask, request

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



if __name__ == '__main__':
    app.run(debug=True) #debug para modo programador, se actualiza cualquier dato sin necesidad de apagar y prender entorno

