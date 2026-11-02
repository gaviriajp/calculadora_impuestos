import sys
import os

sys.path.append("src")

from flask import Flask
from view.web import vista_calculos

# Constructor de Flask
app = Flask(__name__)

# Registrar el Blueprint para la vista web MVC
app.register_blueprint(vista_calculos.vista)

if __name__ == '__main__':
    # Permite ejecutar la aplicacion localmente
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=True)
