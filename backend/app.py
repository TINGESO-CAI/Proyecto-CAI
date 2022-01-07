from copy import Error
from datetime import datetime
from logging import exception
from operator import mod
import re
from sys import meta_path
from typing import Sequence, Text
import requests
from flask import Flask, jsonify, request,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy.orm import query
import sqlalchemy.orm.exc
import json
from docxtpl import DocxTemplate

from sqlalchemy.sql import text
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.operators import custom_op
import db.modelos as mo

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

db= mo.objeto_db()
app= Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'loginmaldito'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cai"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

ma = Marshmallow(app)
migrate= Migrate(app,db)

# LOGIN

login_manager = LoginManager()
login_manager.init_app(app)

participante_schema = mo.ParticipanteSchema()
participante_schemas = mo.ParticipanteSchema(many=True)

curso_schema = mo.CursoSchema()
curso_schemas = mo.CursoSchema(many=True)

empresa_schema = mo.EmpresaSchema()
empresa_schemas = mo.EmpresaSchema(many=True)

relator_schema = mo.RelatorSchema()
relator_schemas = mo.RelatorSchema(many=True)

factura_schema= mo.FacturaSchema()
factura_schemas= mo.FacturaSchema(many=True)

instancia_schema=mo.InstanciaSchema()
instancia_schemas=mo.InstanciaSchema(many=True)

contacto_schema= mo.ContactoSchema()
contacto_schemas= mo.ContactoSchema(many=True)

cuenta_schema= mo.CuentaSchema()
cuenta_schemas= mo.CuentaSchema(many=True)

# -----------------------------------------------------------------------------------------------------
# -----------------------------------------CUENTA------------------------------------------------------
# -----------------------------------------------------------------------------------------------------


@app.route('/registrar', methods=['POST'])
def registrar_cuenta():
	correo = request.json['correo']
	contrasena = request.json['contrasena']
	nombre = request.json['nombre']
	apellido = request.json['apellido']
	rut = request.json['rut']



	nueva_cuenta = mo.Cuenta(correo,contrasena,nombre,apellido,rut)

	db.session.add(nueva_cuenta)
	db.session.commit()

	resultado = cuenta_schema.dump(nueva_cuenta)

	return jsonify(resultado)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return mo.Cuenta.query.get(int(user_id))

@app.route('/entrar', methods=['POST'])
def entrar_cuenta():
	correo = request.json['correo']
	contrasena = request.json['contrasena']
	usuario = mo.Cuenta.autenticar(correo,contrasena)

	if not usuario:
		return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

	try:
		load_user(usuario.id)
		login_user(usuario)
		return jsonify("El usuario de id "+str(usuario.id)+" se ha logeado")
	except Exception as e:
		return jsonify(str(e))

@app.route('/salir')
@login_required
def salir_cuenta():
    logout_user()
    return jsonify("deslogeaste jiji")

@app.route('/prueba')
@login_required
def prueba():
	return jsonify("FUNCIONA JIJI")
@app.route('/cuenta/permisos',methods=["GET"])
@login_required
def obtener_permisos():
	if current_user.is_authenticated:
		user_id = current_user.get_id()
	cuenta=mo.Cuenta.query.get(user_id)
	permiso={"nivel_acceso": cuenta.nivel_acceso}
	
	return jsonify(permiso)


# -----------------------------------------------------------------------------------------------------
# -----------------------------------PARTICIPANTE------------------------------------------------------
# -----------------------------------------------------------------------------------------------------	

@app.route("/participante/agregar",methods=["POST"])
@login_required
def crear_participante():
	
	rut=request.json['rut']
	nombre=request.json['nombre']
	apellido_paterno=request.json['apellido_paterno']
	apellido_materno=request.json['apellido_materno']
	genero=request.json['genero']
	nivel_educacional=request.json['nivel_educacional']
	fecha_nacimiento=request.json['fecha_nacimiento']
	nacionalidad=request.json['nacionalidad']
	tipo_inscripcion=request.json['tipo_inscripcion']
	ocupacion=request.json['ocupacion']
	fono_personal=request.json['fono_personal']
	fono_corporativo=request.json['fono_corporativo']
	correo_corporativo=request.json['correo_corporativo']
	correo_personal=request.json['correo_personal']
	razon_social=request.json['razon_social']
	
	nuevo_participante=mo.Participante(rut,nombre,apellido_paterno,apellido_materno,genero,nivel_educacional,fecha_nacimiento,nacionalidad,tipo_inscripcion,
	ocupacion,fono_personal,fono_corporativo,correo_personal,correo_corporativo,razon_social)
	
	db.session.add(nuevo_participante)
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"El participante ya ha sido ingresado"})
	
	resultado = participante_schema.dump(nuevo_participante)

	return jsonify(resultado)
	
@app.route("/participante/agregar/archivo",methods=["POST"])
def crear_participante_archivo():
	participantes=request.json['participantes']
	lista_participantes_rechazados=[]
	for persona in  participantes:
		nuevo_participante=mo.Participante(
			persona["rut"],
			persona["nombre"],
			persona["apellido_paterno"],
			persona["apellido_materno"],
			persona["genero"],
			persona["nivel_educacional"],
			persona["fecha_nacimiento"],
			persona["nacionalidad"],
			persona["tipo_inscripcion"],
			persona["ocupacion"],
			persona["razon_social"],
			persona["fono_personal"],
			persona["fono_corporativo"],
			persona["correo_corporativo"],
			persona["correo_personal"]					
			)
		db.session.add(nuevo_participante)
		try:
			db.session.commit()
		except:
			lista_participantes_rechazados.append(nuevo_participante)
			db.session.rollback()
	
	participantes_rechazados=participante_schemas.dump(lista_participantes_rechazados)

	return jsonify({"1.respuesta":"Los siguientes participantes no se han podido ingresar, duplicados o errores, revise:","2.participantes":participantes_rechazados})
	
