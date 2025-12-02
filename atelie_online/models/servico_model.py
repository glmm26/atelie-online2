from . import db
from datetime import datetime

class Servico(db.Model):
    __tablename__ = 'servicos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nome_cliente = db.Column(db.String(100), nullable=False)
    tipo_servico = db.Column(db.String(100), nullable=False)  # estamparia, conserto, customizacao
    descricao = db.Column(db.Text, nullable=True)
    material = db.Column(db.String(100), nullable=True)
    destinatario = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(50), default='Pendente', nullable=False)  # Pendente, Em Progresso, Concluído, Entregue
    status_atualizado_por = db.Column(db.String(150), nullable=True)
    data_pedido = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, usuario_id, nome_cliente, tipo_servico, descricao=None, material=None, destinatario=None):
        self.usuario_id = usuario_id
        self.nome_cliente = nome_cliente
        self.tipo_servico = tipo_servico
        self.descricao = descricao
        self.material = material
        self.destinatario = destinatario
        self.data_pedido = datetime.utcnow()
        self.data_atualizacao = datetime.utcnow()

