import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, session, redirect, url_for, jsonify

from app.utils.decorators import role_required

from app.services.orders_service import (
    obtener_clientes,
    obtener_aplicaciones,
    crear_solicitud_cliente,
    obtener_solicitudes_pendientes
)
from app.services.dev_service import (
    obtener_desarrolladores,
    obtener_proyectos_por_dev,
    asignar_dev_a_proyecto,
    crear_nuevo_desarrollador,
    obtener_desarrollador_por_credenciales,
    obtener_desarrollador_por_id,
    actualizar_desarrollador,
    eliminar_desarrollador
)
from app.services.projects_service import (
    obtener_portafolio_publico,
    obtener_proyecto_por_id,
    crear_nuevo_proyecto,
    actualizar_proyecto,
    eliminar_proyecto
)

base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.getenv('SECRET_KEY', 'super-secret-key-appforge')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        detalles = request.form.get('detalles')

        resultado = crear_solicitud_cliente(nombre, telefono, email, detalles)
        
        return jsonify({
            'exito': resultado.get("exito", False),
            'password_temporal': resultado.get("password_temporal"),
            'datos': {
                'nombre': nombre,
                'email': email,
                'telefono': telefono,
                'detalles': detalles
            }
        })

    return render_template('contact.html')

@app.route('/portafolio')
def portafolio():
    apps = obtener_portafolio_publico()
    return render_template('portafolio/index.html', aplicaciones=apps)