@app.route("/participante/obtener",methods=["GET"])
def filtro_participante():

	rut=request.args.get('rut')
	nombre=request.args.get('nombre')
	apellido_paterno=request.args.get('apellido_paterno')
	apellido_materno=request.args.get('apellido_materno')
	genero=request.args.get('genero')
	nivel_educacional=request.args.get('nivel_educacional')
	fecha_nacimiento=request.args.get('fecha_nacimiento')
	nacionalidad=request.args.get('nacionalidad')
	tipo_inscripcion=request.args.get('tipo_inscripcion')
	ocupacion=request.args.get('ocupacion')
	fono_personal=request.args.get('fono_personal')
	fono_corporativo=request.args.get('fono_corporativo')
	correo_personal=request.args.get('correo_personal')
	correo_corporativo=request.args.get('correo_corporativo')
	razon_social=request.args.get('razon_social')
 
	participantes = mo.Participante.query.filter()

	if rut != None:
		participantes = participantes.filter(mo.Participante.rut==rut)
	if nombre != None:
		participantes = participantes.filter(mo.Participante.nombre==nombre)
	if apellido_paterno!= None:
		participantes = participantes.filter(mo.Participante.apellido_paterno==apellido_paterno)
	if apellido_materno != None:
		participantes = participantes.filter(mo.Participante.apellido_materno==apellido_materno)
	if genero != None:
		participantes = participantes.filter(mo.Participante.genero==genero)
	if nivel_educacional != None:
		participantes = participantes.filter(mo.Participante.nivel_educacional==nivel_educacional)
	if fecha_nacimiento != None:
		participantes = participantes.filter(mo.Participante.fecha_nacimiento==fecha_nacimiento)
	if nacionalidad!= None:
		participantes = participantes.filter(mo.Participante.nacionalidad==nacionalidad)
	if tipo_inscripcion!= None:
		participantes = participantes.filter(mo.Participante.tipo_inscripcion==tipo_inscripcion)
	if ocupacion!= None:
		participantes = participantes.filter(mo.Participante.ocupacion==ocupacion)
	if fono_personal!= None:
		participantes = participantes.filter(mo.Participante.fono_personal==fono_personal)
	if fono_corporativo!= None:
		participantes = participantes.filter(mo.Participante.fono_corporativo==fono_corporativo)
	if correo_personal!= None:
		participantes = participantes.filter(mo.Participante.correo_personal==correo_personal)
	if correo_corporativo!= None:
		participantes = participantes.filter(mo.Participante.correo_corporativo==correo_personal)
	if razon_social!= None:
		participantes = participantes.filter(mo.Participante.razon_social==razon_social)
			
	participantes_filtrado = participante_schemas.dump(participantes)
	
	return jsonify(participantes_filtrado)

@app.route("/participante/obtener/rut",methods=["GET"])
def obtener_ruts():

	rut_curso = db.session.query(mo.Participante.rut).all()
	participantes = participante_schemas.dump(rut_curso)
	
	return jsonify(participantes)

@app.route("/participante/<rut>/instancias",methods=["GET"])
def obtener_cursos_inscritos_participante(rut):
	participante = mo.Participante.query.get(rut)
	instancias = instancia_schemas.dump(participante.instancias)
	return jsonify(instancias)

@app.route("/participante/editar",methods=["PUT"])
def editar_participante():

	rut_aux=request.args.get('rut')
	participante = mo.Participante.query.get(rut_aux) # Capturo al participante
	
	# Nuevos datos
	nombre=request.json['nombre']
	apellido_paterno=request.json['apellido_paterno']
	apellido_materno=request.json['apellido_materno']
	genero=request.json['genero']
	nivel_educacional=request.json['nivel_educacional']
	fecha_nacimiento=request.json['fecha_nacimiento']
	nacionalidad=request.json['nacionalidad']
	tipo_inscripcion=request.json['tipo_inscripcion']
	ocupacion=request.json['ocupacion']
	fono_personal=request.json['fono_personal']
	fono_corporativo=request.json['fono_corporativo']
	correo_corporativo=request.json['correo_corporativo']
	correo_personal=request.json['correo_personal']
	razon_social=request.json['razon_social']

	# Actualizacion
	if nombre != participante.nombre:
		participante.nombre = nombre
	if apellido_paterno != participante.apellido_paterno:
		participante.apellido_paterno = apellido_paterno
	if apellido_materno != participante.apellido_materno:
		participante.apellido_materno = apellido_materno
	if genero != participante.genero:
		participante.genero = genero
	if nivel_educacional != participante.nivel_educacional:
		participante.nivel_educacional = nivel_educacional
	if fecha_nacimiento != participante.fecha_nacimiento:
		participante.fecha_nacimiento = fecha_nacimiento
	if nacionalidad != participante.nacionalidad:
		participante.nacionalidad = nacionalidad
	if tipo_inscripcion != participante.tipo_inscripcion:
		participante.tipo_inscripcion = tipo_inscripcion
	if ocupacion != participante.ocupacion:
		participante.ocupacion = ocupacion
	if fono_personal != participante.fono_personal:
		participante.fono_personal = fono_personal
	if fono_corporativo != participante.fono_corporativo:
		participante.fono_corporativo = fono_corporativo
	if correo_corporativo != participante.correo_corporativo:
		participante.correo_corporativo = correo_corporativo
	if correo_personal != participante.correo_personal:
		participante.correo_personal = correo_personal
	if razon_social != participante.razon_social:
		participante.razon_social = razon_social

	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"Revise bien los campos de actualizacion"})
	
	resultado = participante_schema.dump(participante)

	return jsonify(resultado)

