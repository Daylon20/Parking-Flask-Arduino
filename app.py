from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_la_maqueta' # Cambia esto por lo que quieras

# --- CONFIGURACIÓN DE LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Nombre de la función que renderiza el login

# --- BASE DE DATOS DE USUARIOS (Simulada para la Opción A) ---
# En una maqueta, podemos usar un diccionario. 
# Aquí puedes ver los correos y las contraseñas (hasheadas por seguridad).
users_db = {
    "admin@parking.com": {
        "password": generate_password_hash("1234"), 
        "nombre": "Administrador"
    },
    "invitado@test.com": {
        "password": generate_password_hash("abcd"), 
        "nombre": "Usuario Invitado"
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

# --- RUTAS DE CONTROL DE ACCESO ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        # Verificamos si el correo existe y la contraseña es correcta
        user_data = users_db.get(email)
        
        if user_data and check_password_hash(user_data['password'], password):
            user = User(email)
            # remember=True hace que no tengan que volver a iniciar sesión
            login_user(user, remember=remember)
            return redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- TU RUTA PRINCIPAL (PROTEGIDA) ---

@app.route('/')
@login_required  # Si no están logueados, los manda al login automáticamente
def index():
    return render_template('parking.html') # Este es tu HTML del parking

# Ruta para que tu JS siga funcionando
@app.route('/status')
@login_required
def status():
    # Aquí iría tu lógica actual de lectura de sensores/pines
    # Ejemplo de retorno:
    estados = { "p2":0, "p3":1, "p4":0, "p5":0, "p6":1, "p7":0 }
    return jsonify(estados)

if __name__ == '__main__':
    app.run(debug=True)
