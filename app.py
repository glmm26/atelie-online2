import os
from flask import Flask, render_template, jsonify
from flask_login import LoginManager, current_user
from atelie_online.models import db
from atelie_online.models.usuario import Usuario
from atelie_online.models.servico_model import Servico
from atelie_online.controllers.auth_controller import auth_bp
from atelie_online.controllers.cliente_controller import cliente_bp
from atelie_online.controllers.servico_controller import servico_bp
from atelie_online.controllers.material_controller import material_bp
from atelie_online.controllers.pedidos_controller import pedidos_bp

def create_app():
    app = Flask(__name__, template_folder='atelie_online/templates', static_folder='atelie_online/static')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@db:5432/atelie_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.environ.get('SECRET_KEY', 'troque_essa_chave')

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cliente_bp, url_prefix='/clientes')
    app.register_blueprint(servico_bp, url_prefix='/servicos')
    app.register_blueprint(material_bp, url_prefix='/material')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')

    @app.route('/')
    def home():
        # If the app is using session-based login (session['usuario_id']), prefer that user
        from flask import session
        from flask_login import current_user as flask_current_user

        user_obj = None
        try:
            if 'usuario_id' in session:
                user_obj = Usuario.query.get(int(session['usuario_id']))
        except Exception:
            user_obj = None

        # pass a user-like object named current_user to keep templates unchanged
        resolved = (user_obj or flask_current_user)
        # debug: print which user object was resolved for the template
        try:
            print(f"Home current_user resolved: id={(resolved.id if resolved and hasattr(resolved,'id') else None)}, foto={(resolved.foto if resolved and hasattr(resolved,'foto') else None)}")
        except Exception:
            pass
        return render_template('index.html', current_user=resolved)

    @app.route('/api/meus-pedidos', methods=['GET'])
    def api_meus_pedidos():
        """API endpoint para retornar os pedidos do usuário logado em JSON"""
        from flask import session
        from flask_login import current_user as flask_current_user
        
        # Determinar o usuário logado
        user_obj = None
        try:
            if 'usuario_id' in session:
                user_obj = Usuario.query.get(int(session['usuario_id']))
            else:
                user_obj = flask_current_user
        except Exception:
            user_obj = None
        
        if not user_obj or not user_obj.is_authenticated:
            return jsonify({
                'success': False,
                'error': 'Usuário não autenticado'
            }), 401
        
        try:
            # Buscar todos os serviços/pedidos do usuário pelo nome
            pedidos = Servico.query.filter_by(nome_cliente=user_obj.nome).order_by(Servico.data_pedido.desc()).all()

            pedidos_data = []
            for pedido in pedidos:
                pedidos_data.append({
                    'id': pedido.id,
                    'tipo_servico': pedido.tipo_servico,
                    'descricao': pedido.descricao,
                    'status': getattr(pedido, 'status', 'Pendente'),
                    'material': getattr(pedido, 'material', None),
                    'data_pedido': pedido.data_pedido.isoformat() if hasattr(pedido, 'data_pedido') and pedido.data_pedido else ''
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

    @app.route('/admin_dashboard')
    def admin_dashboard():
        from flask import session, redirect, url_for, render_template

        #tirar estes comentário quando login ok - é apenas para ver css do admin
        #if 'usuario_id' not in session or not session.get('is_admin'):
            #return redirect(url_for('auth.login'))
        return render_template('admin_dashboard.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