@app.route("/participante/eliminar",methods=["DELETE"])
def eliminar_participante():
	
	rut_aux=request.args.get('rut')
	participante = mo.Participante.query.get(rut_aux) # Capturo al participante
	
	try:
		db.session.delete(participante)
		db.session.commit()
		msg="el participante "+participante.rut+" fue eliminado correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"El usuario a eliminar no existe"})
 
# -----------------------------------------------------------------------------------------------------
# ------------------------------------------CURSO------------------------------------------------------
# -----------------------------------------------------------------------------------------------------	

@app.route("/curso/agregar",methods=["POST"])
def crear_curso():

	sence = request.json['sence']
	nombre = request.json['nombre']
	modalidad = request.json['modalidad']
	categoria = request.json['categoria']
	horas_curso = request.json['horas_curso']
	valor_efectivo_participante = request.json['valor_efectivo_participante']
	valor_imputable_participante = request.json['valor_imputable_participante']
	resolucion_sence = request.json['resolucion_sence']
	resolucion_usach = request.json['resolucion_usach']
	estado = request.json['estado']
	f_vigencia = request.json['f_vigencia']

	nuevo_curso=mo.Curso(sence,nombre,modalidad,categoria,horas_curso,valor_efectivo_participante,valor_imputable_participante,resolucion_sence,resolucion_usach,estado,f_vigencia)

	db.session.add(nuevo_curso)
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"El curso ya ha sido ingresado"})
	return jsonify({"respuesta":"Curso ingresado correctamente!"})

	
@app.route("/curso/obtener",methods=["GET"])
def obtener_curso():

	sence = request.args.get('sence')
	nombre = request.args.get('nombre')
	modalidad = request.args.get('modalidad')
	categoria = request.args.get('categoria')
	horas_curso = request.args.get('horas_curso')
	valor_efectivo_participante = request.args.get('valor_efectivo_participante')
	valor_imputable_participante = request.args.get('valor_imputable_participante')
	resolucion_sence = request.args.get('resolucion_sence')
	resolucion_usach = request.args.get('resolucion_usach')
	estado = request.args.get('estado')
	f_vigencia = request.args.get('f_vigencia')

	cursos = mo.Curso.query.filter()
	
	if sence != None:
		cursos = cursos.filter(mo.Curso.sence==sence)
	if nombre != None:
		cursos = cursos.filter(mo.Curso.nombre==nombre)
	if modalidad!= None:
		cursos = cursos.filter(mo.Curso.modalidad==modalidad)
	if categoria != None:
		cursos = cursos.filter(mo.Curso.categoria==categoria)
	if horas_curso != None:
		cursos = cursos.filter(mo.Curso.horas_curso==horas_curso)
	if valor_efectivo_participante != None:
		cursos = cursos.filter(mo.Curso.valor_efectivo_participante==valor_efectivo_participante)
	if valor_imputable_participante != None:
		cursos = cursos.filter(mo.Curso.valor_imputable_participante==valor_imputable_participante)
	if resolucion_sence!= None:
		cursos = cursos.filter(mo.Curso.resolucion_sence==resolucion_sence)
	if resolucion_usach!= None:
		cursos = cursos.filter(mo.Curso.resolucion_usach==resolucion_usach)
	if estado!= None:
		cursos = cursos.filter(mo.Curso.estado==estado)
	if f_vigencia!= None:
		cursos = cursos.filter(mo.Curso.f_vigencia==f_vigencia)
		
	cursos_filtrado = curso_schemas.dump(cursos)
	
	return jsonify(cursos_filtrado)

@app.route("/curso/obtener/sence",methods=["GET"])
def obtener_sences():

	sence_curso = db.session.query(mo.Curso.sence).all()
	cursos = curso_schemas.dump(sence_curso)
	
	return jsonify(cursos)

@app.route("/curso/obtener/sences_con_instancia",methods=["GET"])
def obtener_sences_existente():
	sence_curso = mo.Curso.query.all()

	cursos_con_inst=[]
	for c in sence_curso:
		if len(c.instancias)!=0:
			cursos_con_inst.append(c)
	cursos = curso_schemas.dump(cursos_con_inst)
	return jsonify(cursos)

@app.route("/curso/eliminar",methods=["DELETE"])
def eliminar_curso():
	
	sence_aux=request.args.get('sence')
	curso = mo.Curso.query.get(sence_aux) # Capturo al curso
	
	try:
		db.session.delete(curso)
		db.session.commit()
		msg="el curso de nombre "+curso.nombre+" fue eliminado correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"El curso a eliminar no existe"})
	
