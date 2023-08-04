from crypt import methods
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/usuario")
def usuario():
    return render_template('usuario.html')

@app.route("/usuario/cadastro")
def cadastro_user():
    return render_template('cadastro_user.html')

@app.route("/usuario/cadastro/caduser", methods=['POST'])
def caduser():
    return request.form

@app.route("/usuario/relvendas")
def relvendas():
    return render_template('relvendas.html')

@app.route("/usuario/relcompras")
def relcompras():
    return render_template('relcompras.html')

@app.route("/usuario/carteira")
def carteira():
    return render_template('carteira.html')

@app.route("/usuario/cartao/cadcartao", methods=['POST'])
def cadcartao():
    return request.form

@app.route("/produtos")
def produtos():
    return render_template('produtos.html')

@app.route("/produtos/cadastro")
def cadastro_prod():
    return render_template('cadastro_prod.html')

@app.route("/produtos/cadastro/cadprod", methods=['POST'])
def cadprod():
    return request.form

@app.route("/produtos/perguntas")
def perguntas():
    return render_template('perguntas.html')

@app.route("/produtos/catergoria")
def categoria():
    return render_template('categoria.html')

@app.route("/produtos/favoritos")
def favoritos():
    return f"<h4>Favorito Adicionado com Sucesso</h4>"

@app.route("/produtos/comprar")
def comprar():
    return f"<h4>Compra Realizada com Sucesso</h4>"

@app.route("/sobre")
def sobre():
    return render_template('sobre.html')

@app.route("/contato")
def contato():
    return render_template('contato.html')

@app.route("/contato/cadcont", methods=['POST'])
def cadcont():
    return request.form