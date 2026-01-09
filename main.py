from flask import Flask, render_template

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



if __name__ == '__main__':
    app.run(debug=True) #debug para modo programador, se actualiza cualquier dato sin necesidad de apagar y prender entorno