# -----------------------------------------------------------------------------------------------------
# --------------------------------------INSTANCIA------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
@app.route("/instancia/agregar",methods=["POST"])
def crear_instancia_curso():

	#id_instancia = request.json['id_instancia']
	sence = request.json['sence']
	direccion = request.json['direccion']
	malla = request.json['malla']
	fecha_inicio = request.json['fecha_inicio']
	fecha_termino = request.json['fecha_termino']
	
	nuevo_instancia_curso=mo.Instancia(sence=sence,direccion=direccion,malla=malla,fecha_inicio=fecha_inicio,fecha_termino=fecha_termino)
	print(nuevo_instancia_curso)
	db.session.add(nuevo_instancia_curso)
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"La instancia del curso ya ha sido ingresada"})
	return jsonify({"respuesta":"La instancia del curso ha sido ingresado correctamente!"})

@app.route("/instancia/obtener",methods=["GET"])
def obtener_instancia_curso():

	id_instancia = request.args.get('id_instancia')
	sence = request.args.get('sence')
	direccion = request.args.get('direccion')
	malla = request.args.get('malla')
	fecha_inicio = request.args.get('fecha_inicio')
	fecha_termino = request.args.get('fecha_termino')

	instancias = mo.Instancia.query.filter()
	
	if id_instancia != None:
		instancias = instancias.filter(mo.Instancia.id_instancia==id_instancia)
	if sence != None:
		instancias = instancias.filter(mo.Instancia.sence==sence)
	if direccion!= None:
		instancias = instancias.filter(mo.Instancia.direccion==direccion)
	if malla != None:
		instancias = instancias.filter(mo.Instancia.malla==malla)
	if fecha_inicio != None:
		instancias = instancias.filter(mo.Instancia.fecha_inicio==fecha_inicio)
	if fecha_termino != None:
		instancias = instancias.filter(mo.Instancia.fecha_termino==fecha_termino)
		
	instancias_cursos_filtrado = instancia_schemas.dump(instancias)
	
	return jsonify(instancias_cursos_filtrado)

@app.route("/instancia/editar",methods=["PUT"])
def editar_instancia():

	id_instancia_aux=request.args.get('id_instancia')
	instancia = mo.Instancia.query.get(id_instancia_aux) # Captura de instancia
	
	# Nuevos datos
	sence = request.json['sence']
	direccion = request.json['direccion']
	malla = request.json['malla']
	fecha_inicio = request.json['fecha_inicio']
	fecha_termino = request.json['fecha_termino']

	# Actualizacion
	if sence != instancia.sence:
		instancia.sence = sence
	if direccion != instancia.direccion:
		instancia.direccion = direccion
	if malla != instancia.malla:
		instancia.malla = malla
	if fecha_inicio != instancia.fecha_inicio:
		instancia.fecha_inicio = fecha_inicio
	if fecha_termino != instancia.fecha_termino:
		instancia.fecha_termino = fecha_termino
	
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"Revise bien los campos de actualizacion"})
	
	resultado = instancia_schema.dump(instancia)

	return jsonify(resultado)

@app.route("/instancia/eliminar",methods=["DELETE"])
def eliminar_instancias():
	
	id_aux=request.args.get('id_instancia')
	instancia = mo.Instancia.query.get(id_aux) # Capturo al participante
	
	try:
		db.session.delete(instancia)
		db.session.commit()
		msg="La instancia de id "+str(instancia.id_instancia)+" fue eliminado correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"La instancia a eliminar no existe"})

	
@app.route("/instancia/obtener_razones_sociales/<id_instancia>",methods=["GET"])
def obtener_razones_sociales_validas(id_instancia):

	instancia = mo.Instancia.query.get(id_instancia)
	aux=[]
	lista_razones_sociales=[]
	for i in instancia.alumnos:
		if not (i.razon_social in aux):
			lista_razones_sociales.append({"razon_social":i.razon_social})
			aux.append(i.razon_social)
	return jsonify(lista_razones_sociales)
	
@app.route("/instancia/obtener/id",methods=["GET"])
def obtener_ids():

	ids_instancias = db.session.query(mo.Instancia.id_instancia).all()
	instancias = instancia_schemas.dump(ids_instancias)
	
	return jsonify(instancias )
		
# -----------------------------------------------------------------------------------------------------
# ----------------------------------------EMPRESA------------------------------------------------------
# -----------------------------------------------------------------------------------------------------	

@app.route("/empresa/agregar",methods=["POST"])
def crear_empresa():

	razon_social = request.json['razon_social']
	giro = request.json['giro']
	atencion = request.json['atencion']
	departamento = request.json['departamento']
	rut = request.json['rut']
	direccion = request.json['direccion']
	comuna = request.json['comuna']

	nuevo_empresa=mo.Empresa(razon_social,giro,atencion,departamento,rut,direccion,comuna)

	db.session.add(nuevo_empresa)
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"La empresa ya ha sido ingresada"})
	return jsonify({"respuesta":"Empresa ingresada correctamente!"})

@app.route("/empresa/obtener",methods=["GET"])
def filtro_empresas():

	razon_social = request.args.get('razon_social')
	giro = request.args.get('giro')
	atencion = request.args.get('atencion')
	departamento = request.args.get('departamento')
	rut = request.args.get('rut')
	direccion = request.args.get('direccion')
	comuna = request.args.get('comuna')

	empresas = mo.Empresa.query.filter()

	if razon_social != None:
		empresas = empresas.filter(mo.Empresa.razon_social==razon_social)
	if giro != None:
		empresas = empresas.filter(mo.Empresa.giro==giro)
	if atencion != None:
		empresas = empresas.filter(mo.Empresa.atencion==atencion)
	if departamento!= None:
		empresas = empresas.filter(mo.Empresa.departamento==departamento)
	if rut != None:
		empresas = empresas.filter(mo.Empresa.rut==rut)
	if direccion != None:
		empresas = empresas.filter(mo.Empresa.direccion==direccion)
	if comuna != None:
		empresas = empresas.filter(mo.Empresa.comuna==comuna)

	empresas_filtrados = empresa_schemas.dump(empresas)
	
	return jsonify(empresas_filtrados)

