from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

# Estado inicial de las 6 plazas (1 = libre)
estado_parking = [1, 1, 1, 1, 1, 1]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update')
def update():
    global estado_parking
    for i in range(6):
        valor = request.args.get(f'p{i+2}')
        if valor is not None:
            estado_parking[i] = int(valor)
    return "OK"

@app.route('/api/estado')
def get_estado():
    return jsonify({'estados': estado_parking})

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=puerto)
