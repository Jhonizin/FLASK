from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)

# Modelo simples de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(100))

# Rota: listar usuários
@app.route('/usuarios')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

# Rota: cadastrar usuário
@app.route('/usuarios/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        novo = Usuario(
            nome=request.form['nome'],
            email=request.form['email'],
            senha=request.form['senha']
        )
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('listar_usuarios'))
    return render_template('usuarios/cadastrar.html')


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
