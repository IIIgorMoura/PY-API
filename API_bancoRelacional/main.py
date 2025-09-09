# SQL_ALCHEMY
    # é o que permite a conexão da API com o BD
    # pip install flask_sqlalchemy

# FLASK - permite a criação de API com Python

# Response e Request -> Requisição
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask('carros')


# SQL_ALCHEMY cria e modifica td no DB
    # por isso vamos adicionar 'tracking' e revisão de alterações
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# URI] = 'siteDB://user:senha' // '%40' é o '@', pq o char @ é usado como declarador do IP
# 1: User - 2: Senha - 3: 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_carro'



# nome pode ser diferente
mybd = SQLAlchemy(app)

# Classe para definir modelo dos dados que correspondem a tabela do db
    # Em POO, class é o padrão/estrutura/template a ser seguido
    # Em POO, o objeto são os registros, os valores que serão criados, usando o class como molde
class Carros(mybd.Model):
    __tablename__ = 'tb_carro'
    id_carro = mybd.Column(mybd.Integer, primary_key=True)
    marca = mybd.Column(mybd.String(255))
    modelo = mybd.Column(mybd.String(255))
    ano = mybd.Column(mybd.String(255))
    cor = mybd.Column(mybd.String(255))
    valor = mybd.Column(mybd.String(255))
    numero_vendas = mybd.Column(mybd.String(255))

    # converter o objeto do carro em json, pois originalmente é em colunas
    def to_json(self):
        return {
            # o primeiro 'id_carro' tem que ser igual ao q está no DB, o do self é a variável previamente usada no programa
            "id_carro": self.id_carro,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "valor": float(self.valor),
            "numero_vendas": self.numero_vendas
        }
    


# --------------------------------------------

# Method 1 - GET
@app.route('/carros', methods=['GET'])
def seleciona_carro():
    # var para armazenar o que recebemos da API
    carro_selecionado = Carros.query.all()