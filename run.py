from flask import Flask, render_template, request, redirect, flash
import sqlite3
import os
from flask import send_from_directory

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # pode ser qualquer string


app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['dados_login'] = []

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#====================================================================
@app.route('/')
def index():
    return render_template('index.html')

#==================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    usuario = request.form['usuario']
    senha = request.form['senha']

    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    sql = "SELECT * FROM tb_login WHERE usuario = ? AND senha = ?"
    cursor.execute(sql, (usuario, senha))
    login_usuario = cursor.fetchone()

    if login_usuario:
        app.config['dados_login'] = login_usuario
        return redirect('/bem_vindo')
    else:
        flash('Usuário ou senha incorretos!', 'error')
        return redirect('/')
    
#===================================================================
@app.route('/bem_vindo', methods=['GET'])
def bem_vindo():
    if not app.config['dados_login']:
        return redirect('/')
    
    usuario_logado = app.config['dados_login']
    nome_usuario = usuario_logado[3] if len(usuario_logado) > 3 else "Usuário desconhecido"

    return render_template('bem_vindo.html', nome_usuario=nome_usuario)

#============================================================================

@app.route('/logout')
def logout():
    app.config['dados_login'] = []
    return redirect('/')

@app.route('/cadastro_cliente', methods=['GET'])
def cadastro_cliente():
    if not app.config['dados_login']:
        return redirect('/')
    
    usuario_logado = app.config['dados_login']
    nome_usuario = usuario_logado[3] if len(usuario_logado) > 3 else "Usuário desconhecido"
    
    return render_template('cadastro_cliente.html', nome_usuario=nome_usuario)

#=======================================================================
@app.route('/enviar_cliente', methods=['POST'])
def enviar_cliente():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    cpf = request.form['cpf']
    rua = request.form['rua']
    numero = request.form['numero']
    cidade = request.form['cidade']
    estado = request.form['estado']
    data_cadastro = request.form['data_cadastro']
    cep = request.form['cep']

    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    sql = 'INSERT INTO tb_clientes (nome, email, telefone, rua, numero, cidade, estado, cep, data_cadastro, cpf) VALUES (?,?,?,?,?,?,?,?,?,?)'
    cursor.execute(sql, (nome, email, telefone, rua, numero, cidade, estado, cep, data_cadastro, cpf))
    
    conexao.commit()
    conexao.close()

    flash(f'Cliente "{nome}" cadastrado com sucesso!', 'success')
    return redirect('/cadastro_cliente')

#======================================================================

@app.route('/consulta_cliente', methods=['GET'])
def consulta_cliente():
    nome = request.args.get('nome', None)

    if not os.path.exists('models/cadastro.db'):
        return redirect('/')
    
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    sql = 'SELECT * FROM tb_clientes'
    cursor.execute(sql)
    clientes = cursor.fetchall()

    conexao.close()

    usuario_logado = app.config['dados_login']
    nome_usuario = usuario_logado[3] if len(usuario_logado) > 3 else "Usuário desconhecido"

    return render_template('consulta_cliente.html', clientes=clientes, nome_usuario=nome_usuario)

#==============================================================

