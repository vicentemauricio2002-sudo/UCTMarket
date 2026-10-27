from flask import Flask, jsonify

app = Flask(__name__)


# Esta es la ruta para el valor remoto que pide la evaluación
@app.route('/config_remota', methods=['GET'])
def get_config_remota():
  return jsonify(
      {'mensaje_bienvenida': 'Bienvenido a UCTMarket (Desde Servidor)'}
  )


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)