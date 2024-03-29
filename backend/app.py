# IMPORTACIONES	GENERALES
from copy import Error
from datetime import datetime
from logging import exception
from operator import mod
import re
from sys import meta_path
from typing import Sequence, Text
from marshmallow.fields import Boolean, Date
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
from datetime import datetime, date

from sqlalchemy.sql import text
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.operators import custom_op
from werkzeug.wrappers import response
import db.modelos as mo

# LOGIN
from flask_jwt_extended import JWTManager,jwt_required, create_access_token, get_jwt_identity
import jwt as jwtLib

# Configuracion de la app
db= mo.objeto_db()
app= Flask(__name__)
cors=CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cai" # conexion con la bd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = False # Para mostrar las query SQL
#LOGIN
app.config['JWT_SECRET_KEY'] = 'LvZXgGRpQBR4@Uc3ZxZ2Polnhmc6dwBXdSW3MX6S8cwzW88gG&!CvNG2hw5gG1tEbYXW#e5w^jiajDKnp3PK#6F*52ljqFE8Q@$ti2Y!YVES$QvmchE&D9#dKoB46M3XzT$*9U8hD!R@gcC5g2KKlcpFqxEI6S1L91u&j#JULJ!BPg$zvs5#jmw*^xHD8Xq#zFQQ49'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
db.init_app(app)

ma = Marshmallow(app) # Para el uso de sqlalchemy
migrate= Migrate(app,db) # Para el uso de los migrate

# LOGIN
jwt = JWTManager(app)

# Definicon de los schemas
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
@app.before_request
def before_request():
	if request.endpoint != 'entrar':
		token=request.headers.get('token')
		if token is None or len(token)==0:
			return None

def validar_permiso(token,nivel_requerido):
	payload = jwtLib.decode(token,'LvZXgGRpQBR4@Uc3ZxZ2Polnhmc6dwBXdSW3MX6S8cwzW88gG&!CvNG2hw5gG1tEbYXW#e5w^jiajDKnp3PK#6F*52ljqFE8Q@$ti2Y!YVES$QvmchE&D9#dKoB46M3XzT$*9U8hD!R@gcC5g2KKlcpFqxEI6S1L91u&j#JULJ!BPg$zvs5#jmw*^xHD8Xq#zFQQ49',algorithms=["HS256"])
	cuenta = mo.Cuenta.query.filter(mo.Cuenta.correo==str(payload["sub"])).first()
	if cuenta.nivel_acceso<=nivel_requerido:
		return True
	else:
		return False
#obtener permiso(token,nivel)
#permiso del token
#devolver true



# Funcion encargada de registar una cuenta
@app.route('/registrar', methods=['POST'])
def registrar_cuenta():
	if not validar_permiso(request.headers.get('token'),0):
		return None
	token=request.headers.get('token')
	#if not obtenerpermiso(token,0)
		#return jsonify de no permisos
	# Request de los json
	correo = request.json['correo']
	contrasena = request.json['contrasena']
	nombre = request.json['nombre']
	apellido = request.json['apellido']
	rut = request.json['rut']

	# Se crea la instancia cuenta con los datos capturados
	nueva_cuenta = mo.Cuenta(correo,contrasena,nombre,apellido,rut)

	# Se agrega y se sube a la db
	db.session.add(nueva_cuenta)
	try:
		db.session.commit()
	except:
		return jsonify("Error")
	# Se realiza un "dump" de los schemas para moder "jsonifear"
	resultado = cuenta_schema.dump(nueva_cuenta)

	return jsonify(resultado)

# Funcion respecto al login
@app.route('/entrar', methods=['POST'])
def entrar_cuenta():

	
	# Request de los json
	correo = request.json['correo']
	contrasena = request.json['contrasena']

	# Se instancia la clase Cuenta con el metodo de autenticar definido
	usuario = mo.Cuenta.autenticar(correo,contrasena)

	# En caso de que el usario no este en la db
	if not usuario:
		return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

	try:
		access_token = create_access_token(identity=correo)
		# nombre,rut y correo , token
		return jsonify({'nombre': usuario.nombre,
			'rut': usuario.rut,
			'correo': usuario.correo,
			'token': access_token})
	except Exception as e:
		return jsonify(str(e))

@app.route('/cuenta/editar',methods=["PUT"])
def editar_cuenta():
	if not validar_permiso(request.headers.get('token'),0):
		return None	
	
	id_aux=request.json['id']

	cuenta = mo.Cuenta.query.get(id_aux)
	correo=request.json['correo']
	nombre=request.json['nombre']
	apellidos=request.json['apellido']
	rut=request.json['rut']
	if rut != cuenta.rut:
		cuenta.rut = rut
	if nombre != cuenta.nombre:
		cuenta.nombre = nombre
	if apellidos != cuenta.apellido:
		cuenta.apellido = apellidos
	if correo != cuenta.correo:
		cuenta.correo = correo

	try:
		# Los agrego a la bd
		db.session.commit() 
	except:
		return jsonify({"respuesta":"Revise bien los campos de actualizacion"})
	return jsonify({"respuesta":"edicion exitosa"})

@app.route("/cuenta/eliminar",methods=["DELETE"])
def eliminar_cuenta():
	if not validar_permiso(request.headers.get('token'),0):
		return None	

	# Request del rut ingresado por la ruta
	# ej: /participante/editar?id=xxxxxxxx-x
	id=request.args.get('id')
	cuenta = mo.Cuenta.query.get(id) # Capturo al participante
	
	try:
		# Borro al participante de la base de dato
		db.session.delete(cuenta)
		db.session.commit()
		msg="la cuenta de "+cuenta.correo+" fue eliminada correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"la cuenta  a eliminar no existe"})
@app.route('/cuenta/editar_acceso',methods=["PUT"])
def editar_cuenta_acceso():
	if not validar_permiso(request.headers.get('token'),2):
		return None	
	
	id_aux=request.json['id_cuenta']

	cuenta = mo.Cuenta.query.get(id_aux)
	nivel_acceso=request.json['nivel_acceso']
	if nivel_acceso != cuenta.nivel_acceso:
		cuenta.nivel_acceso = nivel_acceso

	try:
		# Los agrego a la bd
		db.session.commit() 
	except:
		return jsonify({"respuesta":"Revise bien los campos de actualizacion"})
	return jsonify({"respuesta":"edicion exitosa"})

