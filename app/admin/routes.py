from datetime import date

from flask import render_template, redirect, request
from flask.helpers import url_for

from . import admin_bp
from .forms import FileForm, DetailForm
from .models import DetalleRes, Resumen, Paciente, ProfObra, ObraSoc



@admin_bp.route('/manager')
def manager():
    return render_template('admin/manager.html')

@admin_bp.route('/reumenview')
def resumenview():
    rows = DetalleRes.row_query()
    resumen_list = []
    for i in range(rows):
        detalle = DetalleRes.get_all()[i]
        resumen_id = detalle.id_resumen
        resumen = Resumen.get_total(resumen_id)
        profobra_id = resumen.id_profesional_obra_social
        paciente_id = resumen.id_paciente
        paciente = Paciente.get_total(paciente_id)
        prof_obra = ProfObra.get_total(profobra_id)
        obrasoc_id = prof_obra.id_obra_social
        obra_soc = ObraSoc.get_total(obrasoc_id)

        detalle.registro = detalle.id
        detalle.nom_paciente = paciente.nombre
        detalle.n_afiliado = paciente.n_afiliado
        detalle.obra_social = obra_soc.nombre
        detalle.diente = detalle.diente
        detalle.cara = detalle.cara
        detalle.total = resumen.importe_total
        detalle.fecha = resumen.fecha
        resumen_list.append(detalle)
    return render_template("admin/resumenview.html",
                             resumen_list=resumen_list,
                             detalle=detalle)

@admin_bp.route('/professional')
def professional():
    return render_template('admin/professional.html')


@admin_bp.route('/formprofesional')
def formprofessional():
    return render_template('admin/formprofessional.html')


@admin_bp.route('/formpatient')
def formpatient():
    return render_template('admin/formpatient.html')


@admin_bp.route('/formfile', methods=['GET', 'POST'])
def formfile():
    form = FileForm()
    if form.validate_on_submit():
        obrasocial = form.obrasocial.data
        numafil = form.numafil.data
        paciente_id = Paciente.get_id(numafil)
        obrasoc_id = obrasocial.id
        prof_obra_soc_id = ProfObra.get_id(obrasoc_id)

        newfile = Resumen(
            id_paciente=paciente_id.id,
            id_profesional_obra_social=prof_obra_soc_id.id,
            importe_total=0,
            fecha=date.today())
        newfile.save()
        return redirect(url_for("admin.formpractices", 
                                resumen_id=newfile.id))
    return render_template('admin/formfile.html', 
                            form=form)


@admin_bp.route('/formpractices', methods=['GET', 'POST'])
def formpractices():
    resumen_id = request.args.get('resumen_id')
    resumen = Resumen.get(resumen_id)
    form_detalle = DetailForm()
    if form_detalle.validate_on_submit():
        codigo = form_detalle.codigo.data
        diente = form_detalle.diente.data
        cara = form_detalle.cara.data
        cantidad = form_detalle.cantidad.data

        total = int(codigo.importe * cantidad)
        resumen.importe_total = total
        resumen.save()

        newdetail = DetalleRes(
            id_resumen=resumen_id,
            id_practica=codigo.id,
            diente=diente,
            cara=cara,
            importe_unitario=codigo.importe,
            cantidad=cantidad)
        newdetail.save()
        
        return render_template('admin/professional.html')
    return render_template("admin/formpractices.html", 
                            resumen_id=resumen_id, 
                            form_detalle=form_detalle)
