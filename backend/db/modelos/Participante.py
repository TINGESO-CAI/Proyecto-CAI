from ...server import db
class Participante:
	__tablename__ = 'participante'

	rut = db.Column(db.Text, primary_key=True)
	nombre = db.Column(db.Text)
	apellido_paterno = db.Column(db.Text)
	apellido_materno = db.Column(db.Text)
	genero = db.Column(db.Integer)
	fecha_nacimiento = db.Column(db.Date)
	nivel_educacional = db.Column(db.Text)
	nacionalidad = db.Column(db.Text)
	tipo_inscripcion = db.Column(db.Text)
	ocupacion = db.Column(db.Text)
	correo = db.Column(db.Text)
	fono = db.Column(db.Text)
	razon_social = db.Column(db.ForeignKey('empresa.razon_social'))

	empresa = db.relationship('Empresa')
	curso = db.relationship('Curso', secondary='participante_curso')
	def __init__(self,rut,nombre,apellido_paterno,apellido_materno,genero,nivel_educacional,fecha_nacimiento,nacionalidad,tipo_inscripcion,ocupacion,correo,fono,razon_social):
		self.rut = rut
		self.nombre=nombre
		self.apellido_paterno=apellido_paterno
		self.apellido_materno=apellido_materno
		self.genero=genero
		self.nivel_educacional=nivel_educacional
		self.fecha_nacimiento=fecha_nacimiento
		self.nacionalidad=nacionalidad
		self.tipo_inscripcion=tipo_inscripcion
		self.ocupacion=ocupacion
		self.correo=correo
		self.fono=fono
		self.razon_social=razon_social