@app.route('/cuenta/obtener/todos',methods=["GET"])
def obtener_cuentas():
	if not validar_permiso(request.headers.get('token'),0):
		return None	

	cuentas = mo.Cuenta.query.all()
	dump=cuenta_schemas.dump(cuentas)
	return jsonify(dump)
		
@app.route('/cuenta/permisos',methods=["GET"])
def obtener_permisos():
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	token = request.args.get('token')

	payload = jwtLib.decode(token,'LvZXgGRpQBR4@Uc3ZxZ2Polnhmc6dwBXdSW3MX6S8cwzW88gG&!CvNG2hw5gG1tEbYXW#e5w^jiajDKnp3PK#6F*52ljqFE8Q@$ti2Y!YVES$QvmchE&D9#dKoB46M3XzT$*9U8hD!R@gcC5g2KKlcpFqxEI6S1L91u&j#JULJ!BPg$zvs5#jmw*^xHD8Xq#zFQQ49',algorithms=["HS256"])
	print(payload["sub"])
	cuenta = mo.Cuenta.query.filter(mo.Cuenta.correo==str(payload["sub"])).first()

	dump={"nivel_acceso":cuenta.nivel_acceso}
	return jsonify(dump)

	'''
	cuenta=db.session.query(mo.Cuenta).filter(mo.Cuenta.correo==get_jwt_identity())
	permiso={
		"nombre": cuenta.nombre + " " + cuenta.apellido,
		"rut": cuenta.rut,
		"correo": cuenta.correo,
		"nivel_acceso": cuenta.nivel_acceso
		}
	
	return jsonify(permiso)
	'''

# -----------------------------------------------------------------------------------------------------
# -----------------------------------PARTICIPANTE------------------------------------------------------
# -----------------------------------------------------------------------------------------------------	

# Funcion para agregar un participante
@app.route("/participante/agregar",methods=["POST"])
def crear_participante():
	if not validar_permiso(request.headers.get('token'),2):
		return None
		
	# Request de los json
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
	
	# Crear instancia de participante con los datos
	nuevo_participante=mo.Participante(rut,nombre,apellido_paterno,apellido_materno,genero,nivel_educacional,fecha_nacimiento,nacionalidad,tipo_inscripcion,
	ocupacion,fono_personal,fono_corporativo,correo_personal,correo_corporativo,razon_social)
	
	# Agregamos el nuevo participante
	db.session.add(nuevo_participante)
	try:
		# Lo agregamos a la db
		db.session.commit() 
	except:
		return jsonify({"respuesta":"El participante ya ha sido ingresado"})
	
	# Se ejecuta el dump
	resultado = participante_schema.dump(nuevo_participante)

	return jsonify(resultado)

# Funcion para filtrar por algun parametro o entregar todos los participantes
@app.route("/participante/obtener",methods=["GET"])
def filtro_participante():
	if not validar_permiso(request.headers.get('token'),3):
		return None	
	if not validar_permiso(request.headers.get('token'),3):
		return None
	# Request de los json a traves de la ruta
	# ej: /participante/obtener?tipo_inscripcion=XX
	# ej: /participante/obtener?tipo_inscripcion=xxxx&genero=xx
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
	
	# Se instancian todos los participantes
	participantes = mo.Participante.query.filter()

	# En esta seccion se iran filtrando segun los atributos entregados en la ruta
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

	# Se hace el dump retornando los participantes filtrados segun los parametros dados
	participantes_filtrado = participante_schemas.dump(participantes)
	
	return jsonify(participantes_filtrado)

# Se obtienen todos los ruts de los participantes
@app.route("/participante/obtener/rut",methods=["GET"])
def obtener_ruts():
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	# Se sacan todos los ruts de los participantes con query().all()
	rut_curso = db.session.query(mo.Participante.rut).all()
	# Se hace el dump de los ruts
	participantes = participante_schemas.dump(rut_curso)
	
	return jsonify(participantes)

# Se obtienen todas las instancias de un participante especifico
@app.route("/participante/<rut>/instancias",methods=["GET"])
def obtener_cursos_inscritos_participante(rut):
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	# Tomamos al participante del rut ingresado
	participante = mo.Participante.query.get(rut)
	
	# Gracias a los backref, se obtienen todas las instancias de este rut
	instancias = instancia_schemas.dump(participante.instancias)

	return jsonify(instancias)

# Funcion encargada de editar/actualizar los participantes
@app.route("/participante/editar",methods=["PUT"])
def editar_participante():
	if not validar_permiso(request.headers.get('token'),2):
		return None	


	# Request del rut ingresado por la ruta
	# ej: /participante/editar/xxxxxxxx-x
	rut_aux=request.args.get('rut')
	# Capturo al participante
	participante = mo.Participante.query.get(rut_aux) 
	
	# Capturo los nuevos datos
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

	# Realizo la Actualizacion de los atributos
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
		# Los agrego a la bd
		db.session.commit() 
	except:
		return jsonify({"respuesta":"Revise bien los campos de actualizacion"})
	
	# dump para mostrarlos y guardarlos como json
	resultado = participante_schema.dump(participante)

	return jsonify(resultado)

# Funcion encargada de borrar al participante de la bd
@app.route("/participante/eliminar",methods=["DELETE"])
def eliminar_participante():
	if not validar_permiso(request.headers.get('token'),1):
		return None	

	# Request del rut ingresado por la ruta
	# ej: /participante/editar/xxxxxxxx-x
	rut_aux=request.args.get('rut')
	participante = mo.Participante.query.get(rut_aux) # Capturo al participante
	
	try:
		# Borro al participante de la base de dato
		db.session.delete(participante)
		db.session.commit()
		msg="el participante "+participante.rut+" fue eliminado correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"El usuario a eliminar no existe"})

@app.route("/participante/obtener/independientes",methods=["GET"])
def obtener_independientes():
	if not validar_permiso(request.headers.get('token'),3):
		return None	

		participantes = db.session.query(mo.Participante).filter(mo.Participante.empresa==None)

		resultado= participante_schemas.dump(participantes)

		return jsonify(resultado)
 
# -----------------------------------------------------------------------------------------------------
# ------------------------------------------CURSO------------------------------------------------------
# -----------------------------------------------------------------------------------------------------	

