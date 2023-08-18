from crypt import methods
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect
from flask_login import (current_user, LoginManager,
                             login_user, logout_user,
                             login_required)
from datetime import datetime
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testuser:toledo22@localhost:3306/Offer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = 'HelloWorld'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column ('usu_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(45))
    nome = db.Column ('nome', db.String(100))
    email = db.Column ('email', db.String(100))
    senha = db.Column ('senha', db.String(256))
    telefone = db.Column ('telefone', db.String(20))
    rua =  db.Column ('rua', db.String(150))
    numero = db.Column ('numero', db.String(10))
    bairro = db.Column ('bairro', db.String(45))
    cidade = db.Column ('cidade', db.String(45))
    estado = db.Column ('estado', db.String(45))
    cep = db.Column ('cep', db.String(10))

    favoritos = db.relationship("Favorito", back_populates="usuario")

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

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Cartao(db.Model):
    __tablename__ = "cartao"
    id = db.Column ('cartao_id', db.Integer, primary_key=True)
    num_cartao = db.Column('num_cartao', db.String(20))
    nome_cartao = db.Column ('_nome_cartao', db.String(45))
    month = db.Column ('month', db.String(2))
    year = db.Column ('year', db.String(4))
    cvc = db.Column ('cvc', db.String(3))
    usuario_id = db.Column('usu_id', db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, num_cartao, nome_cartao, month, year, cvc, usuario_id):
        self.num_cartao = num_cartao
        self.nome_cartao = nome_cartao
        self.month = month
        self.year = year
        self.cvc = cvc
        self.usuario_id = usuario_id

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(150))
    desc = db.Column('cat_desc', db.String(150))

    produto = db.relationship("Produto", back_populates="categoria")

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

    favoritos = db.relationship("Favorito", back_populates="produto")
    categoria = db.relationship('Categoria', foreign_keys=[cat_id], backref=db.backref('produtos', lazy=True))
    usuario = db.relationship('Usuario', foreign_keys=[usu_id], backref=db.backref('produtos', lazy=True))


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

class Favorito(db.Model):
    __tablename__ = "favorito"
    id = db.Column('fav_id', db.Integer, primary_key=True)
    usuario_id = db.Column('usu_id', db.Integer, db.ForeignKey("usuario.usu_id"))
    produto_id = db.Column('anu_id', db.Integer, db.ForeignKey("produto.anu_id"))

    usuario = db.relationship("Usuario", back_populates="favoritos")
    produto = db.relationship("Produto", back_populates="favoritos")

    def __init__(self, usuario_id, produto_id):
        self.usuario_id = usuario_id
        self.produto_id = produto_id

class Compra(db.Model):
    __tablename__ = "compra"
    id = db.Column('compra_id', db.Integer, primary_key=True)
    produto_id = db.Column('anu_id', db.Integer, db.ForeignKey("produto.anu_id"))
    vendedor_id = db.Column('vendedor_id', db.Integer, db.ForeignKey("usuario.usu_id"))
    comprador_id = db.Column('comprador_id', db.Integer, db.ForeignKey("usuario.usu_id"))
    cartao_id = db.Column('cartao_id', db.Integer, db.ForeignKey("cartao.cartao_id"))
    quantidade = db.Column('quantidade', db.Integer)
    data_hora = db.Column('data_hora', db.DateTime)

    produto = db.relationship("Produto")
    vendedor = db.relationship("Usuario", foreign_keys=[vendedor_id])
    comprador = db.relationship("Usuario", foreign_keys=[comprador_id])
    cartao = db.relationship("Cartao")

    def __init__(self, produto_id, vendedor_id, comprador_id, cartao_id, quantidade):
        self.produto_id = produto_id
        self.vendedor_id = vendedor_id
        self.comprador_id = comprador_id
        self.cartao_id = cartao_id
        self.quantidade = quantidade
        self.data_hora = datetime.now()

class Pergunta(db.Model):
    __tablename__ = "pergunta"
    id = db.Column('pergunta_id', db.Integer, primary_key=True)
    produto_id = db.Column('produto_id', db.Integer, db.ForeignKey("produto.anu_id"))
    texto = db.Column('texto', db.String(500))
    
    resposta = db.relationship("Resposta", uselist=False, back_populates="pergunta")

    def __init__(self, produto_id, texto):
        self.produto_id = produto_id
        self.texto = texto

class Resposta(db.Model):
    __tablename__ = "resposta"
    id = db.Column('resposta_id', db.Integer, primary_key=True)
    pergunta_id = db.Column('pergunta_id', db.Integer, db.ForeignKey("pergunta.pergunta_id"))
    texto = db.Column('texto', db.String(500))

    pergunta = db.relationship("Pergunta", back_populates="resposta")

    def __init__(self, pergunta_id, texto):
        self.pergunta_id = pergunta_id
        self.texto = texto

