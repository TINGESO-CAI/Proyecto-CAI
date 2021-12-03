from ...server import db
class Empresa:
	__tablename__ = 'empresa'

	razon_social = db.Column(db.Text, primary_key=True)
	giro = db.Column(db.Text)
	atencion = db.Column(db.Text)
	departamento = db.Column(db.Text)
	rut = db.Column(db.Text)
	direccion = db.Column(db.Text)
	comuna = db.Column(db.Text)
	correo = db.Column(db.Text)
	fono = db.Column(db.Text)

	def __init__(self,razon_social,giro,atencion,departamento,rut,direccion,comuna,correo,fono):
		self.razon_social = razon_social
		self.giro=giro
		self.atencion=atencion
		self.departamento=departamento
		self.rut=rut
		self.direccion=direccion
		self.comuna=comuna
		self.correo=correo
		self.fono=fono
	