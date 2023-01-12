from app import db

class Resumen(db.Model):
    __tablename__ = 'resumen'
    id = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('paciente.id', ondelete='CASCADE'), nullable=False)
    id_profesional_obra_social = db.Column(db.Integer, db.ForeignKey('profesional_obra_social.id', ondelete='CASCADE'),nullable=False)
    importe_total = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
                           
    @classmethod
    def get_total(cls, id):
        return Resumen.query.filter_by(id=id).first()

    @classmethod
    def resumen_query(cls):
        return Resumen.query
    
    @classmethod
    def get(cls, resumen_id):
        return Resumen.query.filter_by(id=resumen_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

class DetalleRes(db.Model):
    __tablename__ = 'detalle_resumen'
    id = db.Column(db.Integer, primary_key=True)
    id_resumen = db.Column(db.Integer, db.ForeignKey('resumen.id', ondelete='CASCADE'), nullable=False)
    id_practica = db.Column(db.Integer, db.ForeignKey('practica.id', ondelete='CASCADE'), nullable=False)
    diente = db.Column(db.String(2), nullable=False)
    cara = db.Column(db.String(5), nullable=False)
    importe_unitario = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    @classmethod
    def get_all(cls):
        return DetalleRes.query.all()

    def detalleres_query(self):
        return DetalleRes.query
        
    @classmethod
    def row_query(cls):
        return db.session.query(DetalleRes).count()

    def save(self):
        db.session.add(self)
        db.session.commit()


class Paciente(db.Model):
    __tablename__ = 'paciente'
    id = db.Column(db.Integer, primary_key=True)
    id_obra_social_plan = db.Column(db.Integer, db.ForeignKey('obra_social_plan.id', ondelete='CASCADE'),
                                    nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    fec_nac = db.Column(db.Date, nullable=False)
    n_afiliado = db.Column(db.String(20), nullable=False)
    genero = db.Column(db.Boolean, nullable=False)

    @classmethod
    def get_total(cls, id):
        return Paciente.query.filter_by(id=id).first()

    @classmethod
    def get_id(cls, n_afiliado):
        return Paciente.query.filter_by(n_afiliado=n_afiliado).first()

    @classmethod
    def paciente_query(cls):
        return Paciente.query


class Especialidad(db.Model):
    __tablename__ = 'especialidad'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    @classmethod
    def especialidad_query(cls):
        return Especialidad.query


class ProfEsp(db.Model):
    __tablename__ = 'profesional_especialidad'
    id = db.Column(db.Integer, primary_key=True)
    id_profesional = db.Column(db.Integer, db.ForeignKey('profesional.id', ondelete='CASCADE'), nullable=False)
    id_especialidad = db.Column(db.Integer, db.ForeignKey('especialidad.id', ondelete='CASCADE'), nullable=False)

    @classmethod
    def profesp_query(cls):
        return ProfEsp.query


class ProfObra(db.Model):
    __tablename__ = 'profesional_obra_social'
    id = db.Column(db.Integer, primary_key=True)
    id_obra_social = db.Column(db.Integer, db.ForeignKey('obra_social.id', ondelete='CASCADE'), nullable=False)
    id_profesional = db.Column(db.Integer, db.ForeignKey('profesional.id', ondelete='CASCADE'), nullable=False)
    condicion = db.Column(db.Boolean, nullable=False)

    @classmethod
    def get_all(cls):
        return ProfObra.query.all()

    @classmethod
    def row_query(cls):
        return db.session.query(ProfObra).count()

    @classmethod
    def profobra_query(cls):
        return ProfObra.query

    @classmethod
    def get_total(cls, id):
        return ProfObra.query.filter_by(id=id).first()

    @classmethod
    def get_id(cls, id_obra_social):
        return ProfObra.query.filter_by(id_obra_social=id_obra_social).first()


class Plan(db.Model):
    __tablename__ = 'plan'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    cobertura = db.Column(db.Integer, nullable=False)

    @classmethod
    def plan_query(cls):  # new
        return Plan.query


class ObraSocPlan(db.Model):
    __tablename__ = 'obra_social_plan'
    id = db.Column(db.Integer, primary_key=True)
    id_obra_social = db.Column(db.Integer, db.ForeignKey('obra_social.id', ondelete='CASCADE'), nullable=False)
    id_plan = db.Column(db.Integer, db.ForeignKey('plan.id', ondelete='CASCADE'), nullable=False)

    def obrasocplan_query(self):
        return ObraSocPlan.query


class ObraSoc(db.Model):
    __tablename__ = 'obra_social'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    cuit = db.Column(db.String(15), nullable=False)
    domicilio_postal = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(14), nullable=False)
    condicion = db.Column(db.Boolean, nullable=False)

    @classmethod
    def obrasoc_query(cls):  # new
        return ObraSoc.query

    @classmethod
    def get_total(cls, id):
        return ObraSoc.query.filter_by(id=id).first()

    @classmethod
    def get_id(cls, nombre):
        return ObraSoc.query.filter_by(nombre=nombre).first()


class ObraSocPractica(db.Model):
    __tablename__ = 'obra_social_practica'
    id = db.Column(db.Integer, primary_key=True)
    id_obra_social_plan = db.Column(db.Integer, db.ForeignKey('obra_social_plan.id', ondelete='CASCADE'),nullable=False)
    id_practica = db.Column(db.Integer, db.ForeignKey('practica.id', ondelete='CASCADE'), nullable=False)

    @classmethod
    def obrasocpractica_query(cls):
        return ObraSocPractica.query


class Practica(db.Model):
    __tablename__ = 'practica'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    codigo = db.Column(db.String(6), nullable=False)
    importe = db.Column(db.Integer, nullable=False)

    def get_id_importe(codigo):
        return Practica.query.filter_by(codigo=codigo).first()

    @classmethod
    def practica_query(cls):
        return Practica.query
