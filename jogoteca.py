from flask import Flask, render_template, request, redirect, session, flash, url_for


class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console


game_1 = Game('God of War', 'Fight', 'Playstation 2')
game_2 = Game('Gran Turismo', 'Race', 'Playstation 2')
game_3 = Game('Fifa 24', 'Soccer', 'Playstation 4')
game_list = [game_1, game_2, game_3]


app = Flask(__name__)
app.secret_key = 'schmeller'


@app.route('/')
def index():
    return render_template('lista.html', title='Jogos', game_list=game_list)


@app.route('/newGame')
def new_game():
    return render_template('new_game.html', title='Cadastrar novo game') 


@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    game = Game(name, category, console)
    game_list.append(game)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    if '12345' == request.form['password']:
        session['usuario_logado'] = request.form['username']
        flash(session['usuario_logado'] + ' logado com sucesso!')
        proxima_pagina = request.form.get('proxima')
        if proxima_pagina and proxima_pagina.startswith('/'):
            return redirect(proxima_pagina)
        else:
            return redirect(url_for('index'))

    else:
        flash('Senha incorreta. Tente novamente.', 'error')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['Usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))


@app.route('/novo')
def novo():
    if 'Usuario_logado' not in session or session['Usuario_logado'] is None:
        return redirect(url_for('login'))
    return render_template('new_game.html', titulo='Novo Jogo')


app.run(debug=True)
