from flask import Flask, render_template, jsonify, request
import os # Necesario para Render

app = Flask(__name__)

NUM_PLAZAS = 6
# Estado inicial: 1 para libre, 0 para ocupado (o viceversa según tu conexión)
estado_parking = [1] * NUM_PLAZAS 

# RUTA QUE RECIBE LOS DATOS DEL ARDUINO
@app.route('/update')
def update():
    global estado_parking
    try:
        # Recogemos los 6 datos (p2, p3, p4, p5, p6, p7) que envía el Arduino
        estado_parking[0] = int(request.args.get('p2', 1))
        estado_parking[1] = int(request.args.get('p3', 1))
        estado_parking[2] = int(request.args.get('p4', 1))
        estado_parking[3] = int(request.args.get('p5', 1))
        estado_parking[4] = int(request.args.get('p6', 1))
        estado_parking[5] = int(request.args.get('p7', 1))
        
        print(f"Estados actualizados: {estado_parking}")
        return "OK", 200
    except Exception as e:
        return str(e), 400

@app.route('/')
def index():
    plazas_info = []
    for i in range(NUM_PLAZAS):
        grupo_index = i // 2  
        plaza_en_grupo = (i % 2) + 1 
        info = {
            'nombre_grupo': f"GRUPO {grupo_index + 1}",
            'nombre_plaza': f"Plaza {plaza_en_grupo}",
            'tipo': "PLAZA ADAPTADA" if plaza_en_grupo == 2 else ""
        }
        plazas_info.append(info)
    return render_template('index.html', plazas_info=plazas_info)

@app.route('/api/estado')
def get_estado():
    return jsonify({'estados': estado_parking})

if __name__ == '__main__':
    # ESTO ES LO MÁS IMPORTANTE PARA RENDER:
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
