from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

# Estado inicial: -1 (Amarillo/ERR) hasta que el Arduino mande datos
estado_parking = [-1] * 6 

@app.route('/')
def index():
    plazas_info = []
    # Generamos los 3 grupos (1, 2, 3)
    for g in range(1, 4):
        # Para cada grupo, generamos 2 plazas (1 y 2)
        for p in range(1, 3):
            # La segunda plaza de cada grupo es la adaptada
            es_adaptada = (p == 2)
            
            plazas_info.append({
                'nombre_grupo': f"GRUPO {g}",
                'nombre_plaza': f"Plaza {p}",
                'tipo': "PLAZA ADAPTADA" if es_adaptada else ""
            })
    
    return render_template('index.html', plazas_info=plazas_info)

@app.route('/update')
def update():
    global estado_parking
    try:
        # Recibe p2, p3, p4, p5, p6, p7 desde Arduino
        for i in range(6):
            valor = request.args.get(f'p{i+2}')
            if valor is not None:
                estado_parking[i] = int(valor)
        return "OK", 200
    except Exception as e:
        return str(e), 400

@app.route('/api/estado')
def get_estado():
    return jsonify({'estados': estado_parking})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
