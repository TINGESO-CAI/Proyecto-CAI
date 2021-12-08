from operator import mod
from typing import Text
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
import json

app= Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cai"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

import db.modelos as mo

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
	try:
		razon_social=request.json['razon_social']
	except:
		razon_social=None
	
	nuevo_participante=mo.Participante(rut,nombre,apellido_paterno,apellido_materno,genero,nivel_educacional,fecha_nacimiento,nacionalidad,tipo_inscripcion,ocupacion,correo,fono,razon_social)
	
	db.session.add(nuevo_participante)
	try:
		db.session.commit() 
	except:
		return jsonify({"respuesta":"El participante ya ha sido ingresado"})
	
	resultado = participante_schema.dump(nuevo_participante)

	return jsonify(resultado)

@app.route("/participante/obtener/todos",methods=["GET"])
def obtener_todos():

	participante_schema = mo.ParticipanteSchema(many=True)

	todosParticipante = mo.Participante.query.all()
	listaParticipante = participante_schema.dump(todosParticipante)

	return jsonify(listaParticipante)

@app.route("/participante/obtener/rut",methods=["GET"])
def obtener_por_rut():

	participante_schema = mo.ParticipanteSchema()

	rut=request.json['rut']
	rutParticipante = mo.Participante.query.get(rut)

	participante = participante_schema.dump(rutParticipante)
	
	return jsonify(participante)

@app.route("/participante/filtro",methods=["GET"])
def filtro():

	participante_schema = mo.ParticipanteSchema()



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

	empresa_schema = mo.EmpresaSchema()

	razon_social=request.json['razon_social']
	razon_Social_Empresa = mo.Empresa.query.get(razon_social)
	empresa = empresa_schema.dump(razon_Social_Empresa)
	
	return jsonify(empresa)

# AUN NO SE TERMINA ***
@app.route("/empresa/obtener/rut",methods=["GET"])
def e_obtener_por_rut():

	empresa_schema = mo.EmpresaSchema()

	rut=request.json['rut']
	print(rut)
	rutEmpresa = db.session.query(mo.Empresa).filter(mo.Empresa.rut == rut)
	empresa = empresa_schema.dump(rutEmpresa)
	
	return jsonify(rutEmpresa)

if __name__ == '__main__':
	app.run(debug=True)