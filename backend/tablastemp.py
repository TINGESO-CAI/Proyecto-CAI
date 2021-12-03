from sqlalchemy import Column, Date, ForeignKey, Integer, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Curso(Base):
    __tablename__ = 'curso'

    sence = Column(Text, primary_key=True)
    nombre = Column(Text)
    modalidad = Column(Text)
    categoria = Column(Text)
    horas_curso = Column(Integer)
    valor_efectivo_participante = Column(Integer)
    valor_imputable_participante = Column(Integer)
    resolucion_sence = Column(Text)
    resolucion_usach = Column(Text)
    estado = Column(Text)
    f_vigencia = Column(Date)


class Empresa(Base):
    __tablename__ = 'empresa'

    razon_social = Column(Text, primary_key=True)
    giro = Column(Text)
    atencion = Column(Text)
    departamento = Column(Text)
    rut = Column(Text)
    direccion = Column(Text)
    comuna = Column(Text)
    correo = Column(Text)
    fono = Column(Text)


class Factura(Base):
    __tablename__ = 'factura'

    id_factura = Column(Integer, primary_key=True, server_default=text("nextval('factura_id_factura_seq'::regclass)"))
    num_registro = Column(Text)
    estado = Column(Integer)
    tipo_pago = Column(Integer)
    num_hes = Column(Text)
    fecha_emision = Column(Date)
    fecha_vencimiento = Column(Date)

    participante = relationship('Participante', secondary='participante_factura')


class Orden(Base):
    __tablename__ = 'orden'

    id_orden = Column(Integer, primary_key=True, server_default=text("nextval('orden_id_orden_seq'::regclass)"))
    sence = Column(Text)
    cancelacion = Column(Integer)
    fecha_inicio = Column(Date)
    fecha_termino = Column(Date)

    participante = relationship('Participante', secondary='participante_orden')


class Relator(Base):
    __tablename__ = 'relator'

    rut = Column(Text, primary_key=True)
    nombre = Column(Text)
    apellido_paterno = Column(Text)
    apellido_materno = Column(Text)
    titulo = Column(Text)
    cv = Column(Text)
    fecha_nacimiento = Column(Date)
    numero_cuenta = Column(Text)
    banco = Column(Text)
    tipo_cuenta = Column(Text)

    curso = relationship('Curso', secondary='relator_curso')


class Participante(Base):
    __tablename__ = 'participante'

    rut = Column(Text, primary_key=True)
    nombre = Column(Text)
    apellido_paterno = Column(Text)
    apellido_materno = Column(Text)
    genero = Column(Integer)
    fecha_nacimiento = Column(Date)
    nivel_educacional = Column(Text)
    nacionalidad = Column(Text)
    tipo_inscripcion = Column(Text)
    ocupacion = Column(Text)
    correo = Column(Text)
    fono = Column(Text)
    razon_social = Column(ForeignKey('empresa.razon_social'))

    empresa = relationship('Empresa')
    curso = relationship('Curso', secondary='participante_curso')


t_relator_curso = Table(
    'relator_curso', metadata,
    Column('rut', ForeignKey('relator.rut')),
    Column('sence', ForeignKey('curso.sence'))
)


t_participante_curso = Table(
    'participante_curso', metadata,
    Column('rut', ForeignKey('participante.rut')),
    Column('sence', ForeignKey('curso.sence'))
)


t_participante_factura = Table(
    'participante_factura', metadata,
    Column('rut', ForeignKey('participante.rut')),
    Column('id_factura', ForeignKey('factura.id_factura'), nullable=False, server_default=text("nextval('participante_factura_id_factura_seq'::regclass)"))
)


t_participante_orden = Table(
    'participante_orden', metadata,
    Column('rut', ForeignKey('participante.rut')),
    Column('id_orden', ForeignKey('orden.id_orden'), nullable=False, server_default=text("nextval('participante_orden_id_orden_seq'::regclass)"))
)