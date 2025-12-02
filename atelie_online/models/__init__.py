from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar todos os modelos para que o SQLAlchemy os reconheça
from .material_model import Material