@app.route("/empresa/obtener/razon_social",methods=["GET"])
def obtener_por_razon_social():

	razon_Social_Empresa = db.session.query(mo.Empresa.razon_social).all()
	empresa = empresa_schemas.dump(razon_Social_Empresa)
	
	return jsonify(empresa)
@app.route("/empresa/eliminar",methods=["DELETE"])
def eliminar_empresa():
	
	razon_social=request.args.get('razon_social')
	empresa = mo.Empresa.query.get(razon_social) # Capturo al participante
	
	try:
		db.session.delete(empresa)
		db.session.commit()
		msg="el empresa "+empresa.razon_social+" fue eliminado correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"La empresa a eliminar no existe"})
# -----------------------------------------------------------------------------------------------------
# --------------------------------------RELATOR--------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
@app.route("/relator/obtener",methods=["GET"])
def filtro_relator():
	
	rut= request.args.get('rut')
	nombre = request.args.get('nombre')
	apellido_paterno = request.args.get('apellido_paterno')
	apellido_materno = request.args.get('apellido_materno')
	titulo = request.args.get('titulo')
	genero = request.args.get('genero')
	cv = request.args.get('cv')
	fecha_nacimiento = request.args.get('fecha_nacimiento')
	numero_cuenta = request.args.get('numero_cuenta')
	banco = request.args.get('banco')
	tipo_cuenta = request.args.get('tipo_cuenta')
	fono_personal = request.args.get('fono_personal')
	fono_corporativo = request.args.get('fono_corporativo')
	correo_personal = request.args.get('correo_personal')
	correo_corporativo = request.args.get('correo_corporativo')
	
	relator = mo.Relator.query.filter()

	if rut != None:
		relator = relator.filter(mo.Relator.rut==rut)
	if nombre != None:
		relator = relator.filter(mo.Relator.nombre==nombre)
	if apellido_paterno!= None:
		relator = relator.filter(mo.Relator.apellido_paterno==apellido_paterno)
	if apellido_materno != None:
		relator = relator.filter(mo.Relator.apellido_materno==apellido_materno)
	if titulo != None:
		relator = relator.filter(mo.Relator.titulo==titulo)
	if genero != None:
		relator = relator.filter(mo.Relator.genero==genero)
	if cv != None:
		relator = relator.filter(mo.Relator.cv==cv)
	if fecha_nacimiento != None:
		relator = relator.filter(mo.Relator.fecha_nacimiento==fecha_nacimiento)
	if numero_cuenta != None:
		relator = relator.filter(mo.Relator.numero_cuenta==numero_cuenta)
	if banco != None:
		relator = relator.filter(mo.Relator.banco==banco)
	if tipo_cuenta != None:
		relator = relator.filter(mo.Relator.tipo_cuenta==tipo_cuenta)
	if fono_personal != None:
		relator = relator.filter(mo.Relator.fono_personal==fono_personal)
	if fono_corporativo != None:
		relator = relator.filter(mo.Relator.fono_corporativo==fono_corporativo)
	if correo_personal != None:
		relator = relator.filter(mo.Relator.correo_personal==correo_personal)
	if correo_corporativo != None:
		relator = relator.filter(mo.Relator.correo_corporativo==correo_corporativo)

	relator_filtrados = relator_schemas.dump(relator)
	
	return jsonify(relator_filtrados)

@app.route("/relator/agregar",methods=["POST"])
def crear_relator():

	rut=request.json['rut']
	nombre=request.json['nombre']
	apellido_paterno=request.json['apellido_paterno']
	apellido_materno=request.json['apellido_materno']
	titulo=request.json['titulo']
	genero=request.json['genero']
	cv=request.json['cv']
	fecha_nacimiento=request.json['fecha_nacimiento']
	numero_cuenta=request.json['numero_cuenta']
	banco=request.json['banco']
	tipo_cuenta=request.json['tipo_cuenta']
	fono_personal=request.json['fono_personal']
	fono_corporativo=request.json['fono_corporativo']
	correo_corporativo=request.json['correo_corporativo']
	correo_personal=request.json['correo_personal']
	
	nuevo_relator=mo.Relator(rut,nombre,apellido_paterno,apellido_materno,titulo,genero,cv,fecha_nacimiento,numero_cuenta,banco,tipo_cuenta,fono_personal,
	fono_corporativo,correo_corporativo,correo_personal)
	
	db.session.add(nuevo_relator)
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"El relator ya ha sido ingresado"})
	
	resultado = relator_schema.dump(nuevo_relator)

	return jsonify(resultado)