@app.route('/excluir_cliente/<int:id>', methods=['GET'])
def excluir(id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
 
    sql = 'DELETE FROM tb_clientes WHERE cliente_id = ?'
    cursor.execute(sql, (id,))
 
    conexao.commit()
    conexao.close()
 
    return redirect('/consulta_cliente')
#============================================================

@app.route('/excluir_fornecedor/<int:id>', methods=['GET'])
def excluir_fornecedor(id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    sql = 'DELETE FROM tb_fornecedores WHERE fornecedor_id = ?'
    cursor.execute(sql, (id,))

    conexao.commit()
    conexao.close()

    return redirect('/consulta_fornecedor')

#=======================================================

@app.route('/excluir/<int:id>', methods=['GET'])
def excluir_usuario(id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()
 
    sql = 'DELETE FROM tb_login WHERE usuario_id = ?'
    cursor.execute(sql, (id,))
 
    conexao.commit()
    conexao.close()
 
    return redirect('/consulta_usuario')

#==========================================================
@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        rua = request.form['rua']
        numero = request.form['numero']
        cidade = request.form['cidade']
        estado = request.form['estado']
        cep = request.form['cep']

        sql = "UPDATE tb_clientes SET nome = ?, email = ?, telefone = ?, cpf = ?, rua = ?, numero = ?, cidade = ?, estado = ?, cep = ? WHERE cliente_id = ?"
        cursor.execute(sql, (nome, email, telefone, cpf, rua, numero, cidade, estado, cep, id))

        conexao.commit()
        conexao.close()

        return redirect('/consulta_cliente')
    
    else:
        cursor.execute("SELECT * FROM tb_clientes WHERE cliente_id = ?", (id,))
        cliente = cursor.fetchone()
        conexao.close()

    return render_template('editar_cliente.html', cliente=cliente)

#=================================================================

@app.route('/cadastro_fornecedor')
def cadastro_fornecedor():
    if not app.config['dados_login']:
        return redirect('/')
    
    usuario_logado = app.config['dados_login']
    nome_usuario = usuario_logado[3] if len(usuario_logado) > 3 else "Usuário desconhecido"

    return render_template('cadastro_fornecedor.html', nome_usuario=nome_usuario)

#=================================================================

@app.route('/enviar_fornecedor', methods=['POST'])
def enviar_fornecedor():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    cnpj = request.form['cnpj']
    rua = request.form['rua']
    numero = request.form['numero']
    cidade = request.form['cidade']
    estado = request.form['estado']
    cep = request.form['cep']

    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    sql = 'INSERT INTO tb_fornecedores (nome, email, telefone, cnpj, rua, numero, cidade, estado, cep) VALUES (?,?,?,?,?,?,?,?,?)'
    cursor.execute(sql, (nome, email, telefone, cnpj, rua, numero, cidade, estado, cep))

    conexao.commit()
    conexao.close()

    flash(f'Fornecedor "{nome}" cadastrado com sucesso!', 'success')
    return redirect('/cadastro_fornecedor')

#=====================================================================

@app.route('/consulta_fornecedor', methods=['GET'])
def consulta_fornecedor():
    nome = request.args.get('nome', None)

    if not app.config['dados_login']:
        return redirect('/')
    
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    sql = 'SELECT * FROM tb_fornecedores'
    cursor.execute(sql)
    fornecedores = cursor.fetchall()

    conexao.close()

    usuario_logado = app.config['dados_login']
    nome_usuario = usuario_logado[3] if len(usuario_logado) > 3 else "Usuário desconhecido"

    return render_template('consulta_fornecedor.html', fornecedores=fornecedores, nome_usuario=nome_usuario)

#==============================================================

@app.route('/visualizar_cliente/<int:cliente_id>', methods=['GET'])
def visualizar_cliente(cliente_id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    sql = 'SELECT * FROM tb_clientes WHERE cliente_id = ?'
    cursor.execute(sql, (cliente_id,))
    cliente = cursor.fetchone()

    usuario_logado = app.config['dados_login']
    nome_usuario = usuario_logado[3] if len(usuario_logado) > 3 else "Usuário desconhecido"

    return render_template('visualizar_cliente.html', cliente=cliente, nome_usuario=nome_usuario)


#=================================================================

@app.route('/visualizar_fornecedor/<int:fornecedor_id>', methods=['GET'])
def visualizar_fornecedor(fornecedor_id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    sql = 'SELECT * FROM tb_fornecedores WHERE fornecedor_id = ?'
    cursor.execute(sql, (fornecedor_id,))
    fornecedor = cursor.fetchone()

    usuario_logado = app.config['dados_login']
    nome_usuario = usuario_logado[3] if len(usuario_logado) > 3 else "Usuário desconhecido"

    return render_template('visualizar_fornecedor.html', fornecedor=fornecedor, nome_usuario=nome_usuario)

#=====================================================================================

@app.route('/editar_fornecedor/<int:id>', methods=['GET', 'POST'])
def editar_fornecedor(id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cnpj = request.form['cnpj']
        rua = request.form['rua']
        numero = request.form['numero']
        cidade = request.form['cidade']
        estado = request.form['estado']
        data_cadastro = request.form['data_cadastro']
        cep = request.form['cep']

        sql = "UPDATE tb_fornecedores SET nome = ?, email = ?, telefone = ?, cnpj = ?, rua = ?, numero = ?, cidade = ?, estado = ?, data_cadastro = ?, cep = ? WHERE fornecedor_id = ?"
        cursor.execute(sql, (nome, email, telefone, cnpj, rua, numero, cidade, estado, data_cadastro, cep, id))

        conexao.commit()
        conexao.close()

        return redirect('/consulta_fornecedor')
    
    else:
        cursor.execute("SELECT * FROM tb_fornecedores WHERE fornecedor_id = ?", (id,))
        fornecedor = cursor.fetchone()
        conexao.close()

    return render_template('editar_fornecedor.html', fornecedor=fornecedor)

#==============================================================================

@app.route('/cadastro_usuario')
def cadastro_usuario():

    
    usuario_logado = app.config['dados_login']
    nome_usuario = usuario_logado[3] if len(usuario_logado) > 3 else "Usuário desconhecido"

    return render_template('cadastro_usuario.html', nome_usuario=nome_usuario)

#=================================================================

@app.route('/enviar_usuario', methods=['POST'])
def enviar_usuario():
    usuario = request.form['usuario']
    senha = request.form['senha']
    nome_usuario = request.form['nome_usuario']

    # Processar upload de imagem
    imagem = request.files.get('imagem')
    nome_imagem = None  # Default caso não haja imagem
    if imagem and imagem.filename != "":
        nome_imagem = f"{usuario}_{imagem.filename}"  # Nome único
        caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], nome_imagem)
        imagem.save(caminho_imagem)
    else:
        nome_imagem = None


    # Salvar dados no banco de dados
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    sql = '''
    INSERT INTO tb_login (usuario, senha, nome_usuario, imagem) 
    VALUES (?, ?, ?, ?)
    '''
    cursor.execute(sql, (usuario, senha, nome_usuario, nome_imagem))

    conexao.commit()
    conexao.close()

    return redirect('/consulta_usuario')

#==============================================================================

@app.route('/consulta_usuario', methods=['GET'])
def consulta_usuario():
    nome = request.args.get('nome', None)
    

    if not app.config['dados_login']:
        return redirect('/')
    
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM tb_login")
    usuarios = cursor.fetchall()

    conexao.close()

    usuario_logado = app.config['dados_login']
    nome_usuario = usuario_logado[3] if len(usuario_logado) > 3 else "Usuário desconhecido"

    return render_template('consulta_usuario.html', login=usuarios, nome_usuario=nome_usuario)
#============================================================================

@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar(id):

    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        usuario = request.form['usuario']
        senha = request.form['senha']

        sql = "UPDATE tb_login SET nome_usuario = ?, usuario = ?, senha = ? WHERE usuario_id = ?"
        cursor.execute(sql, (nome_usuario, usuario, senha, id)) 

        conexao.commit()
        conexao.close()

        return redirect('/consulta_usuario')
    
    else:
        cursor.execute("SELECT * FROM tb_login WHERE usuario_id = ?", (id,))
        usuarios = cursor.fetchone()
        conexao.close()

    return render_template('editar_usuario.html', usuario=usuarios)


#=====================================================================

@app.route('/visualizar_usuario/<int:usuario_id>', methods=['GET'])
def visualizar_usuario(usuario_id):
    conexao = sqlite3.connect('models/cadastro.db')
    cursor = conexao.cursor()

    sql = 'SELECT * FROM tb_login WHERE usuario_id = ?'
    cursor.execute(sql, (usuario_id,))
    usuario = cursor.fetchone()

    usuario_logado = app.config['dados_login']
    nome_usuario = usuario_logado[3] if len(usuario_logado) > 3 else "Usuário desconhecido"

    return render_template('visualizar_usuario.html', usuario=usuario, nome_usuario=nome_usuario)

#================================================================

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)