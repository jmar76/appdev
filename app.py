from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_cors import CORS
import db
from models import Tarea
from models import Sinergias
from models import Registro
from datetime import datetime

app = Flask(__name__)
CORS(app)

# La barra (el slash) se conoce como la página de inicio (página home).
# Vamos a definir para esta ruta, el comportamiento a seguir.
@app.route('/index')
def home():
    if "email" in session:
        todas_las_tareas = db.session.query(Tarea).all()  # Consultamos y almacenamos todas las tareas de la base de datos
        tarea_uno = db.session.query(Tarea).filter_by(id=1)
        tarea_dos = db.session.query(Tarea).filter_by(id=2)
        tarea_tres = db.session.query(Tarea).filter_by(id=3)
        tarea_cuatro = db.session.query(Tarea).filter_by(id=4)
        tarea_cinco = db.session.query(Tarea).filter_by(id=5)
        tarea_seis = db.session.query(Tarea).filter_by(id=6)
        tarea_siete = db.session.query(Tarea).filter_by(id=7)
        tarea_ocho = db.session.query(Tarea).filter_by(id=8)
        tarea_nueve = db.session.query(Tarea).filter_by(id=9)
        comentarios = db.session.query(Sinergias).all()
        username = db.session.query(Registro).filter_by(email=session["email"]).all()
        # Ahora en la variable todas_las_tareas se tienen almacenadas todas las tareas. Vamos a entregar esta variable al template index.html
        return render_template("index.html", lista_de_tareas=todas_las_tareas, tarea_uno=tarea_uno,
                               tarea_dos=tarea_dos, tarea_tres=tarea_tres, tarea_cuatro=tarea_cuatro,
                               tarea_cinco=tarea_cinco, tarea_seis=tarea_seis, tarea_siete=tarea_siete,
                               tarea_ocho=tarea_ocho, tarea_nueve=tarea_nueve, comentarios=comentarios, username=username)
    else:
        return render_template("login.html")

@app.route('/crear-tarea', methods = ['POST'])
def crear():
    tarea = Tarea(contenido= request.form['contenido_tarea'], hecha=False, nombre= request.form['desarrolladores'], fecha =datetime.now() )# id no es necesario asignarlo manualmente, porque la primary key se genera automáticamente
    db.session.add(tarea)  # Añadir el objeto de Tarea a la base de datos
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    db.session.close()#cierra la base de datos
    return redirect(url_for('home')) # Esto nos redirecciona a la función home()

@app.route('/comentarios', methods = ['POST'])
def comentarios():
    agregar = Sinergias(nombre= request.form['nombre'], titulo= request.form['titulo'], comentarios= request.form['comentarios'], fecha =datetime.now() )# id no es necesario asignarlo manualmente, porque la primary key se genera automáticamente
    db.session.add(agregar)  # Añadir el objeto de Tarea a la base de datos
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    db.session.close()#cierra la base de datos
    flash("hola")
    return redirect(url_for('home')) # Esto nos redirecciona a la función home()

@app.route('/eliminar-comentario/<id>')
def eliminar_comentario(id):
    eliminar_comentario = db.session.query(Sinergias).filter_by(id=int(id)).delete() # Se busca dentro de la base de datos, aquel registro cuyo id coincida con el aportado por el parametro de la ruta. Cuando se encuentra se elimina
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    db.session.close()  # cierra la base de datos
    return redirect(url_for('home'))

@app.route('/eliminar-tarea/<id>')
def eliminar(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).delete() # Se busca dentro de la base de datos, aquel registro cuyo id coincida con el aportado por el parametro de la ruta. Cuando se encuentra se elimina
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    db.session.close()  # cierra la base de datos
    return redirect(url_for('home')) # Esto nos redirecciona a la función home(), y si todo ha ido bien, al refrescar, la tarea eliminada ya no aparecera en el listado

@app.route('/eliminar-toda-tarea')
def eliminar_todas():
    tarea = db.session.query(Tarea).delete() # Se busca dentro de la base de datos, aquel registro cuyo id coincida con el aportado por el parametro de la ruta. Cuando se encuentra se elimina
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    db.session.close()  # cierra la base de datos
    return redirect(url_for('home')) # Esto nos redirecciona a la función home(), y si todo ha ido bien, al refrescar, la tarea eliminada ya no aparecera en el listado

@app.route('/modificar-tarea', methods = ['POST'])
def modificar():
    modificar_nombre = db.session.query(Tarea).filter_by(id=int(request.form['id'])).first() # Se busca dentro de la base de datos, aquel registro cuyo id coincida con el aportado por el parametro de la ruta. Cuando se encuentra se elimina
    modificar_nombre.nombre = request.form['nuevo_desarrolladores']
    modificar_nombre.contenido = request.form['nuevo_contenido_tarea']
    db.session.add(modificar_nombre)
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    db.session.close()  # cierra la base de datos
    return redirect(url_for('home')) # Esto nos redirecciona a la función home(), y si todo ha ido bien, al refrescar, la tarea eliminada ya no aparecera en el listado

@app.route('/mover-id/<id>', methods = ['POST'])
def modificar_comentario(id):
    operar = db.session.query(Sinergias).filter_by(id=int(id)).first()
    operar.comentarios = request.form['modifica']
    operar.fecha = datetime.now()
    db.session.add(operar)
    db.session.commit()  # Ejecutar la operación pendiente de la base de datos
    db.session.close()  # cierra la base de datos
    return redirect(url_for('home'))

@app.route('/tarea-hecha/<id>')
def hecha(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first() # Se obtiene la tarea que se busca
    tarea.hecha = not(tarea.hecha) # Guardamos en la variable booleana de la tarea, su contrario
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    db.session.close()  # cierra la base de datos
    return redirect(url_for('home'))# Esto nos redirecciona a la función home()

@app.route('/registro', methods = ['POST'])
def registro():
    registro = Registro(username=request.form['username'],
                        email=request.form['email'],
                        password=request.form['password'])
    db.session.add(registro)  # Añadir el objeto de Tarea a la base de datos
    db.session.commit()  # Ejecutar la operación pendiente de la base de datos
    db.session.close()  # cierra la base de datos
    flash("Usuario registrado correctamente!")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("email", None)
    return render_template("login.html")

@app.route('/', methods = ['POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = db.session.query(Registro).filter_by(email=email).first()

        if user is not None and user.verify_password(password):
            session["email"] = email
            return redirect(url_for('home'))
        else:
            flash("Email o Password incorrectos, pruebe de nuevo!")
            return render_template("login.html")

@app.route('/registro_url')
def registro_url():
    return render_template("registro.html")

@app.route('/')
def login_url():
    return render_template("login.html")

if __name__ == '__main__':
    app.secret_key = 'gf468rghrghrtgh6&!2kghbmjfh'

    db.Base.metadata.create_all(db.engine)  # Creamos el modelo de datos
    app.run(debug=True) # El debug=True hace que cada vez que reiniciemos el servidor o modifiquemos codigo,
# el servidor de Flask se reinicie solo