@app.route("/relator/editar",methods=["PUT"])
def editar_relator():

	rut_aux=request.args.get('rut')
	relator = mo.Relator.query.get(rut_aux) # Capturo al relator
	
	# Nuevos datos
	nombre=request.json['nombre']
	apellido_paterno=request.json['apellido_paterno']
	apellido_materno=request.json['apellido_materno']
	titulo=request.json['titulo']
	genero=request.json['genero']
	cv=request.json['cv']
	fecha_nacimiento=request.json['fecha_nacimiento']
	numero_cuenta=request.json['numero_cuenta']
	banco=request.json['banco']
	tipo_cuenta=request.json['tipo_cuenta']
	fono_personal=request.json['fono_personal']
	fono_corporativo=request.json['fono_corporativo']
	correo_corporativo=request.json['correo_corporativo']
	correo_personal=request.json['correo_personal']

	# Actualizacion
	if nombre != relator.nombre:
		relator.nombre = nombre
	if apellido_paterno != relator.apellido_paterno:
		relator.apellido_paterno = apellido_paterno
	if apellido_materno != relator.apellido_materno:
		relator.apellido_materno = apellido_materno
	if genero != relator.genero:
		relator.genero = genero
	if titulo != relator.titulo:
		relator.titulo = titulo
	if cv != relator.cv:
		relator.cv = cv
	if fecha_nacimiento != relator.fecha_nacimiento:
		relator.fecha_nacimiento = fecha_nacimiento
	if numero_cuenta != relator.numero_cuenta:
		relator.numero_cuenta = numero_cuenta
	if banco != relator.banco:
		relator.banco = banco
	if tipo_cuenta != relator.tipo_cuenta:
		relator.tipo_cuenta = tipo_cuenta
	if fono_personal != relator.fono_personal:
		relator.fono_personal = fono_personal
	if fono_corporativo != relator.fono_corporativo:
		relator.fono_corporativo = fono_corporativo
	if correo_corporativo != relator.correo_corporativo:
		relator.correo_corporativo = correo_corporativo
	if correo_personal != relator.correo_personal:
		relator.correo_personal = correo_personal

	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"Revise bien los campos de actualizacion"})
	
	resultado = participante_schema.dump(relator)

	return jsonify(resultado)

@app.route("/relator/eliminar",methods=["DELETE"])
def eliminar_relator():
	
	relator_aux=request.args.get('rut')
	relator = mo.Relator.query.get(relator_aux) # Capturo el relator
	
	try:
		db.session.delete(relator)
		db.session.commit()
		msg="El relator de rut "+relator.rut+" fue eliminado correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"El relator a eliminar no existe"})

# -----------------------------------------------------------------------------------------------------
# --------------------------------------CONTACTO-------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

@app.route("/contacto/agregar",methods=["POST"])
def crear_contacto():

	#id_contacto=request.json['id_contacto']
	correo=request.json['correo']
	fono=request.json['fono']
	descripcion=request.json['descripcion'] #PROBLEMAS CON LA DESCRIPCION, SALE NULL
	razon_social=request.json['razon_social']
	
	nuevo_contacto=mo.Contacto(correo,fono,descripcion,razon_social)
	
	db.session.add(nuevo_contacto)
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"El contacto ya ha sido ingresado"})
	resultado = contacto_schema.dump(nuevo_contacto)

	return jsonify(resultado)

@app.route("/contacto/obtener",methods=["GET"])
def filtro_contacto():
	
	id_contacto= request.args.get('id_contacto')
	razon_social = request.args.get('razon_social')
	correo = request.args.get('correo')
	fono = request.args.get('fono')
	descripcion = request.args.get('descripcion')
	
	contacto = mo.Contacto.query.filter()

	if id_contacto != None:
		contacto = contacto.filter(mo.Contacto.id_contacto==id_contacto)
	if razon_social != None:
		contacto = contacto.filter(mo.Contacto.razon_social==razon_social)
	if correo!= None:
		contacto = contacto.filter(mo.Contacto.correo==correo)
	if fono != None:
		contacto = contacto.filter(mo.Contacto.fono==fono)
	if descripcion != None:
		contacto = contacto.filter(mo.Contacto.descripcion==descripcion)
	contacto=contacto.order_by(mo.Contacto.id_contacto.desc())
	contacto_filtrados = contacto_schemas.dump(contacto)
	
	return jsonify(contacto_filtrados)

@app.route("/contacto/eliminar",methods=["DELETE"])
def eliminar_contacto():
	
	contacto_aux=request.args.get('id_contacto')
	contacto = mo.Contacto.query.get(contacto_aux) # Capturo el contacto
	
	try:
		db.session.delete(contacto)
		db.session.commit()
		msg="El contacto de id "+str(contacto.id_contacto)+" fue eliminado correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"El contacto a eliminar no existe"})

@app.route("/contacto/obtener_empresa",methods=["GET"])
def obtener_contactos_empresa():

	empresas = mo.Empresa.query.all()
	empresas_contactos=[]
	for i in empresas:
		aux=empresa_schema.dump(i)
		aux["contactos"]=contacto_schemas.dump(i.contactos)
		empresas_contactos.append(aux)

	return jsonify(empresas_contactos)
	
# -----------------------------------------------------------------------------------------------------
# ---------------------------------------FACTURA-------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

