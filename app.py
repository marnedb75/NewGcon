import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Colaborador, Fornecedor

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave-secreta-desenv-gcon')

# Lê as configurações das variáveis de ambiente (com fallback para os valores padrões)
DB_HOST = os.environ.get('DB_HOST', '172.27.8.12')
DB_USER = os.environ.get('DB_USER', 'app_newgcon')
DB_PASS = os.environ.get('DB_PASS', '')
DB_NAME = os.environ.get('DB_NAME', 'gcon')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

# --- ROTAS DE COLABORADORES ---
@app.route('/colaboradores')
def listar_colaboradores():
    colaboradores = Colaborador.query.filter_by(_excluido='0').limit(100).all()
    return render_template('colaboradores.html', colaboradores=colaboradores)


# --- ROTAS DE FORNECEDORES ---

# READ + SEARCH: Listagem e Pesquisa
@app.route('/fornecedores')
def listar_fornecedores():
    search = request.args.get('q', '').strip()
    query = Fornecedor.query

    if search:
        # Busca flexível por Nome, CNPJ, CPF ou Representante
        query = query.filter(
            (Fornecedor.nome.ilike(f'%{search}%')) |
            (Fornecedor.cnpj.ilike(f'%{search}%')) |
            (Fornecedor.cpf.ilike(f'%{search}%')) |
            (Fornecedor.representante.ilike(f'%{search}%'))
        )

    fornecedores = query.limit(100).all()
    return render_template('fornecedores.html', fornecedores=fornecedores, search=search)

# CREATE: Criar Fornecedor
@app.route('/fornecedores/novo', methods=['POST'])
def criar_fornecedor():
    novo = Fornecedor(
        nome=request.form.get('nome'),
        representante=request.form.get('representante'),
        cnpj=request.form.get('cnpj'),
        cpf=request.form.get('cpf'),
        registro_inter=request.form.get('registro_inter')
    )
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('listar_fornecedores'))

# UPDATE: Editar Fornecedor
@app.route('/fornecedores/editar/<int:id>', methods=['POST'])
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    fornecedor.nome = request.form.get('nome')
    fornecedor.representante = request.form.get('representante')
    fornecedor.cnpj = request.form.get('cnpj')
    fornecedor.cpf = request.form.get('cpf')
    fornecedor.registro_inter = request.form.get('registro_inter')

    db.session.commit()
    return redirect(url_for('listar_fornecedores'))

# DELETE: Excluir Fornecedor
@app.route('/fornecedores/excluir/<int:id>', methods=['POST'])
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    db.session.delete(fornecedor)
    db.session.commit()
    return redirect(url_for('listar_fornecedores'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)