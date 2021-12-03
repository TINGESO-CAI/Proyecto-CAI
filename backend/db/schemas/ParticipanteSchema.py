from ...server import ma
class ParticipanteSchema(ma.Schema):
    class Meta:
        fields = ('rut','nombre',
        'apellido_paterno','apellido_materno',
        'genero','fecha_nacimiento','nivel_educacional',
        'nacionalidad','tipo_inscripcion','ocupacion',
        'correo')
