from flask import Flask, request, render_template, url_for, jsonify, session
from werkzeug.utils import redirect
from werkzeug.exceptions import abort

app = Flask(__name__)

app.secret_key = 'Mi_llave_secreta'


@app.route('/')
def index():
    if 'username' in session:
        return f'El usuario ya ha hecho login {session["username"]}'
    else:
        return 'NO HA HECHO LOGIN'
    # app.logger.debug('Mensaje a nivel debug')
    # app.logger.info('Mensaje a nivel info')
    # app.logger.warning('Mensaje a nivel warning') # sio esta en produccion se muestra desde warning hacia adelante
    # app.logger.error('Mensaje a nivel error')

    app.logger.info(f'Entramos al path {request.path}')

    return 'Hola Mundo desde Flask.'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Omitimos validacion de usuario y password
        usuario = request.form['username']
        #agregar el usuario a la sesion
        session['username'] = usuario
        # session['password'] = request.form['password']
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))


@app.route('/saludar/<nombre>')
def saludar(nombre):
    return f'Saludos {nombre.upper()}'


@app.route('/edad/<int:edad>')
def mostrar_edad(edad):
    return f'Tu edad es: {edad}'


@app.route('/mostrar/<nombre>', methods=['GET', 'POST'])
def mostrar_nombre(nombre):
    # return f'Tu nombre es: {nombre}'
    return render_template('mostrar.html', nombre=nombre)


@app.route('/redireccionar')
def redireccionar():
    return redirect(url_for('mostrar_nombre', nombre='Juan'))


@app.route('/salir')
def salir():
    return abort(404)


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('error404.html', error=error), 404


# REST Representational state transfer
@app.route('/api/mostrar/<nombre>', methods=['GET', 'POST'])
def mostrar_json(nombre):
    valores = {'nombre': nombre, 'metodo_http': request.method}
    return jsonify(valores)




if __name__ == '__main__':
    app.run(debug=True, port=5000)