# Funcion encargada de agregar un curso
@app.route("/curso/agregar",methods=["POST"])
def crear_curso():
	if not validar_permiso(request.headers.get('token'),2):
		return None
	
	# Request de los json
	sence = request.json['sence']
	nombre = request.json['nombre']
	modalidad = request.json['modalidad']
	categoria = request.json['categoria']
	horas_curso = request.json['horas_curso']
	valor_efectivo_participante = request.json['valor_efectivo_participante']
	valor_imputable_participante = request.json['valor_imputable_participante']
	resolucion_sence = request.json['resolucion_sence']
	resolucion_usach = request.json['resolucion_usach']
	f_vigencia = request.json['f_vigencia']

	# Se instancia el nuevo cuso
	nuevo_curso=mo.Curso(sence,nombre,modalidad,categoria,horas_curso,valor_efectivo_participante,valor_imputable_participante,resolucion_sence,resolucion_usach,f_vigencia)

	# Se agrega el nuevo curso ingresado
	db.session.add(nuevo_curso)
	try:
		# Se agrega a la bd
		db.session.commit() 
	except:
		return jsonify({"respuesta":"El curso ya ha sido ingresado"})
	return jsonify({"respuesta":"Curso ingresado correctamente!"})

# Funcion encarga de filtar los cursos
@app.route("/curso/obtener",methods=["GET"])
def obtener_curso():
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	# Request de los json
	# ej: /curso/obtener?modalidad=xxxx
	# ej: /curso/obtener?modalidad=xxxx&estado=xxxx
	sence = request.args.get('sence')
	nombre = request.args.get('nombre')
	modalidad = request.args.get('modalidad')
	categoria = request.args.get('categoria')
	horas_curso = request.args.get('horas_curso')
	valor_efectivo_participante = request.args.get('valor_efectivo_participante')
	valor_imputable_participante = request.args.get('valor_imputable_participante')
	resolucion_sence = request.args.get('resolucion_sence')
	resolucion_usach = request.args.get('resolucion_usach')
	f_vigencia = request.args.get('f_vigencia')

	# Se insancian todos los cursos para posteriormente ser filtrados
	cursos = mo.Curso.query.filter()
	
	# En base al los parmetros ingresados por la ruta, se filtran los datos
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
	if f_vigencia!= None:
		cursos = cursos.filter(mo.Curso.f_vigencia==f_vigencia)

	# se realiza los dump	
	cursos_filtrado = curso_schemas.dump(cursos)
	
	return jsonify(cursos_filtrado)

# Funcion que obtiene todos los sence de todos los cursos
@app.route("/curso/obtener/sence",methods=["GET"])
def obtener_sences():
	if not validar_permiso(request.headers.get('token'),3):
		return None	
	# Se toma todos los curso
	sence_curso = db.session.query(mo.Curso.sence).all()
	# Se realiza el dump
	cursos = curso_schemas.dump(sence_curso)
	
	return jsonify(cursos)

# Funcion que retorna todos los sence con instancias
@app.route("/curso/obtener/sences_con_instancia",methods=["GET"])
def obtener_sences_existente():
	if not validar_permiso(request.headers.get('token'),3):
		return None	
	# se toman todos los cursos
	sence_curso = mo.Curso.query.all()

	cursos_con_inst=[]
	# con el for se agregan todos los cursos que tienen instancias
	for c in sence_curso:
		if len(c.instancias)!=0:
			cursos_con_inst.append(c)
	# se realiza el dump
	cursos = curso_schemas.dump(cursos_con_inst)
	return jsonify(cursos)
# Funcion que se encarga de editar o actualizar una instancia
@app.route("/curso/editar",methods=["PUT"])
def editar_curso():
	if not validar_permiso(request.headers.get('token'),2):
		return None	


	# Request de los json
	# ej: /instacia/editar?id_instancia=xxxx
	sence_aux=request.args.get('sence')
	# Captura de instancia
	curso = mo.Curso.query.get(sence_aux) 
	
	# Nuevos datos
	sence = request.json['sence']
	nombre = request.json['nombre']
	modalidad = request.json['modalidad']
	categoria = request.json['categoria']
	horas_curso=request.json['horas_curso']
	valor_efectivo_participante=request.json['valor_efectivo_participante']
	valor_imputable_participante=request.json['valor_imputable_participante']
	f_vigencia = request.json['f_vigencia']
	resolucion_sence=request.json['resolucion_sence']
	resolucion_usach=request.json['resolucion_usach']

	# Actualizacion
	if sence != curso.sence:
		curso.sence = sence
	if nombre != curso.nombre:
		curso.nombre = nombre
	if modalidad != curso.modalidad:
		curso.modalidad = modalidad
	if categoria != curso.categoria:
		curso.categoria = categoria
	if horas_curso != curso.horas_curso:
		curso.horas_curso = horas_curso
	if valor_efectivo_participante != curso.valor_efectivo_participante:
		curso.valor_efectivo_participante = valor_efectivo_participante
	if valor_imputable_participante != curso.valor_imputable_participante:
		curso.valor_imputable_participante = valor_imputable_participante
	if f_vigencia != curso.f_vigencia:
		curso.f_vigencia = f_vigencia
	if resolucion_sence != curso.resolucion_sence:
		curso.resolucion_sence = resolucion_sence
	if resolucion_usach != curso.resolucion_usach:
		curso.resolucion_usach = resolucion_usach
	
	try:
		# Se agrega a la db
		db.session.commit() 
	except:
		return jsonify({"respuesta":"Revise bien los campos de actualizacion"})
	
	# Se crea el dump
	resultado = curso_schema.dump(curso)

	return jsonify(resultado)

# Funcion que se usa para eliminar
@app.route("/curso/eliminar",methods=["DELETE"])
def eliminar_curso():
	if not validar_permiso(request.headers.get('token'),1):
		return None	
	# Request de los json
	# ej: /curso/eliminar?sence=xxxx
	sence_aux=request.args.get('sence')
	curso = mo.Curso.query.get(sence_aux) # Capturo al curso
	
	try:
		# se elimina de la db
		db.session.delete(curso)
		db.session.commit()
		msg="el curso de nombre "+curso.nombre+" fue eliminado correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"El curso a eliminar no existe"})
	
