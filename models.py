from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Colaborador(db.Model):
    __tablename__ = 'colaborador'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpf = db.Column(db.String(20), nullable=False)
    nome = db.Column(db.String(50))
    sexo = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date)
    data_contratacao = db.Column(db.Date)
    _excluido = db.Column(db.String(1), default='0')