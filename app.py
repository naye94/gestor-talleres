# -*- coding: utf-8 -*-
import sys
import os

# Aseguramos los paths para que las importaciones no fallen
ruta_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(ruta_actual))

from flask import Flask, render_template, request, redirect, url_for, flash, session
from modelo.usuarioDao import UsuarioDao
from controlador.tallerController import TallerController
from controlador.servicioController import ServicioController
from controlador.mecanicoController import MecanicoController
from controlador.vehiculoController import VehiculoController
from controlador.clienteController import ClienteController

# SOLUCIÓN DE RUTA ABSOLUTA: Forzamos a Flask a buscar exactamente en la carpeta 'vista'
ruta_vistas = os.path.join(ruta_actual, 'vista')
ruta_templates = os.path.join(ruta_vistas, 'templates')

app = Flask(__name__)
# Le decimos a Flask que busque los HTML en ambas carpetas
app.jinja_loader.searchpath = [ruta_vistas, ruta_templates]
app.secret_key = 'miclavesecretataller'

# Instancias de los controladores
taller_controller = TallerController()
servicio_controller = ServicioController()
mecanico_controller = MecanicoController()
vehiculo_controller = VehiculoController()
cliente_controller = ClienteController()

# ========================================================
# 🔐 BLINDAJE DE RUTAS GLOBAL (BEFORE REQUEST)
# ========================================================
@app.before_request
def verificar_autenticacion():
    # Permitimos rutas públicas sin exigir logueo
    rutas_publicas = ['login', 'login_mecanico', 'static']
    if request.endpoint in rutas_publicas:
        return

    # Si se intenta entrar al flujo de mecánicos, validamos su sesión específica
    if request.endpoint and request.endpoint.startswith('mecanico') or request.endpoint == 'menu_mecanico':
        if 'mecanico_id' not in session:
            flash('Debes iniciar sesión como mecánico para acceder.', 'danger')
            return redirect(url_for('login_mecanico'))
        return

    # Para cualquier otra ruta del sistema (Administrador), validamos la sesión de Supabase
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

# ==========================================
# RUTAS DE AUTENTICACIÓN (SUPABASE)
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('txtEmail')
        password = request.form.get('txtPassword')
        
        auth_response = UsuarioDao.iniciar_sesion(email, password)
        
        # Validación nativa para objetos de respuesta de Supabase Auth
        if auth_response and hasattr(auth_response, 'user') and auth_response.user:
            session['usuario_id'] = auth_response.user.id
            return redirect(url_for('index'))
            
        # Si llega aquí, es porque la autenticación falló en Supabase o los datos no coinciden
        return render_template('login.html', error="Correo o contraseña incorrectos")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Sesión de administrador cerrada correctamente.', 'info')
    return redirect(url_for('login'))

# ==========================================
# RUTAS PRINCIPALES Y CRUD TALLERES
# ==========================================

@app.route('/')
def index():
    talleres = taller_controller.obtener_todos()
    return render_template('index.html', talleres=talleres)

