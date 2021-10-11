import db
import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class Tarea(db.Base):
    __tablename__ = "tarea"
    id = Column(Integer, primary_key=True) # Identificador único de cada tarea (no puede haber dos tareas con el mismo id, por eso es primary key)
    contenido = Column(String(20), nullable=False) # Contenido de la tarea, un texto de máximo 200 caracteres
    hecha = Column(Boolean) # Booleano que indica si una tarea ha sido hecha o no
    nombre = Column(String(10), nullable=False)
    fecha = Column(String(200), nullable=False)

    def __init__(self, contenido, hecha, nombre,fecha): # Recordemos que el id no es necesario crearlo manualmente, lo añade la base de datos automaticamente
        self.contenido = contenido
        self.hecha = hecha
        self.nombre = nombre
        self.fecha = fecha

    def __repr__(self):
        return "Tarea {}: {} ({})".format(self.id, self.contenido, self.hecha,self.nombre, self.fecha)
    def __str__(self):
        return "Tarea {}: {} ({})".format(self.id, self.contenido, self.hecha,self.nombre, self.fecha )

class Sinergias(db.Base):
    __tablename__ = "sinergia"
    id = Column(Integer, primary_key=True) # Identificador único de cada tarea (no puede haber dos tareas con el mismo id, por eso es primary key)
    nombre = Column(String(100), nullable=False) # Contenido de la tarea, un texto de máximo 200 caracteres
    titulo = Column(String(100), nullable=False) # Booleano que indica si una tarea ha sido hecha o no
    comentarios = Column(String(200), nullable=False)
    fecha = Column(String(200), nullable=False)

    def __init__(self, nombre, titulo, comentarios, fecha): # Recordemos que el id no es necesario crearlo manualmente, lo añade la base de datos automaticamente
        self.nombre = nombre
        self.titulo = titulo
        self.comentarios = comentarios
        self.fecha = fecha
    def __repr__(self):
        return "Sinergias {}: {} ({})".format(self.id, self.nombre,self.titulo, self.comentarios)
    def __str__(self):
        return "Sinergias {}: {} ({})".format(self.id, self.nombre, self.titulo, self.comentarios)

class Registro(db.Base):
    __tablename__ = "registro"
    id = Column(Integer, primary_key=True) # Identificador único de cada tarea (no puede haber dos tareas con el mismo id, por eso es primary key)
    username = Column(String(30), nullable=False) # Contenido de la tarea, un texto de máximo 200 caracteres
    email = Column(String(30), nullable=False) # Booleano que indica si una tarea ha sido hecha o no
    password = Column(String(20), nullable=False)

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = self.__create_password(password)

    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)