# -----------------------------------------------------------------------------------------------------
# --------------------------------------INSTANCIA------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
@app.route("/intancia/obtener/id",methods=["GET"])
def obtener_instancias():
	if not validar_permiso(request.headers.get('token'),3):
		return None	
	# Se toma todos los curso
	id_instancias = db.session.query(mo.Instancia.id_instancia).all()
	# Se realiza el dump
	instancias = instancia_schemas.dump(id_instancias)
	
	return jsonify(instancias)

# Funcion que se encarga de agregar una instancia
@app.route("/instancia/agregar",methods=["POST"])
def crear_instancia_curso():
	if not validar_permiso(request.headers.get('token'),2):
		return None
	
	sence = request.json['sence']
	direccion = request.json['direccion']
	malla = request.json['malla']
	fecha_inicio = request.json['fecha_inicio']
	fecha_termino = request.json['fecha_termino']
	estado = request.json['estado']
	
	# Crea la instancia de instancia XD
	nuevo_instancia_curso=mo.Instancia(sence,direccion,malla,fecha_inicio,fecha_termino,estado)

	# se agrega la instancia
	db.session.add(nuevo_instancia_curso)
	try:
		# se sube a la db
		db.session.commit() 
	except:
		return jsonify({"respuesta":"La instancia del curso ya ha sido ingresada"})
	return jsonify({"respuesta":"La instancia del curso ha sido ingresado correctamente!"})

# Funcion para filtrar las instancias
@app.route("/instancia/obtener",methods=["GET"])
def obtener_instancia_curso():
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	# Request de los json
	# ej: /instacia/obtener?sence=xxxx
	# ej: /instancia/obtener?fecha_inicio=xxxx&malla=xxxx
	id_instancia = request.args.get('id_instancia')
	sence = request.args.get('sence')
	direccion = request.args.get('direccion')
	malla = request.args.get('malla')
	fecha_inicio = request.args.get('fecha_inicio')
	fecha_termino = request.args.get('fecha_termino')
	estado = request.args.get('estado')

	# Se traen todas las instancias
	instancias = mo.Instancia.query.filter()
	
	# En base al los parmetros ingresados por la ruta, se filtran los datos
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
	if estado != None:
		instancias = instancias.filter(mo.Instancia.estado==estado)
	
	# Se crea el dump
	instancias_cursos_filtrado = instancia_schemas.dump(instancias)
	
	return jsonify(instancias_cursos_filtrado)

# Funcion que se encarga de editar o actualizar una instancia
@app.route("/instancia/editar",methods=["PUT"])
def editar_instancia():
	if not validar_permiso(request.headers.get('token'),2):
		return None	


	# Request de los json
	# ej: /instacia/editar?id_instancia=xxxx
	id_instancia_aux=request.args.get('id_instancia')
	# Captura de instancia
	instancia = mo.Instancia.query.get(id_instancia_aux) 
	
	# Nuevos datos
	sence = request.json['sence']
	direccion = request.json['direccion']
	malla = request.json['malla']
	fecha_inicio = request.json['fecha_inicio']
	fecha_termino = request.json['fecha_termino']
	estado = request.json['estado']

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
	if estado != instancia.estado:
		instancia.estado = estado
	
	try:
		# Se agrega a la db
		db.session.commit() 
	except:
		return jsonify({"respuesta":"Revise bien los campos de actualizacion"})
	
	# Se crea el dump
	resultado = instancia_schema.dump(instancia)

	return jsonify(resultado)

# Funcion que elimina la instancia
@app.route("/instancia/eliminar",methods=["DELETE"])
def eliminar_instancias():
	if not validar_permiso(request.headers.get('token'),1):
		return None	
	# Request de los json
	# ej: /instacia/eliminar?id_instancia=xxxx
	id_aux=request.args.get('id_instancia')
	instancia = mo.Instancia.query.get(id_aux) # Capturo al participante
	
	try:
		# se borra de la db
		db.session.delete(instancia)
		db.session.commit()
		msg="La instancia de id "+str(instancia.id_instancia)+" fue eliminado correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"La instancia a eliminar no existe"})

# Funcion que se encarga de obtener todas las razones sociales asociada a un id
@app.route("/instancia/obtener_razones_sociales/<id_instancia>",methods=["GET"])
def obtener_razones_sociales_validas(id_instancia):
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	# Capturamos la instancia segun el id ingresado
	instancia = mo.Instancia.query.get(id_instancia)
	aux=[]
	lista_razones_sociales=[]
	for i in instancia.alumnos:
		if not (i.razon_social in aux):
			lista_razones_sociales.append({"razon_social":i.razon_social})
			aux.append(i.razon_social)
	return jsonify(lista_razones_sociales)

# Funcion que obtiene todos los id de las instancias que existan
@app.route("/instancia/obtener/id",methods=["GET"])
def obtener_ids():
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	# capturamos todas las instancias 
	ids_instancias = db.session.query(mo.Instancia.id_instancia).all()
	# se hace el dump para capturar como json
	instancias = instancia_schemas.dump(ids_instancias)
	
	return jsonify(instancias)

# Funcion que obtiene
@app.route("/instancia/obtener_todo/<id_instancia>",methods=["GET"])
def obtener_todo(id_instancia):
	if not validar_permiso(request.headers.get('token'),3):
		return None	
	
	instancia = mo.Instancia.query.get(id_instancia)
	profesores = instancia.profesores
	alumnos = instancia.alumnos

	resultado = []
	participantes_facturados=[]
	
	for i in alumnos:
		for f in i.facturas:
			if f.id_instancia == int(id_instancia):
				if not (i in participantes_facturados):
					participantes_facturados.append(i)
					completo=participante_schema.dump(i)
					completo["id_factura"]=f.id_factura
					completo["creada"]=True
					completo["mandada"]=f.mandada
					completo["pagada"]=f.pagada
					completo["fecha_emision"]=(f.fecha_emision).strftime('%Y-%m-%d') 
					completo["fecha_vencimiento"]=(f.fecha_emision).strftime('%Y-%m-%d') 
					resultado.append(completo)
	
	alumnos_no_fact = []
	for i in alumnos:
		if i not in participantes_facturados:
			alumnos_no_fact.append(i)
			completo=participante_schema.dump(i)
			completo["id_factura"]= None
			completo["creada"]= False
			completo["mandada"]=False 
			completo["pagada"]= False
			completo["fecha_emision"]=None
			completo["fecha_vencimiento"]=None
			resultado.append(completo)


	resultado={'relatores':relator_schemas.dump(profesores),
	'participante':resultado}
	return jsonify(resultado)
	
	

