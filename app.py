from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
import db_conection
import code_generator
import pathlib
from datetime import datetime
import pyglp
import os
import json


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.secret_key = '9Kd2O27rAQKz'

db = SQLAlchemy(app)

# Classe  DB
class Usuarios(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    age = db.Column(db.String(150))
    email = db.Column(db.String(150))
    phone = db.Column(db.String(150))

    def __int__(self, name, username, password, age, email, phone):
        self.name = name
        self.username = username
        self.password = password
        self.age = age
        self.email = email
        self.phone = phone

class Logs(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    user = db.Column(db.String(150))
    action = db.Column(db.String(250))

    def __int__(self, date, time, user, action):
        self.date = date
        self.time = time
        self.user = user
        self.action = action

# Classe produto
class Produto():
    codigo = "gerado"
    title = "gerado"
    value = "gerado"
    
    def __init__(self, codigo, title, value):
        self.codigo = codigo
        self.title = title
        self.value = value
        


# Rotas de Login e Cadastro

@app.route('/', methods=['GET', 'POST'])
def index():
    username = ''
    if 'username' in session:
        username = session['username']
        return redirect(url_for('painel'))
    else:
        return render_template('index.html', username=username)


@app.route('/logar', methods=['POST'])
def logar():
    if request.form['user'] != "":
        usuario = Usuarios.query.filter_by(username=request.form['user']).first()
        if usuario != None and usuario.username == request.form['user'] and usuario.password == request.form['senha']:
            session['username'] = request.form['user']
            if usuario.username == "admin":
                salvarLog(f"{session['username']}", f"<LOGIN>")
                return render_template('painel_admin.html', username=request.form['user'])
            else:
                salvarLog(f"{session['username']}", f"<LOGIN>")
                return render_template('painel.html', username=request.form['user'])
        else:
            return render_template('login.html', msg="Usuario ou senha invalida!", msg_like='')
    else:
        return render_template('login.html', msg="Prencha os campos corretamente!", msg_like='')


@app.route('/registrar', methods=['POST'])
def registrar():
    usuario = Usuarios.query.filter_by(username=request.form['user']).first()
    if usuario != None:
        msg = "O usuario informado ja está em uso."
        return render_template('register.html', msg=msg)
    else:
        name = request.form['name']
        user = request.form['user']
        passw = request.form['senha']
        age = request.form['age']
        email = request.form['email']
        phone = request.form['phone']
        usuario_novo = Usuarios(name=name, username=user, password=passw, age=age, email=email, phone=phone)
        db.session.add(usuario_novo)
        db.session.commit()
        salvarLog("/register", f"<REGISTER> | User: {user}")
        return render_template('login.html', msg_like=("Você foi cadastrado com sucesso!", "Realize seu login abaixo!"))

@app.route('/logout')
def logout():
    salvarLog(f"{session['username']}", f"<LOGOUT>")
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', msg_like=('', ''))

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/painel')
def painel():
    username = ''
    if 'username' in session:
        username = session['username']
        if username == 'admin':
            usuarios_gerais = Usuarios.query.all()
            return render_template('painel_admin.html', username=username, usuarios=usuarios_gerais)
        else:
            return render_template('painel.html', username=username)
    else:
        return render_template('index.html', username=username)

@app.route('/delete/<int:id>')
def delete(id):
    if session['username'] == "admin":
        usuario = Usuarios.query.get(id)

        salvarLog(f"{session['username']}", f"<DELET> | User: {usuario.username}")

        db.session.delete(usuario)
        db.session.commit()

        return redirect(url_for('painel'))
    else:
        redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    usuario = Usuarios.query.get(id)
    if request.method == 'POST':
        usuario.name = request.form['name']
        usuario.username = request.form['user']
        usuario.password = request.form['senha']
        usuario.age = request.form['age']
        usuario.email = request.form['email']
        usuario.phone = request.form['phone']

        salvarLog(f"{session['username']}", f"<EDIT> | User: {usuario.username}")
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', usuario=usuario)


# Metodo de consulta

@app.route('/consulta', methods=['POST', 'GET'])
def consulta():
    produto = Produto("0000000000000", "Clique no campo e digite o codigo do produto!", "0,00")
    return render_template('consulta.html', produto=produto)

@app.route('/consultar', methods=['POST'])
def consultar():    
    codigo = request.form['codigo']
    resultado = db_consulta.consulta(codigo)
    produto = Produto(codigo, resultado['PRODUTO'], resultado['VALOR'])
    salvarLog(f"{session['username']}", f"<CODEBAR-SEARCH> | Code: {codigo} | Item: {produto.title}")
    return render_template('consulta.html', produto=produto)

@app.route('/buscar_codigo', methods=['POST'])
def buscar():
    if request.files.get('foto_codigo').filename != "":
        imagem_codigo = request.files.get('foto_codigo')
        nome_do_arquivo = imagem_codigo.filename
        imagem_codigo.save(str(pathlib.Path().absolute())+"\\temp\\"+str(nome_do_arquivo))

        codigo_extract = code_generator.BarcodeReader("./temp/"+str(imagem_codigo.filename))
        resultado = db_consulta.consulta(codigo_extract)
        produto = Produto(codigo_extract, resultado['PRODUTO'], resultado['VALOR'])
        salvarLog(f"{session['username']}", f"<IMG-CODEBAR-SEARCH> | Code: {codigo_extract} | Item: {produto.title}")
        return render_template('consulta.html', produto=produto)
    else:
        return redirect(url_for('lercode'))

@app.route('/lercode', methods=['GET'])
def lercode():
    return render_template('lercode.html')

@app.route('/users_manager', methods=['POST'])
def users_manager():
    username = ''
    if 'username' in session:
        username = session['username']
        if username == 'admin':
            usuarios_gerais = Usuarios.query.all()
            return render_template('usersmanager.html', username=username, usuarios=usuarios_gerais)
        else:
            return render_template('painel.html', username=username)
    else:
        return render_template('index.html', username=username)
    
@app.route('/logs_system', methods=['POST'])
def log_system():
    if session['username'] == "admin":

        stmt = select(Logs).order_by(Logs.id.desc())
        logs_sys_ = db.session.execute(stmt).fetchall()
        

        return render_template('logs_sys.html', username=session['username'], logs_sys=logs_sys_)
    else:
        redirect(url_for('index'))

@app.route('/perfil', methods=['GET', 'POST'])
def configs():
    if session['username'] != None:
        username = session['username']
        usuario = Usuarios.query.filter_by(username=username).first()
        #salvarLog(f"{session['username']}", f"<EDIT> | User: {usuario.username}")
        #db.session.commit()
        return render_template('perfil.html', usuario=usuario)
    else:
        return redirect(url_for('index'))

@app.route('/salvar_perfil', methods=['POST'])
def save_configs():
    if session['username'] != None:
        username = session['username']
        usuario = Usuarios.query.filter_by(username=username).first()

        usuario.name = request.form['name']
        usuario.username = request.form['user']
        usuario.password = request.form['senha']
        usuario.age = request.form['age']
        usuario.email = request.form['email']
        usuario.phone = request.form['phone']

        salvarLog(f"{session['username']}", f"<EDIT> | User: {usuario.username}")
        db.session.commit()
        
        return redirect(url_for('painel'))
    else:
        return redirect(url_for('index'))

@app.route('/gerar_placa', methods=['GET','POST'])
def gerar_placas():
    if session['username'] != "" and session['username'] != None:
        return render_template('gerar_placa.html')
    else:
        redirect(url_for('index'))

@app.route('/gerar_pagina', methods=['POST'])
def gerar_pagina():
    if session['username'] != "" and session['username'] != None:
        lista_codes = [] #class dict
        string_full = str(request.form['lista']).split(",")
        for i in string_full:
            if i != "":
                lista_codes.append(i)
        list_dicionario = pyglp.DictGen().generateDictAuto(lista_codes=lista_codes)
        objeto_pyglp = pyglp.PyGLP()
        objeto_pyglp.initialize(session['username'], list_dicionario)
        path_arquivo = "/files/placas_de_preco/{user}/".format(user=session['username'])+str(objeto_pyglp.pdf_file_name)
        salvarLog(f"{session['username']}", f"<PDF-LABEL-GENERATE> | file: {objeto_pyglp.pdf_file_name}")
        return render_template('pdf_view.html', pdf_file=path_arquivo)
        
    else:
        return redirect(url_for('index'))
    
@app.route('/abrir_pdf', methods=['GET'])
def abrir_pdf():
    #path_arquivo = f"/files/placas_de_preco/admin/"+"admin_01-08-2023_15-46-52.pdf"
    path_arquivo = "/files/placas_de_preco/{user}/".format(user=session['username'])
    return render_template('pdf_view.html', pdf_file=path_arquivo)

def salvarLog(user_, action_):
    user = user_
    date = datetime.today().strftime('%Y-%m-%d')
    time = datetime.today().strftime('%H:%M')
    action = action_
    logs_novo = Logs(date=date,time=time,user=user,action=action)
    db.session.add(logs_novo)
    db.session.commit()

# Metodo RUN
"""
Cole seu codigo aqui: 


"""
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db_consulta = db_conection.ServerDB()
    app.run(debug=True)

"""
Cole seu codigo aqui: 

if __name__ == '__main__':
    db_consulta = db_conection.ServerDB()
    from waitress import serve
    host = "0.0.0.0"
    port = 5000
    print(f"!- Server Start | HOST: {host} | PORT: {port} -!")
    serve(app, host=host, port=port)
    print("!- Server STOP -!")

"""

