from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Diccionario inicial con todos los pines en 0 (Libre)
estados = {
    "p2": 0, "p3": 0,
    "p4": 0, "p5": 0,
    "p6": 0, "p7": 0
}

@app.route('/')
def index():
    return render_template('index.html')

# ESTA RUTA AHORA ACEPTA TODOS LOS PINES A LA VEZ
@app.route('/update', methods=['GET'])
def update():
    # Recoge todos los parámetros de la URL (?p2=1&p3=0...)
    parametros = request.args.to_dict()
    
    for pin, valor in parametros.items():
        if pin in estados:
            try:
                estados[pin] = int(valor)
            except:
                continue
    
    return "OK", 200

@app.route('/status')
def status():
    return jsonify(estados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
