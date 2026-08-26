from flask import Flask, render_template
from app.services.orders_service import (
    obtener_clientes,
    obtener_aplicaciones,
    obtener_desarrolladores,
    obtener_detalles_proyecto
)

app = Flask(__name__, template_folder='app/templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/success')
def success():
    return render_template('sucess.html')

@app.route('/portafolio')
def portafolio():
    apps = obtener_aplicaciones()
    return render_template('portafolio/index.html', aplicaciones=apps)

@app.route('/portafolio/detalle/<int:id_app>')
def portafolio_detalle(id_app):
    detalles = obtener_detalles_proyecto()
    equipo = [d for d in detalles if d.get('id_app') == id_app]
    return render_template('portafolio/detail.html', equipo=equipo, id_app=id_app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)