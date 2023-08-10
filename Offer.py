from crypt import methods
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testuser:toledo22@localhost:3306/Offer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column ('usu_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(45))
    nome = db.Column ('_nome', db.String(100))
    email = db.Column ('email', db.String(100))
    senha = db.Column ('senha', db.String(25))
    telefone = db.Column ('telefone', db.String(20))
    rua =  db.Column ('rua', db.String(150))
    numero = db.Column ('numero', db.String(10))
    bairro = db.Column ('bairro', db.String(45))
    cidade = db.Column ('cidade', db.String(45))
    estado = db.Column ('estado', db.String(45))
    cep = db.Column ('cep', db.String(10))

    def __init__(self, username, nome, email, senha, telefone, rua, numero, bairro, cidade, estado, cep):
        self.username = username
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep

class Cartao(db.Model):
    __tablename__ = "cartao"
    id = db.Column ('cartao_id', db.Integer, primary_key=True)
    num_cartao = db.Column('num_cartao', db.String(20))
    nome_cartao = db.Column ('_nome_cartao', db.String(45))
    month = db.Column ('month', db.String(2))
    year = db.Column ('year', db.String(4))
    cvc = db.Column ('cvc', db.String(3))

    def __init__(self, num_cartao, nome_cartao, month, year, cvc):
        self.num_cartao = num_cartao
        self.nome_cartao = nome_cartao
        self.month = month
        self.year = year
        self.cvc = cvc

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(150))
    desc = db.Column('cat_desc', db.String(150))

    def __init__ (self, nome, desc):
        self.nome = nome
        self.desc = desc

class Produto(db.Model):
    __tablename__ = "produto"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    prod_nome = db.Column('prod_nome', db.String(45))
    prod_desc = db.Column('prod_desc', db.String(250))
    prod_espec = db.Column('prod_espec', db.String(250))
    prod_marca = db.Column('prod_marca', db.String(45))
    prod_modelo = db.Column('prod_modelo', db.String(45))
    prod_qtd = db.Column('prod_qtd', db.String(45))
    prod_preco = db.Column('prod_preco', db.String(45))
    cat_id = db.Column('cat_id', db.Integer, db.ForeignKey("categoria.cat_id"))
    usu_id = db.Column('usu_id', db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, prod_nome, prod_desc, prod_espec, prod_marca, prod_modelo, prod_qtd, prod_preco, cat_id, usu_id):
        self.prod_nome = prod_nome
        self.prod_desc = prod_desc
        self.prod_espec = prod_espec
        self.prod_marca = prod_marca
        self.prod_modelo = prod_modelo
        self.prod_qtd = prod_qtd
        self.prod_preco = prod_preco
        self.cat_id = cat_id
        self.usu_id = usu_id

@app.errorhandler(404)
def pagnaoencontrada(error):
    return render_template('pagnaoencontrada.html')

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/central")
def central():
    return render_template('central_usuario.html', titulo="Minha Conta")

@app.route("/usuario")
def usuario():
    return render_template('usuario.html',  usuarios = Usuario.query.all(), titulo="Usuário")

@app.route("/usuario/criar", methods=['POST'])
def criarusuario():
    usuario = Usuario(request.form.get('user'), request.form.get('nome'), request.form.get('email'), request.form.get('passwd'), request.form.get('telefone'), request.form.get('rua'), request.form.get('numero'), request.form.get('bairro'), request.form.get('cidade'), request.form.get('estado'), request.form.get('cep'))
    db.session.add(usuario)
    db.session.commit()                  
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.username = request.form.get('user')
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.senha = request.form.get('passwd')
        usuario.rua = request.form.get('rua')
        usuario.numero = request.form.get('numero')
        usuario.bairro = request.form.get('bairro')
        usuario.cidade = request.form.get('cidade')
        usuario.estado = request.form.get('estado')
        usuario.cep = request.form.get('cep')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario'))
    return render_template('eusuario.html', usuario = usuario, titulo="Usuario")

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))     

@app.route("/relatorios/vendas")
def relvendas():
    return render_template('relvendas.html', titulo="Vendas")

@app.route("/relatorios/compras")
def relcompras():
    return render_template('relcompras.html', titulo="Compras")

@app.route("/cartao")
def cartao():
    return render_template('cartao.html', cartoes = Cartao.query.all(), titulo="Cartão de Crédito")

