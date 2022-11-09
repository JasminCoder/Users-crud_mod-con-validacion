#Importar flask
from flask import Flask

#inicializar app
app = Flask(__name__)

#declarar llave secreta / el texto amarillo se puede cambiar x lo q uno quiera
app.secret_key = "Esta es mi llave secreta ;)"
