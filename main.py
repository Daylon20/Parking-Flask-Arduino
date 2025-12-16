from flask import Flask, render_template, jsonify, request # ¡IMPORTANTE! Importar 'request'
# Ya NO necesitamos serial, time, ni threading
# import serial
# import time
# import threading

# --- CONFIGURACIÓN DE PARKING ---
NUM_PLAZAS = 6     

# Estado inicial (Simulado en 0, 1, o -1 si está desconectado)
# Usaremos 1 para Ocupado (LOW del sensor) y 0 para Libre (HIGH del sensor)
estado_parking = [-1] * NUM_PLAZAS 
app = Flask(__name__)

# ===================================================
# 1. RUTA DE RECEPCIÓN (EL ARDUINO ENVÍA DATOS AQUÍ)
# ===================================================
# El Arduino enviará una solicitud POST a esta dirección, 
# conteniendo la variable 'data' con los estados (ej: data=101010)
@app.route('/api/update_data', methods=['POST'])
def actualizar_estado():
    global estado_parking
    
    # 1. Verificar y obtener los datos enviados por POST
    # Arduino envía los datos como "data=101010" en el cuerpo del POST
    if 'data' not in request.form:
        # Si el Arduino no envía el parámetro 'data', da un error 400
        return "Falta el parámetro 'data' en la petición POST.", 400

    estados_recibidos = request.form['data']
    
    # 2. Procesar y actualizar el estado
    if len(estados_recibidos) == NUM_PLAZAS:
        try:
            # Convierte la cadena recibida (ej: "101010") a una lista de enteros [1, 0, 1, 0, 1, 0]
            nuevos_estados = [int(c) for c in estados_recibidos]
            estado_parking = nuevos_estados
            
            # ¡Respuesta de Éxito! Envía 200 al Arduino para que no dé Timeout (-3)
            return "OK", 200
        except ValueError:
            return "Error de formato de datos (No son solo 0s y 1s)", 400
    
    return "Datos incompletos (Longitud incorrecta)", 400


# ===================================================
# 2. RUTA PRINCIPAL (CARGA LA PÁGINA WEB)
# ===================================================
@app.route('/')
def index():
    plazas_info = []
    
    for i in range(NUM_PLAZAS):
        grupo_index = i // 2  
        plaza_en_grupo = (i % 2) + 1 
        
        info = {
            'nombre_grupo': f"GRUPO {grupo_index + 1}",
            'nombre_plaza': f"Plaza {plaza_en_grupo}",
            'tipo': "" 
        }
        
        # Etiqueta para plazas adaptadas (la segunda de cada grupo)
        if plaza_en_grupo == 2:
            info['tipo'] = "PLAZA ADAPTADA"
            
        plazas_info.append(info)
            
    return render_template('index.html', plazas_info=plazas_info)

# ===================================================
# 3. RUTA DE LA API (ACTUALIZA LOS COLORES EN LA WEB)
# ===================================================
@app.route('/api/estado')
def get_estado():
    # Devuelve la lista del último estado de las 6 plazas a la web para que se actualice
    return jsonify({'estados': estado_parking})

# ===================================================
# INICIO DEL SERVIDOR
# ===================================================
if __name__ == '__main__':
    print("[*] Servidor web de recepción iniciado. Ejecutando en puerto 5001.")
    # Usamos host='0.0.0.0' para que sea accesible desde ngrok/LocalTunnel
    app.run(host='0.0.0.0', port=5001)