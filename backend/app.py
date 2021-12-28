from datetime import datetime
from operator import mod
from typing import Text
import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
import sqlalchemy.orm.exc
import json

from sqlalchemy.sql import text
import db.modelos as mo
db= mo.objeto_db()
app= Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cai"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

ma = Marshmallow(app)
migrate= Migrate(app,db)

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

orden_schema= mo.OrdenSchema()
orden_schemas= mo.OrdenSchema(many=True)

instancia_schema=mo.InstanciaSchema()
instancia_schemas=mo.InstanciaSchema(many=True)

contacto_schema= mo.ContactoSchema()
contacto_schemas= mo.ContactoSchema(many=True)

@app.route("/paises/obtener",methods=["GET"])
def obtener_paises():
	r = requests.get('https://restcountries.com/v3.1/all?fields=translations',)
	paises=r.json()
	respuesta=[]
	for x in paises:
		resp=x['translations']['spa']['common']
		respuesta.append(resp)
	return jsonify(respuesta)
"""
@app.route('/regiones/chile/obtener',methods=["GET"])
def obtener_regiones_chile():
	r = requests.get('https://apis.digital.gob.cl/dpa/regiones',)
	regiones=r.json()
	respuesta=[]
	for x in regiones:
		resp={
			'codigo':x['codigo'],
			'nombre': x['nombre']
		}
		respuesta.append(resp)
	return jsonify(respuesta)
@app.route('/comunas/chile/obtener/region=<codigo>',methods=['GET'])
def obtener_comuna_por_region(codigo):
	if int(codigo)<1 and int(codigo)>16:
		return jsonify({"respuesta":"codigo de region no valido"})
	url='https://apis.digital.gob.cl/dpa/regiones/'+codigo+'/comunas'
	print(url)
	r = requests.get(url=url)
	comunas=r.json()
	respuesta=[]
	for x in comunas:
		resp=x['nombre']
		respuesta.append(resp)
	return jsonify(respuesta)
"""
# -----------------------------------------------------------------------------------------------------
# -----------------------------------PARTICIPANTE------------------------------------------------------
# -----------------------------------------------------------------------------------------------------	

@app.route("/participante/agregar",methods=["POST"])
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
	#{participantes=[{participabte1},{participabte2},{participabte2}]}
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

	sence_curso = db.session.query(mo.Curso.rut).all()
	cursos = curso_schemas.dump(sence_curso)
	
	return jsonify(cursos)

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

# *** TERMINAR ESTO ***
@app.route("/instancia/<sence>/vigentes",methods=["GET"])
def obtener_instancias_vigentes(sence):
	instancias = mo.Instancia.query.filter()
	instancias = instancias.filter(mo.Instancias.sence==sence)
	
	participante = mo.Participante.query.get(rut)
	instancias = instancia_schemas.dump(participante.instancias)
	return jsonify(instancias)
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
	if giro != None:
		empresas = empresas.filter(mo.Empresa.razon_social==razon_social)
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
	fono_corporativo=request.json['fono_coperativo']
	correo_personal=request.json['correo_personal']
	correo_corporativo=request.json['correo_corporativo']
	
	nuevo_relator=mo.Relator(rut,nombre,apellido_paterno,apellido_materno,titulo,genero,cv,fecha_nacimiento,numero_cuenta,banco,tipo_cuenta,fono_personal,
	fono_corporativo,correo_personal,correo_corporativo)
	
	db.session.add(nuevo_relator)
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"El relator ya ha sido ingresado"})
	
	resultado = relator_schema.dump(nuevo_relator)

	return jsonify(resultado)

# -----------------------------------------------------------------------------------------------------
# --------------------------------------CONTACTO-------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

@app.route("/contacto/agregar",methods=["POST"])
def crear_contacto():

	id_contacto=request.json['id_contacto']
	correo=request.json['correo']
	fono=request.json['fono']
	descripcion=request.json['descripcion'] #PROBLEMAS CON LA DESCRIPCION, SALE NULL
	razon_social=request.json['razon_social']
	
	nuevo_contacto=mo.Contacto(id_contacto,correo,fono,descripcion,razon_social)
	
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

	contacto_filtrados = contacto_schemas.dump(contacto)
	
	return jsonify(contacto_filtrados)

# -----------------------------------------------------------------------------------------------------
# ---------------------------------------FACTURA-------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