@app.route("/cartao/criar", methods=['POST'])
def novocartao():
    cartao = Cartao(request.form.get('num_cartao'), request.form.get('nome_cartao'), request.form.get('month'), request.form.get('year'), request.form.get('cvc'))
    db.session.add(cartao)
    db.session.commit()                  
    return redirect(url_for('cartao'))

@app.route("/cartao/detalhar/<int:id>")
def buscarcartao(id):
    cartao = Cartao.query.get(id)
    return cartao.num_cartao

@app.route("/cartao/editar/<int:id>", methods=['GET','POST'])
def editarcartao(id):
    cartao = Cartao.query.get(id)
    if request.method == 'POST':
        cartao.num_cartao = request.form.get('num_cartao')
        cartao.nome_cartao = request.form.get('nome_cartao')
        cartao.month = request.form.get('month')
        cartao.year = request.form.get('year')
        cartao.cvc = request.form.get('cvc')
        db.session.add(cartao)
        db.session.commit()
        return redirect(url_for('cartao'))
    return render_template('ecartao.html', cartao = cartao, titulo="Cartao")

@app.route("/cartao/deletar/<int:id>")
def deletarcartao(id):
    cartao = Cartao.query.get(id)
    db.session.delete(cartao)
    db.session.commit()
    return redirect(url_for('cartao'))     

@app.route("/categoria")
def categoria():
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo='Categoria')

@app.route("/categoria/criar", methods=['POST'])
def criarcategoria():
    categoria = Categoria(request.form.get('nome'), request.form.get('desc'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/categoria/detalhar/<int:id>")
def buscarcategoria(id):
    categoria = Categoria.query.get(id)
    return categoria.nome

@app.route("/categoria/editar/<int:id>", methods=['GET','POST'])
def editarcategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.nome = request.form.get('nome')
        categoria.desc = request.form.get('desc')
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('categoria'))
    return render_template('ecategoria.html', categoria = categoria, titulo="Categoria")

@app.route("/categoria/deletar/<int:id>")
def deletarcategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))     

@app.route("/produtos")
def produto():
    return render_template('produtos.html', produtos = Produto.query.all(), categorias = Categoria.query.all(), usuarios = Usuario.query.all(), titulo="Produtos")

@app.route("/produtos/criar", methods=['POST'])
def criarproduto():
    produto = Produto(request.form.get('nome'), request.form.get('desc'), request.form.get('espec'), request.form.get('marca'), request.form.get('modelo'), request.form.get('qtd'),request.form.get('preco'),request.form.get('cat'),request.form.get('usu'))
    db.session.add(produto)
    db.session.commit()
    return redirect(url_for('produto'))

@app.route("/produtos/detalhar/<int:id>")
def buscarproduto(id):
    produto = Produto.query.get(id)
    return Produto.nome

@app.route("/produtos/editar/<int:id>", methods=['GET','POST'])
def editarproduto(id):
    produto = Produto.query.get(id)
    if request.method == 'POST':
        produto.prod_nome = request.form.get('nome')
        produto.prod_desc = request.form.get('desc')
        produto.prod_espec = request.form.get('espec')
        produto.prod_marca = request.form.get('marca')
        produto.prod_modelo = request.form.get('modelo')
        produto.prod_qtd = request.form.get('qtd')
        produto.prod_preco = request.form.get('preco')
        produto.cat_id = request.form.get('cat')
        produto.usu_id = request.form.get('usu')
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('produto'))
    return render_template('eprodutos.html', categorias = Categoria.query.all(), usuarios = Usuario.query.all(), produto = produto, titulo="Produto")

@app.route("/produtos/deletar/<int:id>")
def deletarproduto(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('produto'))     

@app.route("/prod/perguntas")
def perguntas():
    return render_template('perguntas.html')

@app.route("/prod/favoritos")
def favoritos():
    return f"<h4>Favorito Adicionado com Sucesso</h4>"

@app.route("/prod/comprar")
def comprar():
    return f"<h4>Compra Realizada com Sucesso</h4>"

@app.route("/sobre")
def sobre():
    return render_template('sobre.html', titulo="Sobre Nós")

@app.route("/contato")
def contato():
    return render_template('contato.html', titulo="Contatos")

if __name__ == 'Offer':
   with app.app_context():
        db.create_all()