from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import json

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cai"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

import db.modelos as mo

@app.route('/api/v1.0/test')
def test():
	return jsonify("Probando a ver si devuelve2")

@app.route("/crear_participante",methods=["POST"])
def crear_participante():

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
	nuevo_participante=mo.Participante(rut,nombre,apellido_paterno,apellido_materno,genero,nivel_educacional,fecha_nacimiento,nacionalidad,tipo_inscripcion,ocupacion,correo,fono,razon_social)
	
	db.session.add(nuevo_participante)
	try:
		db.session.commit() # con esto lo agrego *super importante*
	except:
		return jsonify({"respuesta":"Participante ya ha sido ingresado"})
	return jsonify({"respuesta":"Participante creado correctamente!"})
if __name__ == '__main__':
	app.run(debug=True)