import os
from flask import Flask, render_template
from models import db, Colaborador

app = Flask(__name__)

# Lê as configurações das variáveis de ambiente (com fallback para os valores padrões)
DB_HOST = os.environ.get('DB_HOST', '172.27.8.12')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', '')
DB_NAME = os.environ.get('DB_NAME', 'gcon')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/colaboradores')
def listar_colaboradores():
    colaboradores = Colaborador.query.filter_by(_excluido='0').limit(100).all()
    return render_template('colaboradores.html', colaboradores=colaboradores)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)