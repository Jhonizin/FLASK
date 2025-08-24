from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Usuario, Produto, Categoria, Pedido, ItemPedido, Pergunta
from functools import wraps

app = Flask(__name__)
app.secret_key = "luiz"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Faça login para acessar esta página.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ------------------ LOGIN ------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["usuario"].strip().lower()
        senha = request.form["senha"].strip()
        usuario = Usuario.query.filter_by(email=email, senha=senha).first()
        if usuario:
            session['user_id'] = usuario.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("home"))
        else:
            flash("Usuário ou senha incorretos", "danger")
            return render_template("login.html")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("login"))

# ------------------ HOME ------------------
@app.route('/')
@login_required
def home():
    return render_template('home.html')

# ------------------ USUÁRIOS ------------------
@app.route("/usuarios")
@login_required
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/usuarios/novo", methods=["GET", "POST"])
@login_required
def novo_usuario():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip().lower()
        senha = request.form["senha"].strip()
        usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for("listar_usuarios"))
    return render_template("form_usuario.html")

@app.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_usuario(id):
    usuario = Usuario.query.get(id)
    if request.method == "POST":
        usuario.nome = request.form["nome"].strip()
        usuario.email = request.form["email"].strip().lower()
        db.session.commit()
        return redirect(url_for("listar_usuarios"))
    return render_template("form_usuario.html", usuario=usuario)

@app.route("/usuarios/excluir/<int:id>")
@login_required
def excluir_usuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for("listar_usuarios"))

# ------------------ CATEGORIAS ------------------
@app.route("/categorias")
@login_required
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template("categorias.html", categorias=categorias)

@app.route("/categorias/novo", methods=["GET", "POST"])
@login_required
def nova_categoria():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        categoria = Categoria(nome=nome)
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for("listar_categorias"))
    return render_template("form_categoria.html")

@app.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_categoria(id):
    categoria = Categoria.query.get(id)
    if request.method == "POST":
        categoria.nome = request.form["nome"].strip()
        db.session.commit()
        return redirect(url_for("listar_categorias"))
    return render_template("form_categoria.html", categoria=categoria)

@app.route("/categorias/excluir/<int:id>")
@login_required
def excluir_categoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for("listar_categorias"))

# ------------------ PRODUTOS ------------------
@app.route("/produtos")
@login_required
def listar_produtos():
    produtos = Produto.query.all()
    return render_template("produtos.html", produtos=produtos)

@app.route("/produtos/novo", methods=["GET", "POST"])
@login_required
def novo_produto():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        preco = float(request.form["preco"])
        categoria_id = int(request.form["categoria_id"])
        produto = Produto(nome=nome, preco=preco, categoria_id=categoria_id)
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for("listar_produtos"))
    categorias = Categoria.query.all()
    return render_template("form_produto.html", categorias=categorias)

@app.route("/produtos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_produto(id):
    produto = Produto.query.get(id)
    if request.method == "POST":
        produto.nome = request.form["nome"].strip()
        produto.preco = float(request.form["preco"])
        produto.categoria_id = int(request.form["categoria_id"])
        db.session.commit()
        return redirect(url_for("listar_produtos"))
    categorias = Categoria.query.all()
    return render_template("form_produto.html", produto=produto, categorias=categorias)

@app.route("/produtos/excluir/<int:id>")
@login_required
def excluir_produto(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for("listar_produtos"))

# ------------------ OUTRAS PÁGINAS ------------------
@app.route('/meus_anuncios')
@login_required
def meus_anuncios():
    return render_template('meus_anuncios.html')

@app.route('/favoritos')
@login_required
def favoritos():
    return render_template('favoritos.html')

@app.route('/compras')
@login_required
def compras():
    return render_template('compras.html')

@app.route('/vendas')
@login_required
def vendas():
    return render_template('vendas.html')

# ------------------ ROTA DEFAULT PARA LOGIN ------------------
# Redireciona qualquer rota não encontrada para home/login
@app.errorhandler(404)
def page_not_found(e):
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
