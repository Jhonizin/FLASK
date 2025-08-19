from flask import Flask, render_template, request, redirect, url_for
from models import db, Usuario, Produto, Categoria, Pedido, ItemPedido, Pergunta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# ------------------ CRUD USUARIO ------------------
@app.route("/usuarios")
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/usuarios/novo", methods=["GET", "POST"])
def novo_usuario():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for("listar_usuarios"))
    return render_template("form_usuario.html")

@app.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    usuario = Usuario.query.get(id)
    if request.method == "POST":
        usuario.nome = request.form["nome"]
        usuario.email = request.form["email"]
        db.session.commit()
        return redirect(url_for("listar_usuarios"))
    return render_template("form_usuario.html", usuario=usuario)

@app.route("/usuarios/excluir/<int:id>")
def excluir_usuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for("listar_usuarios"))


@app.route("/produtos")
def listar_produtos():
    produtos = Produto.query.all()
    return render_template("produtos.html", produtos=produtos)

@app.route("/produtos/novo", methods=["GET", "POST"])
def novo_produto():
    if request.method == "POST":
        nome = request.form["nome"]
        preco = float(request.form["preco"])
        categoria_id = int(request.form["categoria_id"])
        produto = Produto(nome=nome, preco=preco, categoria_id=categoria_id)
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for("listar_produtos"))
    categorias = Categoria.query.all()
    return render_template("form_produto.html", categorias=categorias)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/categorias')
def categorias():
    return render_template('categorias.html')

@app.route('/meus_anuncios')
def meus_anuncios():
    return render_template('meus_anuncios.html')

@app.route('/favoritos')
def favoritos():
    return render_template('favoritos.html')

@app.route('/compras')
def compras():
    return render_template('compras.html')

@app.route('/vendas')
def vendas():
    return render_template('vendas.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
