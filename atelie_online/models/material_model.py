from . import db
from datetime import datetime

class Material(db.Model):
    __tablename__ = 'materiais'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    unidade_medida = db.Column(db.String(20), nullable=False)  # metros, unidades, kg, etc
    descricao = db.Column(db.Text)
    preco_unitario = db.Column(db.Float)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, nome, quantidade, unidade_medida, descricao=None, preco_unitario=None):
        self.nome = nome
        self.quantidade = quantidade
        self.unidade_medida = unidade_medida
        self.descricao = descricao
        self.preco_unitario = preco_unitario
        
    def __repr__(self):
        return f"<Material {self.nome}>"