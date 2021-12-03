from ...server import db
class Orden:
	__tablename__ = 'orden'

	id_orden = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('orden_id_orden_seq'::regclass)"))
	sence = db.Column(db.Text)
	cancelacion = db.Column(db.Integer)
	fecha_inicio = db.Column(db.Date)
	fecha_termino = db.Column(db.Date)

	participante = db.relationship('Participante', secondary='participante_orden')
	def __init__(self,id_orden,sence,cancelacion,fecha_inicio,fecha_termino):
		self.id_orden = id_orden
		self.sence=sence
		self.cancelacion=cancelacion
		self.fecha_inicio=fecha_inicio
		self.fecha_termino=fecha_termino

	