@app.route('/taller/crear', methods=['POST'])
def crear_taller():
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    try:
        taller_controller.crear_taller(type('Taller', (), {
            'nombre': nombre,
            'direccion': direccion,
            'telefono': telefono
        })())
        flash('Taller creado exitosamente.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('index'))

@app.route('/taller/editar/<int:id_taller>', methods=['POST'])
def editar_taller(id_taller):
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    try:
        taller_controller.actualizar_taller(id_taller, nombre, direccion, telefono)
        flash('Taller actualizado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('index'))

@app.route('/taller/eliminar/<int:id_taller>', methods=['POST'])
def eliminar_taller(id_taller):
    try:
        taller_controller.borrar_taller(id_taller)
        flash('Taller eliminado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('index'))

@app.route('/buscar_taller', methods=['GET'])
def buscar_taller():
    nombre = request.args.get('nombre', '')
    talleres = [t for t in taller_controller.obtener_todos() if nombre.lower() in t[1].lower()]
    return render_template('index.html', talleres=talleres, nombre_busqueda=nombre)

@app.route('/taller/<int:id_taller>/gestionar', methods=['GET'])
def gestionar_taller(id_taller):
    taller = taller_controller.obtener_taller(id_taller)
    servicios = [s for s in servicio_controller.obtener_todos() if s[4] == id_taller]
    mecanicos = [m for m in mecanico_controller.obtener_todos() if m[5] == id_taller]
    vehiculos = [v for v in vehiculo_controller.obtener_todos() if v[6] == id_taller]
    clientes = cliente_controller.obtener_todos()
    nombre_busqueda = request.args.get('nombre', '')
    nombre_busqueda_mecanico = request.args.get('nombre_mecanico', '')
    nombre_busqueda_vehiculo = request.args.get('nombre_vehiculo', '')
    tab = request.args.get('tab', 'servicio')
    if nombre_busqueda:
        servicios = [s for s in servicios if nombre_busqueda.lower() in s[1].lower()]
    if nombre_busqueda_mecanico:
        mecanicos = [m for m in mecanicos if nombre_busqueda_mecanico.lower() in m[1].lower()]
    if nombre_busqueda_vehiculo:
        vehiculos = [v for v in vehiculos if nombre_busqueda_vehiculo.lower() in v[2].lower()]
    return render_template(
        'gestionar_taller.html',
        taller=taller,
        servicios=servicios,
        nombre_busqueda=nombre_busqueda,
        mecanicos=mecanicos,
        nombre_busqueda_mecanico=nombre_busqueda_mecanico,
        vehiculos=vehiculos,
        nombre_busqueda_vehiculo=nombre_busqueda_vehiculo,
        clientes=clientes,
        tab=tab
    )

# ==========================================
# CRUD SERVICIOS
# ==========================================

@app.route('/taller/<int:id_taller>/servicio/crear', methods=['POST'])
def crear_servicio(id_taller):
    from modelo.servicio import Servicio
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    costo = request.form['costo']
    try:
        servicio_controller.crear_servicio(Servicio(nombre, descripcion, costo, id_taller))
        flash('Servicio creado exitosamente.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('gestionar_taller', id_taller=id_taller))

@app.route('/taller/<int:id_taller>/servicio/editar/<int:id_servicio>', methods=['POST'])
def editar_servicio(id_taller, id_servicio):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    costo = request.form['costo']
    try:
        servicio_controller.actualizar_servicio(id_servicio, nombre, descripcion, costo, id_taller)
        flash('Servicio actualizado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('gestionar_taller', id_taller=id_taller))

@app.route('/taller/<int:id_taller>/servicio/eliminar/<int:id_servicio>', methods=['POST'])
def eliminar_servicio(id_taller, id_servicio):
    try:
        servicio_controller.borrar_servicio(id_servicio)
        flash('Servicio eliminado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('gestionar_taller', id_taller=id_taller))

# ==========================================
# CRUD MECÁNICOS
# ==========================================

@app.route('/taller/<int:id_taller>/mecanico/crear', methods=['POST'])
def crear_mecanico(id_taller):
    from modelo.mecanico import Mecanico
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    especialidad = request.form['especialidad']
    telefono = request.form['telefono']
    try:
        mecanico_controller.crear_mecanico(Mecanico(nombre, apellido, especialidad, telefono, id_taller))
        flash('Mecánico creado exitosamente.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('gestionar_taller', id_taller=id_taller, tab='mecanico'))

@app.route('/taller/<int:id_taller>/mecanico/editar/<int:id_mecanico>', methods=['POST'])
def editar_mecanico(id_taller, id_mecanico):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    especialidad = request.form['especialidad']
    telefono = request.form['telefono']
    try:
        mecanico_controller.actualizar_mecanico(id_mecanico, nombre, apellido, especialidad, telefono)
        flash('Mecánico actualizado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('gestionar_taller', id_taller=id_taller, tab='mecanico'))

@app.route('/taller/<int:id_taller>/mecanico/eliminar/<int:id_mecanico>', methods=['POST'])
def eliminar_mecanico(id_taller, id_mecanico):
    try:
        mecanico_controller.eliminar_mecanico(id_mecanico)
        flash('Mecánico eliminado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('gestionar_taller', id_taller=id_taller, tab='mecanico'))

# ==========================================
# CRUD VEHÍCULOS Y CLIENTES
# ==========================================

@app.route('/taller/<int:id_taller>/vehiculo/crear', methods=['POST'])
def crear_vehiculo(id_taller):
    from modelo.vehiculo import Vehiculo
    placa = request.form['placa']
    marca = request.form['marca']
    modelo_v = request.form['modelo']
    color = request.form['color']
    id_cliente = request.form['id_cliente']
    try:
        vehiculo_controller.crear_vehiculo(Vehiculo(placa, marca, modelo_v, color, id_cliente, id_taller))
        flash('Vehículo creado exitosamente.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('gestionar_taller', id_taller=id_taller, tab='vehiculo'))

@app.route('/taller/<int:id_taller>/vehiculo/editar/<int:id_vehiculo>', methods=['POST'])
def editar_vehiculo(id_taller, id_vehiculo):
    placa = request.form['placa']
    marca = request.form['marca']
    modelo_v = request.form['modelo']
    color = request.form['color']
    id_cliente = request.form['id_cliente']
    try:
        vehiculo_controller.actualizar_vehiculo(id_vehiculo, placa, marca, modelo_v, color, id_cliente, id_taller)
        flash('Vehículo actualizado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('gestionar_taller', id_taller=id_taller, tab='vehiculo'))

@app.route('/taller/<int:id_taller>/vehiculo/eliminar/<int:id_vehiculo>', methods=['POST'])
def eliminar_vehiculo(id_taller, id_vehiculo):
    try:
        vehiculo_controller.borrar_vehiculo(id_vehiculo)
        flash('Vehículo eliminado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('gestionar_taller', id_taller=id_taller, tab='vehiculo'))

@app.route('/cliente/editar/<int:id_cliente>', methods=['POST'])
def editar_cliente(id_cliente):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    correo = request.form['correo']
    try:
        cliente_controller.actualizar_cliente(id_cliente, nombre, apellido, telefono, correo)
        flash('Cliente actualizado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    id_taller = request.args.get('id_taller')
    return redirect(url_for('gestionar_taller', id_taller=id_taller, tab='vehiculo'))

@app.route('/cliente/eliminar/<int:id_cliente>', methods=['POST'])
def eliminar_cliente(id_cliente):
    try:
        cliente_controller.borrar_cliente(id_cliente)
        flash('Cliente eliminado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    id_taller = request.args.get('id_taller')
    return redirect(url_for('gestionar_taller', id_taller=id_taller, tab='vehiculo'))

# ==========================================
# INTERFAZ Y RUTAS DEL MECÁNICO
# ==========================================

@app.route('/login_mecanico', methods=['GET', 'POST'])
def login_mecanico():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        mecanicos = mecanico_controller.obtener_todos()
        mecanico = next((m for m in mecanicos if m[1] == nombre and m[2] == apellido and m[4] == telefono), None)
        if mecanico:
            session['mecanico_id'] = mecanico[0]
            session['id_taller'] = mecanico[5]
            flash('Bienvenido, {} {}'.format(mecanico[1], mecanico[2]), 'success')
            return redirect(url_for('menu_mecanico'))
        else:
            flash('Credenciales incorrectas.', 'danger')
    return render_template('login_mecanico.html')

@app.route('/logout_mecanico')
def logout_mecanico():
    session.pop('mecanico_id', None)
    session.pop('id_taller', None)
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('login_mecanico'))

@app.route('/menu_mecanico', methods=['GET', 'POST'])
def menu_mecanico():
    id_taller = session['id_taller']
    tab = request.args.get('tab', 'servicio')
    nombre_servicio = request.args.get('nombre_servicio', '')
    nombre_vehiculo = request.args.get('nombre_vehiculo', '')
    nombre_cliente = request.args.get('nombre_cliente', '')
    servicios = [s for s in servicio_controller.obtener_todos() if s[4] == id_taller]
    vehiculos = [v for v in vehiculo_controller.obtener_todos() if v[6] == id_taller]
    clientes = cliente_controller.obtener_todos()
    if nombre_servicio:
        servicios = [s for s in servicios if nombre_servicio.lower() in s[1].lower()]
    if nombre_vehiculo:
        vehiculos = [v for v in vehiculos if nombre_vehiculo.lower() in v[2].lower()]
    if nombre_cliente:
        clientes = [c for c in clientes if nombre_cliente.lower() in c[1].lower()]
    return render_template(
        'menu_mecanico.html',
        servicios=servicios,
        vehiculos=vehiculos,
        clientes=clientes,
        tab=tab,
        nombre_servicio=nombre_servicio,
        nombre_vehiculo=nombre_vehiculo,
        nombre_cliente=nombre_cliente
    )

@app.route('/mecanico/servicio/crear', methods=['POST'])
def mecanico_crear_servicio():
    from modelo.servicio import Servicio
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    costo = request.form['costo']
    id_taller = session['id_taller']
    try:
        servicio_controller.crear_servicio(Servicio(nombre, descripcion, costo, id_taller))
        flash('Servicio creado exitosamente.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('menu_mecanico', tab='servicio'))

@app.route('/mecanico/servicio/editar/<int:id_servicio>', methods=['POST'])
def mecanico_editar_servicio(id_servicio):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    costo = request.form['costo']
    id_taller = session['id_taller']
    try:
        servicio_controller.actualizar_servicio(id_servicio, nombre, descripcion, costo, id_taller)
        flash('Servicio actualizado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('menu_mecanico', tab='servicio'))

@app.route('/mecanico/servicio/eliminar/<int:id_servicio>', methods=['POST'])
def mecanico_eliminar_servicio(id_servicio):
    try:
        servicio_controller.borrar_servicio(id_servicio)
        flash('Servicio eliminado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('menu_mecanico', tab='servicio'))

@app.route('/mecanico/vehiculo/crear', methods=['POST'])
def mecanico_crear_vehiculo():
    from modelo.vehiculo import Vehiculo
    placa = request.form['placa']
    marca = request.form['marca']
    modelo_v = request.form['modelo']
    color = request.form['color']
    id_cliente = request.form['id_cliente']
    id_taller = session['id_taller']
    try:
        vehiculo_controller.crear_vehiculo(Vehiculo(placa, marca, modelo_v, color, id_cliente, id_taller))
        flash('Vehículo creado exitosamente.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('menu_mecanico', tab='vehiculo'))

@app.route('/mecanico/vehiculo/editar/<int:id_vehiculo>', methods=['POST'])
def mecanico_editar_vehiculo(id_vehiculo):
    placa = request.form['placa']
    marca = request.form['marca']
    modelo_v = request.form['modelo']
    color = request.form['color']
    id_cliente = request.form['id_cliente']
    id_taller = session['id_taller']
    try:
        vehiculo_controller.actualizar_vehiculo(id_vehiculo, placa, marca, modelo_v, color, id_cliente, id_taller)
        flash('Vehículo actualizado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('menu_mecanico', tab='vehiculo'))

@app.route('/mecanico/vehiculo/eliminar/<int:id_vehiculo>', methods=['POST'])
def mecanico_eliminar_vehiculo(id_vehiculo):
    try:
        vehiculo_controller.borrar_vehiculo(id_vehiculo)
        flash('Vehículo eliminado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('menu_mecanico', tab='vehiculo'))

@app.route('/mecanico/cliente/crear', methods=['POST'])
def mecanico_crear_cliente():
    from modelo.cliente import Cliente
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    correo = request.form['correo']
    try:
        cliente_controller.crear_cliente(Cliente(nombre, apellido, telefono, correo))
        flash('Cliente creado exitosamente.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('menu_mecanico', tab='cliente'))

@app.route('/mecanico/cliente/editar/<int:id_cliente>', methods=['POST'])
def mecanico_editar_cliente(id_cliente):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    correo = request.form['correo']
    try:
        cliente_controller.actualizar_cliente(id_cliente, nombre, apellido, telefono, correo)
        flash('Cliente actualizado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('menu_mecanico', tab='cliente'))

@app.route('/mecanico/cliente/eliminar/<int:id_cliente>', methods=['POST'])
def mecanico_eliminar_cliente(id_cliente):
    try:
        cliente_controller.borrar_cliente(id_cliente)
        flash('Cliente eliminado.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('menu_mecanico', tab='cliente'))

if __name__ == '__main__':
    # 🌐 Render asigna un puerto dinámico mediante la variable de entorno
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto, debug=False)
