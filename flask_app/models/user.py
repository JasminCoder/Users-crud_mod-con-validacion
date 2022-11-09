#coneccion con la BD
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash #importamos flash para enviar mensajes de validacion

import re #importando expresones regulares (siempre es igual.. para validar q el correo ingresado sea valido)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:

    def __init__(self, data):
        #data = {"id": 1, "first_name":"Elena", "last_name":"De Troya", "email":"elena@dojo.com", 
        #"created_at":"2022-09-26", "update_at":"2022-09-26"}
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.update_at = data['update_at']
        self.password = data['password']


    @classmethod
    def guardar(cls, formulario):
        #formulario = {"first_name":"Juana", "last_name":"De Arco", "email":"juana@cd.com"}
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s )" 
        #->INSERT INTO users(first_name, last_name, email) VALUES('Juana', 'De Arco', 'juana@codingdojo.com')
        result = connectToMySQL('esquema_usuarios_ch').query_db(query, formulario)
        return result


#usuarios index.html
    @classmethod
    def muestra_usuarios(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('esquema_usuarios_ch').query_db(query)
        #[
            #{"id": "1", "first_name":"Elena", "last_name":"De Troya"..},
            #{"id": "2", "first_name":"Juana", "last_name":"De Arco"...}
        #]
        users = []
        for u in results: #en u voy a estar guardando mi diccionario
            user = cls(u) #user = User(u) -> {"id": "1", "first_name":"Elena", "last_name":"De Troya"..}
            users.append(user)
        return users


    #para borrar usuario
    @classmethod
    def borrar(cls, formulario):
        #formulario = {"id":"1"}
        query = "DELETE FROM users WHERE id = %(id)s"
        result = connectToMySQL('esquema_usuarios_ch').query_db(query, formulario)
        return result



    @classmethod
    def mostrar(cls, formulario):
        #formulario = {"id": "1"}
        query = "SELECT * FROM users WHERE id = %(id)s" #obtenemos el usuario con todas sus columnas / select siempre regresa una lista
        result = connectToMySQL('esquema_usuarios_ch').query_db(query, formulario) #result es una lista
        #result = (lista con 1 diccionario)[
            #{"id": "1", "first_name":"Elena".....}
        #]
        diccionario = result[0] #diccionario = {"id":"1"} / guardamos en el diccionario en la lista
        usuario = cls(diccionario) #usuario = User(diccionario)
        return usuario


    #funcion para update
    @classmethod
    def actualizar(cls, formulario):
        #recibimos formulario q será igual a... formulario = {"id":"1", "first_name":"Elena".....}
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id=%(id)s"
        result = connectToMySQL('esquema_usuarios_ch').query_db(query, formulario)
        return result


    #validar usuario (se usa metodo estatico)
    @staticmethod
    def valida_usuario(formulario): #se quiere recibir un diccionario con lo q se quiere validar (formulario se puede cambiar
    #x ej, se puede poner "usuario" solo fijarse de poner la misma palabra abajo en los if len(aqui[]) o sea, dentro de method debe llamarse igual)
        is_valid = True #asumimos q todo en el usuario está correcto / is_valid es una variable q se puede llamar como uno quiera
        if len(formulario['first_name']) < 3:
            flash('Nombre debe tener al menos 3 caracteres', 'registro') #primer texto es el mensaje, 'registro' es una 
            #etiqueta, si estamos validado mas de un dato, se deben poner diferentes etiquetas, con el texto q uno quiera
            is_valid = False

        if len(formulario['last_name']) < 3:
            flash('Apellido debe de tener al menos 3 caracteres', 'registro')
            is_valid = False

        if len(formulario['password']) < 6:
            flash('Contraseña debe de tener al menos 6 caracteres', 'registro')
            is_valid = False


        #Verificamos con expresiones regulares q nuestro correo tenga el formato correcto
        if not EMAIL_REGEX.match(formulario['email']): #este email, debe ser igual al name q tenemos en el formulario
            flash('Email invalido', 'registro') #Esta es el mensaje q se va a desplegar x lo q se puede cambiar
            is_valid = False

        #Consultar si ya existe ese correo electronico
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('esquema_usuarios_ch').query_db(query, formulario)
        if len(results) >= 1: #Si existe algun registro con ese correo, este "results" debe coincidir con el de la linea de arriba
            flash('Email registrado previamente', 'registro') #mensaje
            is_valid = False

        return is_valid

