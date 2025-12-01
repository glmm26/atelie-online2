from flask import Blueprint, render_template, request, redirect, url_for, flash
from atelie_online.models.material_model import Material
from atelie_online.models import db

material_bp = Blueprint('materiais', __name__, template_folder='../templates')

@material_bp.route('/materiais', methods=['GET'])
def listar_materiais():
    materiais = Material.query.all()
    return render_template('listar_materiais.html', materiais=materiais)

@material_bp.route('/materiais/cadastrar', methods=['GET', 'POST'])
def cadastrar_material():
    if request.method == 'POST':
        nome = request.form.get('nome')
        quantidade = request.form.get('quantidade')
        unidade_medida = request.form.get('unidade_medida')
        descricao = request.form.get('descricao')
        preco_unitario = request.form.get('preco_unitario')
        
        try:
            quantidade = int(quantidade)
            preco_unitario = float(preco_unitario) if preco_unitario else None
        except ValueError:
            flash('Quantidade deve ser um número inteiro e preço deve ser um número válido', 'danger')
            return redirect(url_for('materiais.cadastrar_material'))
        
        material = Material(
            nome=nome,
            quantidade=quantidade,
            unidade_medida=unidade_medida,
            descricao=descricao,
            preco_unitario=preco_unitario
        )
        
        try:
            db.session.add(material)
            db.session.commit()
            flash('Material cadastrado com sucesso!', 'success')
            return redirect(url_for('materiais.listar_materiais'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar material: {str(e)}', 'danger')
            return redirect(url_for('materiais.cadastrar_material'))
            
    return render_template('cadastrar_material.html')

@material_bp.route('/materiais/editar/<int:id>', methods=['GET', 'POST'])
def editar_material(id):
    material = Material.query.get_or_404(id)
    
    if request.method == 'POST':
        material.nome = request.form.get('nome')
        material.quantidade = int(request.form.get('quantidade'))
        material.unidade_medida = request.form.get('unidade_medida')
        material.descricao = request.form.get('descricao')
        preco = request.form.get('preco_unitario')
        material.preco_unitario = float(preco) if preco else None
        
        try:
            db.session.commit()
            flash('Material atualizado com sucesso!', 'success')
            return redirect(url_for('materiais.listar_materiais'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar material: {str(e)}', 'danger')
    
    return render_template('editar_material.html', material=material)

@material_bp.route('/materiais/excluir/<int:id>', methods=['POST'])
def excluir_material(id):
    material = Material.query.get_or_404(id)
    try:
        db.session.delete(material)
        db.session.commit()
        flash('Material excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir material: {str(e)}', 'danger')
    return redirect(url_for('materiais.listar_materiais'))