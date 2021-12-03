from ...server import db
class Relator:
	__tablename__ = 'relator'

	rut = db.Column(db.Text, primary_key=True)
	nombre = db.Column(db.Text)
	apellido_paterno = db.Column(db.Text)
	apellido_materno = db.Column(db.Text)
	titulo = db.Column(db.Text)
	cv = db.Column(db.Text)
	fecha_nacimiento = db.Column(db.Date)
	numero_cuenta = db.Column(db.Text)
	banco = db.Column(db.Text)
	tipo_cuenta = db.Column(db.Text)

	curso = db.relationship('Curso', secondary='relator_curso')
	def __init__(self,rut,nombre,apellido_paterno,apellido_materno,titulo,cv,fecha_nacimiento,numero_cuenta,banco,tipo_cuenta):
		self.rut = rut
		self.nombre=nombre
		self.apellido_paterno=apellido_paterno
		self.apellido_materno=apellido_materno
		self.titulo=titulo
		self.cv=cv
		self.fecha_nacimiento=fecha_nacimiento
		self.numero_cuenta=numero_cuenta
		self.banco=banco
		self.tipo_cuenta=tipo_cuenta
	
