from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask('clientes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senai%40134@127.0.0.1/db_clinicavetdbd'

db = SQLAlchemy(app)

class Clientes (db.Model):
    __tablename__ = 'tb_clientes',
    id_cliente = db.Column(db.Integer, primary_key = True),
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
    
# CRUD = Create Read Update Delete

# --------------------------------------
# Method 1: GET (Read)
@app.route('/clientes', methods=['GET'])



# --------------------------------------
# Method 1.1: GET Filtro (Read)
@app.route('/clientes', methods=['GET'])



# ---------------------------------------
# Method 1: POST (Create)
@app.route('/clientes', methods=['POST'])
           


# --------------------------------------
# Method 1: PUT (Update)
@app.route('/clientes', methods=['PUT'])
           


# -----------------------------------------
# Method 1: DELETE (Delete)
@app.route('/clientes', methods=['DELETE'])



# -----------------------------------------
# Executar API
@app.run(port=5000, host='localhost', debug=True)