# -----------------------------------------------------------------------------------------------------
# ----------------------------------------EMPRESA------------------------------------------------------
# -----------------------------------------------------------------------------------------------------	

# Funcion para crear una empresa
@app.route("/empresa/agregar",methods=["POST"])
def crear_empresa():
	if not validar_permiso(request.headers.get('token'),2):
		return None
	
	# Request de los json
	razon_social = request.json['razon_social']
	giro = request.json['giro']
	atencion = request.json['atencion']
	departamento = request.json['departamento']
	rut = request.json['rut']
	direccion = request.json['direccion']
	comuna = request.json['comuna']

	# Se crea la instancia de empresa
	nuevo_empresa=mo.Empresa(razon_social,giro,atencion,departamento,rut,direccion,comuna)

	# Se agrega la instancia
	db.session.add(nuevo_empresa)
	try:
		# Se agrega a la db
		db.session.commit() 
	except:
		return jsonify({"respuesta":"La empresa ya ha sido ingresada"})
	return jsonify({"respuesta":"Empresa ingresada correctamente!"})

# Funcion que se encarga de filtar las empresas
@app.route("/empresa/obtener",methods=["GET"])
def filtro_empresas():
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	# Request de los json
	# ej: /empresa/obtener?giro=xxxx
	# ej: /empresa/obtener?giro=xxxx&departamento=xxxx
	razon_social = request.args.get('razon_social')
	giro = request.args.get('giro')
	atencion = request.args.get('atencion')
	departamento = request.args.get('departamento')
	rut = request.args.get('rut')
	direccion = request.args.get('direccion')
	comuna = request.args.get('comuna')

	# Se traen todas las empresas
	empresas = mo.Empresa.query.filter()

	# En base al los parmetros ingresados por la ruta, se filtran los datos
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

	# Se hace el dump
	empresas_filtrados = empresa_schemas.dump(empresas)
	
	return jsonify(empresas_filtrados)

# Funcion que se encarga de editar o actualizar una empresa
@app.route("/empresa/editar",methods=["PUT"])
def editar_empresa():
	if not validar_permiso(request.headers.get('token'),2):
		return None	


	# Request de los json
	# ej: /empresa/editar?razon_social=xxxx
	razon_social_aux=request.args.get('razon_social')
	# Captura la empresa
	empresa = mo.Empresa.query.get(razon_social_aux) 
	
	# Nuevos datos
	giro = request.json['giro']
	atencion = request.json['atencion']
	departamento = request.json['departamento']
	rut = request.json['rut']
	direccion = request.json['direccion']
	comuna = request.json['comuna']

	# Actualizacion
	if giro != empresa.giro:
		empresa.giro = giro
	if atencion != empresa.atencion:
		empresa.atencion = atencion
	if departamento != empresa.departamento:
		empresa.departamento = departamento
	if rut != empresa.rut:
		empresa.rut = rut
	if direccion != empresa.direccion:
		empresa.direccion = direccion
	if comuna != empresa.comuna:
		empresa.comuna = comuna
	
	try:
		# Se agrega a la db
		db.session.commit() 
	except:
		return jsonify({"respuesta":"Revise bien los campos de actualizacion"})
	
	# Se crea el dump
	resultado = empresa_schema.dump(empresa)

	return jsonify(resultado)

# Funcion que trae todas las razones sociales de las empresas
@app.route("/empresa/obtener/razon_social",methods=["GET"])
def obtener_por_razon_social():
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	# Se traen todas las razones sociales
	razon_Social_Empresa = db.session.query(mo.Empresa.razon_social).all()
	# Se hace el dump
	empresa = empresa_schemas.dump(razon_Social_Empresa)
	
	return jsonify(empresa)

# Funcion que elimina una empresa
@app.route("/empresa/eliminar",methods=["DELETE"])
def eliminar_empresa():
	if not validar_permiso(request.headers.get('token'),1):
		return None	
	# Request de los json
	# ej: /empresa/eliminar?razon_social=xxxx
	razon_social=request.args.get('razon_social')
	empresa = mo.Empresa.query.get(razon_social) # Capturo a la empresa
	
	try:
		# Se elimina de la db
		db.session.delete(empresa)
		db.session.commit()
		msg="el empresa "+empresa.razon_social+" fue eliminado correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"La empresa a eliminar no existe"})

# -----------------------------------------------------------------------------------------------------
# --------------------------------------RELATOR--------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

# Funcion que se encarga de obtener un relator
@app.route("/relator/obtener",methods=["GET"])
def filtro_relator():
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	# Request de los json
	# ej: /relator/obtener?genero=xxxx
	# ej: /relator/obtener?genero=xxxx&banco=xxxx
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
	
	# Se obtienen todos los relatores
	relator = mo.Relator.query.filter()

	# En base al los parmetros ingresados por la ruta, se filtran los datos
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

	# Se hace el dump
	relator_filtrados = relator_schemas.dump(relator)
	
	return jsonify(relator_filtrados)

# Funcion que agrega un relator
@app.route("/relator/agregar",methods=["POST"])
def crear_relator():
	if not validar_permiso(request.headers.get('token'),2):
		return None
	
	# Request json
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
	
	# Se crea la instancia de relator
	nuevo_relator=mo.Relator(rut,nombre,apellido_paterno,apellido_materno,titulo,genero,cv,fecha_nacimiento,numero_cuenta,banco,tipo_cuenta,fono_personal,
	fono_corporativo,correo_corporativo,correo_personal)
	
	# Se arega la instancia
	db.session.add(nuevo_relator)
	try:
		# Se agrega a la db
		db.session.commit() 
	except:
		return jsonify({"respuesta":"El relator ya ha sido ingresado"})
	
	# Se crea el dump
	resultado = relator_schema.dump(nuevo_relator)

	return jsonify(resultado)

