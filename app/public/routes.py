from flask import render_template, redirect, url_for

from .import public_bp
from app import public

from app.admin.models import ObraSoc, ProfObra
from app.auth.models import Profesional, Persona


@public_bp.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('auth.login'))

@public_bp.route('/profobra', methods=['GET', 'POST'])
def profobra():
    rows = ProfObra.row_query()
    prof_obra_list = []
    for i in range(rows):
        profobra = ProfObra.get_all()[i]
        obrasoc_id = profobra.id_obra_social
        profesional_id = profobra.id_profesional

        nombre_obrasoc = ObraSoc.get_total(obrasoc_id) 
        persona_prof = Profesional.get_total(profesional_id)
        persona_id = persona_prof.id_persona
        persona = Persona.get_total(persona_id)

        profobra.obrasoc = nombre_obrasoc.nombre
        profobra.profesional = persona.nombre
        
        prof_obra_list.append(profobra)

    return render_template("public/profobra.html",
                             prof_obra_list=prof_obra_list,
                             profobra=profobra)

