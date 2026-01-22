from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'clave_secreta_maqueta_las_vegas' 
CORS(app)

# --- BASE DE DATOS TEMPORAL EN MEMORIA ---
# Esta variable guardará lo que mande el Arduino
estados_globales = { 
    "p2": 0, "p3": 0, "p4": 0, "p5": 0, "p6": 0, "p7": 0 
}

# --- CONFIGURACIÓN DE LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users_db = {
    "admin@parking.com": {
        "password": generate_password_hash("1234"), 
        "nombre": "Administrador"
    },
    "invitado@parking.com": {
        "password": generate_password_hash("abcd"), 
        "nombre": "Invitado"
    }
}

class User(UserMixin):
    def __init__(self, email):
        self.id = email
        self.nombre = users_db[email]['nombre']

@login_manager.user_loader
def load_user(user_id):
    if user_id not in users_db:
        return None
    return User(user_id)

# --- RUTAS DE NAVEGACIÓN ---

@app.route('/')
def home():
    # Si ya está logueado, va al parking. Si no, al login.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/parking')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_data = users_db.get(email)
        
        if user_data and check_password_hash(user_data['password'], password):
            user = User(email)
            login_user(user, remember=True)
            return redirect(url_for('index'))
        else:
            flash('Acceso denegado')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- RUTAS DE DATOS (ESTO ES LO QUE ARREGLA EL ARDUINO) ---

@app.route('/update', methods=['POST'])
def update():
    """ RUTA PARA EL ARDUINO: Aquí recibe los datos del ESP32 """
    global estados_globales
    try:
        # Obtenemos el JSON que envía el Arduino
        nuevos_datos = request.get_json()
        if nuevos_datos:
            # Actualizamos nuestra "base de datos" con lo que mandó el sensor
            estados_globales.update(nuevos_datos)
            return jsonify({"mensaje": "Datos actualizados"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/status')
def status():
    """ RUTA PARA LA WEB: El index.html lee esta ruta cada 2 segundos """
    return jsonify(estados_globales)

if __name__ == '__main__':
    app.run(debug=True)
