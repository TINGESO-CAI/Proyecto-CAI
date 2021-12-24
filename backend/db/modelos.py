from flask_sqlalchemy import SQLAlchemy 
from marshmallow import Schema, fields, ValidationError, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from sqlalchemy.schema import CreateColumn
from sqlalchemy.ext.compiler import compiles



db=SQLAlchemy()


relator_instancia=db.Table('relator_instancia',
	db.Column('rut',db.Text, db.ForeignKey('relator.rut')),
	db.Column('id_instancia',db.Integer, db.ForeignKey('instancia.id_instancia'))
	)
	
participante_instancia=db.Table('participante_instancia',
	db.Column('rut',db.Text, db.ForeignKey('participante.rut')),
	db.Column('id_instancia',db.Integer, db.ForeignKey('instancia.id_instancia'))
)

partipante_factura= db.Table('participante_factura',
	db.Column('rut',db.Text, db.ForeignKey('participante.rut')),
	db.Column('id_factura',db.Integer, db.ForeignKey('factura.id_factura'))
)

partipante_orden=db.Table('participante_orden',
	db.Column('rut',db.Text, db.ForeignKey('participante.rut')),
	db.Column('id_orden',db.Integer, db.ForeignKey('orden.id_orden'))
)



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

class CursoSchema(SQLAlchemyAutoSchema):
	class Meta:
		fields = ('sence','nombre',
		'modalidad','categoria','horas_curso','valor_efectivo_participante','valor_imputable_participante',
		'resolucion_sence','resolucion_usach','estado','f_vigencia')

class Instancia(db.Model):
	
	__tablename__ = 'instancia'
	id_instancia = db.Column(db.Integer, primary_key=True)
	sence = db.Column(db.ForeignKey('curso.sence'))
	direccion = db.Column(db.Text)
	malla = db.Column(db.Boolean)
	fecha_inicio = db.Column(db.Date)
	fecha_termino = db.Column(db.Date)
	
	curso = db.relationship('Curso')
	
	def __init__(self,id_instancia,sence,direccion,malla,fecha_inicio,fecha_termino):
		self.id_instancia = id_instancia
		self.sence = sence
		self.direccion = direccion
		self.malla = malla 
		self.fecha_inicio = fecha_inicio
		self.fecha_termino = fecha_termino

class InstanciaSchema(SQLAlchemyAutoSchema):
	class Meta:
		fields = ('id_instancia','sence','direccion',
		'malla','fecha_inicio','fecha_termino')		
		
class Orden(db.Model):
	__tablename__ = 'orden'

	id_orden = db.Column(db.Integer, primary_key=True)
	sence = db.Column(db.Text)
	cancelacion = db.Column(db.Integer)
	fecha_inicio = db.Column(db.Date)
	fecha_termino = db.Column(db.Date)
	persona_asignada_o = db.relationship('Participante', secondary='participante_orden', backref=db.backref('asignar_orden',lazy='dinamic'))
	
	def __init__(self,id_orden,sence,cancelacion,fecha_emision,fecha_vencimiento):
		self.id_orden = id_orden
		self.sence=sence
		self.cancelacion=cancelacion
		self.fecha_emision=fecha_emision
		self.fecha_vencimiento=fecha_vencimiento

class OrdenSchema(SQLAlchemyAutoSchema):
	class Meta:
		fields = ('id_orden','sence',
		'cancelacion','fecha_emision','fecha_vencimiento')

class Factura(db.Model):
	__tablename__ = 'factura'

	id_factura = db.Column(db.Integer, primary_key=True)
	sence = db.Column(db.Text)
	num_registro = db.Column(db.Text)
	estado = db.Column(db.Integer)
	tipo_pago = db.Column(db.Integer)
	num_hes = db.Column(db.Text)
	fecha_emision = db.Column(db.Date)
	fecha_vencimiento = db.Column(db.Date)
	persona_asignada_f = db.relationship('Participante', secondary='participante_orden', backref=db.backref('asignar_factura',lazy='dinamic'))
	
	def __init__(self,id_factura,sence,num_registro,estado,tipo_pago,num_hes,fecha_emision,fecha_vencimiento):
		self.id_factura = id_factura
		self.sence = sence
		self.num_registro =num_registro
		self.estado = estado
		self.tipo_pago = tipo_pago
		self.num_hes = num_hes
		self.fecha_emision = fecha_emision
		self.fecha_vencimiento =fecha_vencimiento

class OrdenSchema(SQLAlchemyAutoSchema):
	class Meta:
		fields = ('id_orden','sence',
		'cancelacion','fecha_emision','fecha_vencimiento')

class Empresa(db.Model):
	__tablename__ = 'empresa'

	razon_social = db.Column(db.Text, primary_key=True)
	giro = db.Column(db.Text)
	atencion = db.Column(db.Text)
	departamento = db.Column(db.Text)
	rut = db.Column(db.Text)
	direccion = db.Column(db.Text)
	comuna = db.Column(db.Text)


	def __init__(self,razon_social,giro,atencion,departamento,rut,direccion,comuna):
		self.razon_social = razon_social
		self.giro=giro
		self.atencion=atencion
		self.departamento=departamento
		self.rut=rut
		self.direccion=direccion
		self.comuna=comuna


class EmpresaSchema(SQLAlchemyAutoSchema):
	class Meta:
		fields = ('razon_social','giro',
		'atencion','departamento','rut',
		'direccion','comuna')

class Participante(db.Model):
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
	fono_personal=db.Column(db.Text)
	fono_corporativo=db.Column(db.Text)
	correo_corporativo=db.Column(db.Text)
	correo_personal=db.Column(db.Text)
	
	razon_social = db.Column(db.ForeignKey('empresa.razon_social'))

	empresa = db.relationship('Empresa')

	def __init__(self,rut,nombre,apellido_paterno,apellido_materno,genero,nivel_educacional,fecha_nacimiento,nacionalidad,tipo_inscripcion,ocupacion,razon_social):
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
		self.razon_social=razon_social

class ParticipanteSchema(SQLAlchemyAutoSchema):
	class Meta:
		fields = ('rut','nombre',
		'apellido_paterno','apellido_materno',
		'genero','fecha_nacimiento','nivel_educacional',
		'nacionalidad','tipo_inscripcion','ocupacion',
		'razon_social')

class Relator(db.Model):
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
	fono_personal=db.Column(db.Text)
	fono_corporativo=db.Column(db.Text)
	correo_corporativo=db.Column(db.Text)
	correo_personal=db.Column(db.Text)
	
	inscripciones = db.relationship('Instancia', secondary='relator_instancia', backref=db.backref('inscribir',lazy='dinamic'))
	

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
	
class RelatorSchema(SQLAlchemyAutoSchema):
	class Meta:
		fields = ('rut','nombre',
		'apellido_paterno','apellido_materno',
		'titulo','cv','fecha_nacimiento',
		'numero_cuenta','banco','tipo_cuenta')
		

class Contacto(db.Model):
	__tablename__ = 'contacto'
	id_contacto = db.Column(db.Integer, primary_key=True,autoincrement=True)
	correo = db.Column(db.Text)
	fono = db.Column(db.Text)
	razon_social = db.Column(db.ForeignKey('empresa.razon_social'))
	empresa = db.relationship('Empresa')
	def __init__(self,correo,fono,razon_social):
		self.correo = correo
		self.fono = fono
		self.razon_social=razon_social
class ContactoSchema(SQLAlchemyAutoSchema):
	class Meta:
		fields = ('id_contacto','contacto','fono','razon_social')	
	
def objeto_db():
	global db
	return db