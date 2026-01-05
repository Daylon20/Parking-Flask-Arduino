from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

NUM_PLAZAS = 6
# 1 = Libre, 0 = Ocupado
estado_parking = [1] * NUM_PLAZAS 

@app.route('/update')
def update():
    global estado_parking
    try:
        # Recogemos los datos del pin 2 al 7
        for i in range(NUM_PLAZAS):
            param = f'p{i+2}'
            valor = request.args.get(param)
            if valor is not None:
                estado_parking[i] = int(valor)
        return "OK", 200
    except Exception as e:
        return str(e), 400

@app.route('/')
def index():
    plazas_info = []
    for i in range(NUM_PLAZAS):
        grupo = i // 2 + 1
        plaza = (i % 2) + 1
        plazas_info.append({
            'nombre_grupo': f"GRUPO {grupo}",
            'nombre_plaza': f"Plaza {plaza}",
            'tipo': "PLAZA ADAPTADA" if plaza == 2 else ""
        })
    return render_template('index.html', plazas_info=plazas_info)

@app.route('/api/estado')
def get_estado():
    return jsonify({'estados': estado_parking})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
