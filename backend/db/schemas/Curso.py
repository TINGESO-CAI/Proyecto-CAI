from ...server import db
class Curso(db.Model):
	__tablename__ = 'curso'
	sence = db.Column(db.Text, primary_key=True)
	nombre = db.Column(db.Text)
	modalidad = db.Column(db.Text)
	categoria = db.Column(db.Text)
	horas_curso = db.Column(db.Integer)
	valor_efectivo_participante = db.Column(db.Integer)
	valor_imputable_participante = db.Column(db.Integer)
	resolucion_sence = db.Column(db.Text)
	resolucion_usach = db.Column(db.Text)
	estado = db.Column(db.Text)
	f_vigencia = db.Column(db.Date)
	def __init__(self,sence,nombre,modalidad,categoria,horas_curso,valor_efectivo_participante,valor_imputable_participante,resolucion_sence,resolucion_usach,estado,f_vigencia):
		self.sence = sence
		self.nombre=nombre
		self.modalidad=modalidad
		self.categoria=categoria
		self.horas_curso=horas_curso
		self.valor_efectivo_participante=valor_efectivo_participante
		self.valor_imputable_participante=valor_imputable_participante
		self.resolucion_sence=resolucion_sence
		self.resolucion_usach=resolucion_usach
		self.estado=estado
		self.f_vigencia=f_vigencia