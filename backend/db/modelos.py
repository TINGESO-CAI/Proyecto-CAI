from flask_sqlalchemy import SQLAlchemy 
from marshmallow import Schema, fields, ValidationError, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import backref

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

participante_factura = db.Table('participante_factura',
	db.Column('rut',db.Text, db.ForeignKey('participante.rut')),
	db.Column('id_factura',db.Integer, db.ForeignKey('factura.id_factura'))
)

participante_orden=db.Table('participante_orden',
	db.Column('rut',db.Text, db.ForeignKey('participante.rut')),
	db.Column('id_orden',db.Integer, db.ForeignKey('orden.id_orden'))
)

class Contacto(db.Model):
	__tablename__ = 'contacto'
	id_contacto = db.Column(db.Integer, primary_key=True,autoincrement=True)
	correo = db.Column(db.Text)
	fono = db.Column(db.Text)
	descripcion = db.Column(db.Text)
	razon_social = db.Column(db.ForeignKey('empresa.razon_social'))

	empresa = db.relationship('Empresa')
	def __init__(self,id_contacto,correo,fono,descripcion,razon_social):
		self.id_contacto = id_contacto
		self.correo = correo
		self.fono = fono
		self.descpricion=descripcion
		self.razon_social=razon_social
		

class ContactoSchema(SQLAlchemyAutoSchema):
	class Meta:
		fields = ('id_contacto','correo','fono','descripcion','razon_social')	


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
	instancias = db.relationship('Instancia', backref=db.backref("curso"))
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

class Empresa(db.Model):
	__tablename__ = 'empresa'

	razon_social = db.Column(db.Text, primary_key=True)
	giro = db.Column(db.Text)
	atencion = db.Column(db.Text)
	departamento = db.Column(db.Text)
	rut = db.Column(db.Text)
	direccion = db.Column(db.Text)
	comuna = db.Column(db.Text)

	contactos=db.relationship('Contacto',backref=db.backref('contacto'))
	empleados=db.relationship('Participante',backref=db.backref('participante'))

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

class Factura(db.Model):
	__tablename__ = 'factura'

	id_factura = db.Column(db.Integer, primary_key=True)
	sence = db.Column(db.Text)
	num_cai = db.Column(db.Text)
	estado = db.Column(db.Integer)
	num_hes = db.Column(db.Text)
	fecha_emision = db.Column(db.Date)
	fecha_vencimiento = db.Column(db.Date)
	enviar_factura = db.Column(db.Integer)
	especificar = db.Column(db.Text)
	num_orden = db.Column(db.Text)
	observacion = db.Column(db.Text)

	def __init__(self,id_factura,sence,num_cai,estado,num_hes,fecha_emision,fecha_vencimiento,enviar_factura,especificar,num_orden,observacion):
		self.id_factura = id_factura
		self.sence = sence
		self.num_cai =num_cai
		self.estado = estado
		self.num_hes = num_hes
		self.fecha_emision = fecha_emision
		self.fecha_vencimiento =fecha_vencimiento
		self.enviar_factura = enviar_factura
		self.especificar = especificar
		self.num_orden = num_orden
		self.observacion = observacion

class FacturaSchema(SQLAlchemyAutoSchema):
	class Meta:
		fields = ('id_factura','sence','num_cai'
		'estado','tipo_pago','num_hes', 'fecha_emision','fecha_vencimiento','enviar_factura','especificar','num_orden','observacion')


class Instancia(db.Model):
	
	__tablename__ = 'instancia'
	id_instancia = db.Column(db.Integer, primary_key=True)
	sence = db.Column(db.ForeignKey('curso.sence'))
	direccion = db.Column(db.Text)
	malla = db.Column(db.Boolean)
	fecha_inicio = db.Column(db.Date)
	fecha_termino = db.Column(db.Date)

	
	
	def __init__(self,sence,direccion,malla,fecha_inicio,fecha_termino):
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
	persona_asignada_o = db.relationship('Participante', secondary='participante_orden', backref=db.backref('asignar_orden'))
	
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
	facturas = db.relationship('Factura', secondary='participante_factura', backref=db.backref('facturas_alumnos'))

	instancias = db.relationship('Instancia', secondary='participante_instancia', backref=db.backref('alumnos', lazy='dynamic'))
	
	razon_social = db.Column(db.ForeignKey('empresa.razon_social'))
	empresa = db.relationship('Empresa')

	def __init__(self,rut,nombre,apellido_paterno,apellido_materno,genero,nivel_educacional,fecha_nacimiento,nacionalidad,tipo_inscripcion,ocupacion,fono_personal,fono_corporativo,correo_corporativo,correo_personal,razon_social):
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
		self.fono_personal=fono_personal
		self.fono_corporativo=fono_corporativo
		self.correo_corporativo=correo_corporativo
		self.correo_personal=correo_personal
		self.razon_social=razon_social
	

class ParticipanteSchema(SQLAlchemyAutoSchema):
	class Meta:
		fields = ('rut','nombre',
		'apellido_paterno','apellido_materno',
		'genero','fecha_nacimiento','nivel_educacional',
		'nacionalidad','tipo_inscripcion','ocupacion',
		'razon_social','fono_personal','fono_corporativo','correo_corporativo','correo_personal')

class Relator(db.Model):
	__tablename__ = 'relator'
	rut = db.Column(db.Text, primary_key=True)
	nombre = db.Column(db.Text)
	apellido_paterno = db.Column(db.Text)
	apellido_materno = db.Column(db.Text)
	titulo = db.Column(db.Text)
	genero = db.Column(db.Integer)
	cv = db.Column(db.Text)
	fecha_nacimiento = db.Column(db.Date)
	numero_cuenta = db.Column(db.Text)
	banco = db.Column(db.Text)
	tipo_cuenta = db.Column(db.Text)
	fono_personal=db.Column(db.Text)
	fono_corporativo=db.Column(db.Text)
	correo_corporativo=db.Column(db.Text)
	correo_personal=db.Column(db.Text)
	
	dicta_instancia = db.relationship('Instancia', secondary='relator_instancia', backref=db.backref('profesores', lazy='dynamic'))
	

	def __init__(self,rut,nombre,apellido_paterno,apellido_materno,titulo,genero,cv,fecha_nacimiento,numero_cuenta,banco,tipo_cuenta):
		self.rut = rut
		self.nombre=nombre
		self.apellido_paterno=apellido_paterno
		self.apellido_materno=apellido_materno
		self.titulo=titulo
		self.genero=genero
		self.cv=cv
		self.fecha_nacimiento=fecha_nacimiento
		self.numero_cuenta=numero_cuenta
		self.banco=banco
		self.tipo_cuenta=tipo_cuenta
	
class RelatorSchema(SQLAlchemyAutoSchema):
	class Meta:
		fields = ('rut','nombre',
		'apellido_paterno','apellido_materno',
		'titulo','genero','cv','fecha_nacimiento',
		'numero_cuenta','banco','tipo_cuenta','fono_personal','fono_corporativo','correo_corporativo','correo_personal')

		


	
def objeto_db():
	global db
	return db