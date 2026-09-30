from flask import Blueprint, render_template
from app.services.projects_service import obtener_portafolio_publico, obtener_proyecto_por_id

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

@portfolio_bp.route('/')
def index():
    proyectos = obtener_portafolio_publico()
    return render_template('portafolio/index.html', proyectos=proyectos)

@portfolio_bp.route('/<int:id_app>')
def detail(id_app):
    proyecto = obtener_proyecto_por_id(id_app)
    return render_template('portafolio/detail.html', proyecto=proyecto)