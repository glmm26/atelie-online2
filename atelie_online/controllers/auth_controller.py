from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from atelie_online.models.usuario import Usuario
from atelie_online.models import db
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not email or not senha:
            flash('Todos os campos são obrigatórios!', 'danger')
            return redirect(url_for('auth.register'))

        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('auth.register'))

        novo_usuario = Usuario(nome=nome, email=email)
        novo_usuario.set_senha(senha)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao cadastrar: {str(e)}', 'danger')
            return redirect(url_for('auth.register'))

    return render_template('registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.verificar_senha(senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['is_admin'] = usuario.is_admin

            flash('Login realizado com sucesso!', 'success')
            if usuario.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('clientes.index'))

        flash('E-mail ou senha incorretos.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = Usuario.query.get(session['usuario_id'])
    if not user:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('auth.login'))
    
    # Debug: imprime informações sobre a foto e caminhos
    if user.foto:
        import os
        # `current_app` is imported at module level; avoid re-importing inside the function
        photo_path = os.path.join(current_app.static_folder, 'uploads', user.foto)
        print(f"Foto do usuário: {user.foto}")
        print(f"Caminho completo: {photo_path}")
        print(f"Arquivo existe: {os.path.exists(photo_path)}")
        print(f"URL gerada: {url_for('static', filename='uploads/' + user.foto)}")

    # trata upload de foto de perfil
    if request.method == 'POST':
        if 'foto' not in request.files:
            flash('Nenhum arquivo selecionado.', 'warning')
            return redirect(url_for('auth.profile'))

        file = request.files['foto']
        if file and file.filename:
            from werkzeug.utils import secure_filename
            import os

            # validações simples
            ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            MAX_BYTES = 2 * 1024 * 1024  # 2 MB

            filename = secure_filename(file.filename)
            _, ext = os.path.splitext(filename)
            ext = ext.lower().lstrip('.')

            if ext not in ALLOWED_EXT:
                flash('Extensão não permitida. Use png, jpg, jpeg, gif ou webp.', 'danger')
                return redirect(url_for('auth.profile'))

            # tenta validar tamanho do arquivo (pode falhar em alguns storages)
            try:
                file.stream.seek(0, os.SEEK_END)
                size = file.stream.tell()
                file.stream.seek(0)
            except Exception:
                size = None

            if size and size > MAX_BYTES:
                flash('Arquivo muito grande. Máximo 2 MB.', 'danger')
                return redirect(url_for('auth.profile'))

            import time
            # include timestamp to avoid browser cache issues when replacing the same filename
            new_filename = f"user_{user.id}_{int(time.time())}.{ext}"

            # Debug: imprime os caminhos para verificar
            print(f"Static folder: {current_app.static_folder}")
            print(f"Static URL path: {current_app.static_url_path}")
            
            upload_folder = os.path.join(current_app.static_folder, 'uploads')
            os.makedirs(upload_folder, exist_ok=True)

            save_path = os.path.join(upload_folder, new_filename)
            try:
                file.save(save_path)
                # optionally remove previous image file to avoid accumulating files
                try:
                    if user.foto:
                        old_path = os.path.join(upload_folder, user.foto)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                except Exception:
                    pass

                user.foto = new_filename
                db.session.commit()
                flash('Foto de perfil atualizada com sucesso.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao salvar a foto: {str(e)}', 'danger')

        return redirect(url_for('auth.profile'))

    return render_template('profile.html', user=user)