# Funcion encargada de editar o actualizar los datos de un relator
@app.route("/relator/editar",methods=["PUT"])
def editar_relator():
	if not validar_permiso(request.headers.get('token'),2):
		return None	


	# Request de los json
	# ej: /relator/obtener?rut=xxxx
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
		# Se agregan a la db
		db.session.commit() 
	except:
		return jsonify({"respuesta":"Revise bien los campos de actualizacion"})
	
	# Se hace el dump
	resultado = participante_schema.dump(relator)

	return jsonify(resultado)

# Funcion que se encarga de eliminar un relator
@app.route("/relator/eliminar",methods=["DELETE"])
def eliminar_relator():
	if not validar_permiso(request.headers.get('token'),1):
		return None	
	# Request de los json
	# ej: /relator/eliminar?rut=xxxx
	relator_aux=request.args.get('rut')
	relator = mo.Relator.query.get(relator_aux) # Capturo el relator
	
	try:
		# Se eliminan de la db
		db.session.delete(relator)
		db.session.commit()
		msg="El relator de rut "+relator.rut+" fue eliminado correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"El relator a eliminar no existe"})

# -----------------------------------------------------------------------------------------------------
# --------------------------------------CONTACTO-------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

# Funcion que se encarga de agregar un contacto
@app.route("/contacto/agregar",methods=["POST"])
def crear_contacto():
	if not validar_permiso(request.headers.get('token'),2):
		return None
	
	# Request de los json
	correo=request.json['correo']
	fono=request.json['fono']
	descripcion=request.json['descripcion']
	razon_social=request.json['razon_social']
	
	# Se crea la instancia
	nuevo_contacto=mo.Contacto(correo,fono,descripcion,razon_social)
	
	# Se agrega la instancia
	db.session.add(nuevo_contacto)
	try:
		# Se agrega a la db
		db.session.commit() 
	except:
		return jsonify({"respuesta":"El contacto ya ha sido ingresado"})
	resultado = contacto_schema.dump(nuevo_contacto)

	return jsonify(resultado)

# Funcion que se encarga de filtrar los contactos
@app.route("/contacto/obtener",methods=["GET"])
def filtro_contacto():
	if not validar_permiso(request.headers.get('token'),3):
		return None	
	
	# Request de los json
	# ej: /contacto/obtener?razon_social=xxxx
	id_contacto= request.args.get('id_contacto')
	correo = request.args.get('correo')
	fono = request.args.get('fono')
	descripcion = request.args.get('descripcion')
	razon_social = request.args.get('razon_social')
	
	# Se capturar todos los contactos
	contacto = mo.Contacto.query.filter()

	# En base al los parmetros ingresados por la ruta, se filtran los datos
	if id_contacto != None:
		contacto = contacto.filter(mo.Contacto.id_contacto==id_contacto)
	if correo!= None:
		contacto = contacto.filter(mo.Contacto.correo==correo)
	if fono != None:
		contacto = contacto.filter(mo.Contacto.fono==fono)
	if descripcion != None:
		contacto = contacto.filter(mo.Contacto.descripcion==descripcion)
	if razon_social != None:
		contacto = contacto.filter(mo.Contacto.razon_social==razon_social)

	# Se ordenan de mayor a menor id 
	contacto=contacto.order_by(mo.Contacto.id_contacto.desc())
	contacto_filtrados = contacto_schemas.dump(contacto)
	
	return jsonify(contacto_filtrados)

# Funcion que elimina los contactos
@app.route("/contacto/eliminar",methods=["DELETE"])
def eliminar_contacto():
	if not validar_permiso(request.headers.get('token'),1):
		return None	
	# Request de los json
	# ej: /contacto/eliminar?id_contacto=xxxx
	contacto_aux=request.args.get('id_contacto')
	contacto = mo.Contacto.query.get(contacto_aux) # Capturo el contacto
	
	try:
		# Se elimina el contacto de la db
		db.session.delete(contacto)
		db.session.commit()
		msg="El contacto de id "+str(contacto.id_contacto)+" fue eliminado correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"El contacto a eliminar no existe"})

# Funcion que se encarga de editar un contacto
@app.route("/contacto/editar",methods=["PUT"])
def editar_contacto():
	if not validar_permiso(request.headers.get('token'),2):
		return None	


	# Request de los json
	# ej: /contacto/editar?id_contacto=xxxx
	id_contacto_aux=request.args.get('id_contacto')
	# Captura de contacto
	contacto = mo.Contacto.query.get(id_contacto_aux) 
	
	# Nuevos datos
	correo = request.json['correo']
	fono = request.json['fono']
	descripcion = request.json['descripcion']

	# Actualizacion
	if correo != contacto.correo:
		contacto.correo = correo
	if fono != contacto.fono:
		contacto.fono = fono
	if descripcion != contacto.descripcion:
		contacto.descripcion =descripcion
	
	try:
		# Se agrega a la db
		db.session.commit() 
	except:
		return jsonify({"respuesta":"Revise bien los campos de actualizacion"})
	
	# Se crea el dump
	resultado = contacto_schema.dump(contacto)

	return jsonify(resultado)

# Funcion que obtiene todas las empresas con sus contacos pertinentes
@app.route("/contacto/obtener_empresa",methods=["GET"])
def obtener_contactos_empresa():
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	# Se obtienen todas las empresas
	empresas = mo.Empresa.query.all()
	empresas_contactos=[]
	for i in empresas:
		aux=empresa_schema.dump(i)
		aux["contactos"]=contacto_schemas.dump(i.contactos)
		empresas_contactos.append(aux)

	return jsonify(empresas_contactos)

# Funcion que entrega los contactos asociados a una razon social
@app.route("/contacto/obtener/<razon_social>",methods=["GET"])
def obtener_contactos_razon_social(razon_social):
	if not validar_permiso(request.headers.get('token'),3):
		return None	
	empresa = mo.Empresa.query.get(razon_social)
	contactos=[]
	for i in empresa.contactos:
		if i.fono != None:
			contactos.append({"fono":i.fono})
	return jsonify(contactos)

# Funcion que entrega las descripciones de una razon y fono asociada
# REVISAR ESTA QUERY***
# HACER QUERY DECIFRADO TOKEN***
@app.route("/contacto/obtener_descripcion",methods=["GET"])
def obtener_descripcion():
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	# /contacto/obtener_descripcion?razon_social=XXXX&fono=XXXX
	razon_social = request.args.get('razon_social')
	fono = request.args.get('fono')
	
	contacto = mo.Contacto.query.all()
	desc = []
	for i in contacto:
		if i.fono!=None:
			if (i.razon_social==razon_social and i.fono==fono):
				desc.append({"descripcion":i.descripcion})
	
	return jsonify(desc)

