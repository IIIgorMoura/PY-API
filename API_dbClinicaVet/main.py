from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask('ClinicaVetBD')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senai%40134@127.0.0.1/ClinicaVetBD'


db = SQLAlchemy(app)

class Clientes (db.Model):
    __tablename__ = 'tb_clientes'
    id_cliente = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(255))
    endereco = db.Column(db.String(255))
    telefone = db.Column(db.String(255))

    def to_json(self):
        return {
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "endereco": self.endereco,
            "telefone": self.telefone
        }
    


class Pets(db.Model):
    __tablename__ = 'tb_pets'

    id_pet = db.Column(db.Integer, primary_key=True) #, autoincrement=True
    nome = db.Column(db.String(255))
    tipo = db.Column(db.String(255))
    raca = db.Column(db.String(255))
    data_nascimento = db.Column(db.Date())
    id_clienteF = db.Column(db.Integer, db.ForeignKey('tb_clientes.id_cliente'), nullable=False)
    idade = db.Column(db.String(16))

    def to_json(self):
        return {
            "id_pet": self.id_pet,
            "nome": self.nome,
            "tipo": self.tipo,
            "raca": self.raca,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "id_cliente": self.id_clienteF,
            "idade": self.idade
        }

        
    
# CRUD = Create Read Update Delete


# função de API Feedback
def gera_resposta(status, conteudo, mensagem=False):
    body = {}
    body['Conteúdo'] = conteudo
    if (mensagem):
        body['Mensagem'] = mensagem

    return Response(json.dumps(body), status=status, mimetype='application/json')



# # --------------------------------------
# Method 1: GET (Read)
@app.route('/clientes', methods=['GET'])
def select_clientes():
    select_cliente = Clientes.query.all()

    cliente_json = [
        cliente.to_json()
        for cliente in select_cliente
    ]

    return gera_resposta(200, 'Clientes', cliente_json)

# //------------------//
@app.route('/pets', methods=['GET'])
def select_pets():
    select_pet = Pets.query.all()

    pet_json = [
        pet.to_json()
        for pet in select_pet
    ]

    return gera_resposta(200, 'Pets', pet_json)



# # --------------------------------------
# # Method 1.1: GET Filtro (Read)
@app.route('/clientes/<int:id_cliente_p>', methods=['GET'])
def select_clientes_filter(id_cliente_p):
    select_cliente_id = Clientes.query.filter_by(id_cliente=id_cliente_p).first()
    cliente_json = select_cliente_id.to_json()

    return gera_resposta(200, cliente_json)



# //------------------//
@app.route('/pets/<int:id_pet_p>', methods=['GET'])
def select_pets_filter(id_pet_p):
    select_pet_id = Pets.query.filter_by(id_pet=id_pet_p).first()
    pet_json = select_pet_id.to_json()

    return gera_resposta(200, pet_json)



# # ---------------------------------------
# Method 2: POST (Create)
@app.route('/clientes', methods=['POST'])
def cadastrar_cliente():
    requisicao = request.get_json()

    try:
        cliente = Clientes(
            id_cliente = requisicao['id_cliente'],
            nome = requisicao['nome'],
            endereco = requisicao['endereco'],
            telefone = requisicao['telefone']
        )

        db.session.add(cliente)
        db.session.commit()

        return gera_resposta(201, cliente.to_json(), 'Cliente cadastrado com sucesso!')

    except Exception as e:
        print('Erro ao tentar cadastrar o cliente: ', e)
        return gera_resposta(400, {}, 'Erro ao tentar cadastrar o cliente')
    


# //------------------//
@app.route('/pets', methods=['POST'])
def cadastrar_pet():
    requisicao = request.get_json()

    try:
        pet = Pets(
            # ' = requisicao[''],'
            id_pet = requisicao['id_pet'],
            nome = requisicao['nome'],
            tipo = requisicao['tipo'],
            raca = requisicao['raca'],
            data_nascimento = requisicao['data_nascimento'],
            id_clienteF = requisicao['id_cliente'],
            idade = requisicao['idade']
        )

        db.session.add(pet)
        db.session.commit()

        return gera_resposta(201, pet.to_json(), 'Pet cadastrado com sucesso!')

    except Exception as e:
        print('Erro ao tentar cadastrar o pet: ', e)
        return gera_resposta(400, {}, 'Erro ao tentar cadastrar o pet')



# # --------------------------------------
# Method 3: PUT (Update)
@app.route('/clientes/<id_cliente_p>', methods=['PUT'])
def update_cliente(id_cliente_p):
    select_cliente_id = Clientes.query.filter_by(id_cliente=id_cliente_p).first()
    requisicao = request.get_json()

    try:
        if ('nome' in requisicao):
            select_cliente_id.nome = requisicao['nome']
        if ('endereco' in requisicao):
            select_cliente_id.endereco = requisicao['endereco']
        if ('telefone' in requisicao):  
            select_cliente_id.telefone = requisicao['telefone']
    
        db.session.add(select_cliente_id)
        db.session.commit()

        return gera_resposta(200, select_cliente_id.to_json(), 'Dados do cliente atualizados!')
    
    except Exception as e:
        print('Err ao tentar atualizar: ', e)
        

# # -----------------------------------------
# Method 4: DELETE (Delete)
@app.route('/clientes/<id_cliente_p>', methods=['DELETE'])
def delete_cliente(id_cliente_p):
    select_cliente_id = Clientes.query.filter_by(id_cliente=id_cliente_p).first()

    try:
        db.session.delete(select_cliente_id)
        db.session.commit()
        return gera_resposta(200, select_cliente_id.to_json(), "Deletado com sucesso!")
    except Exception as e:
        print('Erro ao tentar deletar o cliente:', e)
        return gera_resposta(400, {}, "Erro ao tentar deletar!")


# -----------------------------------------
# Executar API
app.run(port=5000, host='localhost', debug=True)