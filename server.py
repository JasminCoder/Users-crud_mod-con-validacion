#importacion flask_app
from flask_app import app

#importacion de controladores
from flask_app.controllers import users_controller

#Ejecucion de la app
if __name__=="__main__":
    app.run(debug=True)