# -----------------------------------------------------------------------------------------------------
# ---------------------------------------FACTURA-------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

# Funcion de agreagar una factura
@app.route("/factura/agregar",methods=["POST"])
def crear_factura():
	if not validar_permiso(request.headers.get('token'),2):
		return None
	
	# Se obtiene el id
	num_factura=db.session.query(mo.Factura).order_by(mo.Factura.id_factura.desc()).first()
	if num_factura is None:
		num_factura=1
	else:
		num_factura=num_factura.id_factura+1
	
	# Request de los json
	num_cai=request.json['num_registro'] # Es ingresable
	num_hes=request.json['num_hes'] 
	fecha_emision=datetime.today().strftime('%Y-%m-%d') 
	fecha_vencimiento=request.json['fecha_vencimiento'] 
	sence=request.json['sence']
	id_instancia=request.json['id_instancia']
	razon_social=request.json['razon_social']
	fono_empresa=request.json['fono_empresa']
	
	# ----------- INFO GENERAL ---------------------------
	
	enviar_factura = request.json['enviar_factura']
	x=["","",""]
	x[enviar_factura]="X"
	especificar = request.json['especificar']
	num_orden = request.json['num_orden'] 
	observacion = request.json['obs']

	# ----------- INFO DEL CURSO -------------------------
	curso_factura = mo.Curso.query.get(sence)
	instancia_factura = mo.Instancia.query.get(id_instancia)
	
	nombre_curso = curso_factura.nombre
	sence_curso = curso_factura.sence
	horas_curso = curso_factura.horas_curso
	fecha_inicio_instancia = instancia_factura.fecha_inicio
	fecha_termino_instancia = instancia_factura.fecha_termino
	num_registro_sence = instancia_factura.id_instancia
	valor_curso = curso_factura.valor_efectivo_participante
	estado = instancia_factura.estado
	
	# --------- INFO DE PARTICIPANTES ----------------------
	lista_participantes = request.get_json()
	lista_rut=[] # Lista con los ruts de los participante

	# Se le asignan la solicitud a todos los participantes de la instancia
	for participante in lista_participantes['participantes']:
		lista_rut.append(participante['rut'])

	# ----------- INFO DE LA EMPRESA ------------------------
	if razon_social is None:
		
		participante=mo.Participante.query.get(lista_rut[0])
		nombre_rs = participante.nombre
		apellido_paterno_rs = participante.apellido_paterno
		apellido_materno_rs = participante.apellido_materno
		if(participante.nombre == None):
			nombre_rs = ''
		if(participante.apellido_paterno == None):
			apellido_paterno_rs = ''
		if(participante.apellido_materno == None):
			apellido_materno_rs = ''
		razon_social = nombre_rs+' '+apellido_paterno_rs+' '+apellido_materno_rs
		giro_empresa= ""
		atencion_empresa= ""
		departamento_empresa = ""
		rut_empresa=participante.rut
		direccion_empresa = request.json["direccion_particular"]
		comuna_empresa = request.json["comuna_particular"]
		fono_empresa=participante.fono_personal
	else:
		empresa_factura = mo.Empresa.query.get(razon_social)
		giro_empresa = empresa_factura.giro
		atencion_empresa = empresa_factura.atencion
		departamento_empresa = empresa_factura.departamento
		rut_empresa = empresa_factura.rut
		direccion_empresa = empresa_factura.direccion
		comuna_empresa = empresa_factura.comuna
		
	# Se calcula el valor total del curso, multiplicando el num de participantes por el valor
	valor_total=valor_curso*len(lista_rut)
	
	# Se instancia la factura
	nueva_factura=mo.Factura(num_factura,sence,num_cai,estado,num_hes,fecha_emision,fecha_vencimiento,enviar_factura,especificar,num_orden,observacion,id_instancia)
	# Se agrega la factura
	db.session.add(nueva_factura)
	try:
		# Se agrega a la db
		db.session.commit() 
	except:
		return jsonify({"respuesta":"La solicitud de factura ya ha sido ingresada o hay un problema con ella"})
	
	# PARA EL FORMULARIO DEL WORD
	tpl=DocxTemplate("backend/db/data/FORMULARIO_No_4_solicitud_de_factura.docx")

	# para los casos particulares
	if num_cai == None:
		num_cai = ''
	if estado == None:
		estado = ''
	if fecha_emision == None:
		fecha_emision = ''
	if razon_social == None:
		razon_social = ''
	if giro_empresa == None:
		giro_empresa = ''		
	if atencion_empresa == None:
		atencion_empresa = ''
	if departamento_empresa == None:		
		departamento_empresa = ''
	if rut_empresa == None:	
		rut_empresa = ''				
	if direccion_empresa == None:
		direccion_empresa = ''		
	if comuna_empresa == None:
		comuna_empresa = ''			
	if fono_empresa == None:
		fono_empresa = ''					
	if fecha_vencimiento == None:
		fecha_vencimiento = ''
	if nombre_curso == None:
		nombre_curso = ''
	if sence_curso == None:
		sence_curso = ''
	if horas_curso == None:
		horas_curso = ''
	if fecha_inicio_instancia == None:
		fecha_inicio_instancia = ''
	if fecha_termino_instancia == None:
		fecha_termino_instancia = ''
	if num_registro_sence == None:
		num_registro_sence = ''
	if valor_curso == None:
		valor_curso = ''
	if valor_total == None:
		valor_total = ''
	if num_orden == None:
		num_orden = ''
	if especificar == None:
		especificar = ''
	if observacion == None:
		observacion = ''

	parametros={
		"numero_cai":num_cai,
		"estado": estado,
		"id_factura":num_factura,
		"fecha_emision":fecha_emision,
		"razon_social": razon_social, 			# 
		"giro":giro_empresa, 					#
		"atencion":atencion_empresa,			#
		"departamento": departamento_empresa,	#
		"rut":rut_empresa,						#
		"direccion":direccion_empresa,			#
		"comuna":comuna_empresa,				#
		"fono":fono_empresa,					#
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

# Funcion para filtrar u obtener las facturas
@app.route("/factura/obtener",methods=["GET"])
def filtro_factura():
	if not validar_permiso(request.headers.get('token'),3):
		return None	
	
	# Request de los json
	# ej: /factura/obtener?sence=xxxx
	# ej: /factura/obtener?sence=xxxx&estado=xxxx
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
	id_instancia = request.args.get('id_instancia')
	mandada = request.args.get('mandada')
	pagada = request.args.get('pagada')
	
	# Se llaman a todas las facturas
	facturas = mo.Factura.query.filter()

	# En base al los parmetros ingresados por la ruta, se filtran los datos
	if id_factura != None:
		facturas = facturas.filter(mo.Factura.id_factura==id_factura)
	if sence != None:
		facturas = facturas.filter(mo.Factura.sence==sence)
	if estado!= None:
		facturas = facturas.filter(mo.Factura.estado==estado)
	if num_hes != None:
		facturas = facturas.filter(mo.Factura.num_hes==num_hes)
	if fecha_emision != None:
		facturas = facturas.filter(mo.Factura.fecha_emision==fecha_emision)
	if fecha_vencimiento != None:
		facturas = facturas.filter(mo.Factura.fecha_vencimiento==fecha_vencimiento)
	if enviar_factura != None:
		facturas = facturas.filter(mo.Factura.enviar_factura==enviar_factura)
	if especificar != None:
		facturas = facturas.filter(mo.Factura.especificar==especificar)
	if num_orden != None:
		facturas = facturas.filter(mo.Factura.num_orden==num_orden)
	if observacion != None:
		facturas = facturas.filter(mo.Factura.observacion==observacion)
	if num_cai != None:
		facturas = facturas.filter(mo.Factura.num_cai==num_cai)
	if id_instancia != None:
		facturas = facturas.filter(mo.Factura.id_instancia==id_instancia)
	if mandada != None:
		facturas = facturas.filter(mo.Factura.mandada==mandada)
	if pagada != None:
		facturas = facturas.filter(mo.Factura.pagada==pagada)

	facturas=facturas.order_by(mo.Factura.id_factura.desc())
	
	facturas_filtradas = factura_schemas.dump(facturas)
	
	return jsonify(facturas_filtradas)

# Funcion que se encarga de editar un contacto
@app.route("/factura/editar",methods=["PUT"])
def editar_factura():
	if not validar_permiso(request.headers.get('token'),2):
		return None	


	# Request de los json
	# ej: /factura/editar?id_factura=xxxx
	id_factura_aux=request.args.get('id_factura')
	# Captura de contacto
	factura = mo.Factura.query.get(id_factura_aux) 
	
	# Nuevos datos
	mandada = request.json['mandada']
	pagada = request.json['pagada']
	
	# Actualizacion
	if mandada != factura.mandada:
		factura.mandada = mandada
	if pagada != factura.pagada:
		factura.pagada = pagada

	try:
		# Se agrega a la db
		db.session.commit() 
	except:
		return jsonify({"respuesta":"Revise bien los campos de actualizacion"})
	
	# Se crea el dump
	resultado = factura_schema.dump(factura)

	return jsonify(resultado)


@app.route("/factura/eliminar",methods=["DELETE"])
def eliminar_factura():
	if not validar_permiso(request.headers.get('token'),1):
		return None	
	id_factura=request.args.get('id_factura')
	factura = mo.Factura.query.get(id_factura) # Capturo la factura
	
	try:
		db.session.delete(factura)
		db.session.commit()
		msg="La factura "+str(factura.id_factura)+" fue eliminada correctamente"
		return jsonify({"respuesta":msg}) 
	except:
		return jsonify({"respuesta":"La factura a eliminar no existe"})
		
@app.route("/factura/obtener/id",methods=["GET"])
def obtener_ids_facturas():
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	ids_facturas = db.session.query(mo.Factura.id_factura).all()
	facturas = factura_schemas.dump(ids_facturas)
	
	return jsonify(facturas)

@app.route("/factura/descargar/<id>",methods=["GET"])
def descargar(id):
	#if not validar_permiso(request.headers.get('token'),3):
	#	return None	
	ruta="db/facturas_generadas/"+str(id)+".docx"
	return send_file(ruta,as_attachment=True)
		
# -----------------------------------------------------------------------------------------------------
# --------------------------------------TABLAS INTERMEDIAS---------------------------------------------
# -----------------------------------------------------------------------------------------------------

@app.route("/relator_instancia/agregar",methods=["POST"])
def crear_RI():
	if not validar_permiso(request.headers.get('token'),2):
		return None
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
	if not validar_permiso(request.headers.get('token'),2):
		return None
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
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	id_instancia = request.args.get('id_instancia')
	razon_social = request.args.get('razon_social')

	instancia = mo.Instancia.query.get(id_instancia)
	if razon_social is None:
		participantes= instancia.alumnos # REVISAR
	else:
		participantes = instancia.alumnos.filter(mo.Participante.razon_social==razon_social)

	participantes_filtrados = participante_schemas.dump(participantes)

	return jsonify(participantes_filtrados)

@app.route("/participante_instancia/obtener_instancias/<rut>",methods=["GET"])
def obtener_instancias_participante(rut):
	if not validar_permiso(request.headers.get('token'),3):
		return None	

	participante = mo.Participante.query.get(rut)

	instancias = participante.instancias

	lista_instancias = []
	for i in instancias:
		curso = mo.Curso.query.get(i.sence)
		instancia = mo.Instancia.query.get(i.id_instancia)
		permiso={
			"id_instancia": i.id_instancia,
			"nombre": curso.nombre,
			"modalidad": curso.modalidad,
			"fecha_inicio": instancia.fecha_inicio.strftime('%Y-%m-%d'),
			"fecha_termino": instancia.fecha_termino.strftime('%Y-%m-%d')
			}
		lista_instancias.append(permiso)
	
	return jsonify(lista_instancias) 

@app.route("/participante_factura/agregar",methods=["POST"])
def crear_PF():
	if not validar_permiso(request.headers.get('token'),2):
		return None
		
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
	if not validar_permiso(request.headers.get('token'),3):
		return None	
	factura = mo.Factura.query.get(id_factura)
	participantes_filtrados = participante_schemas.dump(factura.facturas_alumnos)

	return jsonify(participantes_filtrados)

if __name__ == '__main__':
	app.run(debug=True)
