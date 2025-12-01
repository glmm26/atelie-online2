from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from atelie_online.models.servico_model import Servico
from atelie_online.models.usuario import Usuario
from atelie_online.models import db
from flask import session

servico_bp = Blueprint('servicos', __name__, template_folder='../templates')

def get_current_user():
    """Retorna o usuário logado considerando session ou flask_login"""
    user_obj = None
    try:
        if 'usuario_id' in session:
            user_obj = Usuario.query.get(int(session['usuario_id']))
        else:
            user_obj = current_user if current_user.is_authenticated else None
    except Exception:
        user_obj = None
    return user_obj

@servico_bp.route('/')
def index():
    return redirect(url_for('servicos.cadastrar_servico'))

@servico_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_servico():
    if request.method == 'POST':
        nome_cliente = request.form.get('nome_cliente')
        tipo_servico = request.form.get('tipo_servico')
        descricao = request.form.get('descricao')

        novo_servico = Servico(None, nome_cliente, tipo_servico, descricao)
        try:
            db.session.add(novo_servico)
            db.session.commit()
            flash('Serviço cadastrado com sucesso!', 'success')
            return redirect(url_for('servicos.listar_servicos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar serviço: {str(e)}', 'danger')
            return redirect(url_for('servicos.cadastrar_servico'))

    return render_template('cadastro_servico.html')

@servico_bp.route('/servicos')
def listar_servicos():
    servicos = Servico.query.all()
    return render_template('lista_servicos.html', servicos=servicos)

@servico_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_servico(id):
    servico = Servico.query.get_or_404(id)
    try:
        db.session.delete(servico)
        db.session.commit()
        flash('Serviço excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir serviço: {str(e)}', 'danger')
    return redirect(url_for('servicos.listar_servicos'))

@servico_bp.route('/projeto')
def projeto():
    return render_template('projeto.html')

@servico_bp.route('/customizacao', methods=['GET', 'POST'])
def customizacao():
    if request.method == 'POST':
        user = get_current_user()
        material = request.form.get('material')
        descricao = request.form.get('descricao', '')
        
        if not material:
            flash('Por favor, selecione um material', 'danger')
            return redirect(url_for('servicos.customizacao'))
        
        # Salva pedido pendente na sessão e redireciona para a página de checkout
        if user:
            # preços básicos (poderiam vir de configuração/DB)
            price = 120.00
            session['pending_order'] = {
                'tipo_servico': 'Customização',
                'descricao': descricao or f'Material: {material}',
                'material': material,
                'price': price
            }
            return redirect(url_for('servicos.checkout'))
        else:
            flash('Você precisa estar logado para fazer um pedido', 'warning')
            return redirect(url_for('auth.login'))
    
    return render_template('customizacao.html')

@servico_bp.route('/conserto', methods=['GET', 'POST'])
def conserto():
    if request.method == 'POST':
        user = get_current_user()
        material = request.form.get('material')
        descricao = request.form.get('descricao', '')
        
        if not material:
            flash('Por favor, selecione um material', 'danger')
            return redirect(url_for('servicos.conserto'))
        
        # Salva pedido pendente na sessão e redireciona para a página de checkout
        if user:
            price = 80.00
            session['pending_order'] = {
                'tipo_servico': 'Conserto',
                'descricao': descricao or f'Material: {material}',
                'material': material,
                'price': price
            }
            return redirect(url_for('servicos.checkout'))
        else:
            flash('Você precisa estar logado para fazer um pedido', 'warning')
            return redirect(url_for('auth.login'))
    
    return render_template('conserto.html')

@servico_bp.route('/estamparia', methods=['GET', 'POST'])
def estamparia():
    if request.method == 'POST':
        user = get_current_user()
        imagem = request.files.get('imagem')
        descricao = request.form.get('descricao', '')
        
        if not user:
            flash('Você precisa estar logado para fazer um pedido', 'warning')
            return redirect(url_for('auth.login'))
        
        # Salva pedido pendente (incluir nome do arquivo se houver) e redireciona para checkout
        filename = None
        if imagem:
            filename = imagem.filename
        price = 50.00
        session['pending_order'] = {
            'tipo_servico': 'Estamparia',
            'descricao': descricao or 'Pedido de estampa enviado',
            'material': None,
            'imagem': filename,
            'price': price
        }
        return redirect(url_for('servicos.checkout'))
    
    return render_template('estamparia.html')

@servico_bp.route('/material')
def material():
    return render_template('mat_cons.html')


@servico_bp.route('/checkout', methods=['GET'])
def checkout():
    """Mostra a página de pagamento para o pedido pendente salvo na sessão."""
    pending = session.get('pending_order')
    user = get_current_user()
    if not pending:
        flash('Nenhum pedido pendente encontrado.', 'warning')
        return redirect(url_for('home'))
    if not user:
        flash('Você precisa estar logado para continuar o pagamento.', 'warning')
        return redirect(url_for('auth.login'))

    return render_template('checkout.html', pending=pending, user=user)


@servico_bp.route('/checkout/confirm', methods=['POST'])
def checkout_confirm():
    """Processa (simulado) o pagamento e cria o pedido no banco."""
    print('POST /checkout/confirm recebido')
    pending = session.get('pending_order')
    user = get_current_user()
    try:
        if pending and user:
            # verificar se o usuário incluiu dados de entrega
            include_delivery = request.form.get('include_delivery')
            destinatario = None
            if include_delivery:
                # ler campos de entrega (podem estar vazios)
                nome_dest = request.form.get('entrega_nome', '').strip()
                endereco = request.form.get('entrega_endereco', '').strip()
                cidade = request.form.get('entrega_cidade', '').strip()
                estado = request.form.get('entrega_estado', '').strip()
                cep = request.form.get('entrega_cep', '').strip()
                partes = []
                if nome_dest:
                    partes.append(nome_dest)
                if endereco:
                    partes.append(endereco)
                loc = ', '.join([p for p in [cidade, estado] if p])
                if loc:
                    partes.append(loc)
                if cep:
                    partes.append(f'CEP {cep}')
                if partes:
                    destinatario = ' | '.join(partes)

            novo_pedido = Servico(
                usuario_id=user.id,
                nome_cliente=user.nome,
                tipo_servico=pending.get('tipo_servico'),
                descricao=pending.get('descricao'),
                material=pending.get('material'),
                destinatario=destinatario
            )
            db.session.add(novo_pedido)
            db.session.commit()
            session.pop('pending_order', None)
            flash('✅ Pagamento confirmado — pedido realizado com sucesso!', 'success')
        else:
            flash('Pedido ou usuário não encontrado, mas fluxo finalizado.', 'warning')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao criar pedido, mas fluxo finalizado: {str(e)}', 'danger')
    print('Redirecionando para home...')
    return redirect(url_for('home'))

@servico_bp.route('/api/meus-pedidos', methods=['GET'])
def api_meus_pedidos():
    """API endpoint para retornar os pedidos do usuário logado em JSON"""
    user = get_current_user()
    
    if not user:
        return jsonify({
            'success': False,
            'error': 'Usuário não autenticado'
        }), 401
    
    try:
        # Buscar todos os pedidos do usuário
        pedidos = Servico.query.filter_by(usuario_id=user.id).order_by(Servico.data_pedido.desc()).all()
        
        pedidos_data = []
        for pedido in pedidos:
            pedidos_data.append({
                'id': pedido.id,
                'tipo_servico': pedido.tipo_servico,
                'descricao': pedido.descricao,
                'destinatario': pedido.destinatario,
                'status': pedido.status,
                'material': pedido.material,
                'data_pedido': pedido.data_pedido.isoformat()
            })
        
        return jsonify({
            'success': True,
            'pedidos': pedidos_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