@app.errorhandler(404)
def pagnaoencontrada(error):
    return render_template('pagnaoencontrada.html')

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        passwd = hashlib.sha512(str(request.form.get('passwd')).encode("utf-8")).hexdigest()
        user = Usuario.query.filter_by(email=email, senha=passwd).first()

        if user:
            login_user(user)
            return redirect(url_for('central'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/central")
@login_required
def central():
    return render_template('central_usuario.html', titulo="Minha Conta")

@app.route("/usuario")
def usuario():
    return render_template('usuario.html', usuarios = Usuario.query.all(), titulo="Usuário")

@app.route("/usuario/gerenciar")
@login_required
def gerenciaruser():    
    usuario = current_user
    return render_template('gerenciaruser.html', usuario=usuario, titulo="Usuário")

@app.route("/usuario/criar", methods=['POST'])
def criarusuario():
    hash = hashlib.sha512(str(request.form.get('passwd')).encode("utf-8")).hexdigest()
    usuario = Usuario(request.form.get('user'), request.form.get('nome'), request.form.get('email'), hash, request.form.get('telefone'), request.form.get('rua'), request.form.get('numero'), request.form.get('bairro'), request.form.get('cidade'), request.form.get('estado'), request.form.get('cep'))
    db.session.add(usuario)
    db.session.commit()                  
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhar/<int:id>")
@login_required
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
@login_required
def editarusuario(id):
    if request.method == 'POST':
        usuario.username = request.form.get('user')
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.senha = hash = hashlib.sha512(str(request.form.get('passwd')).encode("utf-8")).hexdigest()
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
@login_required
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))     

@app.route("/relatorios/vendas")
@login_required
def relvendas():
    usuario_id = current_user.id
    vendas = Compra.query.filter_by(vendedor_id=usuario_id).all()
    return render_template('relvendas.html', vendas=vendas, titulo="Relatório de Vendas")

@app.route("/relatorios/compras")
@login_required
def relcompras():
    usuario_id = current_user.id
    compras = Compra.query.filter_by(comprador_id=usuario_id).all()
    return render_template('relcompras.html', compras=compras, titulo="Relatório de Compras")

@app.route("/cartao")
@login_required
def cartao():
    usuario_id = current_user.id
    cartoes = Cartao.query.filter_by(usuario_id=usuario_id).all()
    return render_template('cartao.html', cartoes = cartoes, titulo="Cartão de Crédito")

@app.route("/cartao/criar", methods=['POST'])
@login_required
def novocartao():
    usuario_id = current_user.id
    cartao = Cartao(request.form.get('num_cartao'), request.form.get('nome_cartao'), request.form.get('month'), request.form.get('year'), request.form.get('cvc'), usuario_id=usuario_id)
    db.session.add(cartao)
    db.session.commit()                  
    return redirect(url_for('cartao'))

@app.route("/cartao/detalhar/<int:id>")
@login_required
def buscarcartao(id):
    cartao = Cartao.query.get(id)
    return cartao.num_cartao

@app.route("/cartao/editar/<int:id>", methods=['GET','POST'])
@login_required
def editarcartao(id):
    cartao = Cartao.query.get(id)
    if request.method == 'POST':
        usuario_id = current_user.id
        cartao.num_cartao = request.form.get('num_cartao')
        cartao.nome_cartao = request.form.get('nome_cartao')
        cartao.month = request.form.get('month')
        cartao.year = request.form.get('year')
        cartao.cvc = request.form.get('cvc')
        cartao.usuario_id = usuario_id
        db.session.add(cartao)
        db.session.commit()
        return redirect(url_for('cartao'))
    return render_template('ecartao.html', cartao = cartao, titulo="Cartao")

@app.route("/cartao/deletar/<int:id>")
@login_required
def deletarcartao(id):
    cartao = Cartao.query.get(id)
    db.session.delete(cartao)
    db.session.commit()
    return redirect(url_for('cartao'))     

@app.route("/categoria")
@login_required
def categoria():
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo='Categoria')

@app.route("/categoria/criar", methods=['POST'])
@login_required
def criarcategoria():
    categoria = Categoria(request.form.get('nome'), request.form.get('desc'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/categoria/detalhar/<int:id>")
@login_required
def buscarcategoria(id):
    categoria = Categoria.query.get(id)
    return categoria.nome

@app.route("/categoria/editar/<int:id>", methods=['GET','POST'])
@login_required
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
@login_required
def deletarcategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))     

@app.route("/produtos")
@login_required
def produto():
    usu_id = current_user.id
    produtos = Produto.query.filter_by(usu_id=usu_id).all()
    return render_template('produtos.html', produtos = produtos, categorias = Categoria.query.all(), titulo="Produtos")

@app.route("/produtos/criar", methods=['POST'])
@login_required
def criarproduto():
    usuario_id = current_user.id
    produto = Produto(request.form.get('nome'), request.form.get('desc'), request.form.get('espec'), request.form.get('marca'), request.form.get('modelo'), request.form.get('qtd'),request.form.get('preco'),request.form.get('cat'),usu_id=usuario_id)
    db.session.add(produto)
    db.session.commit()
    return redirect(url_for('produto'))

