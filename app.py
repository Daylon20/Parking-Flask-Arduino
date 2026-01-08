from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Diccionario para guardar el estado real de los sensores
# 0 = Libre, 1 = Ocupado
estados = {
    "p2": 0, "p3": 0,
    "p4": 0, "p5": 0,
    "p6": 0, "p7": 0
}

@app.route('/')
def index():
    return render_template('index.html')

# RUTA PARA EL ARDUINO: Recibe los datos y los guarda en el diccionario
@app.route('/update', methods=['GET'])
def update():
    pin = request.args.get('pin')
    estado = request.args.get('estado')
    
    if pin in estados:
        try:
            estados[pin] = int(estado)
            return "OK", 200
        except:
            return "Error de formato", 400
    return "Pin no encontrado", 404

# RUTA PARA LA WEB: Entrega los estados guardados en formato JSON
@app.route('/status')
def status():
    return jsonify(estados)

if __name__ == '__main__':
    # Usamos host 0.0.0.0 para que sea visible en la red del móvil
    app.run(host='0.0.0.0', port=5000)
