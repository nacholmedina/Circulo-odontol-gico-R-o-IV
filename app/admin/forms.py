# HEREDAMOS FLASKFORM
from flask_wtf import FlaskForm
# HEREDAMOS 4 COMPONENTES, CAJA DE TEXTO, BOTON SUBMIT, CAMPO PARA CLAVE y AREA DE TEXTO
from wtforms import StringField, IntegerField, SubmitField
# HEREDAMOS VALIDADORES, DATO REQUERIDO, EMAIL Y LARGO DE UN CAMPO
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField  # para lista desplegable

from .models import ObraSoc, Plan, Practica


class FileForm(FlaskForm):
    obrasocial = QuerySelectField(query_factory=ObraSoc.obrasoc_query, allow_blank=True, get_label='nombre')
    plan = QuerySelectField(query_factory=Plan.plan_query, allow_blank=True, get_label='nombre')
    numafil = StringField('Numero de Afiliado', validators=[DataRequired(), Length(max=15, min=1)])
    submit = SubmitField('Seleccionar Prácticas')


class DetailForm(FlaskForm):
    codigo = QuerySelectField(query_factory=Practica.practica_query, allow_blank=True, get_label='codigo')
    diente = StringField('Diente', default="")
    cara = StringField('Cara', default='')
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    submit = SubmitField('Guardar')