@app.route("/factura/agregar",methods=["POST"])
def crear_factura():

	num_factura=db.session.query(mo.Factura).order_by(mo.Factura.id_factura.desc()).first()
	if num_factura is None:
		num_factura=1
	else:
		num_factura=num_factura.id_factura+1
	
	num_cai=request.json['num_registro'] #Este numero se debe ingresar o es fijo?
	estado=request.json['estado']

	num_hes=request.json['num_hes'] #Cuando se ingresa, siempre a veces?
	fecha_emision=request.json['fecha_emision'] #Debe ser simpre la fecha actual?
	fecha_vencimiento=request.json['fecha_vencimiento'] # Esta la definen en base al vencimiento de que?
	sence=request.json['sence']
	id_instancia=request.json['id_instancia']
	razon_social=request.json['razon_social']
	
	# ----------- INFO GENERAL ---------------------------
	
	enviar_factura = request.json['enviar_factura']
	x=["","",""]
	x[enviar_factura]="X"
	especificar = request.json['especificar']
	num_orden = request.json['num_orden'] #Cuando tiene una orden OTIC asociada
	observacion = request.json['obs'] #Agregan un correo o numero de la empresa

	# ----------- INFO DEL CURSO -------------------------
	curso_factura = mo.Curso.query.get(sence)
	instancia_factura = mo.Instancia.query.get(id_instancia)
	empresa_factura = mo.Empresa.query.get(razon_social)
	
	nombre_curso = curso_factura.nombre
	sence_curso = curso_factura.sence
	horas_curso = curso_factura.horas_curso
	fecha_inicio_instancia = instancia_factura.fecha_inicio
	fecha_termino_instancia = instancia_factura.fecha_termino
	num_registro_sence = instancia_factura.id_instancia #es realmente asi?
	valor_curso = curso_factura.valor_efectivo_participante
	
	# En las soli sale participante y un mensaje, ese msj es predeterminado o varia?
	# En una soli agregaron el nombre de otra empresa y el rut correspondiente, cuando se hace eso?

	# ----------- INFO DE LA EMPRESA ------------------------

	# duda existencial, la solicitud de factura es difernet cuando es particular? porq si es asi debe haber una relacion entre factura y empresa
	giro_empresa = empresa_factura.giro
	atencion_empresa = empresa_factura.atencion#con que se rellena este campo? Duda a la clienta
	departamento_empresa = empresa_factura.departamento
	rut_empresa = empresa_factura.rut # aun no responde la duda la clienta sobre el tema del rut
	direccion_empresa = empresa_factura.direccion
	comuna_empresa = empresa_factura.comuna
	fono_empresa = "1234567"
	
	# --------- INFO DE PARTICIPANTES ----------------------
	lista_participantes = request.get_json()
	lista_rut=[] # Lista con los ruts de los participante

	for participante in lista_participantes['participantes']:
		lista_rut.append(participante['rut'])	
	
	valor_total=valor_curso*len(lista_rut)
	nueva_factura=mo.Factura(num_factura,sence,num_cai,estado,num_hes,fecha_emision,fecha_vencimiento,enviar_factura,especificar,num_orden,observacion)
	db.session.add(nueva_factura)
	
	try:
		db.session.commit() 
	except:
		
		return jsonify({"respuesta":"La solicitud de factura ya ha sido ingresada o hay un problema con ella"})
	
	tpl=DocxTemplate("backend/db/data/FORMULARIO_No_4_solicitud_de_factura.docx")
	if estado == 0:
		estado="cerrado"
	else:
		estado="abierto" 
	parametros={
		"numero_cai":num_cai,
		"estado": estado,
		"id_factura":num_factura,
		"fecha_emision":fecha_emision,
		"razon_social": razon_social,
		"giro":giro_empresa,
		"atencion":atencion_empresa,
		"departamento": departamento_empresa,
		"rut":rut_empresa,
		"direccion":direccion_empresa,
		"comuna":comuna_empresa,
		"fono":fono_empresa,
		"fecha_vencimiento":fecha_vencimiento,
		"nombre_curso":nombre_curso,
		"sence":sence_curso,
		"horas_curso":horas_curso,
		"fecha_inicio":fecha_inicio_instancia,
		"fecha_termino":fecha_termino_instancia,
		"registro_sence":num_registro_sence,
		"valor_por_participante":valor_curso,
		"valor_total":valor_total,
		"x1":x[0],
		"x2":x[1],
		"x3":x[2],
		"numero_orden":num_orden,
		"especificar":especificar,
		"observacion":observacion
	}
	tpl.render(parametros)
	tpl.save("backend/db/facturas_generadas/%s.docx"%num_factura)

	for rut in lista_rut:
		participante = mo.Participante.query.get(rut)
		if not(participante in nueva_factura.facturas_alumnos):
			nueva_factura.facturas_alumnos.append(participante)
		
	try:
		db.session.commit()
	except sqlalchemy.orm.exc.FlushError:
		return jsonify({"respuesta":"El participante o la factura no existe"})
	
	resultado = factura_schema.dump(nueva_factura)

	return jsonify(resultado)

# Revisar
@app.route("/factura/obtener",methods=["GET"])
def filtro_factura():
	
	id_factura= request.args.get('id_factura')
	sence = request.args.get('sence')
	estado = request.args.get('estado')
	num_hes = request.args.get('num_hes')
	fecha_emision = request.args.get('fecha_emision')
	fecha_vencimiento = request.args.get('fecha_vencimiento')
	enviar_factura = request.args.get('enviar_factura')
	especificar = request.args.get('especificar')
	num_orden = request.args.get('num_orden')
	observacion = request.args.get('observacion')
	num_cai = request.args.get('num_cai')
	
	factura = mo.Factura.query.filter()

	if id_factura != None:
		factura = factura.filter(mo.Factura.id_factura==id_factura)
	if sence != None:
		factura = factura.filter(mo.Factura.sence==sence)
	if estado!= None:
		factura = factura.filter(mo.Factura.estado==estado)
	if num_hes != None:
		factura = factura.filter(mo.Factura.num_hes==num_hes)
	if fecha_emision != None:
		factura = factura.filter(mo.Factura.fecha_emision==fecha_emision)
	if fecha_vencimiento != None:
		factura = factura.filter(mo.Factura.fecha_vencimiento==fecha_vencimiento)
	if enviar_factura != None:
		factura = factura.filter(mo.Factura.enviar_factura==enviar_factura)
	if especificar != None:
		factura = factura.filter(mo.Factura.especificar==especificar)
	if num_orden != None:
		factura = factura.filter(mo.Factura.num_orden==num_orden)
	if observacion != None:
		factura = factura.filter(mo.Factura.observacion==observacion)
	if num_cai != None:
		factura = factura.filter(mo.Factura.num_cai==num_cai)
	factura=factura.order_by(mo.Factura.id_factura.desc())
	
	facturas_filtradas = factura_schemas.dump(factura)
	
	return jsonify(facturas_filtradas)

