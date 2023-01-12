from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey

from sqlalchemy.orm import backref, relationship

from app import db


class Profesional(db.Model):
    __tablename__ = 'profesional'
    id = db.Column(db.Integer, primary_key=True)
    id_condicion_fiscal = db.Column(db.Integer, nullable=False)
    id_localidad = db.Column(db.Integer, nullable=False)
    id_persona = db.Column(db.Integer, ForeignKey('persona.id'), nullable=False)
    matricula = db.Column(db.String(11), nullable=False)
    fec_nac = db.Column(db.Date, nullable=False)
    direccion = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    telefono = db.Column(db.String(14), nullable=False)
    condicion = db.Column(db.Boolean, nullable=False)   
    persona = relationship("Persona", back_populates="profesional")

    def get_id(matricula):
        return Profesional.query.get(Profesional.id).filter_bi(matricula=matricula)
    @classmethod
    def get_total(cls, id):
        return Profesional.query.filter_by(id=id).first()

class Persona(db.Model):
    __tablename__ = 'persona'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    profesional = relationship("Profesional", back_populates="persona", uselist=False)

    @classmethod
    def get_total(cls, id):
        return Persona.query.filter_by(id=id).first()
    
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    id_tipo_usuario = db.Column(db.Integer(), nullable=False)
    id_persona = db.Column(db.Integer, ForeignKey('persona.id'), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    persona = relationship("Persona", backref = backref("usuario", uselist=False))

    def __repr__(self):
        return f'<Usuario {self.email}>'

    def set_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def is_admin(self):
        return self.id_tipo_usuario == 1


    @property
    def name(self):
        return self.persona.nombre

    @property
    def matricula(self):
        return self.persona.profesional.matricula

    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)

    @staticmethod
    # CAMBIAMOS get_user(email) POR EL METODO get_by_email(eemail) DE LA CLASE USER
    def get_by_email(email):
        user = Usuario.query.filter_by(email=email).first()
        user.set_password()
        return user