@app.route("/factura/agregar",methods=["POST"])
def crear_factura():

	#id_factura=request.json['id_factura'] # Como hacer que el id se aumente solo?
	#num_registro=request.json['num_registro'] #Este numero se debe ingresar o es fijo?
	#estado=request.json['estado'] # El estado lo definimos nosotros?
	#tipo_pago=request.json['tipo_pago'] # Segun yo este no va
	#num_hes=request.json['num_hes'] #Cuando se ingresa, siempre a veces?
	#fecha_emision=request.json['fecha_emision']
	#fecha_vencimiento=request.json['fecha_vencimiento'] # Esta la definen en base al vencimiento de que?
	sence=request.json['sence']

	# ----------- INFO GENERAL ---------------------------

	#num_factura = #Lo usan? puede ser id de factura
	#datos_de = #Sara Perez Rojas - Director Centro USACH - FIJOS
	#datos_a = #Director Ejecutivo Capacitacion USACH - FIJOS
	#nombre_proyecto = #Curso de Capacitacion CAI-2006 / Siempre es el mismo?
	#codigo_proyecto = #CAP-CAI-15 / Siempre es el mismo?
	#enviar_factura = #3 opciones: USACH, EMPRESA, OTRO
	#num_orden = #Cuando tiene una orden OTIC asociada
	#obs = #Agregan un correo o numero de la empresa

	# ----------- INFO DEL CURSO -------------------------
	curso_factura = mo.Curso.query.get(sence)
	
	nombre_curso = curso_factura.nombre
	sence_curso = curso_factura.sence
	horas_curso = curso_factura.horas_curso
	#fecha_incio_instancia = #?
	#fecha_termino_instancia = #?
	#num_registro_sence = # de donde sale, es el que esta en curso? 
	valor_curso = curso_factura.valor_efectivo_participante
	# En las soli sale participante y un mensaje, ese msj es predeterminado o varia?
	# En una soli agregaron el nombre de otra empresa y el rut correspondiente, cuando se hace eso?

	# ----------- INFO DE LA EMPRESA ------------------------

	# con sence, obtener la empresa
	
	# empresa.empleados

	# duda existencial, la solicitud de factura es difernet cuando es particular? porq si es asi debe haber una relacion entre factura y empresa
	# razon_social = 
	# giro_empresa =
	# atencion_empresa = con que se rellena este campo? Duda a la clienta
	# departamento_empresa =
	# rut_empresa = aun no responde la duda la clienta sobre el tema del rut
	# direccion_empresa =
	# fono_empresa =
	'''
	nueva_factura=mo.Factura(id_factura,num_registro,estado,tipo_pago,num_hes,fecha_emision,fecha_vencimiento,sence)
	
	db.session.add(nueva_factura)
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"La solicitud de factura ya ha sido ingresada"})
	
	resultado = factura_schema.dump(nueva_factura)
	'''
	return jsonify("Termine")


@app.route("/factura/obtener",methods=["GET"])
def filtro_factura():
	
	id_factura= request.args.get('id_factura')
	num_registro = request.args.get('num_registro')
	estado = request.args.get('estado')
	tipo_pago = request.args.get('tipo_pago')
	num_hes = request.args.get('num_hes')
	fecha_emision = request.args.get('fecha_emision')
	fecha_vencimiento = request.args.get('fecha_vencimiento')
	sence = request.args.get('sence')
	
	factura = mo.Factura.query.filter()

	if id_factura != None:
		factura = factura.filter(mo.Factura.id_factura==id_factura)
	if num_registro != None:
		factura = factura.filter(mo.Factura.num_registro==num_registro)
	if estado!= None:
		factura = factura.filter(mo.Factura.estado==estado)
	if tipo_pago != None:
		factura = factura.filter(mo.Factura.tipo_pago==tipo_pago)
	if num_hes != None:
		factura = factura.filter(mo.Factura.num_hes==num_hes)
	if fecha_emision != None:
		factura = factura.filter(mo.Factura.fecha_emision==fecha_emision)
	if fecha_vencimiento != None:
		factura = factura.filter(mo.Factura.fecha_vencimiento==fecha_vencimiento)
	if sence != None:
		factura = factura.filter(mo.Factura.sence==sence)

	facturas_filtradas = factura_schemas.dump(factura)
	
	return jsonify(facturas_filtradas)
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