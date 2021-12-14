from operator import mod
from typing import Text
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



# -----------------------------------------------------------------------------------------------------
# -----------------------------------PARTICIPANTE------------------------------------------------------
# -----------------------------------------------------------------------------------------------------	

@app.route("/participante/agregar",methods=["POST"])
def crear_participante():

	participante_schema = mo.ParticipanteSchema()

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


@app.route("/participante",methods=["GET"])
def filtro_participante():

	participante_schema = mo.ParticipanteSchema(many=True)

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
			
	participantes_filtrado = participante_schema.dump(participantes)
	
	return jsonify(participantes_filtrado)

@app.route("/participante/obtener/rut",methods=["GET"])
def obtener_ruts():

	participante_schema = mo.ParticipanteSchema(many=True)
	rut_curso = db.session.query(mo.Participante.rut).all()
	participantes = participante_schema.dump(rut_curso)
	
	return jsonify(participantes)
# -----------------------------------------------------------------------------------------------------
# ------------------------------------------CURSO------------------------------------------------------
# -----------------------------------------------------------------------------------------------------	

@app.route("/curso/agregar",methods=["POST"])
def crear_curso():

	cuso_schema = mo.CursoSchema(many=True)

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
@app.route("/curso/obtener/sence",methods=["GET"])
def obtener_sences():

	curso_schema = mo.CursoSchema(many=True)
	sence_curso = db.session.query(mo.Curso.rut).all()
	cursos = curso_schema.dump(sence_curso)
	
	return jsonify(cursos)
# -----------------------------------------------------------------------------------------------------
# ----------------------------------------EMPRESA------------------------------------------------------
# -----------------------------------------------------------------------------------------------------	

@app.route("/empresa",methods=["GET"])
def filtro_empresas():
	
	empresa_schema = mo.EmpresaSchema(many=True)
	razon_social = request.json['razon_social']
	giro = request.json['giro']
	atencion = request.json['atencion']
	departamento = request.json['departamento']
	rut = request.json['rut']
	direccion = request.json['direccion']
	comuna = request.json['comuna']
	correo = request.json['correo']
	fono = request.json['fono']	
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

	empresas_filtrados = empresa_schema.dump(empresas)
	
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

	empresa_schema = mo.EmpresaSchema(many=True)
	razon_Social_Empresa = db.session.query(mo.Empresa.razon_social).all()
	empresa = empresa_schema.dump(razon_Social_Empresa)
	
	return jsonify(empresa)

if __name__ == '__main__':
	app.run(debug=True)