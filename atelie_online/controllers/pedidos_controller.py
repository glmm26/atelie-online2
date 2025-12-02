from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from atelie_online.models.servico_model import Servico
from atelie_online.models.usuario import Usuario
from atelie_online.models import db

pedidos_bp = Blueprint('pedidos', __name__, template_folder='../templates')


def get_current_user():
    user_obj = None
    try:
        if 'usuario_id' in session:
            user_obj = Usuario.query.get(int(session['usuario_id']))
    except Exception:
        user_obj = None
    return user_obj


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user or not getattr(user, 'is_admin', False):
            flash('Acesso negado. Você precisa ser administrador.', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper


@pedidos_bp.route('/listar')
@admin_required
def listar_pedidos():
    pedidos = Servico.query.order_by(Servico.data_pedido.desc()).all()
    return render_template('admin_pedidos.html', pedidos=pedidos)


@pedidos_bp.route('/marcar_entregue/<int:id>', methods=['POST'])
@admin_required
def marcar_entregue(id):
    pedido = Servico.query.get_or_404(id)
    try:
        pedido.status = 'Entregue'
        db.session.commit()
        flash('Pedido marcado como entregue.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar pedido: {e}', 'danger')
    return redirect(url_for('pedidos.listar_pedidos'))


@pedidos_bp.route('/cancelar/<int:id>', methods=['POST'])
@admin_required
def cancelar_pedido(id):
    pedido = Servico.query.get_or_404(id)
    try:
        pedido.status = 'Cancelado'
        db.session.commit()
        flash('Pedido cancelado.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cancelar pedido: {e}', 'danger')
    return redirect(url_for('pedidos.listar_pedidos'))


@pedidos_bp.route('/excluir/<int:id>', methods=['POST'])
@admin_required
def excluir_pedido(id):
    pedido = Servico.query.get_or_404(id)
    try:
        db.session.delete(pedido)
        db.session.commit()
        flash('Pedido excluído.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir pedido: {e}', 'danger')
    return redirect(url_for('pedidos.listar_pedidos'))


@pedidos_bp.route('/atualizar_status/<int:id>', methods=['POST'])
@admin_required
def atualizar_status(id):
    pedido = Servico.query.get_or_404(id)
    novo_status = request.form.get('status')
    allowed = ['Pendente', 'Em Progresso', 'Entregue', 'Concluida', 'Recusada']
    if novo_status not in allowed:
        flash('Status inválido.', 'danger')
        return redirect(url_for('pedidos.listar_pedidos'))
    try:
        pedido.status = novo_status
        # registrar quem atualizou o status (usuário atual - pode ser admin)
        user = get_current_user()
        if user:
            # gravar nome do usuário; se quiser id, troque para user.id
            pedido.status_atualizado_por = getattr(user, 'nome', str(getattr(user, 'id', '')))
        db.session.commit()
        flash('Status atualizado com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar status: {e}', 'danger')
    return redirect(url_for('pedidos.listar_pedidos'))
