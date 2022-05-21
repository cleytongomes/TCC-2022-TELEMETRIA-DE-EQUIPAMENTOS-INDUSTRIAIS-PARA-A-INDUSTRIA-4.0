from flask import Flask, request, jsonify
from flask_cors import CORS
from conector import ConectorBd

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'API de monitoramento de máquinas'

@app.route('/maquinas', methods=['GET'])
def maquinas():
    bd = ConectorBd()
    maquinas = bd.obter_maquinas()
    return jsonify(maquinas)

@app.route('/estados_maquinas', methods=['GET'])
def estados_maquinas():
    bd = ConectorBd()
    maquinas = bd.obter_estados()
    return jsonify(maquinas)

@app.route('/maquina/<cod_maquina>', methods=['GET'])
def maquina(cod_maquina):
    bd = ConectorBd()
    relacao_estado_tempo = bd.obter_tempo_por_estado(cod_maquina)
    return jsonify(relacao_estado_tempo)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
