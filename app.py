from flaslk import Flask, render_template

app = Flask(__name__)

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
    app.run(debug=True)
