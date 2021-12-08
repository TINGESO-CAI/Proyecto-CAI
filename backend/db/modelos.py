from flask_sqlalchemy import SQLAlchemy 
from marshmallow import Schema, fields, ValidationError, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db=SQLAlchemy()

class Curso(db.Model):
    tablename = 'curso'
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

class Orden(db.Model):
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

class OrdenSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id_orden','sence',
        'cancelacion','fecha_emision','fecha_vencimiento')

class Empresa(db.Model):
    tablename = 'empresa'

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

class EmpresaSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ('razon_social','giro',
        'atencion','departamento','rut',
        'direccion','comuna',
        'correo', 'fono')

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

class ParticipanteSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ('rut','nombre',
        'apellido_paterno','apellido_materno',
        'genero','fecha_nacimiento','nivel_educacional',
        'nacionalidad','tipo_inscripcion','ocupacion',
        'correo')

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
	
class RelatorSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ('rut','nombre',
        'apellido_paterno','apellido_materno',
        'titulo','cv','fecha_nacimiento',
        'numero_cuenta','banco','tipo_cuenta')

t_relator_curso = db.Table(
    'relator_curso', db.metadata,
    db.Column('rut', db.ForeignKey('relator.rut')),
    db.Column('sence', db.ForeignKey('curso.sence'))
)

t_participante_curso = db.Table(
    'participante_curso', db.metadata,
    db.Column('rut', db.ForeignKey('participante.rut')),
    db.Column('sence', db.ForeignKey('curso.sence'))
)

t_participante_factura = db.Table(
    'participante_factura', db.metadata,
    db.Column('rut', db.ForeignKey('participante.rut')),
    db.Column('id_factura', db.ForeignKey('factura.id_factura'), nullable=False, server_default=db.text("nextval('participante_factura_id_factura_seq'::regclass)"))
)

t_participante_orden = db.Table(
    'participante_orden', db.metadata,
    db.Column('rut', db.ForeignKey('participante.rut')),
    db.Column('id_orden', db.ForeignKey('orden.id_orden'), nullable=False, server_default=db.text("nextval('participante_orden_id_orden_seq'::regclass)"))
)