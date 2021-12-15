from operator import mod
from typing import Text
import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
import json

from sqlalchemy.sql import text
import db.modelos as mo
app= Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cai"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

participante_schema = mo.ParticipanteSchema()
participante_schemas = mo.ParticipanteSchema(many=True)

curso_schema = mo.CursoSchema()
curso_schemas = mo.CursoSchema(many=True)

empresa_schema = mo.EmpresaSchema()
empresa_schemas = mo.EmpresaSchema(many=True)

relator_schema = mo.RelatorSchema()
relator_schemas = mo.RelatorSchema(many=True)

#factura_schema= mo.FacturaSchema()
#factura_schemas= mo.FacturaSchema(many=True)

orden_schema= mo.OrdenSchema()
orden_schemas= mo.OrdenSchema(many=True)

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
	correo=request.json['correo']
	fono=request.json['fono']
	razon_social=request.json['razon_social']
	
	nuevo_participante=mo.Participante(rut,nombre,apellido_paterno,apellido_materno,genero,nivel_educacional,fecha_nacimiento,nacionalidad,tipo_inscripcion,ocupacion,correo,fono,razon_social)
	
	db.session.add(nuevo_participante)
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"El participante ya ha sido ingresado"})
	
	resultado = participante_schema.dump(nuevo_participante)

	return jsonify(resultado)


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
	correo=request.args.get('correo')
	fono=request.args.get('fono')
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
	if correo!= None:
		participantes = participantes.filter(mo.Participante.correo==correo)
	if fono!= None:
		participantes = participantes.filter(mo.Participante.fono==fono)
	if razon_social!= None:
		participantes = participantes.filter(mo.Participante.razon_social==razon_social)
			
	participantes_filtrado = participante_schemas.dump(participantes)
	
	return jsonify(participantes_filtrado)

@app.route("/participante/obtener/rut",methods=["GET"])
def obtener_ruts():

	rut_curso = db.session.query(mo.Participante.rut).all()
	participantes = participante_schemas.dump(rut_curso)
	
	return jsonify(participantes)
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
# ----------------------------------------EMPRESA------------------------------------------------------
# -----------------------------------------------------------------------------------------------------	

@app.route("/empresa",methods=["GET"])
def filtro_empresas():
	

	razon_social = request.args.get('razon_social')
	giro = request.args.get('giro')
	atencion = request.args.get('atencion')
	departamento = request.args.get('departamento')
	rut = request.args.get('rut')
	direccion = request.args.get('direccion')
	comuna = request.args.get('comuna')
	correo = request.args.get('correo')
	fono = request.args.get('fono')
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
	if correo != None:
		empresas = empresas.filter(mo.Empresa.correo==correo)
	if fono != None:
		empresas = empresas.filter(mo.Empresa.fono==fono)

	empresas_filtrados = empresa_schemas.dump(empresas)
	
	return jsonify(empresas_filtrados)

@app.route("/empresa/agregar",methods=["POST"])
def crear_empresa():

	razon_social = request.json['razon_social']
	giro = request.json['giro']
	atencion = request.json['atencion']
	departamento = request.json['departamento']
	rut = request.json['rut']
	direccion = request.json['direccion']
	comuna = request.json['comuna']
	correo = request.json['correo']
	fono = request.json['fono']

	nuevo_empresa=mo.Empresa(razon_social,giro,atencion,departamento,rut,direccion,comuna,correo,fono)

	db.session.add(nuevo_empresa)
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"La empresa ya ha sido ingresada"})
	return jsonify({"respuesta":"Empresa ingresada correctamente!"})

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
	cv = request.args.get('cv')
	fecha_nacimiento = request.args.get('fecha_nacimiento')
	numero_cuenta = request.args.get('numero_cuenta')
	banco = request.args.get('banco')
	tipo_cuenta = request.args.get('tipo_cuenta')
	
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

	relator_filtrados = relator_schemas.dump(relator)
	
	return jsonify(relator_filtrados)

@app.route("/relator/agregar",methods=["POST"])
def crear_relator():

	rut=request.json['rut']
	nombre=request.json['nombre']
	apellido_paterno=request.json['apellido_paterno']
	apellido_materno=request.json['apellido_materno']
	titulo=request.json['titulo']
	#genero=request.json['genero']
	cv=request.json['cv']
	fecha_nacimiento=request.json['fecha_nacimiento']
	numero_cuenta=request.json['numero_cuenta']
	banco=request.json['banco']
	tipo_cuenta=request.json['tipo_cuenta']
	
	nuevo_relator=mo.Relator(rut,nombre,apellido_paterno,apellido_materno,titulo,cv,fecha_nacimiento,numero_cuenta,banco,tipo_cuenta)
	
	db.session.add(nuevo_relator)
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"El relator ya ha sido ingresado"})
	
	resultado = relator_schema.dump(nuevo_relator)

	return jsonify(resultado)

#################################
#############TABLA INTERMEDIA####
#################################
@app.route("/relator_curso/agregar",methods=["POST"])
def crear_RC():
	rut=request.json['rut']
	sence=request.json['sence']
	nuevo_RC=mo.Relator_Curso(rut,sence)
	db.session.add(nuevo_RC)
	try:
		db.session.commit()
	except:
		return jsonify({"respuesta":"Esta relacion ya ha sido ingresado"})
	return jsonify({"respuesta":"Relator ha sido ingresado"})

@app.route("/participante_curso/agregar",methods=["POST"])
def crear_PC():
	rut=request.json['rut']
	sence=request.json['sence']
	nuevo_PC=mo.Participante_Curso(rut,sence)
	db.session.add(nuevo_PC)
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"Esta relacion ya ha sido ingresado"})
	return jsonify({"respuesta":"Participante ha sido ingresado"})
if __name__ == '__main__':
	app.run(debug=True)