@app.route("/factura/eliminar",methods=["DELETE"])
def eliminar_factura():
	
	id_factura=request.args.get('id_factura')
	factura = mo.Factura.query.get(id_factura) # Capturo al participante
	
	try:
		db.session.delete(factura)
		db.session.commit()
		msg="La factura "+str(factura.id_factura)+" fue eliminada correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"La factura a eliminar no existe"})
		
@app.route("/factura/obtener/id",methods=["GET"])
def obtener_ids_facturas():

	ids_facturas = db.session.query(mo.Factura.id_factura).all()
	facturas = factura_schemas.dump(ids_facturas)
	
	return jsonify(facturas)

@app.route("/factura/descargar/<id>",methods=["GET"])
def descargar(id):
	ruta="db/facturas_generadas/"+str(id)+".docx"
	return send_file(ruta,as_attachment=True)
		
# -----------------------------------------------------------------------------------------------------
# --------------------------------------TABLAS INTERMEDIAS---------------------------------------------
# -----------------------------------------------------------------------------------------------------

@app.route("/relator_instancia/agregar",methods=["POST"])
def crear_RI():
	request_rut=request.json['rut']
	request_id_instancia=request.json['id_instancia']

	relator = mo.Relator.query.get(request_rut)
	instancia = mo.Instancia.query.get(request_id_instancia)
	
	if not(relator in instancia.profesores):
		instancia.profesores.append(relator)	
	else:
		return jsonify({"respuesta":"El profesor ya dicta este curso"})	
	try:
		db.session.commit()	
	except sqlalchemy.orm.exc.FlushError:
		return jsonify({"respuesta":"El profesor o la instancia no existe"})	
	return jsonify({"respuesta":"El profesor fue asignado con exito"})

@app.route("/participante_instancia/agregar",methods=["POST"])
def crear_PI():
	request_rut=request.json['rut']
	request_id_instancia=request.json['id_instancia']

	participante = mo.Participante.query.get(request_rut)
	instancia = mo.Instancia.query.get(request_id_instancia)
	
	if not(participante in instancia.alumnos):
		instancia.alumnos.append(participante)
	else:
		return jsonify({"respuesta":"El participante ya esta matriculado en este curso"})

	try:
		db.session.commit()
	except sqlalchemy.orm.exc.FlushError:
		return jsonify({"respuesta":"El participante o la instancia no existe"})

	return jsonify({"respuesta":"Participante ha sido matriculado con exito"})

@app.route("/participante_instancia/obtener",methods=["GET"])
def obtener_participante_instancia():
	id_instancia = request.args.get('id_instancia')
	razon_social = request.args.get('razon_social')

	instancia = mo.Instancia.query.get(id_instancia)
	participantes = instancia.alumnos.filter(mo.Participante.razon_social==razon_social)

	participantes_filtrados = participante_schemas.dump(participantes)

	return jsonify(participantes_filtrados)

@app.route("/participante_factura/agregar",methods=["POST"])
def crear_PF():
	
	request_rut=request.json['rut']
	request_id_factura=request.json['id_factura']

	participante = mo.Participante.query.get(request_rut)
	factura = mo.Factura.query.get(request_id_factura)
	
	if not(participante in factura.facturas_alumnos):
		factura.facturas_alumnos.append(participante)
	else:
		return jsonify({"respuesta":"El participante ya esta asociado a esta factura"})

	try:
		db.session.commit()
	except sqlalchemy.orm.exc.FlushError:
		return jsonify({"respuesta":"El participante o la factura no existe"})

	return jsonify({"respuesta":"Participante ha sido asociado a una factura con exito"})
	
@app.route("/participante_factura/obtener/<id_factura>",methods=["GET"])
def obtener_participante_factura(id_factura):
	factura = mo.Factura.query.get(id_factura)
	participantes_filtrados = participante_schemas.dump(factura.facturas_alumnos)

	return jsonify(participantes_filtrados)
"""
No se si esto ira o que

@app.route("/participante_orden/agregar",methods=["POST"])
def crear_PF()
	
	request_rut=request.json['rut']
	request_id_factura=request.json['id_orden']

	participante = mo.Participante.query.get(request_rut)
	factura = mo.Factura.query.get(request_id_factura)
	
	if not(participante in orden.ordenes_alumnos):
		orden.ordenes_alumnos.append(participante)
	else:
		return jsonify({"respuesta":"El participante ya esta asociado a esta orden "})

	try:
		db.session.commit()
	except sqlalchemy.orm.exc.FlushError:
		return jsonify({"respuesta":"El participante o la orden no existe"})

	return jsonify({"respuesta":"Participante ha sido asociado a una orden con exito"})
"""

if __name__ == '__main__':
	app.run(debug=True)