@app.route("/produtos/detalhar/<int:id>")
@login_required
def buscarproduto(id):
    produto = Produto.query.get(id)
    return Produto.nome

@app.route("/produtos/editar/<int:id>", methods=['GET','POST'])
@login_required
def editarproduto(id):
    produto = Produto.query.get(id)
    if request.method == 'POST':
        usuario_id = current_user.id
        produto.prod_nome = request.form.get('nome')
        produto.prod_desc = request.form.get('desc')
        produto.prod_espec = request.form.get('espec')
        produto.prod_marca = request.form.get('marca')
        produto.prod_modelo = request.form.get('modelo')
        produto.prod_qtd = request.form.get('qtd')
        produto.prod_preco = request.form.get('preco')
        produto.cat_id = request.form.get('cat')
        produto.usu_id = usuario_id
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('produto'))
    return render_template('eprodutos.html', categorias = Categoria.query.all(), usuarios = Usuario.query.all(), produto = produto, titulo="Produto")

@app.route("/produtos/deletar/<int:id>")
@login_required
def deletarproduto(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('produto'))

@app.route("/produtos/Comprar")
def produtos_anunciados():
    return render_template('produtos_anunciados.html', produtos = Produto.query.all(), categorias = Categoria.query.all(), usuarios = Usuario.query.all(), titulo="Produtos")

@app.route("/produtos/favoritos")
@login_required
def favoritos():
    usuario_id = current_user.id
    favoritos = Favorito.query.filter_by(usuario_id=usuario_id).all()
    return render_template('favoritos.html', favoritos=favoritos, titulo="Produtos Favoritados")

@app.route("/favoritar/<int:id>", methods=['POST'])
@login_required
def favoritar(id):
    usuario_id = current_user.id
    favorito_existente = Favorito.query.filter_by(usuario_id=usuario_id, produto_id=id).first()
    if favorito_existente:
        print("Este produto já foi favoritado por você.")
    else:
        favorito = Favorito(usuario_id=usuario_id, produto_id=id)
        db.session.add(favorito)
        db.session.commit()
    return redirect(url_for('produtos_anunciados'))

@app.route("/remover_favorito/<int:id>", methods=['POST'])
@login_required
def remover_favorito(id):
    usuario_id = current_user.id
    favorito = Favorito.query.filter_by(usuario_id=usuario_id, produto_id=id).first()
    if favorito:
        db.session.delete(favorito)
        db.session.commit()
    return redirect(url_for('favoritos'))

@app.route("/escolher_compra/<int:produto_id>", methods=['GET', 'POST'])
@login_required
def escolher_compra(produto_id):
    produto = Produto.query.get(produto_id)
    if request.method == 'POST':
        quantidade = int(request.form.get('quantidade'))
        cartao_id = request.form.get('cartao_id')
        comprador_id = current_user.id
        vendedor_id = produto.usu_id
        compra = Compra(produto_id=produto_id, vendedor_id=vendedor_id, comprador_id=comprador_id, cartao_id=cartao_id, quantidade=quantidade)
        db.session.add(compra)
        db.session.commit()
        return redirect (url_for('produtos_anunciados'))
    return render_template('escolher_compra.html', produto=produto, cartoes=Cartao.query.filter_by(usuario_id=current_user.id).all())

@app.route("/realizar_pergunta/<int:produto_id>", methods=['GET', 'POST'])
def realizar_pergunta(produto_id):
    produto = Produto.query.get(produto_id)
    if request.method == 'POST':
        texto_pergunta = request.form.get('texto_pergunta')
        pergunta = Pergunta(produto_id=produto_id, texto=texto_pergunta)
        db.session.add(pergunta)
        db.session.commit()
    perguntas = Pergunta.query.filter_by(produto_id=produto_id).all()
    return render_template('perguntas.html', produto=produto, perguntas=perguntas, titulo="Realizar Pergunta")

@app.route("/responder_perguntas/<int:produto_id>", methods=['GET', 'POST'])
@login_required
def responder_perguntas(produto_id):
    produto = Produto.query.get(produto_id)
    perguntas = Pergunta.query.filter_by(produto_id=produto_id).all()
    if request.method == 'POST':
        pergunta_id = int(request.form.get('pergunta_id'))
        texto_resposta = request.form.get('texto_resposta')
        resposta = Resposta(pergunta_id=pergunta_id, texto=texto_resposta)
        db.session.add(resposta)
        db.session.commit()
    return render_template('respostas.html', produto=produto, perguntas=perguntas, titulo="Responder Perguntas")

@app.route("/sobre")
def sobre():
    return render_template('sobre.html', titulo="Sobre Nós")

@app.route("/contato")
def contato():
    return render_template('contato.html', titulo="Contato")

if __name__ == 'Offer':
   with app.app_context():
        db.create_all()