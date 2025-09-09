# pip install flask
from flask import Flask, request, make_response, jsonify

# make_response, é para fzr resposta n ser só um código
# jsonify é para estruturar mensagem em JSON

from bd import Carros

# armazenar caminho em variável

# esse modulo flask vai subir nossa API localmente
# vamos instanciar o modulo Flask na Var 'app'
app = Flask('carros')



#  Method 1 - View data (GET)
# 1 - Oq esse Method vai fzr?
# 2 - Onde ele vai fazer?

# Onde vai fzr
@app.route('/car', methods=['GET'])

# Oq esse Method vai fzr
def get_carros():
    return Carros




# Method 1.1 - View data by ID (GET)
    # tem q passar o 'caminho_padrao/tipo_dados:nome_coluna'
@app.route('/car/<int:p_id>', methods=['GET'])
def get_carros_id(p_id):
    for carro in Carros:
        if carro.get('id') == p_id:
            return jsonify(carro)
            



# Method 2 - Create new Registers (Post)
# Verificar dados que estão passados na REQUEST e armazenar na base
@app.route('/car', methods=['POST'])
def criar_carro():
    car = request.json
    Carros.append(car)

    # forma simples
    # return car

    # forma ideal
    return make_response(
        jsonify(
            mensagem = 'Carro cadastrado com sucesso!',
            carrinho = car
        )
    )



# Method 3 - Deletar registros (DELETE)
@app.route('/car/<int:id>', methods=['DELETE'])
def excluir_carro(id):
    # enumerate é para: percorrer e armazenar essas infos específicas
    for indice, carro in enumerate(Carros):
        if carro.get('id') == id:
            del Carros[indice]
            return jsonify(
                {'mensagem': 'Carro excluído'}
            )
        




# Method 4 - Editar registros (PUT)
@app.route('/car/<int:id>', methods=['PUT'])
def editar_carro(id):
    carro_alterado = request.get_json()
    for indice, carro in enumerate(Carros):
        if carro.get('id') == id:
            Carros[indice].update(carro_alterado)
            return jsonify(
                Carros[indice]
            )




# Ao final, executar
# # as vezes assim já funciona   
# app.run()
app.run(port=5000, host='localhost', debug=True)


# o link LOCALHOST, só funciona aq
# http://localhost:5000/car