@app.route('/portafolio/detalle/<int:id_app>')
def portafolio_detalle(id_app):
    proyecto = obtener_proyecto_por_id(id_app)
    return render_template('portafolio/detail.html', proyecto=proyecto)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif session['role'] == 'dev':
            return redirect(url_for('dev_dashboard'))
        elif session['role'] == 'cliente':
            return redirect(url_for('cliente_dashboard'))

    if request.method == 'POST':
        rol = request.form.get('rol')
        email = request.form.get('email')
        password = request.form.get('password')

        if rol == 'admin':
            admin_key = request.form.get('master_key')
            master_key = os.getenv('ADMIN_MASTER_KEY', 'ForgeAdmin2026!')
            if admin_key != master_key:
                return render_template('admin/login.html', error="Clave Maestra de Administrador incorrecta.")

            session['user'] = email
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))

        elif rol == 'dev':
            dev = obtener_desarrollador_por_credenciales(email, password)
            if dev:
                session['user'] = dev.get('email')
                session['role'] = 'dev'
                session['dev_id'] = dev.get('id_desarrollador')
                return redirect(url_for('dev_dashboard'))
            else:
                return render_template('admin/login.html', error="Correo o contraseña de desarrollador incorrectos.")

        elif rol == 'cliente':
            session['user'] = email
            session['role'] = 'cliente'
            return redirect(url_for('cliente_dashboard'))

    return render_template('admin/login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    solicitudes = obtener_solicitudes_pendientes()
    return render_template('admin/dashboard.html', solicitudes=solicitudes)

@app.route('/admin/assign/<int:id_app>', methods=['GET', 'POST'])
@role_required('admin')
def admin_assign(id_app):
    if request.method == 'POST':
        id_dev = request.form.get('id_desarrollador')
        rol = request.form.get('rol')
        horas = request.form.get('horas_dedicadas')
        asignar_dev_a_proyecto(id_app, id_dev, rol, horas)
        return redirect(url_for('admin_dashboard'))

    desarrolladores = obtener_desarrolladores()
    proyecto = obtener_proyecto_por_id(id_app)  
    return render_template('admin/assign_dev.html', id_app=id_app, proyecto=proyecto, desarrolladores=desarrolladores)

    desarrolladores = obtener_desarrolladores()
    return render_template('admin/assign_dev.html', id_app=id_app, desarrolladores=desarrolladores)

@app.route('/admin/projects')
@role_required('admin')
def admin_projects():
    proyectos = obtener_aplicaciones()
    return render_template('admin/projects.html', proyectos=proyectos)

@app.route('/admin/new-project', methods=['GET', 'POST'])
@role_required('admin')
def admin_new_project():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        estado = request.form.get('estado')
        fecha_inicio = request.form.get('fecha_inicio')
        es_publico = True if request.form.get('es_publico_portafolio') else False
        
        imagen_portada = request.files.get('imagen_portada')
        imagen_url = None
        if imagen_portada and imagen_portada.filename != '':
            imagen_url = imagen_portada.filename

        crear_nuevo_proyecto(nombre, descripcion, fecha_inicio, es_publico, imagen_url)
        return redirect(url_for('admin_projects'))

    desarrolladores = obtener_desarrolladores()
    return render_template('admin/new_project.html', desarrolladores=desarrolladores)

@app.route('/admin/projects/edit/<int:id_app>', methods=['GET', 'POST'])
@role_required('admin')
def admin_edit_project(id_app):
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        estado = request.form.get('estado')
        fecha_inicio = request.form.get('fecha_inicio')
        es_publico = True if request.form.get('es_publico_portafolio') else False

        nueva_imagen = request.files.get('nueva_imagen')
        imagen_url = None
        if nueva_imagen and nueva_imagen.filename != '':
            filename = nueva_imagen.filename
            filepath = os.path.join(static_dir, 'imagenes', filename)
            nueva_imagen.save(filepath)
            imagen_url = filename

        actualizar_proyecto(id_app, nombre, descripcion, estado, fecha_inicio, imagen_url, es_publico)
        return redirect(url_for('admin_projects'))

    proyecto = obtener_proyecto_por_id(id_app)
    return render_template('admin/edit_project.html', proyecto=proyecto)

@app.route('/admin/projects/delete/<int:id_app>', methods=['POST'])
@role_required('admin')
def admin_delete_project(id_app):
    eliminar_proyecto(id_app)
    return redirect(url_for('admin_projects'))

@app.route('/admin/devs')
@role_required('admin')
def admin_devs():
    programadores = obtener_desarrolladores()
    return render_template('admin/devs.html', programadores=programadores, devs=programadores)

@app.route('/admin/devs/edit/<int:id_dev>', methods=['GET', 'POST'])
@role_required('admin')
def admin_edit_dev(id_dev):
    if request.method == 'POST':
        nombre = request.form.get('nombre_completo')
        especialidad = request.form.get('especialidad')
        email = request.form.get('email')

        actualizar_desarrollador(id_dev, nombre, especialidad, email)
        return redirect(url_for('admin_devs'))

    dev = obtener_desarrollador_por_id(id_dev)
    return render_template('admin/edit_dev.html', dev=dev)

@app.route('/admin/devs/delete/<int:id_dev>', methods=['POST'])
@role_required('admin')
def admin_delete_dev(id_dev):
    eliminar_desarrollador(id_dev)
    return redirect(url_for('admin_devs'))

@app.route('/admin/new-dev', methods=['GET', 'POST'])
@role_required('admin')
def admin_new_dev():
    if request.method == 'POST':
        nombre = request.form.get('nombre_completo') or request.form.get('nombre')
        especialidad = request.form.get('especialidad')
        email = request.form.get('email') or request.form.get('correo')
        contrasena = request.form.get('contrasena')

        crear_nuevo_desarrollador(nombre, especialidad, email, contrasena)
        return redirect(url_for('admin_devs'))

    return render_template('admin/new_dev.html')

@app.route('/dev/dashboard')
@role_required('dev')
def dev_dashboard():
    dev_id = session.get('dev_id', 1)
    mis_proyectos = obtener_proyectos_por_dev(dev_id)
    return render_template('dev/dashboard.html', mis_proyectos=mis_proyectos)

@app.route('/cliente/dashboard')
@role_required('cliente')
def cliente_dashboard():
    return render_template('cliente/dashboard.html')

@app.route('/cliente/enviar-mensaje', methods=['POST'])
@role_required('cliente', 'dev')
def enviar_mensaje():
    mensaje = request.form.get('mensaje')
    return redirect(url_for('cliente_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)