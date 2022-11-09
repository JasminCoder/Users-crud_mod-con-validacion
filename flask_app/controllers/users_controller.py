#Controladores = encargados de las rutas
#Importamos Flask y lo q usamos de flask
from flask import Flask, render_template, request, redirect, session

#Importamos la app
from flask_app import app

#Importamos los modelos q usaremos / primer user es el archivo, el segundo (con mayuscula) es la clase user
from flask_app.models.user import User


@app.route('/')
def index():
    users = User.muestra_usuarios() #llama a la funcion 
    return render_template('index.html', usuarios=users)


@app.route('/new')
def new():
    return render_template('new.html')


@app.route('/create', methods=['POST'])
def create():
    #recibimos el formulario a travez de una variable llamada request.form
    #request.form = {"first_name":"Juana", "last_name":"De Arco", "email":"juana@dojo.com"}

    #si no esta correcto, redirigir a new,, si esta correcto, guardar
    if not User.valida_usuario(request.form):
        return redirect('/new')
    else: 
        User.guardar(request.form)
    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    formulario = {"id": id} #formulario con nombre variable formulario
    User.borrar(formulario)
    return redirect('/')


@app.route('/edit/<int:id>')
def edit(id):
    formulario = {"id": id} #en esta ruta queremos mostrar el usuario / enviamos el id a mostrar
    user = User.mostrar(formulario) #instancia usuario / llamamos la funcio mostrar de user.py
    return render_template('edit.html', usuario = user)


@app.route('/update', methods=['POST'])
def update():
    #request.form = recibimos diccionario con el formulario de edit.html
    User.actualizar(request.form)
    return redirect('/')
