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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senai%40134@127.0.0.1/db_carro'



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
        # retorna tudo na estrutura de colunas
    carro_selecionado = Carros.query.all()

        # por isso precisa ser convertido   
    carro_json = [
        # esse 'to_json' é a função que definimos dentro da classe previamente
        carro.to_json()
        for carro in carro_selecionado           
    ]

    # não precisa do make_response
        # status, 'nome do conteúdo', 'conteudo'
    return gera_resposta(200, "carros", carro_json)



# Respostas padrão
    # status (http) 200 = deu certo; 
    # nome do conteúdo
    # conteudo
    # mensagem (opcional)

def gera_resposta(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
    if (mensagem):
        body['mensagem'] = mensagem

    return Response(json.dumps(body), status=status, mimetype='application/json')
# Dumps - Converte o Dict (body) em Json(json.dumps)



# --------------------------------------------
# execução
    # debug é para não bloquear, pois sem ele acha que está no modo produção
app.run(port=5000, host='localhost', debug=True)