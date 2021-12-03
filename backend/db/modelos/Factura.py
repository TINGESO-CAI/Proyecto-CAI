from ...server import db
class Factura:
	__tablename__ = 'factura'

	id_factura = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('factura_id_factura_seq'::regclass)"))
	num_registro = db.Column(db.Text)
	estado = db.Column(db.Integer)
	tipo_pago = db.Column(db.Integer)
	num_hes = db.Column(db.Text)
	fecha_emision = db.Column(db.Date)
	fecha_vencimiento = db.Column(db.Date)

	participante = db.relationship('Participante', secondary='participante_factura')
	def __init__(self,id_factura,num_registro,estado,tipo_pago,num_hes,fecha_emision,fecha_vencimiento):
		self.id_factura = id_factura
		self.num_registro=num_registro
		self.estado=estado
		self.tipo_pago=tipo_pago
		self.num_hes=num_hes
		self.fecha_emision=fecha_emision
		self.fecha_vencimiento=fecha_vencimiento
	